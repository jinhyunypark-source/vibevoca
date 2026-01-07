// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'word_card_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_WordCardModel _$WordCardModelFromJson(Map<String, dynamic> json) =>
    _WordCardModel(
      id: json['id'] as String,
      word: json['word'] as String,
      meaning: json['meaning'] as String,
      exampleSentence: json['exampleSentence'] as String,
      vibeSentences:
          (json['vibeSentences'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          const [],
      isMemorized: json['isMemorized'] as bool? ?? false,
      failCount: (json['failCount'] as num?)?.toInt() ?? 0,
      originalDeckId: json['originalDeckId'] as String?,
    );

Map<String, dynamic> _$WordCardModelToJson(_WordCardModel instance) =>
    <String, dynamic>{
      'id': instance.id,
      'word': instance.word,
      'meaning': instance.meaning,
      'exampleSentence': instance.exampleSentence,
      'vibeSentences': instance.vibeSentences,
      'isMemorized': instance.isMemorized,
      'failCount': instance.failCount,
      'originalDeckId': instance.originalDeckId,
    };
