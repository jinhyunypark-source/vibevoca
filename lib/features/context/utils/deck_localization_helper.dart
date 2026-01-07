class DeckLocalizationHelper {
  static String getKoreanTitle(String id) {
    // Normalize ID (lowercase, trim)
    final key = id.toLowerCase().trim();
    
    // Map of known English IDs to Korean Titles
    const Map<String, String> _titles = {
      // Categories / Groups ? 
      // Based on CSV "deck_group" column which are like LOGIC_CLARITY, EMOTION_DEPTH
      'logic_clarity': '논리적 명확성',
      'emotion_depth': '감정과 깊이',
      'sensory_details': '감각적 묘사',
      'action_impact': '행동과 임팩트',
      'social_interaction': '사회적 상호작용',
      'business_professional': '비즈니스 프로페셔널',
      'academic_intellectual': '학술 및 지성',
      'daily_routine': '일상 생활과 루틴',
      'travel_adventure': '여행과 모험',
      'arts_culture': '예술과 문화',
      'nature_environment': '자연과 환경',
      'tech_innovation': '기술과 혁신',
      'health_wellness': '건강과 웰니스',
      'food_dining': '음식과 식사',
      'time_planning': '시간과 계획',
      
      // Additional Keys from Screenshot
      'fluency_delivery': '유창성과 전달력',
      'attitude_mindset': '태도와 마인드셋',
      'relationship_communication': '관계와 소통',
    };

    return _titles[key] ?? id; // Fallback to ID if not found
  }
}
