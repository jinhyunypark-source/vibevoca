import 'package:freezed_annotation/freezed_annotation.dart';

part 'download_state.freezed.dart';

/// 카테고리 이미지 팩 다운로드 상태
@freezed
sealed class DownloadState with _$DownloadState {
  /// 다운로드되지 않음
  const factory DownloadState.notDownloaded() = NotDownloaded;

  /// 다운로드 중 (진행률 0.0 ~ 1.0)
  const factory DownloadState.downloading(double progress) = Downloading;

  /// 다운로드 완료
  const factory DownloadState.downloaded() = Downloaded;

  /// 다운로드 오류
  const factory DownloadState.error(String message) = DownloadError;
}
