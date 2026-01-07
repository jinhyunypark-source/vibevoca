-- ============================================
-- Card Sentences - Simplified Schema
-- Version: 2.1
-- Description: Pre-generated sentences per word with interest tags
-- ============================================

-- 예문은 배치 프로세스(LLM)로 사전 생성 후 저장
-- 관심사/직업은 기존 meta_interests 테이블 활용 (profiles.interest_ids로 연결)

-- 1. Card Sentences (단어별 예문)
-- ============================================

CREATE TABLE IF NOT EXISTS public.card_sentences (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

    -- 단어 참조
    card_id UUID REFERENCES public.cards(id) ON DELETE CASCADE NOT NULL,
    word TEXT NOT NULL,  -- cards.front_text 복사 (빠른 조회용)

    -- 예문 내용
    sentence_en TEXT NOT NULL,  -- 영어 예문
    sentence_ko TEXT NOT NULL,  -- 한글 번역/설명

    -- 관심사 태그 (검색용, 예문에 직접 노출 안됨)
    -- meta_interests.code 값들과 매칭 (e.g., ['travel', 'sports'])
    tags TEXT[] DEFAULT '{}',

    -- 분류
    is_default BOOLEAN DEFAULT false,  -- true = 기본 예문 (관심사 무관)
    difficulty TEXT DEFAULT 'intermediate',  -- beginner, intermediate, advanced

    -- 품질 관리
    is_verified BOOLEAN DEFAULT false,  -- 검수 완료 여부
    source TEXT DEFAULT 'llm',  -- llm, manual, imported

    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_card_sentences_card ON public.card_sentences(card_id);
CREATE INDEX IF NOT EXISTS idx_card_sentences_word ON public.card_sentences(word);
CREATE INDEX IF NOT EXISTS idx_card_sentences_tags ON public.card_sentences USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_card_sentences_default ON public.card_sentences(is_default);

COMMENT ON TABLE public.card_sentences IS 'Pre-generated example sentences per word with interest tags';


-- 2. Extend meta_interests (관심사에 관련 태그 추가)
-- ============================================
-- 기존 meta_interests 테이블에 related_tags 컬럼 추가
-- code='travel' → related_tags=['travel', 'adventure', 'tourism', 'destination']

ALTER TABLE public.meta_interests
ADD COLUMN IF NOT EXISTS related_tags TEXT[] DEFAULT '{}';

COMMENT ON COLUMN public.meta_interests.related_tags IS 'Related tags for sentence matching (e.g., travel → [travel, adventure, tourism])';


-- 3. Extend profiles (학습 설정)
-- ============================================
-- profiles.interest_ids는 이미 존재 (meta_interests.id 배열)

ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS learning_level TEXT DEFAULT 'intermediate';

ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS sentence_count INT DEFAULT 2;  -- 카드당 보여줄 예문 수


-- 4. RLS Policies
-- ============================================

ALTER TABLE public.card_sentences ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Sentences are viewable by everyone" ON public.card_sentences
    FOR SELECT USING (true);


-- 5. Helper Functions
-- ============================================

-- 5.1 Get user interest tags from profiles and meta_interests
CREATE OR REPLACE FUNCTION get_user_interest_tags(
    p_user_id UUID
)
RETURNS TEXT[]
LANGUAGE plpgsql
AS $$
DECLARE
    v_tags TEXT[];
BEGIN
    -- profiles.interest_ids → meta_interests.related_tags 수집
    SELECT array_agg(DISTINCT tag)
    INTO v_tags
    FROM profiles p
    CROSS JOIN LATERAL unnest(p.interest_ids) AS interest_id
    JOIN meta_interests mi ON mi.id = interest_id
    CROSS JOIN LATERAL unnest(mi.related_tags) AS tag
    WHERE p.user_id = p_user_id;

    RETURN COALESCE(v_tags, '{}');
END;
$$;

COMMENT ON FUNCTION get_user_interest_tags IS 'Get all related tags from user interests (profiles → meta_interests)';


-- 5.2 Get sentences for a card
CREATE OR REPLACE FUNCTION get_card_sentences(
    p_card_id UUID,
    p_user_tags TEXT[] DEFAULT '{}',  -- 사용자 관심사 관련 태그들
    p_limit INT DEFAULT 2
)
RETURNS TABLE (
    sentence_en TEXT,
    sentence_ko TEXT,
    tags TEXT[],
    is_default BOOLEAN,
    match_type TEXT  -- 'default', 'matched', 'random'
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_default_count INT;
    v_matched_count INT;
    v_total_found INT := 0;
    v_row_count INT;
BEGIN
    -- 50% 기본, 50% 맞춤
    v_default_count := GREATEST(1, p_limit / 2);
    v_matched_count := p_limit - v_default_count;

    -- 1. 기본 예문 (is_default = true)
    RETURN QUERY
    SELECT
        cs.sentence_en,
        cs.sentence_ko,
        cs.tags,
        cs.is_default,
        'default'::TEXT as match_type
    FROM card_sentences cs
    WHERE cs.card_id = p_card_id
      AND cs.is_default = true
      AND cs.is_verified = true
    ORDER BY RANDOM()
    LIMIT v_default_count;

    GET DIAGNOSTICS v_row_count = ROW_COUNT;
    v_total_found := v_total_found + v_row_count;

    -- 2. 관심사 매칭 예문 (tags 겹침)
    IF array_length(p_user_tags, 1) > 0 THEN
        RETURN QUERY
        SELECT
            cs.sentence_en,
            cs.sentence_ko,
            cs.tags,
            cs.is_default,
            'matched'::TEXT as match_type
        FROM card_sentences cs
        WHERE cs.card_id = p_card_id
          AND cs.is_default = false
          AND cs.is_verified = true
          AND cs.tags && p_user_tags  -- 배열 겹침
        ORDER BY
            -- 더 많은 태그 매칭 = 높은 우선순위
            (SELECT COUNT(*) FROM unnest(cs.tags) t WHERE t = ANY(p_user_tags)) DESC,
            RANDOM()
        LIMIT v_matched_count;

        GET DIAGNOSTICS v_row_count = ROW_COUNT;
        v_total_found := v_total_found + v_row_count;
    END IF;

    -- 3. 부족하면 랜덤 예문으로 채움
    IF v_total_found < p_limit THEN
        RETURN QUERY
        SELECT
            cs.sentence_en,
            cs.sentence_ko,
            cs.tags,
            cs.is_default,
            'random'::TEXT as match_type
        FROM card_sentences cs
        WHERE cs.card_id = p_card_id
          AND cs.is_verified = true
        ORDER BY RANDOM()
        LIMIT (p_limit - v_total_found);
    END IF;
END;
$$;

COMMENT ON FUNCTION get_card_sentences IS 'Get 50% default + 50% interest-matched sentences for a card. Use get_user_interest_tags() to get p_user_tags parameter.';


-- 6. Trigger for updated_at
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc'::text, now());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_card_sentences_updated_at
    BEFORE UPDATE ON public.card_sentences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
