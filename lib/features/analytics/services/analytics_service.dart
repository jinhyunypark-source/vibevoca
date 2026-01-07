import 'package:firebase_analytics/firebase_analytics.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

final analyticsServiceProvider = Provider<AnalyticsService>((ref) {
  return AnalyticsService();
});

class AnalyticsService {
  final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;

  Future<void> logScreenView(String screenName) async {
    await _analytics.logScreenView(screenName: screenName);
    if (kDebugMode) {
      print('[Analytics] Screen View: $screenName');
    }
  }

  Future<void> logEvent(String name, {Map<String, Object>? parameters}) async {
    await _analytics.logEvent(name: name, parameters: parameters);
    if (kDebugMode) {
      print('[Analytics] Event: $name, Params: $parameters');
    }
  }

  Future<void> logLogin({String? method}) async {
    await _analytics.logLogin(loginMethod: method);
  }

  Future<void> setUserProperty({required String name, required String value}) async {
    await _analytics.setUserProperty(name: name, value: value);
  }

  Future<void> setUserId(String? id) async {
    await _analytics.setUserId(id: id);
  }
}
