import 'package:freezed_annotation/freezed_annotation.dart';

part 'persona.freezed.dart';
part 'persona.g.dart';

@freezed
abstract class Persona with _$Persona {
  const factory Persona({
    required String id,
    required String name,
    required String job,
    required List<String> interests,
    required String title, // e.g. "The Energetic Striker"
  }) = _Persona;

  factory Persona.fromJson(Map<String, dynamic> json) => _$PersonaFromJson(json);
}
