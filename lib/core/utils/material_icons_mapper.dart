import 'package:flutter/material.dart';

/// Material Icons 이름을 IconData로 동적 변환하는 유틸리티
///
/// 데이터베이스에 저장된 아이콘 이름(문자열)을 Flutter IconData로 변환합니다.
/// Icons 클래스를 직접 참조하여 정확한 아이콘을 반환합니다.
///
/// 사용 예시:
/// ```dart
/// IconData icon = MaterialIconsMapper.getIcon('sports_soccer');
/// Icon(icon)
/// ```
class MaterialIconsMapper {
  // Material Icons 이름 -> IconData 매핑
  // Icons 클래스를 직접 참조하여 정확한 아이콘 보장
  static final Map<String, IconData> _iconMap = {
    // Job/Occupation icons
    'school': Icons.school,
    'code': Icons.code,
    'business_center': Icons.business_center,
    'work': Icons.work,

    // Hobby/Interest icons
    'sports_soccer': Icons.sports_soccer,
    'groups': Icons.groups,
    'flight': Icons.flight,
    'directions_run': Icons.directions_run,
    'chat': Icons.chat,
    'campaign': Icons.campaign,
    'favorite': Icons.favorite,
    'diversity_1': Icons.diversity_1,
    'diversity_3': Icons.diversity_3,
    'movie': Icons.movie,
    'computer': Icons.computer,
    'medical_services': Icons.medical_services,
    'restaurant': Icons.restaurant,

    // Vibe Context icons (Place)
    'wb_sunny': Icons.wb_sunny,
    'home': Icons.home,
    'directions_transit': Icons.directions_transit,
    'train': Icons.directions_subway,
    'coffee': Icons.coffee,

    // Vibe Context icons (Emotion)
    'mood_bad': Icons.mood_bad,
    'sentiment_very_satisfied': Icons.sentiment_very_satisfied,
    'sentiment_very_dissatisfied': Icons.sentiment_very_dissatisfied,
    'sentiment_satisfied': Icons.sentiment_satisfied,
    'battery_alert': Icons.battery_alert,
    'self_improvement': Icons.self_improvement,

    // Vibe Context icons (Environment)
    'ac_unit': Icons.ac_unit,
    'water_drop': Icons.water_drop,
    'local_fire_department': Icons.local_fire_department,
    'thermostat': Icons.thermostat,

    // Communication deck icons
    'psychology': Icons.psychology,
    'record_voice_over': Icons.record_voice_over,
    'short_text': Icons.short_text,
    'handshake': Icons.handshake,

    // Sense & Style deck icons
    'visibility': Icons.visibility,
    'hearing': Icons.hearing,
    'air': Icons.air,
    'touch_app': Icons.touch_app,

    // Intelligence & Judgment deck icons
    'lightbulb': Icons.lightbulb,
    'tips_and_updates': Icons.tips_and_updates,
    'block': Icons.block,

    // Relationships & Social deck icons
    'remove_circle': Icons.remove_circle,
    'diamond': Icons.diamond,

    // Change & Growth deck icons
    'trending_up': Icons.trending_up,
    'trending_down': Icons.trending_down,
    'autorenew': Icons.autorenew,
    'swap_vert': Icons.swap_vert,
    'replay': Icons.replay,

    // Difficulty & Complexity deck icons
    'fitness_center': Icons.fitness_center,
    'spa': Icons.spa,
    'hub': Icons.hub,
    'circle': Icons.circle,

    // Power & Authority deck icons
    'gavel': Icons.gavel,
    'volunteer_activism': Icons.volunteer_activism,
    'military_tech': Icons.military_tech,

    // Size & Quantity deck icons
    'open_in_full': Icons.open_in_full,
    'close_fullscreen': Icons.close_fullscreen,
    'inventory_2': Icons.inventory_2,
    'inventory': Icons.inventory,
    'zoom_out_map': Icons.zoom_out_map,

    // Money & Finance deck icons
    'account_balance': Icons.account_balance,
    'money_off': Icons.money_off,
    'savings': Icons.savings,
    'sell': Icons.sell,
    'payments': Icons.payments,

    // Time & Duration deck icons
    'all_inclusive': Icons.all_inclusive,
    'hourglass_empty': Icons.hourglass_empty,
    'repeat': Icons.repeat,
    'speed': Icons.speed,
    'timeline': Icons.timeline,
    'schedule': Icons.schedule,

    // Legacy/Additional icons
    'brush': Icons.brush,
    'laptop_mac': Icons.laptop_mac,
    'person': Icons.person,
    'memory': Icons.memory,
    'palette': Icons.palette,
    'theater_comedy': Icons.theater_comedy,
    'local_cafe': Icons.local_cafe,
    'import_contacts': Icons.import_contacts,

    // Fallback
    'category': Icons.category,
    'help_outline': Icons.help_outline,
    'style': Icons.style, // Default for flash cards
  };

  /// 아이콘 이름을 IconData로 변환
  ///
  /// [iconName]이 매핑에 없으면 help_outline 아이콘 반환
  static IconData getIcon(String? iconName) {
    if (iconName == null || iconName.isEmpty) {
      return Icons.help_outline;
    }

    final icon = _iconMap[iconName];
    if (icon == null) {
      // 매핑되지 않은 아이콘은 로그 출력 후 기본 아이콘 반환
      debugPrint('⚠️ Unknown icon name: $iconName, using help_outline');
      return Icons.help_outline;
    }

    return icon;
  }

  /// 새 아이콘 추가 (디버깅/개발용)
  ///
  /// Material Icons 추가 시 여기에 등록만 하면 됨
  static void registerIcon(String name, IconData icon) {
    _iconMap[name] = icon;
    debugPrint('✅ Registered icon: $name');
  }

  /// 현재 등록된 모든 아이콘 이름 반환 (디버깅용)
  static List<String> getAllIconNames() {
    return _iconMap.keys.toList()..sort();
  }

  /// 아이콘이 등록되어 있는지 확인
  static bool hasIcon(String iconName) {
    return _iconMap.containsKey(iconName);
  }
}
