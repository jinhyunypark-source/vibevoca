import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import 'package:gap/gap.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/utils/material_icons_mapper.dart';
import 'providers/context_provider.dart';
import 'models/context_item.dart';
import 'providers/deck_collection_provider.dart';
import '../profile/providers/profile_provider.dart';
import 'models/deck_group.dart';
import '../../core/widgets/app_drawer.dart';

class ContextInitPage extends ConsumerWidget {
  const ContextInitPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // 1. Fetch all context items
    final allContextsAsync = ref.watch(allContextOptionsProvider);
    // 2. Watch selected state (List<ContextItem>)
    final selectedItems = ref.watch(selectedContextProvider);
    // 3. User Profile for verification/resume logic
    final userProfileAsync = ref.watch(userProfileProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text("VibeVoca"),
        centerTitle: true,
      ),
      endDrawer: const AppDrawer(),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // HEADER
              const Text(
                "Select your Vibe",
                style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white),
                textAlign: TextAlign.center,
              ).animate().fadeIn().moveY(begin: 10, end: 0),
              
              const Gap(8),
              const Text(
                "당신의 지금의 느낌과 일치하는 아이콘을 선택해 보세요",
                 style: TextStyle(fontSize: 14, color: Colors.white54),
                 textAlign: TextAlign.center,
              ).animate().fadeIn(delay: 200.ms),

              const Gap(30),

              // GRID CONTENT
              Expanded(
                child: allContextsAsync.when(
                  data: (items) {
                    if (items.isEmpty) return const Center(child: Text("No context factors available."));
                    
                    return GridView.builder(
                      itemCount: items.length,
                      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: 3,
                        crossAxisSpacing: 12,
                        mainAxisSpacing: 16,
                        childAspectRatio: 1.0, // Square shape
                      ),
                      itemBuilder: (context, index) {
                         final item = items[index];
                         final isSelected = selectedItems.any((i) => i.id == item.id);
                         
                         return GestureDetector(
                           onTap: () {
                             ref.read(selectedContextProvider.notifier).toggle(item);
                           },
                           child: AnimatedContainer(
                             duration: 200.ms,
                             curve: Curves.easeOut,
                             decoration: BoxDecoration(
                               color: isSelected ? AppColors.primary : AppColors.surface,
                               borderRadius: BorderRadius.circular(16),
                               border: Border.all(
                                 color: isSelected ? AppColors.accent : Colors.white10,
                                 width: isSelected ? 2 : 1,
                               ),
                               boxShadow: isSelected ? [
                                 BoxShadow(
                                   color: AppColors.primary.withOpacity(0.5),
                                   blurRadius: 10,
                                   spreadRadius: 1
                                 )
                               ] : [],
                             ),
                             child: Column(
                               mainAxisAlignment: MainAxisAlignment.center,
                               children: [
                                  Icon(
                                    MaterialIconsMapper.getIcon(item.iconAsset),
                                    color: isSelected ? Colors.white : Colors.white24,
                                    size: 32
                                  ),
                                  const Gap(12),
                                  Text(
                                    item.label,
                                    textAlign: TextAlign.center,
                                    style: TextStyle(
                                      color: isSelected ? Colors.white : Colors.white38,
                                      fontWeight: FontWeight.w600,
                                      fontSize: 12,
                                    ),
                                    maxLines: 2,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                               ],
                             ),
                           ),
                         ).animate().scale(delay: (50 * index).ms, duration: 300.ms);
                      },
                    );
                  },
                  loading: () => const Center(child: CircularProgressIndicator()),
                  error: (e, s) => Center(child: Text("Error: $e", style: const TextStyle(color: Colors.red))),
                ),
              ),

              const Gap(20),

              // ACTION BUTTONS
              // 1. Resume (if needed)
              if (userProfileAsync.value?.lastPlayedDeckId != null)
                Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: OutlinedButton(
                    onPressed: () async {
                       // Resume logic (Duplicated for now, or move to provider)
                       final deckId = userProfileAsync.value!.lastPlayedDeckId!;
                       final repo = ref.read(supabaseRepositoryProvider);
                       final vocabDeck = await repo.getDeckById(deckId);
                       if (vocabDeck != null && context.mounted) {
                          int colorValue = 0xFFFF5733; 
                          try { colorValue = int.parse(vocabDeck.color.replaceAll('#', '0xFF')); } catch (_) {}
                          final deckGroup = DeckGroup(
                             id: vocabDeck.id, title: vocabDeck.title, titleKo: vocabDeck.titleKo ?? vocabDeck.title,
                             color: Color(colorValue), icon: vocabDeck.icon, progress: 0.0,
                          );
                          context.push('/battle', extra: deckGroup);
                       }
                    },
                    style: OutlinedButton.styleFrom(
                      side: const BorderSide(color: Colors.white24),
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                    ),
                    child: const Text("Resume Last Deck", style: TextStyle(color: Colors.white70)),
                  ),
                ),

              // 2. Start Learning (Primary)
              ElevatedButton(
                onPressed: selectedItems.isEmpty ? null : () {
                   // Proceed to Deck Selection (Context is set in provider state)
                   context.push('/deck-selection');
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  disabledBackgroundColor: AppColors.surface,
                  padding: const EdgeInsets.symmetric(vertical: 18),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  elevation: 4,
                  shadowColor: AppColors.primary.withOpacity(0.4),
                ),
                child: Text(
                  "Start Learning (${selectedItems.length}/3)", 
                  style: TextStyle(
                    fontSize: 18, 
                    color: selectedItems.isEmpty ? Colors.white38 : Colors.white, 
                    fontWeight: FontWeight.bold
                  )
                ),
              ).animate().fadeIn(delay: 500.ms).moveY(begin: 20, end: 0),
              
              const Gap(10),
            ],
          ),
        ),
      ),
    );
  }
} // End of ContextInitPage class

// Removed _LargeContextSlot and _ContextOptionsSheet as they are replaced by Grid

