-- ============================================
-- Contextual Sentence System Schema
-- Version: 1.0
-- Description: Dynamic sentence generation based on user context
-- ============================================

-- 1. Extend cards table with word properties
-- ============================================

ALTER TABLE public.cards
ADD COLUMN IF NOT EXISTS part_of_speech TEXT;

ALTER TABLE public.cards
ADD COLUMN IF NOT EXISTS semantic_category TEXT;

ALTER TABLE public.cards
ADD COLUMN IF NOT EXISTS formality TEXT DEFAULT 'both';

COMMENT ON COLUMN public.cards.part_of_speech IS 'Word type: noun, verb, adjective, adverb, phrase';
COMMENT ON COLUMN public.cards.semantic_category IS 'Semantic grouping: emotion, action, description, state, quality';
COMMENT ON COLUMN public.cards.formality IS 'Usage register: formal, casual, both';


-- 2. Sentence Templates
-- ============================================

CREATE TABLE IF NOT EXISTS public.sentence_templates (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

    -- Template targeting
    part_of_speech TEXT NOT NULL,
    semantic_category TEXT,

    -- Template content with placeholders: {word}, {subject}, {object}, {action}, {place}, {time}
    template_en TEXT NOT NULL,
    template_ko TEXT NOT NULL,

    -- Context matching
    context_type TEXT NOT NULL DEFAULT 'general',  -- general, profession, place, emotion, environment, interest
    context_value TEXT,  -- specific value like 'developer', 'home', 'happy'

    -- Hidden tags for interest-based search (NOT displayed in sentence)
    -- e.g., ['baseball', 'sports'] for a sentence about Babe Ruth
    tags TEXT[] DEFAULT '{}',

    -- Quality control
    priority INT DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    is_default BOOLEAN DEFAULT false,  -- true = 기본 예문, false = 맞춤 예문

    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_templates_pos ON public.sentence_templates(part_of_speech);
CREATE INDEX IF NOT EXISTS idx_templates_context ON public.sentence_templates(context_type, context_value);
CREATE INDEX IF NOT EXISTS idx_templates_active ON public.sentence_templates(is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_templates_default ON public.sentence_templates(is_default);
CREATE INDEX IF NOT EXISTS idx_templates_tags ON public.sentence_templates USING GIN(tags);  -- 배열 검색용

COMMENT ON TABLE public.sentence_templates IS 'Sentence structure templates with placeholders for dynamic generation';


-- 3. Context Variables (Placeholder Replacements)
-- ============================================

CREATE TABLE IF NOT EXISTS public.context_variables (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

    -- Variable identification
    placeholder TEXT NOT NULL,  -- {subject}, {action}, {place}, etc.

    -- Context matching
    context_type TEXT NOT NULL,  -- profession, place, emotion, environment
    context_value TEXT NOT NULL,  -- developer, home, happy, sunny

    -- Replacement values
    value_en TEXT NOT NULL,
    value_ko TEXT NOT NULL,

    -- Metadata
    tags TEXT[] DEFAULT '{}',
    priority INT DEFAULT 0,

    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_variables_context ON public.context_variables(context_type, context_value);
CREATE INDEX IF NOT EXISTS idx_variables_placeholder ON public.context_variables(placeholder);

COMMENT ON TABLE public.context_variables IS 'Replacement values for template placeholders based on user context';


-- 4. Profession Vocabulary Pool
-- ============================================

CREATE TABLE IF NOT EXISTS public.profession_vocabulary (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

    profession TEXT NOT NULL UNIQUE,
    profession_ko TEXT NOT NULL,

    -- Word pools (JSONB arrays)
    subjects JSONB DEFAULT '[]'::jsonb,   -- ["the developer", "my colleague"]
    objects JSONB DEFAULT '[]'::jsonb,    -- ["the code", "the bug"]
    actions JSONB DEFAULT '[]'::jsonb,    -- ["debugging", "deploying"]
    places JSONB DEFAULT '[]'::jsonb,     -- ["at the office", "in a meeting"]
    scenarios JSONB DEFAULT '[]'::jsonb,  -- ["after a long meeting"]

    -- Korean equivalents
    subjects_ko JSONB DEFAULT '[]'::jsonb,
    objects_ko JSONB DEFAULT '[]'::jsonb,
    actions_ko JSONB DEFAULT '[]'::jsonb,
    places_ko JSONB DEFAULT '[]'::jsonb,
    scenarios_ko JSONB DEFAULT '[]'::jsonb,

    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_profession_name ON public.profession_vocabulary(profession);

COMMENT ON TABLE public.profession_vocabulary IS 'Domain-specific vocabulary pools for each profession';


-- 5. Generated Sentence Cache
-- ============================================

CREATE TABLE IF NOT EXISTS public.sentence_cache (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

    -- Reference
    card_id UUID REFERENCES public.cards(id) ON DELETE CASCADE NOT NULL,

    -- Context fingerprint
    context_hash TEXT NOT NULL,  -- MD5 hash of context combination

    -- Generated content
    sentence_en TEXT NOT NULL,
    sentence_ko TEXT NOT NULL,

    -- Metadata
    template_id UUID REFERENCES public.sentence_templates(id) ON DELETE SET NULL,
    generation_method TEXT DEFAULT 'template',  -- template, llm, manual
    quality_score FLOAT,

    -- Usage tracking
    usage_count INT DEFAULT 0,
    last_used_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,

    -- Prevent duplicate cache entries
    UNIQUE(card_id, context_hash)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_cache_lookup ON public.sentence_cache(card_id, context_hash);
CREATE INDEX IF NOT EXISTS idx_cache_usage ON public.sentence_cache(usage_count DESC);

COMMENT ON TABLE public.sentence_cache IS 'Cache for generated contextual sentences to improve performance';


-- 6. Interest Tags Mapping (관심사 → 관련 태그)
-- ============================================
-- baseball → ['baseball', 'sports', 'mlb', 'kbo', 'babe_ruth', 'home_run']
-- 예문에는 직접 "baseball"이 없어도 태그로 연결됨

CREATE TABLE IF NOT EXISTS public.interest_tags (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

    -- 관심사 식별자 (meta_interests.slug와 매칭)
    interest_slug TEXT NOT NULL,
    interest_label TEXT NOT NULL,  -- "Baseball", "Music"
    interest_label_ko TEXT,        -- "야구", "음악"

    -- 관련 태그들 (예문 검색용)
    related_tags TEXT[] NOT NULL DEFAULT '{}',

    -- 예시 키워드 (예문에 나올 수 있는 단어들 - 참고용)
    sample_keywords_en TEXT[] DEFAULT '{}',  -- ['Babe Ruth', 'home run', 'pitcher', 'stadium']
    sample_keywords_ko TEXT[] DEFAULT '{}',  -- ['베이브 루스', '홈런', '투수', '야구장']

    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,

    UNIQUE(interest_slug)
);

CREATE INDEX IF NOT EXISTS idx_interest_tags_slug ON public.interest_tags(interest_slug);
CREATE INDEX IF NOT EXISTS idx_interest_tags_tags ON public.interest_tags USING GIN(related_tags);

COMMENT ON TABLE public.interest_tags IS 'Maps user interests to hidden tags for sentence matching';


-- 7. Extend profiles table (instead of creating user_preferences)
-- ============================================
-- profiles 테이블은 이미 존재함 (schema.sql + update_profile_metadata.sql)
-- 기존: id, role, interests, job_id, interest_ids
-- 추가: learning_level, primary_language, show_romanization

ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS learning_level TEXT DEFAULT 'intermediate';

ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS primary_language TEXT DEFAULT 'ko';

ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS show_romanization BOOLEAN DEFAULT false;

COMMENT ON COLUMN public.profiles.learning_level IS 'User learning level: beginner, intermediate, advanced';
COMMENT ON COLUMN public.profiles.primary_language IS 'Primary display language: ko, en';
COMMENT ON COLUMN public.profiles.show_romanization IS 'Show romanization for Korean text';


-- 7. Enable RLS (Row Level Security)
-- ============================================

ALTER TABLE public.sentence_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.context_variables ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.profession_vocabulary ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sentence_cache ENABLE ROW LEVEL SECURITY;

-- Public read access for templates and variables
CREATE POLICY "Templates are viewable by everyone" ON public.sentence_templates
    FOR SELECT USING (true);

CREATE POLICY "Variables are viewable by everyone" ON public.context_variables
    FOR SELECT USING (true);

CREATE POLICY "Professions are viewable by everyone" ON public.profession_vocabulary
    FOR SELECT USING (true);

-- Cache: users can read all, but we track usage
CREATE POLICY "Cache is viewable by everyone" ON public.sentence_cache
    FOR SELECT USING (true);

-- Note: profiles RLS policies already exist in schema.sql


-- 9. Helper Functions
-- ============================================

-- Function to get sentences for a card (50% default + 50% personalized)
CREATE OR REPLACE FUNCTION get_mixed_sentences(
    p_card_id UUID,
    p_interest_tags TEXT[] DEFAULT '{}',  -- 사용자 관심사 관련 태그들
    p_profession TEXT DEFAULT NULL,
    p_limit INT DEFAULT 4  -- 총 예문 개수
)
RETURNS TABLE (
    sentence_en TEXT,
    sentence_ko TEXT,
    source TEXT,  -- 'default', 'interest', 'profession'
    matched_tag TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_card RECORD;
    v_default_count INT;
    v_personalized_count INT;
BEGIN
    -- Get card info
    SELECT * INTO v_card FROM cards WHERE id = p_card_id;

    IF NOT FOUND THEN
        RETURN;
    END IF;

    -- Calculate split: 50% default, 50% personalized
    v_default_count := GREATEST(1, p_limit / 2);
    v_personalized_count := p_limit - v_default_count;

    -- 1. Return DEFAULT sentences (is_default = true OR from card's example_sentences)
    RETURN QUERY
    SELECT
        st.template_en as sentence_en,
        st.template_ko as sentence_ko,
        'default'::TEXT as source,
        NULL::TEXT as matched_tag
    FROM sentence_templates st
    WHERE st.is_active = true
      AND st.is_default = true
      AND (st.part_of_speech = v_card.part_of_speech OR st.part_of_speech IS NULL)
    ORDER BY st.priority DESC, RANDOM()
    LIMIT v_default_count;

    -- 2. Return PERSONALIZED sentences by interest tags
    IF array_length(p_interest_tags, 1) > 0 THEN
        RETURN QUERY
        SELECT
            st.template_en as sentence_en,
            st.template_ko as sentence_ko,
            'interest'::TEXT as source,
            (SELECT unnest(st.tags) INTERSECT SELECT unnest(p_interest_tags) LIMIT 1)::TEXT as matched_tag
        FROM sentence_templates st
        WHERE st.is_active = true
          AND st.is_default = false
          AND st.tags && p_interest_tags  -- 배열 겹침 연산자
          AND (st.part_of_speech = v_card.part_of_speech OR st.part_of_speech IS NULL)
        ORDER BY
            -- 더 많은 태그가 매칭될수록 높은 우선순위
            (SELECT COUNT(*) FROM unnest(st.tags) t WHERE t = ANY(p_interest_tags)) DESC,
            st.priority DESC,
            RANDOM()
        LIMIT v_personalized_count;
    END IF;

    -- 3. If not enough personalized, try profession-based
    IF p_profession IS NOT NULL THEN
        RETURN QUERY
        SELECT
            st.template_en as sentence_en,
            st.template_ko as sentence_ko,
            'profession'::TEXT as source,
            p_profession::TEXT as matched_tag
        FROM sentence_templates st
        WHERE st.is_active = true
          AND st.context_type = 'profession'
          AND st.context_value = p_profession
          AND (st.part_of_speech = v_card.part_of_speech OR st.part_of_speech IS NULL)
        ORDER BY st.priority DESC, RANDOM()
        LIMIT v_personalized_count;
    END IF;
END;
$$;

COMMENT ON FUNCTION get_mixed_sentences IS 'Get 50% default + 50% personalized sentences for a card';


-- Function to get user interest tags from their profile
CREATE OR REPLACE FUNCTION get_user_interest_tags(p_user_id UUID)
RETURNS TEXT[]
LANGUAGE plpgsql
AS $$
DECLARE
    v_tags TEXT[] := '{}';
    v_interest_id UUID;
BEGIN
    -- Get user's interest_ids from profiles
    FOR v_interest_id IN
        SELECT unnest(interest_ids) FROM profiles WHERE id = p_user_id
    LOOP
        -- Get related tags for each interest
        SELECT array_cat(v_tags, it.related_tags) INTO v_tags
        FROM interest_tags it
        JOIN meta_interests mi ON mi.slug = it.interest_slug
        WHERE mi.id = v_interest_id;
    END LOOP;

    RETURN v_tags;
END;
$$;

COMMENT ON FUNCTION get_user_interest_tags IS 'Get all related tags for a user based on their interests';


-- Legacy function for backward compatibility
CREATE OR REPLACE FUNCTION get_contextual_sentence(
    p_card_id UUID,
    p_profession TEXT DEFAULT NULL,
    p_place TEXT DEFAULT NULL,
    p_emotion TEXT DEFAULT NULL,
    p_environment TEXT DEFAULT NULL
)
RETURNS TABLE (
    sentence_en TEXT,
    sentence_ko TEXT,
    source TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Simple version: return from card's example_sentences
    RETURN QUERY
    SELECT
        (c.example_sentences->>0)::TEXT as sentence_en,
        (c.example_sentences->>0)::TEXT as sentence_ko,
        'default'::TEXT as source
    FROM cards c
    WHERE c.id = p_card_id;
END;
$$;

COMMENT ON FUNCTION get_contextual_sentence IS 'Legacy: Get a contextual sentence for a card';


-- 9. Trigger for updated_at
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc'::text, now());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_sentence_templates_updated_at
    BEFORE UPDATE ON public.sentence_templates
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_profession_vocabulary_updated_at
    BEFORE UPDATE ON public.profession_vocabulary
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Note: profiles already has updated_at trigger from main schema
