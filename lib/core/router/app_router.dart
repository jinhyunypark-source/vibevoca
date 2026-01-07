import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../features/onboarding/onboarding_page.dart';
import '../../features/profile/profile_setup_page.dart';
import '../../features/profile/my_profile_page.dart';
import '../../features/context/context_selection_page.dart';
import '../../features/context/context_init_page.dart';
import '../../features/context/deck_selection_page.dart';
import '../../features/battle/deck_battle_page.dart';
import '../../features/settings/settings_page.dart';
import '../../features/auth/login_page.dart';
import '../../features/context/models/deck_group.dart';
import '../../features/profile/dashboard_page.dart';

part 'app_router.g.dart';

@riverpod
GoRouter goRouter(Ref ref) {
  return GoRouter(
    initialLocation: '/login',
    routes: [
      GoRoute(
        path: '/onboarding',
        builder: (context, state) => const OnboardingPage(),
      ),
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginPage(),
      ),
      GoRoute(
        path: '/profile-setup',
        builder: (context, state) => const ProfileSetupPage(),
      ),
      GoRoute(
        path: '/my-profile',
        builder: (context, state) => const MyProfilePage(),
      ),
      GoRoute(
        path: '/context-selection',
        builder: (context, state) => const ContextInitPage(),
      ),
      GoRoute(
        path: '/deck-selection',
        builder: (context, state) => const DeckSelectionPage(),
      ),
      GoRoute(
        path: '/battle',
        builder: (context, state) {
           final deckGroup = state.extra as DeckGroup?;
           return DeckBattlePage(deckGroup: deckGroup);
        },
      ),
      GoRoute(
        path: '/settings',
        builder: (context, state) => const SettingsPage(),
      ),
      GoRoute(
        path: '/dashboard',
        builder: (context, state) => const DashboardPage(),
      ),
    ],
  );
}
