import 'package:freezed_annotation/freezed_annotation.dart';

part 'deck_state_model.freezed.dart';
part 'deck_state_model.g.dart';

@freezed
sealed class DeckState with _$DeckState {
  const factory DeckState({
    required String deckId,
    required String userId,
    @Default(0) int totalCount,
    @Default(0) int memorizedCount,
    @Default(0) int remindCount,
    @Default([]) List<CardState> cardStates,
    
    // Resume Logic
    String? lastViewedCardId,
    
    // Local-only flag to track if this needs syncing
    @JsonKey(includeToJson: false, includeFromJson: false) @Default(false) bool isDirty,
    
    // Timestamp for when it was last modified locally
    @JsonKey(includeToJson: false, includeFromJson: false) DateTime? lastChangedAt,
    
    // DB Timestamps
    DateTime? updatedAt,
  }) = _DeckState;

  factory DeckState.fromJson(Map<String, dynamic> json) => _$DeckStateFromJson(json);
}

@freezed
sealed class CardState with _$CardState {
  const factory CardState({
    required String id,
    /// 'new', 'review', 'memorized'
    @JsonKey(name: 's') required String status, 
    /// Remind Count
    @JsonKey(name: 'rc') @Default(0) int remindCount, 
    /// Re-memorize Count (or Memory Count)
    @JsonKey(name: 'mc') @Default(0) int stepCount, 
  }) = _CardState;

  factory CardState.fromJson(Map<String, dynamic> json) => _$CardStateFromJson(json);
}
