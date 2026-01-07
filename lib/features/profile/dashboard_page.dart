import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:gap/gap.dart';
import '../../core/theme/app_colors.dart';
import '../sync/services/session_service.dart';
import '../context/providers/deck_collection_provider.dart';

class DashboardPage extends ConsumerWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // 1. Get All Local Progress
    final syncService = ref.watch(sessionServiceProvider);
    // We need a way to get *all* cached decks from sync service to aggregate stats.
    // Currently getDeckState(id) is singular. 
    // Let's assume we can get all or iterate. 
    // Actually, syncService.localCache is private.
    // I should expose a method or provider for "All Deck States" or similar.
    // For now, let's assume I can add a getter to SyncService or just iterate if I have the list of all decks from deckCollectionProvider.
    
    final allDecksAsync = ref.watch(deckCollectionProvider);
    
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: AppColors.background,
        title: const Text("Learning Dashboard", style: TextStyle(fontWeight: FontWeight.bold)),
      ),
      body: allDecksAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
        data: (allDecks) {
          // Calculate Stats
          int totalDecks = allDecks.length;
          int completedDecks = 0;
          int inProgressDecks = 0;
          
          int totalCards = 0;
          int memorizedCards = 0;
          
          for (var deck in allDecks) {
            final state = syncService.getDeckState(deck.id);
            final deckTotal = deck.cardCount; // Use static total for accuracy
            totalCards += deckTotal;
            
            if (state != null) {
              memorizedCards += state.memorizedCount;
              if (state.memorizedCount == deckTotal && deckTotal > 0) {
                completedDecks++;
              } else if (state.memorizedCount > 0 || state.remindCount > 0) {
                 inProgressDecks++;
              }
            }
          }
          
          // Data for Charts
          final activeDecks = inProgressDecks;
          final notStartedDecks = totalDecks - completedDecks - inProgressDecks; // Implicit unused
          
          return SingleChildScrollView(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                _buildSummaryCards(completedDecks, activeDecks, memorizedCards, totalCards),
                const Gap(30),
                const Text("Deck Progress", style: TextStyle(fontSize: 18, color: Colors.white, fontWeight: FontWeight.bold)),
                const Gap(20),
                _buildDeckPieChart(completedDecks, activeDecks, notStartedDecks),
                 const Gap(30),
                const Text("Card Memorization", style: TextStyle(fontSize: 18, color: Colors.white, fontWeight: FontWeight.bold)),
                const Gap(20),
                _buildCardBarChart(memorizedCards, totalCards),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildSummaryCards(int completed, int active, int memorized, int total) {
    return Row(
      children: [
        Expanded(
          child: _StatCard(
            label: "Completed Decks",
            value: "$completed",
            icon: Icons.emoji_events,
            color: AppColors.warning,
          ),
        ),
        const Gap(10),
        Expanded(
          child: _StatCard(
             label: "Memorized Cards",
             value: "$memorized / $total",
             icon: Icons.memory,
             color: AppColors.pass,
          ),
        ),
      ],
    );
  }
  
  Widget _buildDeckPieChart(int completed, int active, int notStarted) {
     return SizedBox(
       height: 200,
       child: PieChart(
         PieChartData(
           sections: [
             PieChartSectionData(
               value: completed.toDouble(),
               color: AppColors.warning,
               title: '$completed',
               radius: 50,
               titleStyle: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white),
             ),
             PieChartSectionData(
               value: active.toDouble(),
               color: AppColors.primary,
               title: '$active',
               radius: 45,
               titleStyle: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white),
             ),
             if (notStarted > 0)
             PieChartSectionData(
               value: notStarted.toDouble(),
               color: Colors.white12,
               title: '',
               radius: 40,
             ),
           ],
           sectionsSpace: 4,
           centerSpaceRadius: 40,
         ),
       ),
     );
  }
  
  Widget _buildCardBarChart(int memorized, int total) {
    if (total == 0) return const SizedBox();
    final remaining = total - memorized;
    
    return SizedBox(
       height: 50,
       child: ClipRRect(
         borderRadius: BorderRadius.circular(25),
         child: Row(
           children: [
             Expanded(
               flex: memorized,
               child: Container(
                 color: AppColors.pass,
                 alignment: Alignment.center,
                 child: memorized > 0 ? Text("$memorized", style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)) : null,
               ),
             ),
             Expanded(
               flex: remaining,
               child: Container(
                 color: Colors.white12,
                 alignment: Alignment.center,
                 child: Text("$remaining left", style: const TextStyle(color: Colors.white54, fontSize: 10)),
               ),
             ),
           ],
         ),
       ),
    );
  }
}

class _StatCard extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;
  final Color color;
  
  const _StatCard({required this.label, required this.value, required this.icon, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 28),
          const Gap(10),
          Text(value, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
          Text(label, style: const TextStyle(fontSize: 12, color: Colors.white54)),
        ],
      ),
    );
  }
}
