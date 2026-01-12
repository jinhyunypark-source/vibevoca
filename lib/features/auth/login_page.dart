import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:gap/gap.dart';
import 'package:go_router/go_router.dart';
import 'package:vibevoca/core/theme/app_colors.dart';
import 'package:vibevoca/features/auth/providers/auth_provider.dart';
import 'package:vibevoca/features/context/providers/deck_collection_provider.dart'; // For supabaseRepositoryProvider

class LoginPage extends ConsumerStatefulWidget {
  const LoginPage({super.key});

  @override
  ConsumerState<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends ConsumerState<LoginPage> {
  bool _isSigningIn = false;

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);

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
          if (profile != null && profile.interestIds.isNotEmpty) {
             context.go('/context-selection');
          } else {
             context.go('/profile-setup');
          }
        }
      } else if (next.hasError) {
        if (mounted) {
          setState(() => _isSigningIn = false);
        }
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

              // Primary Action: Start as Guest
              ElevatedButton(
                onPressed: _isSigningIn ? null : () => context.go('/context-selection'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 18),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                  elevation: 8,
                  shadowColor: AppColors.primary.withOpacity(0.5),
                ),
                child: const Text(
                  "Start as Guest",
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 0.5,
                  ),
                ),
              ).animate().fadeIn(delay: 400.ms).moveY(begin: 20, end: 0),

              const Gap(20),

              // Secondary Action: Google Sign In (Handles Sign Up too)
              if (authState.isLoading || _isSigningIn)
                const Center(
                  child: SizedBox(
                    width: 24,
                    height: 24,
                    child: CircularProgressIndicator(
                      color: AppColors.primary,
                      strokeWidth: 2.5,
                    ),
                  )
                )
              else
                OutlinedButton.icon(
                  onPressed: () async {
                    setState(() => _isSigningIn = true);
                    try {
                      await ref.read(authProvider.notifier).signInWithGoogle();
                    } catch (e) {
                      if (mounted) {
                        setState(() => _isSigningIn = false);
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text('Sign in failed: $e')),
                        );
                      }
                    }
                    // Safety check: if after delay we are still here and no user, stop loading.
                    // But usually listener handles success.
                    if (mounted) {
                       // Give it a moment? No, rely on listener.
                       // Use a timeout just in case?
                       /* 
                       Future.delayed(const Duration(seconds: 10), () {
                          if (mounted && _isSigningIn) {
                             setState(() => _isSigningIn = false);
                          }
                       });
                       */
                    }
                  },
                  icon: Image.asset(
                    'assets/images/google_logo.png', // Ensure this asset exists or use Icon
                    height: 24,
                    errorBuilder: (ctx, _, __) => const Icon(Icons.login, color: Colors.white),
                  ),
                  label: const Text(
                    "Continue with Google",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: Colors.white30, width: 1.5),
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30),
                    ),
                  ),
                ).animate().fadeIn(delay: 600.ms).moveY(begin: 20, end: 0),
              
              const Gap(10),
              const Center(
                child: Text(
                  "Sign in to sync your progress across devices",
                  style: TextStyle(color: Colors.white38, fontSize: 12),
                ),
              ),
              
              const Gap(40),
            ],
          ),
        ),
      ),
    );
  }
}
