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
import 'widgets/deck_box.dart';
import '../../l10n/app_localizations.dart';
import 'utils/deck_localization_helper.dart';

class ContextSelectionPage extends ConsumerStatefulWidget {
  const ContextSelectionPage({super.key});

  @override
  ConsumerState<ContextSelectionPage> createState() => _ContextSelectionPageState();
}

class _ContextSelectionPageState extends ConsumerState<ContextSelectionPage> {
  late final PageController _pageController;
  int _currentIndex = 0;

  @override
  void initState() {
    super.initState();
    _pageController = PageController(viewportFraction: 0.55);
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final selectedState = ref.watch(selectedContextProvider);
    // ignore: unused_local_variable
    final isComplete = ref.read(selectedContextProvider.notifier).isComplete;
    final deckCollectionAsync = ref.watch(deckGroupsProvider);
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(l10n.titleContextSelection),
        centerTitle: true,
      ),
      drawer: Drawer(
        backgroundColor: AppColors.surface,
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(color: AppColors.primary),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                   Icon(Icons.person, size: 50, color: Colors.white),
                   SizedBox(height: 10),
                   Text("VibeVoca", style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            ListTile(
              leading: const Icon(Icons.person, color: Colors.white),
              title: const Text("Manage Interests", style: TextStyle(color: Colors.white)),
              onTap: () {
                context.pop(); // Close drawer
                context.push('/profile-setup');
              },
            ),
            ListTile(
              leading: const Icon(Icons.settings, color: Colors.white),
              title: const Text("Settings", style: TextStyle(color: Colors.white)),
              onTap: () {
                context.pop();
                context.push('/settings');
              },
            ),
            const Divider(color: Colors.white24),
          ],
        ),
      ),
      body: deckCollectionAsync.when(
        data: (deckCollection) {
           final currentDeck = (deckCollection.isNotEmpty && _currentIndex < deckCollection.length) 
              ? deckCollection[_currentIndex] 
              : null;
           
           final bgColor = currentDeck?.color.withOpacity(0.15) ?? AppColors.background;

           return AnimatedContainer(
             duration: 500.ms,
             decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    bgColor,
                    AppColors.background,
                  ],
                ),
             ),
             child: Column(
                children: [
                  // 1. Deck Groups (Carousel) - TOP
                  Expanded(
                    flex: 2,
                    child: PageView.builder(
                      controller: _pageController,
                      itemCount: deckCollection.length,
                      onPageChanged: (index) {
                        setState(() {
                          _currentIndex = index;
                        });
                      },
                      itemBuilder: (context, index) {
                        final deck = deckCollection[index];
                        final isFocused = index == _currentIndex;
                        return Center(
                          child: AnimatedScale(
                            scale: isFocused ? 1.0 : 0.85, 
                            duration: 300.ms,
                            curve: Curves.easeOutBack,
                            child: DeckBox(
                              title: deck.titleKo, // Use DB-provided Korean Title
                              deckId: deck.title, // Use Title for asset mapping (e.g. logic_clarity)
                              baseColor: deck.color,
                              progress: deck.progress,
                              status: isFocused ? DeckStatus.current : DeckStatus.locked, // Map selection to new status
                              iconAsset: deck.icon, // Pass icon from DB
                              onTap: () {
                                if (isFocused) {
                                   context.push('/battle', extra: deck);
                                } else {
                                  _pageController.animateToPage(
                                    index, 
                                    duration: 300.ms, 
                                    curve: Curves.easeOut
                                  );
                                }
                              },
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                  
                  const Gap(20),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 30),
                    child: Text(
                      l10n.msgFillContext, 
                      textAlign: TextAlign.center,
                      style: const TextStyle(color: Colors.white54),
                    ),
                  ),
                  const Gap(20),

                  // 2. Context Slots (Selection) - BOTTOM
                  Expanded(
                    flex: 1,
                    child: Container(
                      padding: const EdgeInsets.all(20),
                      decoration: const BoxDecoration(
                        color: AppColors.surface,
                        borderRadius: BorderRadius.vertical(top: Radius.circular(30)),
                      ),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _CompactContextSlot(type: ContextType.place, selectedItem: selectedState.where((i) => i.type == ContextType.place).firstOrNull),
                          const Gap(10),
                          _CompactContextSlot(type: ContextType.emotion, selectedItem: selectedState.where((i) => i.type == ContextType.emotion).firstOrNull),
                           const Gap(10),
                          _CompactContextSlot(type: ContextType.environment, selectedItem: selectedState.where((i) => i.type == ContextType.environment).firstOrNull),
                        ],
                      ),
                    ),
                  ),
                ],
             ),
           );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err', style: const TextStyle(color: Colors.red))),
      ),
    );
  }
}

class _CompactContextSlot extends ConsumerWidget {
  final ContextType type;
  final ContextItem? selectedItem;

  const _CompactContextSlot({required this.type, this.selectedItem});

  String _getTypeLabel(ContextType t) {
     return t.name.toUpperCase();
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Expanded(
      child: GestureDetector(
        onTap: () => _showSelectionSheet(context, ref, type),
        child: Column(
          children: [
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: selectedItem != null ? AppColors.primary.withValues(alpha: 0.2) : Colors.black26,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: selectedItem != null ? AppColors.accent : Colors.white12,
                  ),
                ),
                child: Center(
                  child: Icon(
                    selectedItem != null ? MaterialIconsMapper.getIcon(selectedItem!.iconAsset) : Icons.add,
                    color: selectedItem != null ? AppColors.accent : Colors.grey,
                    size: 30,
                  ),
                ),
              ),
            ),
            const Gap(8),
            Text(_getTypeLabel(type), style: const TextStyle(fontSize: 10, color: Colors.grey, fontWeight: FontWeight.bold)),
            if (selectedItem != null)
              Text(
                selectedItem!.label,
                style: const TextStyle(fontSize: 12, color: Colors.white, fontWeight: FontWeight.bold),
                overflow: TextOverflow.ellipsis,
              ).animate().fadeIn()
          ],
        ),
      ),
    );
  }

  void _showSelectionSheet(BuildContext context, WidgetRef ref, ContextType type) {
    showModalBottomSheet(
      context: context,
      backgroundColor: AppColors.background,
      isScrollControlled: true, // Allow full height if needed
      builder: (ctx) => _ContextOptionsSheet(type: type),
    );
  }
}

class _ContextOptionsSheet extends ConsumerWidget {
  final ContextType type;

  const _ContextOptionsSheet({required this.type});

  String _getTypeLabel(ContextType t) {
     return t.name.toUpperCase();
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // 1. Fetch ALL options and filter locally
    final allOptionsAsync = ref.watch(allContextOptionsProvider);
    final selectedItems = ref.watch(selectedContextProvider);

    return Container(
      padding: const EdgeInsets.all(20),
      height: 400,
      child: Column(
        children: [
           Text("Select ${_getTypeLabel(type)}", style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
           const Gap(20),
           Expanded(
            child: allOptionsAsync.when(
              data: (allOptions) {
                // Filter by type
                final options = allOptions.where((i) => i.type == type).toList();

                if (options.isEmpty) return const Center(child: Text("No options found."));
                return GridView.builder(
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 3,
                    mainAxisSpacing: 10,
                    crossAxisSpacing: 10,
                  ),
                  itemCount: options.length,
                  itemBuilder: (ctx, index) {
                    final item = options[index];
                    final isSelected = selectedItems.any((i) => i.id == item.id);
                    
                    return GestureDetector(
                      onTap: () {
                        // Toggle selection
                        ref.read(selectedContextProvider.notifier).toggle(item);
                        Navigator.pop(ctx);
                      },
                      child: Container(
                        decoration: BoxDecoration(
                          color: isSelected ? AppColors.primary : AppColors.surface,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: isSelected ? AppColors.accent : AppColors.accent.withOpacity(0.3)),
                        ),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(MaterialIconsMapper.getIcon(item.iconAsset), color: isSelected ? Colors.white : AppColors.textPrimary, size: 32),
                            const Gap(8),
                            Text(
                                item.label,
                                style: TextStyle(fontSize: 12, color: isSelected ? Colors.white : null),
                                textAlign: TextAlign.center,
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                );
              },
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, stack) => Center(child: Text('Error: $err')),
            ),
          ),
        ],
      ),
    );
  }
}
