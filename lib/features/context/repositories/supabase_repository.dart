import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:vibevoca/features/context/models/supabase_models.dart';
import 'package:vibevoca/features/profile/models/user_profile_model.dart';
import 'package:vibevoca/features/profile/models/job_interest_model.dart';
import 'package:vibevoca/features/context/models/vibe_sentence.dart';

class SupabaseRepository {
  final SupabaseClient _client;

  SupabaseRepository(this._client);

  // Fetch all Categories
  Future<List<VocabCategory>> getCategories() async {
    final response = await _client
        .from('categories')
        .select()
        .order('created_at', ascending: true);
    
    return (response as List).map((e) => VocabCategory.fromJson(e)).toList();
  }

  // Fetch Decks by Category ID (if needed) or All Decks
  Future<List<VocabDeck>> getDecks({String? categoryId}) async {
    var query = _client.from('decks').select('*, cards(count)');
    
    if (categoryId != null) {
      query = query.eq('category_id', categoryId);
    }
    
    final response = await query.order('order_index', ascending: true);
    return (response as List).map((e) => VocabDeck.fromJson(e)).toList();
  }

  // Fetch Cards by Deck ID
  Future<List<VocabCard>> getCards(String deckId) async {
    final response = await _client
        .from('cards')
        .select()
        .eq('deck_id', deckId)
        .order('order_index', ascending: true);

    return (response as List).map((e) => VocabCard.fromJson(e)).toList();
  }

  // Fetch Cards by IDs (for Review Mode)
  Future<List<VocabCard>> getCardsByIds(List<String> cardIds) async {
    if (cardIds.isEmpty) return [];
    
    final response = await _client
        .from('cards')
        .select()
        .filter('id', 'in', cardIds); // Use filter for 'in' operator

    return (response as List).map((e) => VocabCard.fromJson(e)).toList();
  }

  // Fetch Meta Interests (Job, Hobby, Vibe)
  Future<List<InterestModel>> getInterests({String? category}) async {
    var query = _client.from('meta_interests').select();
    
    if (category != null) {
      query = query.eq('category', category);
    }

    final response = await query.order('order_index', ascending: true);
    return (response as List).map((e) => InterestModel.fromJson(e)).toList();
  }

  Future<UserProfileModel?> getProfile(String userId) async {
    try {
      final response = await _client
          .from('profiles')
          .select()
          .eq('id', userId)
          .maybeSingle();
      
      if (response == null) return null;
      return UserProfileModel.fromJson(response);
    } catch (e) {
      // If profile doesn't exist, return null or handle error
      return null;
    }
  }

  Future<void> updateProfile({
    required String userId,
    List<String>? interestIds,
  }) async {
    final updates = <String, dynamic>{
      if (interestIds != null) 'interest_ids': interestIds,
      'id': userId, // Ensure ID is there for upsert compatibility if needed
    };

    // Upserting to ensure profile exists
    await _client.from('profiles').upsert(updates);
  }

  Future<void> syncUserProfile({
    required String userId,
    required String email,
    required String provider,
  }) async {
    final updates = {
      'id': userId,
      'email': email,
      'auth_provider': provider,
      'last_login': DateTime.now().toIso8601String(),
    };
    // Upsert to create or update
    await _client.from('profiles').upsert(updates);
  }

  Future<void> updateLastPlayedDeck(String userId, String deckId) async {
    await _client.from('profiles').update({
      'last_played_deck_id': deckId,
    }).eq('id', userId);
  }

  Future<void> markDeckCompleted(String userId, String deckId) async {
    try {
      await _client.rpc('append_completed_deck', params: {
        'user_uuid': userId, 
        'deck_uuid': deckId
      });
    } catch (e) {
      // Fallback if RPC doesn't exist (e.g. migration not run): Manual Get -> Update
      final profile = await getProfile(userId);
      if (profile != null) {
         final current = List<String>.from(profile.completedDeckIds);
         if (!current.contains(deckId)) {
           current.add(deckId);
           await _client.from('profiles').update({
             'completed_deck_ids': current,
           }).eq('id', userId);
         }
      }
    }
  }

  Future<VocabDeck?> getDeckById(String deckId) async {
    final response = await _client
        .from('decks')
        .select()
        .eq('id', deckId)
        .maybeSingle();
    
    if (response == null) return null;
    return VocabDeck.fromJson(response);
  }

  Future<List<VibeSentence>> getVibeSentencesForDeck(String deckId, List<String> userTags) async {
    try {
      final response = await _client.rpc('get_vibe_sentences_for_deck', params: {
        'p_deck_id': deckId,
        'p_user_tags': userTags,
      });
      return (response as List).map((e) => VibeSentence.fromJson(e)).toList();
    } catch (e) {
      // Graceful degradation: return empty if RPC fails or table missing
      return [];
    }
  }
  Future<void> resetProfile(String userId) async {
    // Reset profile fields to default
    await _client.from('profiles').update({
      'interest_ids': [],
      'last_played_deck_id': null,
      'completed_deck_ids': [],
      // Keep email/auth_provider as they are identity fields
    }).eq('id', userId);

    // Also clear user deck states from DB (if we store individual rows) 
    // or we might store them in a JSON column? 
    // Currently we sync via `user_backups`.
    // If we have a `user_deck_states` table, we should clear it too. 
    // Assuming `user_deck_states` exists based on schema discussions (Local-First optimization).
    // If it doesn't, we just skip. But checking `user_backups` is key.
    
    // Clear backups
    await _client.from('user_backups').delete().eq('user_id', userId);
  }
}
