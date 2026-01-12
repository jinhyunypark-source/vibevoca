import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import 'package:gap/gap.dart';
import '../../../core/theme/app_colors.dart';
import 'providers/deck_collection_provider.dart';
import 'widgets/deck_box.dart';
import '../../l10n/app_localizations.dart';
import '../../core/widgets/app_drawer.dart';

import 'package:vibevoca/features/auth/providers/auth_provider.dart';
import 'package:vibevoca/features/context/models/deck_group.dart';
import 'package:vibevoca/features/context/models/supabase_models.dart';
import '../profile/providers/profile_provider.dart';
import '../sync/services/session_service.dart';
import 'package:vibevoca/features/analytics/services/analytics_service.dart';

class DeckSelectionPage extends ConsumerStatefulWidget {
  const DeckSelectionPage({super.key});

  @override
  ConsumerState<DeckSelectionPage> createState() => _DeckSelectionPageState();
}

class _DeckSelectionPageState extends ConsumerState<DeckSelectionPage> {
  // We keep track of the expanded category ID
  String? _expandedCategoryId;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref.read(analyticsServiceProvider).logScreenView('DeckSelectionPage');
    });
  }

  @override
  Widget build(BuildContext context) {
    final categoriesAsync = ref.watch(categoriesProvider);
    final rawDecksAsync = ref.watch(deckCollectionProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text("주제 선택", style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1.2)),
        centerTitle: true,
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      endDrawer: const AppDrawer(),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          final reviewDeck = DeckGroup(
            id: 'Review_Session',
            title: 'Review',
            titleKo: '단어 복습',
            icon: 'history_edu', // Custom icon for review
            color: const Color(0xFF6C63FF), // Accent color
            progress: 0.0,
          );
          context.push('/battle', extra: reviewDeck);
        },
        label: const Text("단어 복습", style: TextStyle(fontWeight: FontWeight.bold)),
        icon: const Icon(Icons.refresh),
        backgroundColor: AppColors.accent,
        foregroundColor: Colors.white,
      ),
      body: SafeArea(
        child: categoriesAsync.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (e,s) => Center(child: Text('Error: $e')),
          data: (categories) {
            return rawDecksAsync.when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (e,s) => Center(child: Text('Error: $e')),
              data: (allDecks) {
                if (categories.isEmpty) return const Center(child: Text("No categories found."));

                // Auto-expand first category if none selected
                if (_expandedCategoryId == null && categories.isNotEmpty) {
                    _expandedCategoryId = categories.first.id;
                }

                return ListView.builder(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
                  itemCount: categories.length,
                  itemBuilder: (context, index) {
                     final cat = categories[index];
                     final catDecks = allDecks.where((d) => d.categoryId == cat.id).toList();
                     final isExpanded = cat.id == _expandedCategoryId;
                     
                     // Helper to toggle expansion
                     void toggle() {
                       setState(() {
                         if (isExpanded) {
                           _expandedCategoryId = null; 
                         } else {
                           _expandedCategoryId = cat.id;
                         }
                       });
                     }

                     // Parse Theme Color
                     int colorValue = 0xFF4A90E2; 
                     try { colorValue = int.parse(cat.color.replaceFirst('#', '0xFF')); } catch (_) {}
                     final themeColor = Color(colorValue);

                     // Map Icon
                     IconData catIcon = Icons.layers;
                     switch (cat.icon) {
                       case 'forum': catIcon = Icons.forum; break;
                       case 'palette': catIcon = Icons.palette; break;
                       case 'lightbulb': catIcon = Icons.lightbulb; break;
                       case 'diversity_3': catIcon = Icons.diversity_3; break;
                       case 'trending_up': catIcon = Icons.trending_up; break;
                       case 'gavel': catIcon = Icons.gavel; break;
                       case 'extension': catIcon = Icons.extension; break;
                       case 'bar_chart': catIcon = Icons.bar_chart; break;
                       case 'attach_money': catIcon = Icons.attach_money; break;
                       case 'schedule': catIcon = Icons.schedule; break;
                       default: if (cat.title.startsWith("Comm")) catIcon = Icons.chat;
                     }

                     return AnimatedContainer(
                       duration: 400.ms,
                       curve: Curves.easeOutQuint,
                       margin: const EdgeInsets.only(bottom: 12),
                       decoration: BoxDecoration(
                         color: isExpanded ? AppColors.surface : AppColors.surface.withOpacity(0.5),
                         borderRadius: BorderRadius.circular(16),
                         border: Border.all(
                           color: isExpanded ? themeColor : Colors.white10,
                           width: isExpanded ? 2 : 1
                         )
                       ),
                       child: Column(
                         crossAxisAlignment: CrossAxisAlignment.start,
                         children: [
                           // 1. Accordion Header (Category Title)
                           InkWell(
                             onTap: toggle,
                             borderRadius: BorderRadius.circular(16),
                             child: Container(
                               padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
                               decoration: isExpanded ? BoxDecoration(
                                 boxShadow: [
                                   BoxShadow(
                                     color: themeColor.withOpacity(0.2),
                                     blurRadius: 15,
                                     spreadRadius: -2,
                                     offset: const Offset(0, 4)
                                   )
                                 ]
                               ) : null,
                               child: Row(
                                 children: [
                                   // Category Icon
                                   Icon(
                                      catIcon,
                                      color: isExpanded ? themeColor : Colors.white54,
                                      size: 28,
                                   ),
                                   const Gap(16),
                                   Expanded(
                                     child: Text(
                                       (cat.titleKo ?? cat.title).toUpperCase(),
                                       style: TextStyle(
                                         color: isExpanded ? Colors.white : Colors.white70,
                                         fontWeight: FontWeight.bold,
                                         fontSize: 18,
                                         letterSpacing: 1.1,
                                         shadows: isExpanded ? [
                                            Shadow(color: themeColor.withOpacity(0.6), blurRadius: 10)
                                         ] : []
                                       ),
                                     ),
                                   ),
                                   Icon(
                                      isExpanded ? Icons.keyboard_arrow_up : Icons.keyboard_arrow_down,
                                      color: isExpanded ? themeColor : Colors.white54
                                   )
                                 ],
                               ),
                             ),
                           ),

                           // 2. Expanded Content (Decks Grid)
                           AnimatedCrossFade(
                             firstChild: Container(height: 0), 
                             secondChild: Container(
                               // Added top padding to account for DeckBox 'selected' upward translation (-10px) and shadow
                               padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
                               child: catDecks.isEmpty 
                                 ? const Padding(
                                     padding: EdgeInsets.all(20),
                                     child: Center(child: Text("No decks available.", style: TextStyle(color: Colors.white38))),
                                   )
                                 : GridView.builder(
                                    shrinkWrap: true, // Grid is inside ListView
                                    physics: const NeverScrollableScrollPhysics(), // Scroll with parent
                                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                                      crossAxisCount: 3, 
                                      childAspectRatio: 0.85, // Taller cards to fit text
                                      crossAxisSpacing: 8,    // Narrower gap
                                      mainAxisSpacing: 12,
                                    ),
                                    itemCount: catDecks.length,
                                    itemBuilder: (context, deckIndex) {
                                       final d = catDecks[deckIndex];
                                       final user = ref.read(authProvider).value;
                                       
                                       // Parse color
                                       int colorValue = 0xFFFF5733; 
                                       try { colorValue = int.parse(d.color.replaceAll('#', '0xFF')); } catch (_) {}
                                       final deckColor = Color(colorValue);
                                       
                                       // --- Progress/Stats Logic ---
                                       final syncService = ref.watch(sessionServiceProvider);
                                       final deckState = syncService.getDeckState(d.id);
                                       
                                       // Priority: DeckState (Total from Sync) -> VocabDeck (Count from DB) -> 0
                                       // d is VocabDeck (from deckCollectionProvider)
                                       final int total = d.cardCount;
                                       final int memorized = deckState?.memorizedCount ?? 0;
                                       final int review = deckState?.remindCount ?? 0;
                                       
                                       final userProfile = ref.watch(userProfileProvider).value;
                                       final lastPlayedId = userProfile?.lastPlayedDeckId;
                                       final bool isLastPlayed = d.id == lastPlayedId;
                                       
                                       return DeckBox(
                                          title: d.titleKo ?? d.title, 
                                          deckId: d.title,
                                          baseColor: deckColor, 
                                          progress: total > 0 ? memorized / total : 0.0, 
                                          status: DeckStatus.locked, // Ignored
                                          iconAsset: d.icon,
                                          compact: true,
                                          
                                          // New Stats
                                          memorizedCount: memorized,
                                          reviewCount: review,
                                          totalCount: total,
                                          isLastPlayed: isLastPlayed,
                                          
                                          onTap: () { 
                                            // Always navigate, even if locked
                                            final user = ref.read(authProvider).value;
                                            if (user != null) {
                                               // Update Last Played & Refresh State (Fire & Forget)
                                               ref.read(profileControllerProvider.notifier).updateLastPlayedDeck(d.id);
                                            }
                                            
                                            // Pass group data
                                            final group = DeckGroup(
                                               id: d.id,
                                               title: d.title,
                                               titleKo: d.titleKo ?? d.title,
                                               color: deckColor,
                                               icon: d.icon,
                                               progress: total > 0 ? memorized / total : 0.0,
                                               totalCards: total,
                                            );
                                            if (context.mounted) {
                                               context.push('/battle', extra: group);
                                            }
                                          },
                                       );
                                    },
                                 ),
                             ),
                             crossFadeState: isExpanded ? CrossFadeState.showSecond : CrossFadeState.showFirst,
                             duration: 300.ms,
                             sizeCurve: Curves.easeInOutQuart,
                           ),
                         ],
                       ),
                     );
                  },
                );
              },
            );
          },
        ),
      ),
    );
  }
}
