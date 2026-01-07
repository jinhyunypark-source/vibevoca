import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:vibevoca/features/context/models/deck_group.dart';
import 'package:vibevoca/features/context/models/supabase_models.dart';
import 'package:vibevoca/features/context/repositories/supabase_repository.dart';
import 'package:vibevoca/features/context/providers/context_provider.dart'; // For selectContext
import 'package:vibevoca/features/battle/models/word_card_model.dart';

// --- Repositories ---

final supabaseRepositoryProvider = Provider<SupabaseRepository>((ref) {
  return SupabaseRepository(Supabase.instance.client);
});

// --- State Providers ---

/// AsyncValue provider for Categories (to replace static mocked content later)
final categoriesProvider = FutureProvider<List<VocabCategory>>((ref) async {
  final repo = ref.watch(supabaseRepositoryProvider);
  return repo.getCategories();
});

/// AsyncValue provider for Decks, filtered by selected Category/Context if needed
/// For the MVP, we might want to fetch ALL decks or filter by the Active Context?
/// The original Mock design filtered decks by "DeckGroup.id" based on Context.
/// Supabase Decks are tied to Categories.
/// We will fetch ALL decks for horizontal scroll for now, or filter if we had categories UI.
/// Let's assume we show ALL Decks in the carousel.
final deckCollectionProvider = FutureProvider<List<VocabDeck>>((ref) async {
  final repo = ref.watch(supabaseRepositoryProvider);
  return repo.getDecks();
});

/// Helper to convert VocabDeck (Supabase) to DeckGroup (UI Model) logic if needed.
/// Or we can use VocabDeck directly in the UI. 
/// Since we want to use the existing UI, let's adapt `VocabDeck` to be compatible or just update the UI.
/// Updating the UI to use `VocabDeck` is cleaner.

// Mock Provider Preserved for Compatibility if needed, but we want to switch.
// Let's create a "view model" provider that adapts Supabase data to the List<DeckGroup> expected by UI.

final deckGroupsProvider = FutureProvider<List<DeckGroup>>((ref) async {
  final allDecks = await ref.watch(deckCollectionProvider.future);
  
  // Optional: Listen to Context to sort/filter
  final selectedContext = ref.watch(selectedContextProvider);

  // Convert
  final List<DeckGroup> deckGroups = allDecks.map((deck) {
    // Parse color with safe fallback
    int colorValue = 0xFFFF5733; 
    try {
      colorValue = int.parse(deck.color.replaceFirst('#', '0xFF'));
    } catch (_) {}

    return DeckGroup(
      id: deck.id,
      title: deck.title,
      titleKo: deck.titleKo ?? deck.title, // Fallback to English if null
      color: Color(colorValue),
      icon: deck.icon,
      progress: 0.0, // Initial progress (computed in UI via sync service)
      totalCards: deck.cardCount,
    );
  }).toList();

  // Pseudo-random shuffle based on Context to simulate "personalized recommendation"
  // 2. Sort/Prioritize based on context (Basic Logic: Hash or Seed)
  if (selectedContext.isNotEmpty && deckGroups.isNotEmpty) {
     final seed = selectedContext
        .map((e) => e.id.hashCode)
        .fold(0, (prev, element) => prev + element);
     
     // Shuffle deterministically based on context selection
     // This is a placeholder for "Recommending" decks
  }

  return deckGroups;
});
