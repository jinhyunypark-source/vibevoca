// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'persona.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_Persona _$PersonaFromJson(Map<String, dynamic> json) => _Persona(
  id: json['id'] as String,
  name: json['name'] as String,
  job: json['job'] as String,
  interests: (json['interests'] as List<dynamic>)
      .map((e) => e as String)
      .toList(),
  title: json['title'] as String,
);

Map<String, dynamic> _$PersonaToJson(_Persona instance) => <String, dynamic>{
  'id': instance.id,
  'name': instance.name,
  'job': instance.job,
  'interests': instance.interests,
  'title': instance.title,
};
