import 'package:freezed_annotation/freezed_annotation.dart';
import '../../profile/models/job_interest_model.dart';

part 'user_profile_model.freezed.dart';
part 'user_profile_model.g.dart';

@freezed
abstract class UserProfileModel with _$UserProfileModel {
  const factory UserProfileModel({
    required String id,
    String? role,
    // Unified interest_ids now contains both jobs and interests
    @JsonKey(name: 'interest_ids') @Default([]) List<String> interestIds,
    @JsonKey(name: 'last_played_deck_id') String? lastPlayedDeckId,
    @JsonKey(name: 'completed_deck_ids') @Default([]) List<String> completedDeckIds,
  }) = _UserProfileModel;

  factory UserProfileModel.fromJson(Map<String, dynamic> json) => _$UserProfileModelFromJson(json);
}
