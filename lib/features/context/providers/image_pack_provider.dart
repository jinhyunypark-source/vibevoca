import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:vibevoca/core/services/image_pack_service.dart';
import 'package:vibevoca/core/services/models/download_state.dart';

part 'image_pack_provider.g.dart';

/// ImagePackService 싱글톤 프로바이더
final imagePackServiceProvider = Provider<ImagePackService>((ref) {
  return ImagePackService(Supabase.instance.client);
});

/// 카테고리별 다운로드 상태 프로바이더 (Family)
@riverpod
class CategoryDownloadState extends _$CategoryDownloadState {
  @override
  DownloadState build(String categoryId) {
    // 초기 상태 확인 (비동기)
    _checkInitialState();
    return const DownloadState.notDownloaded();
  }

  Future<void> _checkInitialState() async {
    final service = ref.read(imagePackServiceProvider);
    final isDownloaded = await service.isPackDownloaded(categoryId);

    if (isDownloaded) {
      state = const DownloadState.downloaded();
    }
  }

  /// 다운로드 시작
  Future<void> startDownload() async {
    if (state is Downloading) return; // 이미 다운로드 중

    state = const DownloadState.downloading(0.0);

    try {
      final service = ref.read(imagePackServiceProvider);
      await service.downloadPack(
        categoryId, // categoryId (family parameter)
        onProgress: (progress) {
          state = DownloadState.downloading(progress);
        },
      );
      state = const DownloadState.downloaded();
    } catch (e, stackTrace) {
      print('Image Download Error: $e');
      print(stackTrace);
      state = DownloadState.error(e.toString());
    }
  }

  /// 다운로드 삭제
  Future<void> deletePack() async {
    final service = ref.read(imagePackServiceProvider);
    await service.deletePack(categoryId);
    state = const DownloadState.notDownloaded();
  }

  /// 에러 후 재시도
  void retry() {
    state = const DownloadState.notDownloaded();
  }
}

/// 다운로드된 팩 목록 프로바이더
@riverpod
Future<List<String>> downloadedPacks(Ref ref) async {
  final service = ref.watch(imagePackServiceProvider);
  return service.getDownloadedPackIds();
}

/// 캐시된 이미지 총 용량 프로바이더
@riverpod
Future<int> cachedImageSize(Ref ref) async {
  final service = ref.watch(imagePackServiceProvider);
  return service.getCachedImageSize();
}

/// 데모 카테고리 ID (첫 번째 카테고리)
const demoCategoryId = 'eec83079-d8a3-4516-bf30-fc78977f72cd';

/// 데모 카테고리 여부 확인
bool isDemoCategory(String categoryId) {
  return categoryId == demoCategoryId;
}
