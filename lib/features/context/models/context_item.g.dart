// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'context_item.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_ContextItem _$ContextItemFromJson(Map<String, dynamic> json) => _ContextItem(
  id: json['id'] as String,
  slug: json['slug'] as String,
  type: $enumDecode(_$ContextTypeEnumMap, json['type']),
  label: json['label'] as String,
  iconAsset: json['iconAsset'] as String,
);

Map<String, dynamic> _$ContextItemToJson(_ContextItem instance) =>
    <String, dynamic>{
      'id': instance.id,
      'slug': instance.slug,
      'type': _$ContextTypeEnumMap[instance.type]!,
      'label': instance.label,
      'iconAsset': instance.iconAsset,
    };

const _$ContextTypeEnumMap = {
  ContextType.place: 'place',
  ContextType.emotion: 'emotion',
  ContextType.environment: 'environment',
};
