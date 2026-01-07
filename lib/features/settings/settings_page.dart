import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:gap/gap.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../core/theme/app_colors.dart';
import '../../l10n/app_localizations.dart';
import '../sync/services/session_service.dart';
import '../auth/providers/auth_provider.dart';

class SettingsPage extends ConsumerWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(l10n.titleSettings),
        backgroundColor: AppColors.background,
        elevation: 0,
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          // 1. Edit Profile
          _SettingsTile(
            icon: Icons.person_outline,
            title: l10n.menuEditProfile,
            onTap: () {
               // Navigate to Onboarding with edit mode or similar
               // For MVP, just show snackbar
               ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Profile Edit - Coming Soon")));
            },
          ),
          
          const Gap(16),

          // 2. Dashboard
          _SettingsTile(
            icon: Icons.bar_chart,
            title: l10n.menuDashboard,
            onTap: () {
               ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Dashboard - Coming Soon")));
            },
          ),
          
          const Gap(40),
          const Divider(color: Colors.white24),
          const Gap(20),
          
          // 3. Logout
          _SettingsTile(
            icon: Icons.logout,
            title: l10n.menuLogout,
            color: Colors.white70,
            onTap: () {
               // Implement Logout logic
               context.go('/onboarding'); // Go back to start
            },
          ),

          const Gap(40),
          const _SectionHeader(title: "Data & Sync"),
          const Gap(10),

          // 4. Backup
          _SettingsTile(
            icon: Icons.cloud_upload,
            title: "Backup to Cloud",
            onTap: () async {
              final user = ref.read(authProvider).value;
              if (user == null) {
                _showLoginRequiredDialog(context, ref);
                return;
              }
              try {
                // Show loading
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Backing up...")));
                await ref.read(sessionServiceProvider).backupToCloud();
                if (context.mounted) {
                   ScaffoldMessenger.of(context).hideCurrentSnackBar();
                   ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Backup Successful!", style: TextStyle(color: Colors.white)), backgroundColor: AppColors.pass));
                }
              } catch (e) {
                if (context.mounted) {
                   ScaffoldMessenger.of(context).hideCurrentSnackBar();
                   ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Backup Failed: $e"), backgroundColor: AppColors.fail));
                }
              }
            },
          ),
          
          const Gap(10),

          // 5. Restore
          _SettingsTile(
            icon: Icons.cloud_download,
            title: "Restore from Cloud",
            color: AppColors.warning,
            onTap: () => _showRestoreDialog(context, ref),
          ),
          
          const Gap(16),

          // 6. Reset All
          _SettingsTile(
            icon: Icons.delete_forever,
            title: l10n.menuResetAll,
            color: AppColors.fail,
            onTap: () => _showResetDialog(context, ref, l10n),
          ),
        ],
      ),
    );
  }

  void _showResetDialog(BuildContext context, WidgetRef ref, AppLocalizations l10n) {
    // 1. First Confirmation
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AppColors.surface,
        title: Text(l10n.menuResetAll, style: const TextStyle(color: Colors.white)),
        content: Text(l10n.msgResetConfirm, style: const TextStyle(color: Colors.white70)),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: Text(l10n.commonCancel),
          ),
          TextButton(
            onPressed: () {
               Navigator.pop(ctx); 
               _showSecondConfirmDialog(context, ref);
            },
            child: Text(l10n.commonConfirm, style: const TextStyle(color: AppColors.fail)),
          ),
        ],
      ),
    );
  }

  void _showSecondConfirmDialog(BuildContext context, WidgetRef ref) {
    // 2. Second Confirmation (Double Check)
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AppColors.surface,
        title: const Text("Final Confirmation", style: TextStyle(color: AppColors.fail, fontWeight: FontWeight.bold)),
        content: const Text(
          "This action is irreversible.\nYour profile, learning history, and all stored data will be permanently deleted.\n\nAre you absolutely sure?", 
          style: TextStyle(color: Colors.white70)
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text("Cancel"),
          ),
          TextButton(
            onPressed: () {
               Navigator.pop(ctx);
               _executeReset(context, ref);
            },
            child: const Text("DELETE EVERYTHING", style: TextStyle(color: AppColors.fail, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }

  Future<void> _executeReset(BuildContext context, WidgetRef ref) async {
    // 3. Loading
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (_) => const Center(
        child: Card(
           color: AppColors.surface,
           child: Padding(
             padding: EdgeInsets.all(20),
             child: CircularProgressIndicator(),
           ),
        ),
      ),
    );

    try {
      // 4. Logic Execution
      await ref.read(sessionServiceProvider).resetAllData();
      await Supabase.instance.client.auth.signOut();
      
      if (context.mounted) {
        Navigator.pop(context); // Close Loading
        
        // 5. Success Popup
        showDialog(
          context: context,
          barrierDismissible: false,
          builder: (ctx) => AlertDialog(
            backgroundColor: AppColors.surface,
            icon: const Icon(Icons.check_circle, color: AppColors.pass, size: 50),
            title: const Text("Deletion Complete", style: TextStyle(color: Colors.white)),
            content: const Text(
              "All data has been successfully deleted.\nYou will now be returned to the login screen.", 
              style: TextStyle(color: Colors.white70),
              textAlign: TextAlign.center,
            ),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(ctx);
                  // 6. Navigate to Login/Onboarding
                  context.go('/login');
                },
                child: const Text("OK", style: TextStyle(color: AppColors.pass, fontWeight: FontWeight.bold)),
              )
            ],
          ),
        );
      }
    } catch (e) {
      if (context.mounted) {
        Navigator.pop(context); // Close Loading
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Reset Failed: $e"), backgroundColor: AppColors.fail));
      }
    }
  }
  void _showLoginRequiredDialog(BuildContext context, WidgetRef ref) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AppColors.surface,
        title: const Text("Authentication Required", style: TextStyle(color: Colors.white)),
        content: const Text(
          "You must be logged in to backup your data to the cloud.\nWould you like to sign in with Google now?", 
          style: TextStyle(color: Colors.white70)
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text("Cancel"),
          ),
          TextButton(
            onPressed: () {
               Navigator.pop(ctx);
               context.push('/login');
            },
            child: const Text("Sign In", style: TextStyle(color: AppColors.accent, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }

  void _showRestoreDialog(BuildContext context, WidgetRef ref) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AppColors.surface,
        title: const Text("Restore from Cloud", style: TextStyle(color: Colors.white)),
        content: const Text("This will overwrite your local progress with the data from the cloud. Are you sure?", style: TextStyle(color: Colors.white70)),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text("Cancel"),
          ),
          TextButton(
            onPressed: () async {
               Navigator.pop(ctx); 
               try {
                  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Restoring...")));
                  await ref.read(sessionServiceProvider).restoreFromCloud();
                  if (context.mounted) {
                     ScaffoldMessenger.of(context).hideCurrentSnackBar();
                     ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Restore Complete!", style: TextStyle(color: Colors.white)), backgroundColor: AppColors.pass));
                  }
               } catch (e) {
                 if (context.mounted) {
                   ScaffoldMessenger.of(context).hideCurrentSnackBar();
                   ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Restore Failed: $e"), backgroundColor: AppColors.fail));
                 }
               }
            },
            child: const Text("Restore", style: TextStyle(color: AppColors.warning)),
          ),
        ],
      ),
    );
  }
}

class _SettingsTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final VoidCallback onTap;
  final Color color;

  const _SettingsTile({
    required this.icon,
    required this.title,
    required this.onTap,
    this.color = Colors.white,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      onTap: onTap,
      tileColor: AppColors.surface,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      leading: Icon(icon, color: color),
      title: Text(title, style: TextStyle(color: color, fontSize: 16)),
      trailing: Icon(Icons.chevron_right, color: color.withOpacity(0.5)),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final String title;
  const _SectionHeader({required this.title});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 4, bottom: 4),
      child: Text(
        title.toUpperCase(),
        style: const TextStyle(
          color: Colors.white54,
          fontSize: 12,
          fontWeight: FontWeight.bold,
          letterSpacing: 1.2,
        ),
      ),
    );
  }
}
