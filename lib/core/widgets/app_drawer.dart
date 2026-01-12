import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:gap/gap.dart';
import '../../core/theme/app_colors.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../l10n/app_localizations.dart';
import '../../features/sync/services/session_service.dart';
import '../../features/auth/providers/auth_provider.dart';

class AppDrawer extends ConsumerWidget {
  const AppDrawer({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    
    final user = ref.read(authProvider).value;
    
    return Drawer(
      backgroundColor: AppColors.surface,
      child: Column(
        children: [
          // Header
          Container(
            padding: const EdgeInsets.fromLTRB(20, 60, 20, 20),
            color: AppColors.primary,
            child: Row(
              children: [
                const CircleAvatar(
                  radius: 30,
                  backgroundColor: Colors.white24,
                  child: Icon(Icons.person, size: 40, color: Colors.white),
                ),
                const Gap(16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                         user?.email ?? "VibeVoca User", 
                         style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
                         overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ),
                )
              ],
            ),
          ),
          
          Expanded(
            child: ListView(
              padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 10),
              children: [
                // 1. Manage Interests
                _DrawerTile(
                  icon: Icons.interests,
                  title: "Manage Interests", 
                  onTap: () {
                    context.pop();
                    context.push('/profile-setup');
                  },
                ),
                
                // 2. Learning Dashboard
                _DrawerTile(
                  icon: Icons.bar_chart, 
                  title: l10n.menuDashboard,
                  onTap: () {
                    context.pop();
                    context.push('/dashboard');
                  }
                ),

                const Divider(color: Colors.white10, height: 30),
                const _SectionHeader(title: "Account"),

                 // 3. Logout
                _DrawerTile(
                  icon: Icons.logout,
                  title: l10n.menuLogout,
                  color: Colors.white70,
                  onTap: () async {
                     await ref.read(authProvider.notifier).signOut();
                     if (context.mounted) {
                       context.go('/login');
                     }
                  },
                ),

                const Divider(color: Colors.white10, height: 30),
                const _SectionHeader(title: "Data & Sync"),

                // 4. Backup
                _DrawerTile(
                  icon: Icons.cloud_upload,
                  title: "Backup to Cloud",
                  onTap: () async {
                    if (user == null) {
                       _showGuestRestrictionDialog(context);
                       return;
                    }

                    // Show Loading Dialog (on top of Drawer)
                    showDialog(
                      context: context,
                      barrierDismissible: false,
                      builder: (ctx) => const Center(
                        child: Card(
                           child: Padding(
                             padding: EdgeInsets.all(20),
                             child: CircularProgressIndicator(),
                           ),
                        ),
                      ),
                    );

                    try {
                      await ref.read(sessionServiceProvider).backupToCloud();
                      
                      if (context.mounted) {
                         Navigator.pop(context); // Close Loading
                         // Show Success Dialog
                         showDialog(
                           context: context,
                           builder: (ctx) => AlertDialog(
                             backgroundColor: AppColors.surface,
                             icon: const Icon(Icons.check_circle, color: AppColors.pass, size: 48),
                             title: const Text("Backup Successful!", style: TextStyle(color: Colors.white)),
                             content: const Text("Your progress has been saved to the cloud.", style: TextStyle(color: Colors.white70), textAlign: TextAlign.center),
                             actions: [
                               TextButton(
                                 onPressed: () => Navigator.pop(ctx),
                                 child: const Text("OK", style: TextStyle(color: AppColors.pass, fontWeight: FontWeight.bold)),
                               )
                             ],
                           ),
                         );
                      }
                    } catch (e) {
                      if (context.mounted) {
                         Navigator.pop(context); // Close Loading
                         // Show Error Dialog
                         showDialog(
                           context: context,
                           builder: (ctx) => AlertDialog(
                             backgroundColor: AppColors.surface,
                             icon: const Icon(Icons.error, color: AppColors.fail, size: 48),
                             title: const Text("Backup Failed", style: TextStyle(color: Colors.white)),
                             content: Text("Error: $e", style: const TextStyle(color: Colors.white70)),
                             actions: [
                               TextButton(
                                 onPressed: () => Navigator.pop(ctx),
                                 child: const Text("OK", style: TextStyle(color: Colors.white)),
                               )
                             ],
                           ),
                         );
                      }
                    }
                  },
                ),

                // 5. Restore
                _DrawerTile(
                  icon: Icons.cloud_download,
                  title: "Restore from Cloud",
                  color: AppColors.warning,
                  onTap: () {
                    if (user == null) {
                       _showGuestRestrictionDialog(context);
                       return;
                    }
                    // Do not close drawer immediately to keep context valid
                    _showRestoreDialog(context, ref);
                  },
                ),

                // 6. Reset
                _DrawerTile(
                  icon: Icons.delete_forever,
                  title: l10n.menuResetAll,
                  color: AppColors.fail,
                  onTap: () {
                    // Do not close drawer immediately to keep context valid
                    _showResetDialog(context, ref, l10n, user != null);
                  },
                ),
              ],
            ),
          ),
          
          // Version Info
          Padding(
            padding: const EdgeInsets.all(20.0),
            child: Text("Version 1.0.0", style: TextStyle(color: Colors.white.withOpacity(0.3), fontSize: 12)),
          ),
        ],
      ),
    );
  }

  void _showGuestRestrictionDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AppColors.surface,
        title: const Text("Guest Feature", style: TextStyle(color: Colors.white)),
        content: const Text("Cloud features are not available for guests. Would you like to go to the login screen?", style: TextStyle(color: Colors.white70)),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text("Cancel")),
          TextButton(
            onPressed: () {
              Navigator.pop(ctx);
              context.go('/login');
            },
            child: const Text("Go to Login", style: TextStyle(color: AppColors.primary)),
          ),
        ],
      ),
    );
  }

  void _showResetDialog(BuildContext context, WidgetRef ref, AppLocalizations l10n, bool isUser) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AppColors.surface,
        title: Text(l10n.menuResetAll, style: const TextStyle(color: Colors.white)),
        content: const Text("Would you like to reset all learning data?", style: TextStyle(color: Colors.white70)),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: Text(l10n.commonCancel),
          ),
          TextButton(
            onPressed: () async {
               Navigator.pop(ctx); 
               
               try {
                 ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Resetting all data...")));
                 
                 if (isUser) {
                    // 1. Full Reset (Cloud + Local)
                    await ref.read(sessionServiceProvider).resetAllData();
                 } else {
                    // 2. Local Reset Only (Guest)
                    await ref.read(sessionServiceProvider).clearLocalData();
                 }
                 
                 if (context.mounted) {
                    ScaffoldMessenger.of(context).hideCurrentSnackBar();
                    
                    // Show Success Dialog
                    await showDialog(
                      context: context,
                      barrierDismissible: false,
                      builder: (ctx) => AlertDialog(
                        backgroundColor: AppColors.surface,
                        icon: const Icon(Icons.check_circle, color: AppColors.pass, size: 50),
                        title: const Text("Reset Complete", style: TextStyle(color: Colors.white)),
                        content: const Text(
                          "All data has been deleted.", 
                          style: TextStyle(color: Colors.white70),
                          textAlign: TextAlign.center,
                        ),
                        actions: [], 
                      ),
                    ).timeout(const Duration(seconds: 1), onTimeout: () {
                       if (context.mounted && Navigator.canPop(context)) {
                          Navigator.pop(context); 
                       }
                    });
                    
                    await Future.delayed(const Duration(seconds: 1));
                    
                    // Navigate to Login/Start
                    if (isUser) {
                        await Supabase.instance.client.auth.signOut();
                    }
                    if (context.mounted) {
                       context.go('/login');
                    }
                 }
               } catch (e) {
                 if (context.mounted) {
                   ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Reset Failed: $e"), backgroundColor: AppColors.fail));
                 }
               }
            },
            child: Text(l10n.commonConfirm, style: const TextStyle(color: AppColors.fail)),
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
               Navigator.pop(ctx); // Close Confirm Dialog
               
               // Show Loading
               showDialog(
                  context: context,
                  barrierDismissible: false,
                  builder: (ctx) => const Center(
                    child: Card(
                       child: Padding(
                         padding: EdgeInsets.all(20),
                         child: CircularProgressIndicator(),
                       ),
                    ),
                  ),
               );

               try {
                  await ref.read(sessionServiceProvider).restoreFromCloud();
                  
                  if (context.mounted) {
                     Navigator.pop(context); // Close Loading
                     showDialog(
                       context: context,
                       builder: (ctx) => AlertDialog(
                         backgroundColor: AppColors.surface,
                         icon: const Icon(Icons.check_circle, color: AppColors.pass, size: 48),
                         title: const Text("Restore Complete!", style: TextStyle(color: Colors.white)),
                         content: const Text("Your learning progress has been restored.", style: TextStyle(color: Colors.white70), textAlign: TextAlign.center),
                         actions: [
                           TextButton(
                             onPressed: () => Navigator.pop(ctx),
                             child: const Text("OK", style: TextStyle(color: AppColors.pass, fontWeight: FontWeight.bold)),
                           )
                         ],
                       ),
                     );
                  }
               } catch (e) {
                 if (context.mounted) {
                   Navigator.pop(context); // Close Loading
                   showDialog(
                      context: context,
                      builder: (ctx) => AlertDialog(
                        backgroundColor: AppColors.surface,
                        title: const Text("Restore Failed", style: TextStyle(color: Colors.white)),
                        content: Text("Error: $e", style: const TextStyle(color: Colors.white70)),
                        actions: [TextButton(onPressed: () => Navigator.pop(ctx), child: const Text("OK"))],
                      ),
                   );
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

class _DrawerTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final VoidCallback onTap;
  final Color color;

  const _DrawerTile({
    required this.icon,
    required this.title,
    required this.onTap,
    this.color = Colors.white,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      onTap: onTap,
      dense: true,
      leading: Icon(icon, color: color, size: 22),
      title: Text(title, style: TextStyle(color: color, fontSize: 14)),
      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 0),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      hoverColor: Colors.white10,
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final String title;
  const _SectionHeader({required this.title});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 16, bottom: 8, top: 0),
      child: Text(
        title.toUpperCase(),
        style: const TextStyle(
          color: Colors.white38,
          fontSize: 10,
          fontWeight: FontWeight.bold,
          letterSpacing: 1.5,
        ),
      ),
    );
  }
}
