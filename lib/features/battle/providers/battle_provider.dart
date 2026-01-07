import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../models/word_card_model.dart';
import '../../context/providers/deck_collection_provider.dart'; 
import '../../sync/services/session_service.dart';
import '../../context/providers/context_provider.dart';
import '../../profile/providers/profile_provider.dart';
import '../../auth/providers/auth_provider.dart'; // Ensure Auth is imported if needed for SessionService init check (though usually not needed here)

part 'battle_provider.g.dart';


class BattleSessionState {
  final List<WordCardModel> activeCards;
  final int totalInitialCount;
  
  const BattleSessionState({
    required this.activeCards,
    required this.totalInitialCount,
  });

  int get memorizedCount => totalInitialCount - activeCards.length;
  int get reviewCount => activeCards.where((c) => c.failCount > 0).length;
  bool get isCleared => activeCards.isEmpty;
  
  BattleSessionState copyWith({
    List<WordCardModel>? activeCards,
    int? totalInitialCount,
  }) {
    return BattleSessionState(
      activeCards: activeCards ?? this.activeCards,
      totalInitialCount: totalInitialCount ?? this.totalInitialCount,
    );
  }
}

@riverpod
class BattleController extends _$BattleController {
  @override
  @override
  FutureOr<BattleSessionState> build(String deckId) async {
    final repo = ref.watch(supabaseRepositoryProvider);
    final sessionService = ref.read(sessionServiceProvider);
    
    // --- Review Mode Logic ---
    if (deckId == 'Review_Session') {
       final candidates = sessionService.getAllReviewCandidates();
       if (candidates.isEmpty) {
          return const BattleSessionState(activeCards: [], totalInitialCount: 0);
       }
       
       final ids = candidates.map((c) => c.cardId).toList();
       final cards = await repo.getCardsByIds(ids);
       
       final candidateMap = { for (var c in candidates) c.cardId : c };
       
       var activeCards = cards.map((c) {
          final cand = candidateMap[c.id];
          return WordCardModel(
             id: c.id,
             word: c.frontText,
             meaning: c.backText,
             exampleSentence: c.exampleSentences.isNotEmpty ? c.exampleSentences.first : 'No example.',
             vibeSentences: [], // Context skipped for mixed review
             failCount: cand?.failCount ?? 0,
             originalDeckId: cand?.deckId,
          );
       }).toList();
       
       // Sort by Priority (Fail Count)
       activeCards.sort((a,b) => b.failCount.compareTo(a.failCount));
       
       return BattleSessionState(activeCards: activeCards, totalInitialCount: activeCards.length);
    }
    // -------------------------
    
    // 1. Fetch Raw Cards
    final vocabCards = await repo.getCards(deckId);
    
    // 2. Fetch Progress (Synchronous from Cache)
    final deckState = sessionService.getDeckState(deckId);
    final memorizedIds = deckState?.cardStates
        .where((c) => c.status == 'memorized')
        .map((c) => c.id)
        .toSet() ?? {};
        
    final cardStateMap = {
      for (var c in deckState?.cardStates ?? []) c.id: c
    };

    // 3. Fetch Vibe Sentences
    final profile = await ref.watch(userProfileProvider.future);
    final contextItems = ref.watch(selectedContextProvider);
    // Resolve Interest IDs -> Semantic Tags (Codes)
    final allInterests = await ref.read(interestsProvider.future);
    final interestMap = { for (var i in allInterests) i.id: i.code }; 
    
    final tags = <String>[
      if (profile != null)
         for (final id in profile.interestIds)
            if (interestMap.containsKey(id)) interestMap[id]!,
            
      for (final item in contextItems) item.slug.contains('_') ? item.slug.split('_').last : item.slug, 
    ];
    
    final vibeList = await repo.getVibeSentencesForDeck(deckId, tags);
    final vibeMap = <String, List<String>>{};
    for (var v in vibeList) {
       if ((vibeMap[v.cardId]?.length ?? 0) < 3) { // Limit to 3 max locally
          final uniqueSentence = v.sentenceKo != null ? "${v.sentenceEn}\n(${v.sentenceKo})" : v.sentenceEn;
          vibeMap.putIfAbsent(v.cardId, () => []).add(uniqueSentence);
       }
    }

    // 4. Filter & Map
    final activeCards = vocabCards
        .where((c) => !memorizedIds.contains(c.id))
        .map((c) {
          final state = cardStateMap[c.id];
          return WordCardModel(
            id: c.id,
            word: c.frontText,
            meaning: c.backText,
            exampleSentence: c.exampleSentences.isNotEmpty ? c.exampleSentences.first : 'No example.',
            vibeSentences: vibeMap[c.id] ?? [],
            failCount: state?.remindCount ?? 0,
            originalDeckId: deckId,
          );
        }).toList();

    return BattleSessionState(
      activeCards: activeCards,
      totalInitialCount: vocabCards.length,
    );
  }

  void swipeUp(String cardId) {
    // Memorized / Green Action
    final currentState = state.value;
    if (currentState == null) return;

    if (deckId == 'Review_Session') {
       // --- Review Mode: Decrement Remind Count ---
       final cardIndex = currentState.activeCards.indexWhere((c) => c.id == cardId);
       if (cardIndex == -1) return;
       final card = currentState.activeCards[cardIndex];
       
       if (card.originalDeckId != null) {
          final newCount = (card.failCount > 0) ? card.failCount - 1 : 0;
          
          if (newCount <= 0) {
             // Fully Memorized -> Mark as Memorized in DB
             ref.read(sessionServiceProvider).updateCardProgress(
                card.originalDeckId!,
                cardId,
                'memorized',
                forceRemindCount: 0 
             );
          } else {
             // Count Reduced -> Update Count, Keep Status 'review'
             ref.read(sessionServiceProvider).updateCardProgress(
                card.originalDeckId!,
                cardId,
                'review',
                forceRemindCount: newCount
             );
          }
       }
       // Remove from THIS session (Hide)
       final newCards = List<WordCardModel>.from(currentState.activeCards);
       newCards.removeAt(cardIndex);
       state = AsyncData(currentState.copyWith(activeCards: newCards));
       return;
    }

    // --- Normal Mode: Memorized ---
    // 1. Update Session Service
    ref.read(sessionServiceProvider).updateCardProgress(
      deckId, 
      cardId, 
      'memorized'
    );

    // 2. Update Local State (Remove Card)
    final newCards = currentState.activeCards.where((card) => card.id != cardId).toList();
    state = AsyncData(currentState.copyWith(activeCards: newCards));
  }

  void swipeDown(String cardId) {
    // Review / Red Action
    final currentState = state.value;
    if (currentState == null) return;
    
    if (deckId == 'Review_Session') {
       // --- Review Mode: Increment Remind Count + Requeue ---
       final cardIndex = currentState.activeCards.indexWhere((c) => c.id == cardId);
       if (cardIndex == -1) return;
       final card = currentState.activeCards[cardIndex];
       
       if (card.originalDeckId != null) {
          ref.read(sessionServiceProvider).updateCardProgress(
            card.originalDeckId!, 
            cardId, 
            'review', 
            incrementRemind: true
          );
       }
       
       // Re-queue
       final updatedCard = card.copyWith(failCount: card.failCount + 1);
       final newCards = List<WordCardModel>.from(currentState.activeCards);
       newCards.removeAt(cardIndex);
       newCards.add(updatedCard);
       state = AsyncData(currentState.copyWith(activeCards: newCards));
       return;
    }

    // --- Normal Mode: Increment & Re-queue ---
    // 1. Update Session Service
    ref.read(sessionServiceProvider).updateCardProgress(
      deckId, 
      cardId, 
      'review', 
      incrementRemind: true
    );

    // 2. Update Local State (Re-queue)
    final currentCards = currentState.activeCards;
    final cardIndex = currentCards.indexWhere((c) => c.id == cardId);
    
    if (cardIndex != -1) {
      final card = currentCards[cardIndex].copyWith(failCount: currentCards[cardIndex].failCount + 1);
      final newCards = [...currentCards];
      newCards.removeAt(cardIndex);
      newCards.add(card);
      
      state = AsyncData(currentState.copyWith(activeCards: newCards));
    }
  }
}
