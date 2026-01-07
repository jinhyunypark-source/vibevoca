import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:gap/gap.dart';
import 'package:go_router/go_router.dart';
import 'package:vibevoca/core/theme/app_colors.dart';
import 'package:vibevoca/features/auth/providers/auth_provider.dart';
import 'package:vibevoca/features/context/providers/deck_collection_provider.dart'; // For supabaseRepositoryProvider

class LoginPage extends ConsumerWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authProvider);

    // Listen for successful login handling
    // Listen for successful login handling
    ref.listen(authProvider, (previous, next) async {
      if (next.hasValue && next.value != null) {
        // User logged in. Check if profile exists and has interests/jobs.
        final userId = next.value!.id;
        final repo = ref.read(supabaseRepositoryProvider);
        
        // Use a local loading indicator if needed, but for now just perform check
        final profile = await repo.getProfile(userId);

        if (context.mounted) {
          // If profile exists and has interest_ids (meaning setup completed at least once)
          // Redirect to Context Selection.
          // Always go to Profile Setup as per requested flow
          context.go('/profile-setup');
        }
      } else if (next.hasError) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Login Failed: ${next.error}')),
        );
      }
    });

    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 30),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Spacer(),
              // Logo or App Title
              Center(
                child: Container(
                  width: 100,
                  height: 100,
                  decoration: BoxDecoration(
                    color: AppColors.primary.withOpacity(0.2),
                    shape: BoxShape.circle,
                    boxShadow: [
                      BoxShadow(
                        color: AppColors.primary.withOpacity(0.5),
                        blurRadius: 30,
                        spreadRadius: 5,
                      )
                    ],
                  ),
                  child: const Icon(Icons.record_voice_over, size: 50, color: Colors.white),
                ),
              ).animate().scale(duration: 800.ms, curve: Curves.easeOutBack),
              
              const Gap(30),
              
              const Text(
                "VibeVoca", 
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 2.0
                )
              ).animate().fadeIn().moveY(begin: 10, end: 0),
              
              const Gap(10),
              const Text(
                "Master Vocabulary with Context", 
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Colors.white54,
                  fontSize: 16,
                )
              ).animate().fadeIn(delay: 200.ms),

              const Spacer(),

              // Google Sign-In Button
              if (authState.isLoading)
                const Center(child: CircularProgressIndicator(color: AppColors.primary))
              else
                ElevatedButton.icon(
                  onPressed: () {
                    ref.read(authProvider.notifier).signInWithGoogle();
                  },
                  icon: Image.asset(
                     // We might need a google logo asset, using standard icon for now if asset missing
                     // or creating a placeholder
                    'assets/images/google_logo.png', 
                    height: 24,
                    errorBuilder: (ctx, _, __) => const Icon(Icons.login, color: Colors.black),
                  ),
                  label: const Text(
                    "Sign in with Google",
                    style: TextStyle(
                      color: Colors.black87,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.white,
                    foregroundColor: Colors.black87,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30),
                    ),
                  ),
                ).animate().fadeIn(delay: 400.ms).moveY(begin: 20, end: 0),
              
              const Gap(20),
              
              // Skip option (optional)
              TextButton(
                onPressed: () => context.go('/context-selection'),
                child: const Text("Continue as Guest", style: TextStyle(color: Colors.white54)),
              ),
              
              const Gap(40),
            ],
          ),
        ),
      ),
    );
  }
}
