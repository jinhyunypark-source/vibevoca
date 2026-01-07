#!/usr/bin/env python3
"""
Seed initial data for contextual sentence system:
- Sentence templates (default + interest-based)
- Context variables
- Profession vocabulary
- Interest tags mapping
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client


# ============================================
# Interest Tags Mapping
# ============================================

INTEREST_TAGS = [
    {
        "interest_slug": "baseball",
        "interest_label": "Baseball",
        "interest_label_ko": "야구",
        "related_tags": ["baseball", "sports", "mlb", "kbo", "pitcher", "batter", "stadium"],
        "sample_keywords_en": ["Babe Ruth", "home run", "pitcher", "catcher", "World Series", "Lee Dae-ho"],
        "sample_keywords_ko": ["베이브 루스", "홈런", "투수", "포수", "월드시리즈", "이대호"]
    },
    {
        "interest_slug": "soccer",
        "interest_label": "Soccer",
        "interest_label_ko": "축구",
        "related_tags": ["soccer", "football", "sports", "premier_league", "world_cup", "goal"],
        "sample_keywords_en": ["Messi", "goal", "World Cup", "penalty kick", "Son Heung-min"],
        "sample_keywords_ko": ["메시", "골", "월드컵", "페널티킥", "손흥민"]
    },
    {
        "interest_slug": "music",
        "interest_label": "Music",
        "interest_label_ko": "음악",
        "related_tags": ["music", "concert", "band", "singer", "album", "melody"],
        "sample_keywords_en": ["concert", "album", "melody", "band", "Grammy", "BTS"],
        "sample_keywords_ko": ["콘서트", "앨범", "멜로디", "밴드", "그래미", "방탄소년단"]
    },
    {
        "interest_slug": "gaming",
        "interest_label": "Gaming",
        "interest_label_ko": "게임",
        "related_tags": ["gaming", "esports", "video_game", "rpg", "fps", "mmorpg"],
        "sample_keywords_en": ["level up", "boss fight", "multiplayer", "achievement", "Faker"],
        "sample_keywords_ko": ["레벨업", "보스전", "멀티플레이", "업적", "페이커"]
    },
    {
        "interest_slug": "cooking",
        "interest_label": "Cooking",
        "interest_label_ko": "요리",
        "related_tags": ["cooking", "food", "recipe", "chef", "restaurant", "cuisine"],
        "sample_keywords_en": ["recipe", "ingredient", "chef", "kitchen", "Gordon Ramsay", "Baek Jong-won"],
        "sample_keywords_ko": ["레시피", "재료", "셰프", "주방", "고든 램지", "백종원"]
    },
    {
        "interest_slug": "travel",
        "interest_label": "Travel",
        "interest_label_ko": "여행",
        "related_tags": ["travel", "adventure", "tourism", "destination", "backpacking"],
        "sample_keywords_en": ["destination", "adventure", "landmark", "culture", "backpacking"],
        "sample_keywords_ko": ["목적지", "모험", "랜드마크", "문화", "배낭여행"]
    },
    {
        "interest_slug": "fitness",
        "interest_label": "Fitness",
        "interest_label_ko": "피트니스",
        "related_tags": ["fitness", "gym", "workout", "health", "exercise", "muscle"],
        "sample_keywords_en": ["workout", "gym", "muscle", "training", "marathon"],
        "sample_keywords_ko": ["운동", "헬스장", "근육", "트레이닝", "마라톤"]
    },
    {
        "interest_slug": "movies",
        "interest_label": "Movies",
        "interest_label_ko": "영화",
        "related_tags": ["movies", "film", "cinema", "director", "actor", "oscar"],
        "sample_keywords_en": ["director", "Oscar", "scene", "screenplay", "Bong Joon-ho"],
        "sample_keywords_ko": ["감독", "오스카", "장면", "각본", "봉준호"]
    },
    {
        "interest_slug": "technology",
        "interest_label": "Technology",
        "interest_label_ko": "기술",
        "related_tags": ["technology", "tech", "innovation", "ai", "startup", "gadget"],
        "sample_keywords_en": ["AI", "startup", "innovation", "Elon Musk", "smartphone"],
        "sample_keywords_ko": ["인공지능", "스타트업", "혁신", "일론 머스크", "스마트폰"]
    },
    {
        "interest_slug": "reading",
        "interest_label": "Reading",
        "interest_label_ko": "독서",
        "related_tags": ["reading", "books", "literature", "novel", "author", "library"],
        "sample_keywords_en": ["novel", "author", "bestseller", "chapter", "Haruki Murakami"],
        "sample_keywords_ko": ["소설", "작가", "베스트셀러", "챕터", "무라카미 하루키"]
    },
]


# ============================================
# Sentence Templates
# ============================================

TEMPLATES = [
    # ============================================
    # DEFAULT TEMPLATES (is_default = True)
    # 기본 예문 - 50%로 항상 제공
    # ============================================

    # === ADJECTIVE - Default ===
    {
        "part_of_speech": "adjective",
        "context_type": "general",
        "template_en": "The situation was quite {word}.",
        "template_ko": "상황이 꽤 {word}.",
        "priority": 1,
        "is_default": True,
        "tags": []
    },
    {
        "part_of_speech": "adjective",
        "context_type": "general",
        "template_en": "I felt {word} about the outcome.",
        "template_ko": "결과에 대해 {word} 느꼈다.",
        "priority": 1,
        "is_default": True,
        "tags": []
    },
    {
        "part_of_speech": "adjective",
        "context_type": "general",
        "template_en": "It was a {word} experience.",
        "template_ko": "{word} 경험이었다.",
        "priority": 1,
        "is_default": True,
        "tags": []
    },

    # ============================================
    # INTEREST-BASED TEMPLATES (is_default = False)
    # 관심사 기반 예문 - 태그로 매칭
    # ============================================

    # === BASEBALL / SPORTS ===
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "The pitcher's performance was {word} in the ninth inning.",
        "template_ko": "9회에 투수의 경기력은 {word}.",
        "priority": 10,
        "is_default": False,
        "tags": ["baseball", "sports", "pitcher"]
    },
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "Babe Ruth's legendary swing was simply {word}.",
        "template_ko": "베이브 루스의 전설적인 스윙은 정말 {word}.",
        "priority": 10,
        "is_default": False,
        "tags": ["baseball", "sports", "mlb", "babe_ruth"]
    },
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "The atmosphere in the stadium was {word} during the World Series.",
        "template_ko": "월드시리즈 기간 동안 경기장 분위기는 {word}.",
        "priority": 9,
        "is_default": False,
        "tags": ["baseball", "sports", "stadium", "world_series"]
    },
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "Lee Dae-ho's home run against Japan was {word}.",
        "template_ko": "이대호의 일본전 홈런은 {word}.",
        "priority": 10,
        "is_default": False,
        "tags": ["baseball", "sports", "kbo", "home_run"]
    },

    # === SOCCER / FOOTBALL ===
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "The penalty kick was {word} under such pressure.",
        "template_ko": "그런 압박 속에서 페널티킥은 {word}.",
        "priority": 10,
        "is_default": False,
        "tags": ["soccer", "football", "sports", "goal"]
    },
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "Son Heung-min's goal against Tottenham's rivals was {word}.",
        "template_ko": "손흥민의 라이벌전 골은 {word}.",
        "priority": 10,
        "is_default": False,
        "tags": ["soccer", "football", "sports", "premier_league"]
    },
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "The World Cup final atmosphere was {word}.",
        "template_ko": "월드컵 결승 분위기는 {word}.",
        "priority": 9,
        "is_default": False,
        "tags": ["soccer", "football", "sports", "world_cup"]
    },

    # === MUSIC ===
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "The concert's encore performance was {word}.",
        "template_ko": "콘서트 앵콜 공연은 {word}.",
        "priority": 10,
        "is_default": False,
        "tags": ["music", "concert", "performance"]
    },
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "BTS's new album was {word} according to critics.",
        "template_ko": "비평가들에 따르면 BTS의 새 앨범은 {word}.",
        "priority": 10,
        "is_default": False,
        "tags": ["music", "album", "kpop", "bts"]
    },
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "The melody of the song was {word} and memorable.",
        "template_ko": "그 노래의 멜로디는 {word}고 기억에 남았다.",
        "priority": 9,
        "is_default": False,
        "tags": ["music", "melody", "song"]
    },

    # === GAMING ===
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "The boss fight was {word} but rewarding.",
        "template_ko": "보스전은 {word}지만 보람찼다.",
        "priority": 10,
        "is_default": False,
        "tags": ["gaming", "video_game", "rpg", "boss"]
    },
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "Faker's gameplay in the finals was {word}.",
        "template_ko": "결승전에서 페이커의 플레이는 {word}.",
        "priority": 10,
        "is_default": False,
        "tags": ["gaming", "esports", "lol", "faker"]
    },
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "The multiplayer experience was {word}.",
        "template_ko": "멀티플레이 경험은 {word}.",
        "priority": 9,
        "is_default": False,
        "tags": ["gaming", "multiplayer", "online"]
    },

    # === COOKING / FOOD ===
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "Gordon Ramsay called the dish {word}.",
        "template_ko": "고든 램지는 그 요리를 {word}고 평가했다.",
        "priority": 10,
        "is_default": False,
        "tags": ["cooking", "food", "chef", "gordon_ramsay"]
    },
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "Baek Jong-won's recipe was surprisingly {word}.",
        "template_ko": "백종원의 레시피는 의외로 {word}.",
        "priority": 10,
        "is_default": False,
        "tags": ["cooking", "food", "recipe", "korean_food"]
    },
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "The secret ingredient made the taste {word}.",
        "template_ko": "비밀 재료가 맛을 {word}게 만들었다.",
        "priority": 9,
        "is_default": False,
        "tags": ["cooking", "food", "ingredient"]
    },

    # === MOVIES / FILM ===
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "Bong Joon-ho's Oscar speech was {word}.",
        "template_ko": "봉준호 감독의 오스카 수상 소감은 {word}.",
        "priority": 10,
        "is_default": False,
        "tags": ["movies", "film", "oscar", "director"]
    },
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "The plot twist in the movie was {word}.",
        "template_ko": "영화 속 반전은 {word}.",
        "priority": 9,
        "is_default": False,
        "tags": ["movies", "film", "plot", "cinema"]
    },

    # === TECHNOLOGY ===
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "The AI's response was surprisingly {word}.",
        "template_ko": "AI의 응답은 놀랍게도 {word}.",
        "priority": 10,
        "is_default": False,
        "tags": ["technology", "ai", "innovation"]
    },
    {
        "part_of_speech": "adjective",
        "context_type": "interest",
        "template_en": "Elon Musk's announcement was {word}.",
        "template_ko": "일론 머스크의 발표는 {word}.",
        "priority": 10,
        "is_default": False,
        "tags": ["technology", "tech", "startup", "elon_musk"]
    },

    # ============================================
    # PROFESSION-BASED TEMPLATES
    # ============================================

    # === ADJECTIVE - Profession: Developer ===
    {
        "part_of_speech": "adjective",
        "context_type": "profession",
        "context_value": "developer",
        "template_en": "After {action}, the code review was {word}.",
        "template_ko": "{action} 후, 코드 리뷰가 {word}.",
        "priority": 10
    },
    {
        "part_of_speech": "adjective",
        "context_type": "profession",
        "context_value": "developer",
        "template_en": "The debugging session was {word}, but we found the bug.",
        "template_ko": "디버깅 세션은 {word}, 하지만 버그를 찾았다.",
        "priority": 10
    },
    {
        "part_of_speech": "adjective",
        "context_type": "profession",
        "context_value": "developer",
        "template_en": "The new feature implementation was surprisingly {word}.",
        "template_ko": "새 기능 구현이 의외로 {word}.",
        "priority": 9
    },

    # === ADJECTIVE - Profession: Designer ===
    {
        "part_of_speech": "adjective",
        "context_type": "profession",
        "context_value": "designer",
        "template_en": "The client feedback was {word}, so we revised the design.",
        "template_ko": "클라이언트 피드백이 {word}해서 디자인을 수정했다.",
        "priority": 10
    },
    {
        "part_of_speech": "adjective",
        "context_type": "profession",
        "context_value": "designer",
        "template_en": "The color palette felt {word} for this brand.",
        "template_ko": "이 브랜드에 색상 팔레트가 {word} 느껴졌다.",
        "priority": 9
    },

    # === ADJECTIVE - Profession: Student ===
    {
        "part_of_speech": "adjective",
        "context_type": "profession",
        "context_value": "student",
        "template_en": "The exam was {word}, but I managed to finish.",
        "template_ko": "시험이 {word}, 하지만 어떻게든 끝냈다.",
        "priority": 10
    },
    {
        "part_of_speech": "adjective",
        "context_type": "profession",
        "context_value": "student",
        "template_en": "Studying for the test was {word}.",
        "template_ko": "시험 공부가 {word}.",
        "priority": 9
    },

    # === ADJECTIVE - Place: Home ===
    {
        "part_of_speech": "adjective",
        "context_type": "place",
        "context_value": "home",
        "template_en": "Working from home today was {word}.",
        "template_ko": "오늘 재택근무가 {word}.",
        "priority": 8
    },
    {
        "part_of_speech": "adjective",
        "context_type": "place",
        "context_value": "home",
        "template_en": "The atmosphere at home felt {word}.",
        "template_ko": "집 분위기가 {word} 느껴졌다.",
        "priority": 7
    },

    # === ADJECTIVE - Place: Work ===
    {
        "part_of_speech": "adjective",
        "context_type": "place",
        "context_value": "work",
        "template_en": "The meeting was {word}, but productive.",
        "template_ko": "회의가 {word}, 하지만 생산적이었다.",
        "priority": 8
    },

    # === ADJECTIVE - Place: Commute ===
    {
        "part_of_speech": "adjective",
        "context_type": "place",
        "context_value": "commute",
        "template_en": "The commute this morning was {word}.",
        "template_ko": "오늘 아침 출퇴근이 {word}.",
        "priority": 8
    },

    # === ADJECTIVE - Emotion: Tired ===
    {
        "part_of_speech": "adjective",
        "context_type": "emotion",
        "context_value": "tired",
        "template_en": "Feeling exhausted, everything seemed {word}.",
        "template_ko": "피곤한 기분에, 모든 것이 {word} 보였다.",
        "priority": 7
    },

    # === ADJECTIVE - Emotion: Happy ===
    {
        "part_of_speech": "adjective",
        "context_type": "emotion",
        "context_value": "happy",
        "template_en": "In a good mood, I found the task {word}.",
        "template_ko": "기분이 좋아서, 그 일이 {word} 느껴졌다.",
        "priority": 7
    },

    # === VERB - General ===
    {
        "part_of_speech": "verb",
        "context_type": "general",
        "template_en": "I tried to {word} the problem.",
        "template_ko": "문제를 {word}하려고 노력했다.",
        "priority": 1
    },
    {
        "part_of_speech": "verb",
        "context_type": "general",
        "template_en": "We need to {word} this situation carefully.",
        "template_ko": "이 상황을 신중하게 {word}해야 한다.",
        "priority": 1
    },

    # === VERB - Profession: Developer ===
    {
        "part_of_speech": "verb",
        "context_type": "profession",
        "context_value": "developer",
        "template_en": "The team decided to {word} the legacy code.",
        "template_ko": "팀은 레거시 코드를 {word}하기로 결정했다.",
        "priority": 10
    },
    {
        "part_of_speech": "verb",
        "context_type": "profession",
        "context_value": "developer",
        "template_en": "We had to {word} the API before the release.",
        "template_ko": "릴리스 전에 API를 {word}해야 했다.",
        "priority": 9
    },

    # === NOUN - General ===
    {
        "part_of_speech": "noun",
        "context_type": "general",
        "template_en": "The {word} was unexpected.",
        "template_ko": "{word}은(는) 예상치 못했다.",
        "priority": 1
    },
    {
        "part_of_speech": "noun",
        "context_type": "general",
        "template_en": "I noticed a {word} in the system.",
        "template_ko": "시스템에서 {word}을(를) 발견했다.",
        "priority": 1
    },

    # === NOUN - Profession: Developer ===
    {
        "part_of_speech": "noun",
        "context_type": "profession",
        "context_value": "developer",
        "template_en": "The {word} in the codebase caused issues.",
        "template_ko": "코드베이스의 {word}이(가) 문제를 일으켰다.",
        "priority": 10
    },

    # === ADVERB - General ===
    {
        "part_of_speech": "adverb",
        "context_type": "general",
        "template_en": "She spoke {word} during the presentation.",
        "template_ko": "그녀는 발표 중에 {word} 말했다.",
        "priority": 1
    },
    {
        "part_of_speech": "adverb",
        "context_type": "general",
        "template_en": "The project progressed {word}.",
        "template_ko": "프로젝트가 {word} 진행되었다.",
        "priority": 1
    },
]


# ============================================
# Context Variables
# ============================================

CONTEXT_VARIABLES = [
    # === Profession: Developer ===
    {"placeholder": "{subject}", "context_type": "profession", "context_value": "developer",
     "value_en": "the developer", "value_ko": "개발자"},
    {"placeholder": "{subject}", "context_type": "profession", "context_value": "developer",
     "value_en": "our tech lead", "value_ko": "우리 팀 리드"},
    {"placeholder": "{action}", "context_type": "profession", "context_value": "developer",
     "value_en": "debugging the server", "value_ko": "서버 디버깅"},
    {"placeholder": "{action}", "context_type": "profession", "context_value": "developer",
     "value_en": "reviewing the pull request", "value_ko": "PR 리뷰"},
    {"placeholder": "{action}", "context_type": "profession", "context_value": "developer",
     "value_en": "deploying to production", "value_ko": "프로덕션 배포"},
    {"placeholder": "{object}", "context_type": "profession", "context_value": "developer",
     "value_en": "the code", "value_ko": "코드"},
    {"placeholder": "{object}", "context_type": "profession", "context_value": "developer",
     "value_en": "the bug", "value_ko": "버그"},

    # === Profession: Designer ===
    {"placeholder": "{subject}", "context_type": "profession", "context_value": "designer",
     "value_en": "the designer", "value_ko": "디자이너"},
    {"placeholder": "{action}", "context_type": "profession", "context_value": "designer",
     "value_en": "creating mockups", "value_ko": "목업 제작"},
    {"placeholder": "{action}", "context_type": "profession", "context_value": "designer",
     "value_en": "revising the UI", "value_ko": "UI 수정"},
    {"placeholder": "{object}", "context_type": "profession", "context_value": "designer",
     "value_en": "the design system", "value_ko": "디자인 시스템"},

    # === Profession: Student ===
    {"placeholder": "{subject}", "context_type": "profession", "context_value": "student",
     "value_en": "the student", "value_ko": "학생"},
    {"placeholder": "{action}", "context_type": "profession", "context_value": "student",
     "value_en": "studying for the exam", "value_ko": "시험 공부"},
    {"placeholder": "{action}", "context_type": "profession", "context_value": "student",
     "value_en": "writing the thesis", "value_ko": "논문 작성"},
    {"placeholder": "{object}", "context_type": "profession", "context_value": "student",
     "value_en": "the assignment", "value_ko": "과제"},

    # === Profession: Teacher ===
    {"placeholder": "{subject}", "context_type": "profession", "context_value": "teacher",
     "value_en": "the teacher", "value_ko": "선생님"},
    {"placeholder": "{action}", "context_type": "profession", "context_value": "teacher",
     "value_en": "preparing the lesson", "value_ko": "수업 준비"},
    {"placeholder": "{action}", "context_type": "profession", "context_value": "teacher",
     "value_en": "grading papers", "value_ko": "채점"},

    # === Profession: Marketer ===
    {"placeholder": "{subject}", "context_type": "profession", "context_value": "marketer",
     "value_en": "the marketer", "value_ko": "마케터"},
    {"placeholder": "{action}", "context_type": "profession", "context_value": "marketer",
     "value_en": "analyzing campaign data", "value_ko": "캠페인 데이터 분석"},
    {"placeholder": "{action}", "context_type": "profession", "context_value": "marketer",
     "value_en": "creating ad copy", "value_ko": "광고 카피 작성"},

    # === Place: Home ===
    {"placeholder": "{place}", "context_type": "place", "context_value": "home",
     "value_en": "at home", "value_ko": "집에서"},
    {"placeholder": "{setting}", "context_type": "place", "context_value": "home",
     "value_en": "in a comfortable setting", "value_ko": "편안한 환경에서"},

    # === Place: Work ===
    {"placeholder": "{place}", "context_type": "place", "context_value": "work",
     "value_en": "at the office", "value_ko": "사무실에서"},
    {"placeholder": "{setting}", "context_type": "place", "context_value": "work",
     "value_en": "during a meeting", "value_ko": "회의 중에"},

    # === Place: Commute ===
    {"placeholder": "{place}", "context_type": "place", "context_value": "commute",
     "value_en": "on the subway", "value_ko": "지하철에서"},
    {"placeholder": "{place}", "context_type": "place", "context_value": "commute",
     "value_en": "on my way to work", "value_ko": "출근길에"},

    # === Emotion: Happy ===
    {"placeholder": "{mood}", "context_type": "emotion", "context_value": "happy",
     "value_en": "in a good mood", "value_ko": "기분 좋게"},
    {"placeholder": "{feeling}", "context_type": "emotion", "context_value": "happy",
     "value_en": "feeling cheerful", "value_ko": "활기차게"},

    # === Emotion: Tired ===
    {"placeholder": "{mood}", "context_type": "emotion", "context_value": "tired",
     "value_en": "feeling exhausted", "value_ko": "지친 채로"},
    {"placeholder": "{feeling}", "context_type": "emotion", "context_value": "tired",
     "value_en": "after a long day", "value_ko": "긴 하루 끝에"},

    # === Emotion: Stressed ===
    {"placeholder": "{mood}", "context_type": "emotion", "context_value": "stressed",
     "value_en": "under pressure", "value_ko": "압박감 속에서"},

    # === Environment: Sunny ===
    {"placeholder": "{weather}", "context_type": "environment", "context_value": "sunny",
     "value_en": "on a sunny day", "value_ko": "맑은 날에"},

    # === Environment: Rainy ===
    {"placeholder": "{weather}", "context_type": "environment", "context_value": "rainy",
     "value_en": "on a rainy day", "value_ko": "비 오는 날에"},
]


# ============================================
# Profession Vocabulary
# ============================================

PROFESSION_VOCABULARY = [
    {
        "profession": "developer",
        "profession_ko": "개발자",
        "subjects": ["the developer", "my colleague", "the tech lead", "our team", "the senior engineer"],
        "objects": ["the code", "the bug", "the API", "the database", "the feature", "the pull request"],
        "actions": ["debugging", "deploying", "refactoring", "reviewing code", "writing tests", "optimizing"],
        "places": ["at the office", "in a standup", "during code review", "at my desk", "in a sprint meeting"],
        "scenarios": ["after a long debugging session", "during the sprint review", "before the release deadline",
                      "while pair programming", "after the deployment"],
        "subjects_ko": ["개발자", "동료", "팀 리드", "우리 팀", "시니어 엔지니어"],
        "objects_ko": ["코드", "버그", "API", "데이터베이스", "기능", "PR"],
        "actions_ko": ["디버깅", "배포", "리팩토링", "코드 리뷰", "테스트 작성", "최적화"],
        "places_ko": ["사무실에서", "스탠드업 미팅에서", "코드 리뷰 중", "내 자리에서", "스프린트 미팅에서"],
        "scenarios_ko": ["긴 디버깅 세션 후", "스프린트 리뷰 중", "릴리스 마감 전", "페어 프로그래밍 중", "배포 후"]
    },
    {
        "profession": "designer",
        "profession_ko": "디자이너",
        "subjects": ["the designer", "our creative team", "the UX lead", "the art director"],
        "objects": ["the mockup", "the prototype", "the design system", "the brand guidelines", "the user flow"],
        "actions": ["designing", "iterating", "prototyping", "presenting", "revising"],
        "places": ["in a design review", "at the creative studio", "during a client meeting"],
        "scenarios": ["after client feedback", "before the design handoff", "during user testing"],
        "subjects_ko": ["디자이너", "크리에이티브 팀", "UX 리드", "아트 디렉터"],
        "objects_ko": ["목업", "프로토타입", "디자인 시스템", "브랜드 가이드라인", "사용자 플로우"],
        "actions_ko": ["디자인", "반복 작업", "프로토타이핑", "발표", "수정"],
        "places_ko": ["디자인 리뷰에서", "크리에이티브 스튜디오에서", "클라이언트 미팅 중"],
        "scenarios_ko": ["클라이언트 피드백 후", "디자인 핸드오프 전", "사용자 테스트 중"]
    },
    {
        "profession": "student",
        "profession_ko": "학생",
        "subjects": ["the student", "my classmate", "our study group", "the professor"],
        "objects": ["the assignment", "the thesis", "the exam", "the research paper", "the presentation"],
        "actions": ["studying", "researching", "writing", "presenting", "reviewing"],
        "places": ["in the library", "in class", "at the study cafe", "in the dorm"],
        "scenarios": ["before the exam", "during finals week", "after the lecture", "while preparing the presentation"],
        "subjects_ko": ["학생", "반 친구", "스터디 그룹", "교수님"],
        "objects_ko": ["과제", "논문", "시험", "연구 논문", "발표"],
        "actions_ko": ["공부", "연구", "작성", "발표", "복습"],
        "places_ko": ["도서관에서", "수업 중", "스터디 카페에서", "기숙사에서"],
        "scenarios_ko": ["시험 전", "기말고사 기간에", "강의 후", "발표 준비 중"]
    },
    {
        "profession": "teacher",
        "profession_ko": "선생님",
        "subjects": ["the teacher", "my colleague", "the department head", "the students"],
        "objects": ["the lesson plan", "the curriculum", "the grades", "the classroom"],
        "actions": ["teaching", "preparing", "grading", "mentoring", "explaining"],
        "places": ["in the classroom", "in the teachers' room", "during office hours"],
        "scenarios": ["before class", "after the semester", "during parent-teacher conferences"],
        "subjects_ko": ["선생님", "동료 교사", "학과장", "학생들"],
        "objects_ko": ["수업 계획", "커리큘럼", "성적", "교실"],
        "actions_ko": ["가르치기", "준비", "채점", "멘토링", "설명"],
        "places_ko": ["교실에서", "교무실에서", "오피스 아워 중"],
        "scenarios_ko": ["수업 전", "학기 후", "학부모 상담 중"]
    },
    {
        "profession": "marketer",
        "profession_ko": "마케터",
        "subjects": ["the marketer", "our marketing team", "the brand manager", "the CMO"],
        "objects": ["the campaign", "the analytics", "the ad copy", "the target audience", "the ROI"],
        "actions": ["analyzing", "launching", "optimizing", "measuring", "targeting"],
        "places": ["in a strategy meeting", "at the marketing agency", "during a pitch"],
        "scenarios": ["after the campaign launch", "during A/B testing", "before the quarterly review"],
        "subjects_ko": ["마케터", "마케팅 팀", "브랜드 매니저", "CMO"],
        "objects_ko": ["캠페인", "분석 데이터", "광고 카피", "타겟 고객", "ROI"],
        "actions_ko": ["분석", "런칭", "최적화", "측정", "타겟팅"],
        "places_ko": ["전략 회의에서", "마케팅 에이전시에서", "피칭 중"],
        "scenarios_ko": ["캠페인 런칭 후", "A/B 테스트 중", "분기 리뷰 전"]
    }
]


def main():
    client = get_supabase_client()

    print("=" * 60)
    print("Seeding Contextual Sentence System Data")
    print("=" * 60)

    # 0. Insert interest tags mapping
    print("\n[0/4] Inserting interest tags mapping...")
    for tag in INTEREST_TAGS:
        try:
            client.table('interest_tags').upsert(
                tag,
                on_conflict='interest_slug'
            ).execute()
            print(f"  + {tag['interest_slug']}: {len(tag['related_tags'])} tags")
        except Exception as e:
            print(f"  ! Error: {e}")

    print(f"  Total: {len(INTEREST_TAGS)} interests")

    # 1. Insert sentence templates
    print("\n[1/4] Inserting sentence templates...")
    for template in TEMPLATES:
        try:
            client.table('sentence_templates').upsert(
                template,
                on_conflict='id'
            ).execute()
            print(f"  + {template['part_of_speech']}/{template['context_type']}: OK")
        except Exception as e:
            print(f"  ! Error: {e}")

    print(f"  Total: {len(TEMPLATES)} templates")

    # 2. Insert context variables
    print("\n[2/4] Inserting context variables...")
    for var in CONTEXT_VARIABLES:
        try:
            client.table('context_variables').upsert(
                var,
                on_conflict='id'
            ).execute()
        except Exception as e:
            print(f"  ! Error: {e}")

    print(f"  Total: {len(CONTEXT_VARIABLES)} variables")

    # 3. Insert profession vocabulary
    print("\n[3/4] Inserting profession vocabulary...")
    for prof in PROFESSION_VOCABULARY:
        try:
            client.table('profession_vocabulary').upsert(
                prof,
                on_conflict='profession'
            ).execute()
            print(f"  + {prof['profession']}: OK")
        except Exception as e:
            print(f"  ! Error: {e}")

    print(f"  Total: {len(PROFESSION_VOCABULARY)} professions")

    print("\n" + "=" * 60)
    print("Seeding complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
