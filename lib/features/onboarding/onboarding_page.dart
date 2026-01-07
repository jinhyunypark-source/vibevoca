import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/app_colors.dart';
import 'providers/onboarding_provider.dart';
import 'widgets/onboarding_steps.dart';
import 'widgets/persona_card.dart';

import '../../l10n/app_localizations.dart';

class OnboardingPage extends ConsumerWidget {
  const OnboardingPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(onboardingControllerProvider);
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      body: SafeArea(
        child: state.when(
          data: (persona) {
            if (persona == null) {
              return const OnboardingSteps();
            }
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    "Your Identity",
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.w300),
                  ).animate().fadeIn(duration: 500.ms),
                  const SizedBox(height: 30),
                  PersonaCard(persona: persona),
                  const SizedBox(height: 50),
                  ElevatedButton(
                    onPressed: () {
                      // Navigate to Next Step (Login)
                      context.go('/login');
                    },
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 16),
                      backgroundColor: AppColors.pass,
                    ),
                    child: const Text("Start Journey", style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
                  ).animate().fadeIn(delay: 1000.ms, duration: 500.ms).moveY(begin: 20, end: 0),
                ],
              ),
            );
          },
          error: (err, stack) => Center(child: Text('Error: $err')),
          loading: () => Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const CircularProgressIndicator(color: AppColors.accent),
                const SizedBox(height: 20),
                const Text("Summoning your Persona...").animate().shimmer(),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
