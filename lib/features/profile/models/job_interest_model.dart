import 'package:freezed_annotation/freezed_annotation.dart';

part 'job_interest_model.freezed.dart';
part 'job_interest_model.g.dart';

@freezed
abstract class InterestModel with _$InterestModel {
  const factory InterestModel({
    required String id,
    @Default('job') String category, // job, hobby, vibe
    required String code,
    @JsonKey(name: 'label_en') required String labelEn,
    @JsonKey(name: 'label_ko') required String labelKo,
    String? icon,
    String? color,
    @Default([]) List<String> tags,
    @JsonKey(name: 'order_index') @Default(0) int orderIndex,
  }) = _InterestModel;

  factory InterestModel.fromJson(Map<String, dynamic> json) => _$InterestModelFromJson(json);
}
