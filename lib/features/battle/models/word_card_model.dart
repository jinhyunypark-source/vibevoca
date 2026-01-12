import 'package:freezed_annotation/freezed_annotation.dart';

part 'word_card_model.freezed.dart';
part 'word_card_model.g.dart';

@freezed
abstract class WordCardModel with _$WordCardModel {
  const factory WordCardModel({
    required String id,
    required String word,
    required String meaning,
    required String exampleSentence, // "AI Generated" context
    @Default([]) List<VibeDisplayInfo> vibeSentences,
    @Default(false) bool isMemorized,
    @Default(0) int failCount,
    String? originalDeckId, // Needed for mixed-deck review sessions
  }) = _WordCardModel;

  factory WordCardModel.fromJson(Map<String, dynamic> json) => _$WordCardModelFromJson(json);
}

@freezed
abstract class VibeDisplayInfo with _$VibeDisplayInfo {
  const factory VibeDisplayInfo({
    required String sentence,
    String? icon, // Material Icon name string
    String? tagName, // e.g. "IT", "Business"
  }) = _VibeDisplayInfo;

  factory VibeDisplayInfo.fromJson(Map<String, dynamic> json) => _$VibeDisplayInfoFromJson(json);
}
