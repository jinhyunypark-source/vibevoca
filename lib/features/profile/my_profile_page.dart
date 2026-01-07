import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:vibevoca/core/theme/app_colors.dart';
import 'package:vibevoca/features/auth/providers/auth_provider.dart';
import 'package:vibevoca/features/profile/providers/profile_provider.dart';
import 'package:vibevoca/features/profile/profile_setup_page.dart'; // Reuse setup page logic or widget?
// Actually, let's just reuse ProfileSetupPage logic but wrap it or create a new view if significantly different.
// For now, MyProfile is essentially the same as Setup but with "Log Out" and different header.
// Let's create a dedicated page that embeds the form or navigates to it.

// Re-using ProfileSetupPage logic is efficient. Let's make ProfileSetupPage adaptable or just link to it. 
// But requested feature was "My Profile" with email etc.

class MyProfilePage extends ConsumerWidget {
  const MyProfilePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authProvider).value;
    final profile = ref.watch(userProfileProvider).value;
    final allOptions = ref.watch(interestsProvider).asData?.value;

    // Helper to get selected items
    List<String> getSelectedLabels(List<String> ids, String category) {
      if (allOptions == null) return [];
      return ids.map((id) {
        final option = allOptions.firstWhere((e) => e.id == id, orElse: () => allOptions.first);
        return (option.id == id && option.category == category) ? option.labelKo : '';
      }).where((s) => s != null && s.isNotEmpty).toList().cast<String>();
    }

    final jobLabels = profile != null ? getSelectedLabels(profile.interestIds, 'job') : <String>[];
    final interestLabels = profile != null ? getSelectedLabels(profile.interestIds, 'interest') : <String>[];

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        title: const Text("My Profile"),
        centerTitle: true,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              // 1. User Info Header
              const CircleAvatar(
                radius: 40,
                backgroundColor: AppColors.primary,
                child: Icon(Icons.person, size: 40, color: Colors.white),
              ),
              const SizedBox(height: 16),
              Text(
                user?.email ?? 'Guest User',
                style: const TextStyle(color: Colors.white70, fontSize: 16),
              ),
              
              const SizedBox(height: 32),
              
              // 2. Profile Details Card
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.05),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.white10),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildSectionHeader(context, "Occupation", onEdit: () {
                         context.push('/profile-setup'); // Reuse setup page for editing
                    }),
                    const SizedBox(height: 10),
                    Text(
                      jobLabels.isNotEmpty ? jobLabels.first : 'Not set',
                      style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w500),
                    ),
                    
                    const SizedBox(height: 24),
                    
                    _buildSectionHeader(context, "Interests", onEdit: () {
                        context.push('/profile-setup');
                    }),
                    const SizedBox(height: 10),
                    Wrap(
                      spacing: 8, runSpacing: 8,
                      children: interestLabels.map((label) => Chip(
                        label: Text(label),
                        backgroundColor: AppColors.surface,
                        labelStyle: const TextStyle(color: Colors.white),
                        side: BorderSide.none,
                      )).toList(),
                    ),
                  ],
                ),
              ),
              
              const SizedBox(height: 50),
              
              // 3. Logout Button
              SizedBox(
                width: double.infinity,
                child: OutlinedButton.icon(
                  onPressed: () {
                    ref.read(authProvider.notifier).signOut();
                    context.go('/login');
                  },
                  icon: const Icon(Icons.logout, color: Colors.redAccent),
                  label: const Text("Log Out", style: TextStyle(color: Colors.redAccent)),
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: Colors.redAccent),
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionHeader(BuildContext context, String title, {VoidCallback? onEdit}) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(title, style: const TextStyle(color: AppColors.accent, fontWeight: FontWeight.bold)),
        if (onEdit != null)
          GestureDetector(
            onTap: onEdit,
            child: const Icon(Icons.edit, size: 18, color: Colors.white54),
          ),
      ],
    );
  }
}
