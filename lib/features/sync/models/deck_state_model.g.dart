// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'deck_state_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_DeckState _$DeckStateFromJson(Map<String, dynamic> json) => _DeckState(
  deckId: json['deckId'] as String,
  userId: json['userId'] as String,
  totalCount: (json['totalCount'] as num?)?.toInt() ?? 0,
  memorizedCount: (json['memorizedCount'] as num?)?.toInt() ?? 0,
  remindCount: (json['remindCount'] as num?)?.toInt() ?? 0,
  cardStates:
      (json['cardStates'] as List<dynamic>?)
          ?.map((e) => CardState.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
  lastViewedCardId: json['lastViewedCardId'] as String?,
  updatedAt: json['updatedAt'] == null
      ? null
      : DateTime.parse(json['updatedAt'] as String),
);

Map<String, dynamic> _$DeckStateToJson(_DeckState instance) =>
    <String, dynamic>{
      'deckId': instance.deckId,
      'userId': instance.userId,
      'totalCount': instance.totalCount,
      'memorizedCount': instance.memorizedCount,
      'remindCount': instance.remindCount,
      'cardStates': instance.cardStates,
      'lastViewedCardId': instance.lastViewedCardId,
      'updatedAt': instance.updatedAt?.toIso8601String(),
    };

_CardState _$CardStateFromJson(Map<String, dynamic> json) => _CardState(
  id: json['id'] as String,
  status: json['s'] as String,
  remindCount: (json['rc'] as num?)?.toInt() ?? 0,
  stepCount: (json['mc'] as num?)?.toInt() ?? 0,
);

Map<String, dynamic> _$CardStateToJson(_CardState instance) =>
    <String, dynamic>{
      'id': instance.id,
      's': instance.status,
      'rc': instance.remindCount,
      'mc': instance.stepCount,
    };
