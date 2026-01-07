// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'job_interest_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_InterestModel _$InterestModelFromJson(Map<String, dynamic> json) =>
    _InterestModel(
      id: json['id'] as String,
      category: json['category'] as String? ?? 'job',
      code: json['code'] as String,
      labelEn: json['label_en'] as String,
      labelKo: json['label_ko'] as String,
      icon: json['icon'] as String?,
      color: json['color'] as String?,
      tags:
          (json['tags'] as List<dynamic>?)?.map((e) => e as String).toList() ??
          const [],
      orderIndex: (json['order_index'] as num?)?.toInt() ?? 0,
    );

Map<String, dynamic> _$InterestModelToJson(_InterestModel instance) =>
    <String, dynamic>{
      'id': instance.id,
      'category': instance.category,
      'code': instance.code,
      'label_en': instance.labelEn,
      'label_ko': instance.labelKo,
      'icon': instance.icon,
      'color': instance.color,
      'tags': instance.tags,
      'order_index': instance.orderIndex,
    };
