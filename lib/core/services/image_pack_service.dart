import 'dart:io';
import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:path_provider/path_provider.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:archive/archive.dart';
import 'package:http/http.dart' as http;

/// 카테고리별 이미지 팩 다운로드 및 관리 서비스
class ImagePackService {
  final SupabaseClient _client;

  static const _bucketName = 'category-images';
  static const _localDirName = 'word_images';
  static const _manifestFileName = 'manifest.json';

  // 싱글톤 캐시
  static Map<String, bool>? _downloadedPacks;
  static String? _localBasePath;

  ImagePackService(this._client);

  /// 로컬 이미지 저장 경로
  Future<String> get localBasePath async {
    if (_localBasePath != null) return _localBasePath!;
    final dir = await getApplicationDocumentsDirectory();
    _localBasePath = '${dir.path}/$_localDirName';
    return _localBasePath!;
  }

  /// 마커 파일 경로 (다운로드 완료 표시)
  String _markerPath(String basePath, String categoryId) {
    return '$basePath/.pack_$categoryId';
  }

  /// 카테고리 팩 다운로드 여부 확인
  Future<bool> isPackDownloaded(String categoryId) async {
    // 캐시 확인
    if (_downloadedPacks != null && _downloadedPacks!.containsKey(categoryId)) {
      return _downloadedPacks![categoryId]!;
    }

    final basePath = await localBasePath;
    final markerFile = File(_markerPath(basePath, categoryId));
    final exists = markerFile.existsSync();

    // 캐시 저장
    _downloadedPacks ??= {};
    _downloadedPacks![categoryId] = exists;

    return exists;
  }

  /// 로컬 이미지 경로 조회 (있으면 경로, 없으면 null)
  Future<String?> getLocalImagePath(String cardId) async {
    final basePath = await localBasePath;
    final path = '$basePath/$cardId.jpg';

    if (File(path).existsSync()) {
      return path;
    }
    return null;
  }

  /// 번들 에셋 이미지 존재 여부 확인 (데모 카테고리용)
  static final Map<String, bool> _bundledAssetCache = {};

  Future<bool> checkBundledAssetExists(String assetPath) async {
    if (_bundledAssetCache.containsKey(assetPath)) {
      return _bundledAssetCache[assetPath]!;
    }

    try {
      await rootBundle.load(assetPath);
      _bundledAssetCache[assetPath] = true;
      return true;
    } catch (_) {
      _bundledAssetCache[assetPath] = false;
      return false;
    }
  }

  /// Storage에서 manifest 조회
  Future<Map<String, dynamic>?> getRemoteManifest() async {
    try {
      final signedUrl = await _client.storage
          .from(_bucketName)
          .createSignedUrl(_manifestFileName, 3600);

      final response = await http.get(Uri.parse(signedUrl));
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (e) {
      print('ImagePackService: manifest 조회 실패: $e');
    }
    return null;
  }

  /// 카테고리 팩 다운로드 및 추출
  Future<void> downloadPack(
    String categoryId, {
    void Function(double progress)? onProgress,
  }) async {
    final basePath = await localBasePath;

    // 디렉토리 생성
    final dir = Directory(basePath);
    if (!dir.existsSync()) {
      dir.createSync(recursive: true);
    }

    // 1. Signed URL 생성
    final zipFileName = '${categoryId.toLowerCase()}.zip';
    print('Attemping to download: Bucket=$_bucketName, File=$zipFileName'); // Debug Log
    final signedUrl = await _client.storage
        .from(_bucketName)
        .createSignedUrl(zipFileName, 3600);

    // 2. ZIP 다운로드
    onProgress?.call(0.1);

    final response = await http.get(Uri.parse(signedUrl));
    if (response.statusCode != 200) {
      throw Exception('다운로드 실패: ${response.statusCode}');
    }

    onProgress?.call(0.5);

    // 3. ZIP 추출
    final bytes = response.bodyBytes;
    final archive = ZipDecoder().decodeBytes(bytes);

    final totalFiles = archive.length;
    var extractedFiles = 0;

    for (final file in archive) {
      if (file.isFile) {
        final filename = file.name;
        final data = file.content as List<int>;

        File('$basePath/$filename')
          ..createSync(recursive: true)
          ..writeAsBytesSync(data);

        extractedFiles++;
        final extractProgress = 0.5 + (0.4 * extractedFiles / totalFiles);
        onProgress?.call(extractProgress);
      }
    }

    // 4. 마커 파일 생성 (다운로드 완료 표시)
    final markerFile = File(_markerPath(basePath, categoryId));
    markerFile.writeAsStringSync(DateTime.now().toIso8601String());

    // 캐시 업데이트
    _downloadedPacks ??= {};
    _downloadedPacks![categoryId] = true;

    onProgress?.call(1.0);
  }

  /// 카테고리 팩 삭제 (저장공간 확보)
  Future<int> deletePack(String categoryId) async {
    final basePath = await localBasePath;
    final markerFile = File(_markerPath(basePath, categoryId));

    if (!markerFile.existsSync()) {
      return 0; // 이미 삭제됨
    }

    // manifest에서 해당 카테고리 이미지 목록 가져오기
    // 또는 마커 파일에 이미지 목록 저장해둘 수도 있음
    // 여기서는 간단히 마커만 삭제 (이미지는 유지)
    markerFile.deleteSync();

    // 캐시 업데이트
    _downloadedPacks?[categoryId] = false;

    return 1;
  }

  /// 전체 다운로드된 팩 목록
  Future<List<String>> getDownloadedPackIds() async {
    final basePath = await localBasePath;
    final dir = Directory(basePath);

    if (!dir.existsSync()) return [];

    final packIds = <String>[];
    for (final file in dir.listSync()) {
      if (file is File && file.path.contains('.pack_')) {
        final filename = file.path.split('/').last;
        final categoryId = filename.replaceFirst('.pack_', '');
        packIds.add(categoryId);
      }
    }

    return packIds;
  }

  /// 캐시된 이미지 총 용량 계산
  Future<int> getCachedImageSize() async {
    final basePath = await localBasePath;
    final dir = Directory(basePath);

    if (!dir.existsSync()) return 0;

    var totalSize = 0;
    for (final file in dir.listSync()) {
      if (file is File && file.path.endsWith('.jpg')) {
        totalSize += file.lengthSync();
      }
    }

    return totalSize;
  }

  /// 모든 캐시 삭제
  Future<void> clearAllCache() async {
    final basePath = await localBasePath;
    final dir = Directory(basePath);

    if (dir.existsSync()) {
      dir.deleteSync(recursive: true);
    }

    // 캐시 초기화
    _downloadedPacks = null;
    _localBasePath = null;
  }
}
