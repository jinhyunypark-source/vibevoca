import 'package:flutter/material.dart';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import 'package:gap/gap.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/utils/material_icons_mapper.dart';
import '../context/models/deck_group.dart';
import '../context/providers/context_provider.dart';
import 'providers/battle_provider.dart';
import 'widgets/flash_card.dart';
import '../../l10n/app_localizations.dart';
import '../auth/providers/auth_provider.dart';
import '../profile/providers/profile_provider.dart';
import '../context/providers/deck_collection_provider.dart';
import '../sync/services/session_service.dart';
import 'package:vibevoca/features/analytics/services/analytics_service.dart';

class DeckBattlePage extends ConsumerStatefulWidget {
  final DeckGroup? deckGroup; // Passed from selection
  const DeckBattlePage({super.key, this.deckGroup});

  @override
  ConsumerState<DeckBattlePage> createState() => _DeckBattlePageState();
}

class _DeckBattlePageState extends ConsumerState<DeckBattlePage> {
  // PageController will be late-initialized to set initialPage
  PageController? _pageController; 
  int _initialIndex = 0;
  bool _isInit = false;

  @override
  void initState() {
    super.initState();
    // Log Battle Start
    WidgetsBinding.instance.addPostFrameCallback((_) {
       ref.read(analyticsServiceProvider).logEvent(
           'battle_start', 
           parameters: {'deck_id': widget.deckGroup?.id ?? 'unknown'}
       );
    });
  }

  @override
  void dispose() {
    _pageController?.dispose();
    super.dispose();
  }


  @override
  Widget build(BuildContext context) {
    // Watch the family provider with the deck ID
    final deckAsync = ref.watch(battleControllerProvider(widget.deckGroup?.id ?? '')); 
    
    final l10n = AppLocalizations.of(context)!;

    return deckAsync.when(
      loading: () => const Scaffold(backgroundColor: AppColors.background, body: Center(child: CircularProgressIndicator())),
      error: (err, stack) => Scaffold(backgroundColor: AppColors.background, body: Center(child: Text('Error: $err', style: const TextStyle(color: Colors.white)))),
      data: (session) {
          final isCleared = session.isCleared; 
          
          // --- Empty Review Session Check ---
          if (widget.deckGroup?.id == 'Review_Session' && session.totalInitialCount == 0) {
            return _buildEmptyReviewScreen(context);
          }
          
          if (isCleared) {
            return _buildVictoryScreen(context);
          }

          // --- Resume Logic Initialization ---
          if (!_isInit) {
             final syncService = ref.read(sessionServiceProvider);
             final deckState = syncService.getDeckState(widget.deckGroup?.id ?? '');
             
             if (deckState != null && deckState.lastViewedCardId != null) {
                final resumeIndex = session.activeCards.indexWhere((c) => c.id == deckState.lastViewedCardId);
                if (resumeIndex != -1) {
                  _initialIndex = resumeIndex;
                }
             }
             
             _pageController = PageController(
               viewportFraction: 0.85, 
               initialPage: _initialIndex
             );
             _isInit = true;
          }
          // -----------------------------------
      
          final selectedContext = ref.watch(selectedContextProvider);
      
          return Scaffold(
            backgroundColor: AppColors.background,
            body: Stack(
              children: [
                // 0. Background Effects (Deck Group Info)
                if (widget.deckGroup != null)
                  Positioned.fill(
                    child: Container(
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                          colors: [
                            widget.deckGroup!.color.withOpacity(0.2), // Subtle tint
                            AppColors.background,
                          ],
                        ),
                      ),
                    ),
                  ),
                
                if (widget.deckGroup != null)
                   Positioned(
                     right: -50,
                     top: 100,
                     child: Icon(
                       Icons.style, // Placeholder icon for deck
                       size: 300,
                       color: widget.deckGroup!.color.withOpacity(0.05),
                     ),
                   ),
      
                // 1. Main Game Content
                SafeArea(
                  child: Column(
                    children: [
                      // Top Bar
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            IconButton(
                              icon: const Icon(Icons.arrow_back, color: Colors.white54), 
                              onPressed: () {
                                if (context.canPop()) {
                                  context.pop();
                                } else {
                                  context.go('/context-selection');
                                }
                              },
                            ),
                            Column(
                              children: [
                                Text("주제별 단어 암기", style: const TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1.2)),
                              ],
                            ),
                            // TODO: Implement TTS (Audio Speaker) - Hidden for now
                            const SizedBox(width: 24),
                          ],
                        ),
                      ),
                      
                      // Deck Header (Icon + Title) - Replaces the simple text title in the row above
                      // Deck Header (Icon + Title) - Horizontal Layout
                      if (widget.deckGroup != null)
                        Container(
                          margin: const EdgeInsets.fromLTRB(30, 20, 30, 20),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              // Icon
                              Container(
                                width: 70,
                                height: 70,
                                decoration: BoxDecoration(
                                  color: Colors.white.withOpacity(0.1),
                                  shape: BoxShape.circle,
                                  boxShadow: [
                                    BoxShadow(
                                      color: widget.deckGroup!.color.withOpacity(0.4),
                                      blurRadius: 15,
                                      spreadRadius: 2,
                                    )
                                  ],
                                  border: Border.all(color: Colors.white.withOpacity(0.2)),
                                ),
                                child: Center(
                                  child: _buildHeaderIcon(widget.deckGroup!.icon),
                                ),
                              ).animate().scale(duration: 500.ms, curve: Curves.easeOutBack),
                              
                              const Gap(20),
                              
                              // Title
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      widget.deckGroup!.title, // English Title
                                      style: TextStyle(
                                        color: Colors.white.withOpacity(0.6),
                                        fontSize: 14, // Slightly larger for readability
                                        letterSpacing: 1.0,
                                        fontWeight: FontWeight.w500,
                                      ),
                                    ),
                                    const Gap(4),
                                    Text(
                                      widget.deckGroup!.titleKo,
                                      style: const TextStyle(
                                        color: Colors.white, 
                                        fontSize: 24, 
                                        fontWeight: FontWeight.bold,
                                        letterSpacing: 1.2,
                                        height: 1.0,
                                      ),
                                    ).animate().fadeIn(delay: 200.ms).moveX(begin: 10, end: 0),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      
                      // Stats Dashboard (Total, Review, Memorized)
                      Padding(
                        padding: const EdgeInsets.only(left: 40, right: 40, bottom: 20),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceAround,
                          children: [
                            // Memorized (Green)
                            _buildStatItem("Memorized", session.memorizedCount, AppColors.pass, Icons.check_circle),
                            // Review (Red)
                            _buildStatItem("Review", session.reviewCount, AppColors.fail, Icons.refresh),
                            // Total (White)
                            _buildStatItem("Total", session.totalInitialCount, Colors.white, Icons.filter_none),
                          ],
                        ),
                      ),

                      // Progress Bar (Visual Stack)
                      Container(
                        height: 4,
                        margin: const EdgeInsets.symmetric(horizontal: 40),
                        child: LinearProgressIndicator(
                          value: session.totalInitialCount > 0 
                              ? session.memorizedCount / session.totalInitialCount 
                              : 0.0,
                          backgroundColor: AppColors.surfaceHighlight,
                          color: widget.deckGroup?.color ?? AppColors.primary, 
                          borderRadius: BorderRadius.circular(2),
                        ),
                      ),
                      
                      const Gap(20),
                      
                      Expanded(
                        child: PageView.builder(
                          controller: _pageController,
                          itemCount: session.activeCards.length,
                          physics: const BouncingScrollPhysics(),
                          onPageChanged: (index) {
                             // Save Last Viewed Card
                             if (index >= 0 && index < session.activeCards.length) {
                               final cardId = session.activeCards[index].id;
                               if (widget.deckGroup != null) {
                                  ref.read(sessionServiceProvider).updateLastViewedCard(widget.deckGroup!.id, cardId);
                               }
                             }
                          },
                          itemBuilder: (context, index) {
                            final card = session.activeCards[index];
                            return Padding(
                              padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 20.0), // Increased vertical padding to shrink height
                              child: Dismissible(
                                key: UniqueKey(),
                                direction: DismissDirection.vertical,
                                background: Container(
                                  decoration: BoxDecoration(
                                    color: AppColors.pass.withOpacity(0.8),
                                    borderRadius: BorderRadius.circular(24),
                                  ),
                                  margin: const EdgeInsets.only(bottom: 20),
                                  child: const Center(
                                    child: Column(
                                      mainAxisAlignment: MainAxisAlignment.start,
                                      children: [
                                        Gap(40),
                                        Icon(Icons.archive, color: Colors.white, size: 40),
                                        Text("MEMORIZED", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                                      ],
                                    ),
                                  ),
                                ),
                                secondaryBackground: Container(
                                   decoration: BoxDecoration(
                                     color: AppColors.fail.withOpacity(0.8),
                                     borderRadius: BorderRadius.circular(24),
                                   ),
                                  margin: const EdgeInsets.only(top: 20),
                                   child: const Center(
                                     child: Column(
                                       mainAxisAlignment: MainAxisAlignment.end,
                                       children: [
                                         Text("REVIEW", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                                         Icon(Icons.refresh, color: Colors.white, size: 40),
                                         Gap(40),
                                       ],
                                     ),
                                   ),
                                ),
                                onDismissed: (direction) {
                              if (direction == DismissDirection.up) {
                                // Swipe Up -> Red/Review -> Keep (Re-queue)
                                ref.read(battleControllerProvider(widget.deckGroup?.id ?? '').notifier).swipeDown(card.id);
                              } else {
                                // Swipe Down -> Green/Memorized -> Remove
                                ref.read(battleControllerProvider(widget.deckGroup?.id ?? '').notifier).swipeUp(card.id);
                              }
                                },
                                child: FlashCard(
                                  card: card, 
                                  deckIcon: widget.deckGroup?.icon,
                                  onSwipe: (direction) {
                                    if (direction == DismissDirection.up) {
                                      ref.read(battleControllerProvider(widget.deckGroup?.id ?? '').notifier).swipeDown(card.id);
                                    } else {
                                      ref.read(battleControllerProvider(widget.deckGroup?.id ?? '').notifier).swipeUp(card.id);
                                    }
                                  },
                                ),
                              ),
                            );
                          },
                        ),
                      ),
                
                  // Context Icons (Bottom)
                  if (selectedContext.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 10),
                      child: SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: selectedContext.map((item) {
                            return Padding(
                              padding: const EdgeInsets.symmetric(horizontal: 8.0),
                              child: Container(
                                padding: const EdgeInsets.all(8),
                                decoration: BoxDecoration(
                                  color: Colors.white.withOpacity(0.1),
                                  shape: BoxShape.circle,
                                ),
                                child: Icon(
                                  MaterialIconsMapper.getIcon(item.iconAsset),
                                  size: 20,
                                  color: Colors.white70
                                ),
                              ),
                            );
                          }).toList(),
                        ),
                      ),
                    ),


                ],
              ),
            ),

          ],
        ),
      );
    }, // End data:
  ); // End when
}

  Widget _buildStatItem(String label, int value, Color color, IconData icon) {
    return Column(
      children: [
        Icon(icon, color: color, size: 16),
        const Gap(4),
        Text(
          value.toString(),
          style: TextStyle(
            color: color, 
            fontWeight: FontWeight.bold, 
            fontSize: 16
          ),
        ),
        Text(
          label.toUpperCase(),
          style: TextStyle(
            color: color.withOpacity(0.6), 
            fontSize: 8, 
            fontWeight: FontWeight.bold
          ),
        ),
      ],
    );
  }

  Widget _buildHeaderIcon(String? iconKey) {
    if (iconKey == null) {
       return Icon(Icons.layers, size: 40, color: Colors.white.withOpacity(0.9));
    }
    if (iconKey.startsWith('assets/')) {
        return Image.asset(iconKey, width: 50, height: 50);
    }
    if (iconKey.runes.length <= 2) {
       return Text(iconKey, style: const TextStyle(fontSize: 40));
    }
    return Icon(MaterialIconsMapper.getIcon(iconKey), size: 40, color: Colors.white);
  }

  Widget _buildVictoryScreen(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
             const Icon(Icons.emoji_events, size: 100, color: AppColors.warning).animate().scale(duration: 800.ms, curve: Curves.elasticOut).shimmer(duration: 1500.ms),
             const Gap(20),
             const Text(
               "VICTORY!",
               style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold, color: AppColors.warning, letterSpacing: 2),
             ).animate().fadeIn().moveY(begin: 20, end: 0),
             const Gap(10),
             const Text("The deck has been conquered.", style: TextStyle(color: Colors.white54)),
             const Gap(40),
             ElevatedButton(
               onPressed: () async {
                 // Save Completion
                 final user = ref.read(authProvider).value;
                 if (user != null && widget.deckGroup != null) {
                   await ref.read(supabaseRepositoryProvider).markDeckCompleted(user.id, widget.deckGroup!.id);
                   // Invalidate profile to refresh UI on return
                   ref.invalidate(userProfileProvider);
                 }
                 
                 if (context.mounted) {
                   context.go('/deck-selection');
                 }
               },
               style: ElevatedButton.styleFrom(
                 backgroundColor: AppColors.pass,
                 foregroundColor: Colors.white,
                 padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 16),
                 shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
                 elevation: 5,
               ),
               child: const Text("Return to Lobby", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
             ),
              const Gap(16),
              TextButton.icon(
                onPressed: () async {
                  if (widget.deckGroup != null) {
                    final syncService = ref.read(sessionServiceProvider);
                    // Reset Progress
                    await ref.read(sessionServiceProvider).resetDeckProgress(widget.deckGroup!.id);
                    // Invalidate Battle Provider to reload
                    ref.invalidate(battleControllerProvider(widget.deckGroup!.id));
                    // Invalidate Profile to update stats
                    ref.invalidate(userProfileProvider);
                    // No navigation needed -> Widget will rebuild with new state
                  }
                },
                icon: const Icon(Icons.refresh, color: Colors.white70),
                label: const Text("Re-learn Deck", style: TextStyle(color: Colors.white70)),
              )
          ],
        ),
      ),
    );  
  }
  Widget _buildEmptyReviewScreen(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(30.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
               Container(
                 padding: const EdgeInsets.all(30),
                 decoration: BoxDecoration(
                   color: Colors.white.withOpacity(0.05),
                   shape: BoxShape.circle,
                 ),
                 child: const Icon(Icons.playlist_add_check, size: 80, color: Colors.white24),
               ).animate().scale(duration: 800.ms, curve: Curves.easeOutBack),
               
               const Gap(30),
               
               const Text(
                 "복습할 단어가 없습니다",
                 style: TextStyle(
                   fontSize: 24, 
                   fontWeight: FontWeight.bold, 
                   color: Colors.white,
                   letterSpacing: 1.0
                 ),
               ).animate().fadeIn().moveY(begin: 10, end: 0),
               
               const Gap(16),
               
               const Text(
                 "단어 카드를 위로 스와이프해서\n복습 목록에 추가해보세요!",
                 textAlign: TextAlign.center,
                 style: TextStyle(
                   fontSize: 16, 
                   color: Colors.white54, 
                   height: 1.6
                 ),
               ).animate().fadeIn(delay: 200.ms),
               
               const Gap(50),
               
               ElevatedButton(
                 onPressed: () {
                   if (context.mounted) {
                     context.go('/deck-selection');
                   }
                 },
                 style: ElevatedButton.styleFrom(
                   backgroundColor: AppColors.primary,
                   foregroundColor: Colors.white,
                   padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 16),
                   shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
                   elevation: 4,
                 ),
                 child: const Text("로비로 돌아가기", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
               ).animate().fadeIn(delay: 400.ms).moveY(begin: 20, end: 0),
            ],
          ),
        ),
      ),
    );
  }
}

