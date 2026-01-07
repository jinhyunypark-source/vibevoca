// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'vibe_sentence.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_VibeSentence _$VibeSentenceFromJson(Map<String, dynamic> json) =>
    _VibeSentence(
      cardId: json['card_id'] as String,
      sentenceEn: json['sentence_en'] as String,
      sentenceKo: json['sentence_ko'] as String?,
      tags: (json['tags'] as List<dynamic>).map((e) => e as String).toList(),
    );

Map<String, dynamic> _$VibeSentenceToJson(_VibeSentence instance) =>
    <String, dynamic>{
      'card_id': instance.cardId,
      'sentence_en': instance.sentenceEn,
      'sentence_ko': instance.sentenceKo,
      'tags': instance.tags,
    };
