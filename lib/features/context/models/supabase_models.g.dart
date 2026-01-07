// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'supabase_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_VocabCategory _$VocabCategoryFromJson(Map<String, dynamic> json) =>
    _VocabCategory(
      id: json['id'] as String,
      title: json['title'] as String,
      titleKo: json['title_ko'] as String?,
      description: json['description'] as String?,
      imageUrl: json['image_url'] as String?,
      icon: json['icon'] as String?,
      color: json['color'] as String? ?? '#4A90E2',
    );

Map<String, dynamic> _$VocabCategoryToJson(_VocabCategory instance) =>
    <String, dynamic>{
      'id': instance.id,
      'title': instance.title,
      'title_ko': instance.titleKo,
      'description': instance.description,
      'image_url': instance.imageUrl,
      'icon': instance.icon,
      'color': instance.color,
    };

_VocabDeck _$VocabDeckFromJson(Map<String, dynamic> json) => _VocabDeck(
  id: json['id'] as String,
  categoryId: json['category_id'] as String,
  title: json['title'] as String,
  titleKo: json['title_ko'] as String?,
  orderIndex: (json['order_index'] as num?)?.toInt() ?? 0,
  color: json['color'] as String? ?? '#FF5733',
  icon: json['icon'] as String?,
  cardCount: (_readCardCount(json, 'cardCount') as num?)?.toInt() ?? 0,
);

Map<String, dynamic> _$VocabDeckToJson(_VocabDeck instance) =>
    <String, dynamic>{
      'id': instance.id,
      'category_id': instance.categoryId,
      'title': instance.title,
      'title_ko': instance.titleKo,
      'order_index': instance.orderIndex,
      'color': instance.color,
      'icon': instance.icon,
      'cardCount': instance.cardCount,
    };

_VocabCard _$VocabCardFromJson(Map<String, dynamic> json) => _VocabCard(
  id: json['id'] as String,
  deckId: json['deck_id'] as String,
  frontText: json['front_text'] as String,
  backText: json['back_text'] as String,
  exampleSentences:
      (json['example_sentences'] as List<dynamic>?)
          ?.map((e) => e as String)
          .toList() ??
      const [],
  audioUrl: json['audio_url'] as String?,
);

Map<String, dynamic> _$VocabCardToJson(_VocabCard instance) =>
    <String, dynamic>{
      'id': instance.id,
      'deck_id': instance.deckId,
      'front_text': instance.frontText,
      'back_text': instance.backText,
      'example_sentences': instance.exampleSentences,
      'audio_url': instance.audioUrl,
    };

_VocabContext _$VocabContextFromJson(Map<String, dynamic> json) =>
    _VocabContext(
      id: json['id'] as String,
      type: json['type'] as String,
      slug: json['slug'] as String,
      label: json['label'] as String,
      icon: json['icon'] as String?,
      promptDescription: json['prompt_description'] as String?,
    );

Map<String, dynamic> _$VocabContextToJson(_VocabContext instance) =>
    <String, dynamic>{
      'id': instance.id,
      'type': instance.type,
      'slug': instance.slug,
      'label': instance.label,
      'icon': instance.icon,
      'prompt_description': instance.promptDescription,
    };
