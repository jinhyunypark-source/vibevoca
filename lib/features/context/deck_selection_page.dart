import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import 'package:gap/gap.dart';
import '../../../core/theme/app_colors.dart';
import 'providers/deck_collection_provider.dart';
import 'providers/image_pack_provider.dart';
import 'widgets/deck_box.dart';
import '../../l10n/app_localizations.dart';
import '../../core/widgets/app_drawer.dart';

import 'package:vibevoca/features/auth/providers/auth_provider.dart';
import 'package:vibevoca/features/context/models/deck_group.dart';
import 'package:vibevoca/features/context/models/supabase_models.dart';
import '../profile/providers/profile_provider.dart';
import '../sync/services/session_service.dart';
import 'package:vibevoca/features/analytics/services/analytics_service.dart';
import 'package:vibevoca/core/services/models/download_state.dart';
import 'package:vibevoca/features/ads/widgets/ad_banner_widget.dart';

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

  /// 카테고리별 이미지 팩 다운로드 상태 위젯
  Widget _buildDownloadStatus(String categoryId, Color themeColor) {
    // 데모 카테고리는 이미 번들에 포함됨
    if (isDemoCategory(categoryId)) {
      return const Icon(Icons.check_circle, color: Colors.green, size: 20);
    }

    final downloadState = ref.watch(categoryDownloadStateProvider(categoryId));

    return downloadState.when(
      notDownloaded: () => GestureDetector(
        onTap: () => _showDownloadDialog(categoryId),
        child: Container(
          padding: const EdgeInsets.all(4),
          child: Icon(Icons.cloud_download_outlined, color: Colors.white54, size: 22),
        ),
      ),
      downloading: (progress) => SizedBox(
        width: 22,
        height: 22,
        child: Stack(
          alignment: Alignment.center,
          children: [
            CircularProgressIndicator(
              value: progress,
              strokeWidth: 2,
              backgroundColor: Colors.white24,
              valueColor: AlwaysStoppedAnimation(themeColor),
            ),
            Text(
              '${(progress * 100).toInt()}',
              style: const TextStyle(color: Colors.white70, fontSize: 8),
            ),
          ],
        ),
      ),
      downloaded: () => const Icon(Icons.check_circle, color: Colors.green, size: 20),
      error: (message) => GestureDetector(
        onTap: () => ref.read(categoryDownloadStateProvider(categoryId).notifier).retry(),
        child: const Icon(Icons.error_outline, color: Colors.redAccent, size: 22),
      ),
    );
  }

  /// 다운로드 확인 다이얼로그
  Future<void> _showDownloadDialog(String categoryId) async {
    final user = ref.read(authProvider).value;

    // 비로그인 사용자는 로그인 유도
    if (user == null) {
      showDialog(
        context: context,
        builder: (ctx) => AlertDialog(
          backgroundColor: AppColors.surface,
          title: const Text('로그인 필요', style: TextStyle(color: Colors.white)),
          content: const Text(
            '이미지 팩을 다운로드하려면 로그인이 필요합니다.',
            style: TextStyle(color: Colors.white70),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(ctx).pop(),
              child: const Text('취소'),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(ctx).pop();
                context.push('/login');
              },
              child: const Text('로그인'),
            ),
          ],
        ),
      );
      return;
    }

    // 다운로드 확인
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AppColors.surface,
        title: const Text('이미지 다운로드', style: TextStyle(color: Colors.white)),
        content: const Text(
          '이 카테고리의 단어 이미지를 다운로드하시겠습니까?\n(약 2~3MB)',
          style: TextStyle(color: Colors.white70),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(false),
            child: const Text('취소'),
          ),
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(true),
            child: const Text('다운로드'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      ref.read(categoryDownloadStateProvider(categoryId).notifier).startDownload();
    }
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
        child: Column(
          children: [
            Expanded(
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
                                         // Download Status Widget
                                         _buildDownloadStatus(cat.id, themeColor),
                                         const Gap(8),
                                         Icon(
                                            isExpanded ? Icons.keyboard_arrow_up : Icons.keyboard_arrow_down,
                                            color: isExpanded ? themeColor : Colors.white54
                                         )
                                       ],
                                     ),
                                   ),
                                 ),
      
                                 // 2. Expanded Content (Decks Grid)
                                 // 2. Expanded Content (Decks Grid)
                                 AnimatedCrossFade(
                                   crossFadeState: isExpanded ? CrossFadeState.showSecond : CrossFadeState.showFirst,
                                   duration: 300.ms,
                                   firstChild: Container(height: 0),
                                   secondChild: Container(
                                      // Added top padding to account for DeckBox 'selected' upward translation (-10px) and shadow
                                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
                                      child: catDecks.isEmpty
                                        ? const Padding(
                                            padding: EdgeInsets.all(20),
                                            child: Center(child: Text("No decks available.", style: TextStyle(color: Colors.white38))),
                                          )
                                        : Builder(
                                            builder: (context) {
                                              final isDownloaded = ref.watch(categoryDownloadStateProvider(cat.id)).maybeWhen(
                                                downloaded: () => true,
                                                orElse: () => false,
                                              );
                                              final isDemo = isDemoCategory(cat.id);
                                              final showContent = isDemo || isDownloaded;
      
                                              return Stack(
                                                alignment: Alignment.center,
                                                children: [
                                                  // 1. Deck Grid (Dimmed if not downloaded)
                                                  Opacity(
                                                    opacity: showContent ? 1.0 : 0.3,
                                                    child: IgnorePointer(
                                                      ignoring: !showContent,
                                                      child: GridView.builder(
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
                                                  ),
      
                                                  // 2. Download Button (Overlay)
                                                  if (!showContent)
                                                    Center(
                                                      child: GestureDetector(
                                                        onTap: () => _showDownloadDialog(cat.id),
                                                        child: Container(
                                                          width: 80, height: 80,
                                                          decoration: BoxDecoration(
                                                            color: AppColors.surface.withOpacity(0.9),
                                                            shape: BoxShape.circle,
                                                            border: Border.all(color: themeColor, width: 2),
                                                            boxShadow: [
                                                              BoxShadow(color: Colors.black.withOpacity(0.5), blurRadius: 20, spreadRadius: 5)
                                                            ]
                                                          ),
                                                          child: Icon(Icons.cloud_download_rounded, size: 40, color: themeColor),
                                                        ),
                                                      ),
                                                    ),
                                                ],
                                              );
                                            },
                                          ),
                                    ),
                                 )
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
            
            // AdMob Banner
            const AdBannerWidget(),
          ],
        ),
      ),
    );
  }
}
