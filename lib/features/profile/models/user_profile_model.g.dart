// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user_profile_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_UserProfileModel _$UserProfileModelFromJson(Map<String, dynamic> json) =>
    _UserProfileModel(
      id: json['id'] as String,
      role: json['role'] as String?,
      interestIds:
          (json['interest_ids'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          const [],
      lastPlayedDeckId: json['last_played_deck_id'] as String?,
      completedDeckIds:
          (json['completed_deck_ids'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          const [],
    );

Map<String, dynamic> _$UserProfileModelToJson(_UserProfileModel instance) =>
    <String, dynamic>{
      'id': instance.id,
      'role': instance.role,
      'interest_ids': instance.interestIds,
      'last_played_deck_id': instance.lastPlayedDeckId,
      'completed_deck_ids': instance.completedDeckIds,
    };
