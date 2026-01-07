import 'package:freezed_annotation/freezed_annotation.dart';

part 'vibe_sentence.freezed.dart';
part 'vibe_sentence.g.dart';

@freezed
abstract class VibeSentence with _$VibeSentence {
  const factory VibeSentence({
    @JsonKey(name: 'card_id') required String cardId,
    @JsonKey(name: 'sentence_en') required String sentenceEn,
    @JsonKey(name: 'sentence_ko') String? sentenceKo,
    required List<String> tags,
  }) = _VibeSentence;

  factory VibeSentence.fromJson(Map<String, dynamic> json) => _$VibeSentenceFromJson(json);
}
