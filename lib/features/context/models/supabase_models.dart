
import 'package:freezed_annotation/freezed_annotation.dart';

part 'supabase_models.freezed.dart';
part 'supabase_models.g.dart';

@freezed
abstract class VocabCategory with _$VocabCategory {
  const factory VocabCategory({
    required String id,
    required String title,
    @JsonKey(name: 'title_ko') String? titleKo,
    String? description,
    @JsonKey(name: 'image_url') String? imageUrl,
    String? icon,
    @Default('#4A90E2') String color,
  }) = _VocabCategory;

  factory VocabCategory.fromJson(Map<String, dynamic> json) => _$VocabCategoryFromJson(json);
}

@freezed
abstract class VocabDeck with _$VocabDeck {
  const factory VocabDeck({
    required String id,
    @JsonKey(name: 'category_id') required String categoryId,
    required String title,
    @JsonKey(name: 'title_ko') String? titleKo,
    @JsonKey(name: 'order_index') @Default(0) int orderIndex,
    @Default('#FF5733') String color,
    String? icon,
    @Default(0) @JsonKey(readValue: _readCardCount) int cardCount, // Fetched via count query
  }) = _VocabDeck;

  factory VocabDeck.fromJson(Map<String, dynamic> json) => _$VocabDeckFromJson(json);
}

// Helper to extract count from nested json
Object? _readCardCount(Map map, String key) {
   // Supabase returns { ..., "cards": [{ "count": 10 }] }
   if (map['cards'] != null && map['cards'] is List && (map['cards'] as List).isNotEmpty) {
       final first = (map['cards'] as List).first;
       if (first is Map && first['count'] != null) {
         return first['count'];
       }
   }
   return 0;
}

@freezed
abstract class VocabCard with _$VocabCard {
  const factory VocabCard({
    required String id,
    @JsonKey(name: 'deck_id') required String deckId,
    @JsonKey(name: 'front_text') required String frontText,
    @JsonKey(name: 'back_text') required String backText,
    @JsonKey(name: 'example_sentences') @Default([]) List<String> exampleSentences,
    @JsonKey(name: 'audio_url') String? audioUrl,
  }) = _VocabCard;

  factory VocabCard.fromJson(Map<String, dynamic> json) => _$VocabCardFromJson(json);
}

@freezed
abstract class VocabContext with _$VocabContext {
  const factory VocabContext({
    required String id,
    required String type, // place, emotion, environment
    required String slug,
    required String label,
    String? icon, 
    @JsonKey(name: 'prompt_description') String? promptDescription,
  }) = _VocabContext;

  factory VocabContext.fromJson(Map<String, dynamic> json) => _$VocabContextFromJson(json);
}
