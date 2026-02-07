import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart'; // Import Supabase
import 'package:firebase_core/firebase_core.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart'; // Added import for Mobile Ads
import 'package:vibevoca/core/router/app_router.dart';
import 'package:vibevoca/core/theme/app_theme.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'l10n/app_localizations.dart';

import 'dart:async';
import 'dart:ui' as io;

Future<void> main() async {
  runZonedGuarded(() async {
    WidgetsFlutterBinding.ensureInitialized();

    // Initialize Mobile Ads
    await MobileAds.instance.initialize();

    print("🚀 [Main] App Starting...");

    try {
      // Initialize Supabase
      await Supabase.initialize(
        url: 'https://anizwbojntonkfwgyosa.supabase.co',
        anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFuaXp3Ym9qbnRvbmtmd2d5b3NhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjcyOTgyNzIsImV4cCI6MjA4Mjg3NDI3Mn0.4Jjl6OWoQXyjD-vYMVbZ4hTkECfWT7erW3j8y2Qynd8',
      );
      print("✅ [Main] Supabase initialized");

      // Initialize Firebase (Analytics)
      await Firebase.initializeApp();
      print("✅ [Main] Firebase initialized");
    } catch (e, stack) {
      print("❌ [Main] Supabase init failed: $e\n$stack");
    }

    runApp(const ProviderScope(child: VibeVocaApp()));
  }, (error, stack) {
    print("❌ [Main] Uncaught Error: $error\n$stack");
  });
}

class VibeVocaApp extends ConsumerWidget {
  const VibeVocaApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(goRouterProvider);

    return MaterialApp.router(
      title: 'VibeVoca',
      theme: AppTheme.darkTheme,
      routerConfig: router,
      debugShowCheckedModeBanner: false,
      localizationsDelegates: [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('ko'), // Default
        Locale('en'),
      ],
      scrollBehavior: const MaterialScrollBehavior().copyWith(
        dragDevices: {
          // Enable mouse drag on desktop for easier testing of swipe/scroll
          io.PointerDeviceKind.mouse,
          io.PointerDeviceKind.touch,
          io.PointerDeviceKind.stylus,
          io.PointerDeviceKind.unknown,
        },
      ),
    );
  }
}
