// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'image_pack_provider.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning
/// 카테고리별 다운로드 상태 프로바이더 (Family)

@ProviderFor(CategoryDownloadState)
final categoryDownloadStateProvider = CategoryDownloadStateFamily._();

/// 카테고리별 다운로드 상태 프로바이더 (Family)
final class CategoryDownloadStateProvider
    extends $NotifierProvider<CategoryDownloadState, DownloadState> {
  /// 카테고리별 다운로드 상태 프로바이더 (Family)
  CategoryDownloadStateProvider._({
    required CategoryDownloadStateFamily super.from,
    required String super.argument,
  }) : super(
         retry: null,
         name: r'categoryDownloadStateProvider',
         isAutoDispose: true,
         dependencies: null,
         $allTransitiveDependencies: null,
       );

  @override
  String debugGetCreateSourceHash() => _$categoryDownloadStateHash();

  @override
  String toString() {
    return r'categoryDownloadStateProvider'
        ''
        '($argument)';
  }

  @$internal
  @override
  CategoryDownloadState create() => CategoryDownloadState();

  /// {@macro riverpod.override_with_value}
  Override overrideWithValue(DownloadState value) {
    return $ProviderOverride(
      origin: this,
      providerOverride: $SyncValueProvider<DownloadState>(value),
    );
  }

  @override
  bool operator ==(Object other) {
    return other is CategoryDownloadStateProvider && other.argument == argument;
  }

  @override
  int get hashCode {
    return argument.hashCode;
  }
}

String _$categoryDownloadStateHash() =>
    r'80fd244d3fe6a81471c53b55ce3f64b7ee1e45f0';

/// 카테고리별 다운로드 상태 프로바이더 (Family)

final class CategoryDownloadStateFamily extends $Family
    with
        $ClassFamilyOverride<
          CategoryDownloadState,
          DownloadState,
          DownloadState,
          DownloadState,
          String
        > {
  CategoryDownloadStateFamily._()
    : super(
        retry: null,
        name: r'categoryDownloadStateProvider',
        dependencies: null,
        $allTransitiveDependencies: null,
        isAutoDispose: true,
      );

  /// 카테고리별 다운로드 상태 프로바이더 (Family)

  CategoryDownloadStateProvider call(String categoryId) =>
      CategoryDownloadStateProvider._(argument: categoryId, from: this);

  @override
  String toString() => r'categoryDownloadStateProvider';
}

/// 카테고리별 다운로드 상태 프로바이더 (Family)

abstract class _$CategoryDownloadState extends $Notifier<DownloadState> {
  late final _$args = ref.$arg as String;
  String get categoryId => _$args;

  DownloadState build(String categoryId);
  @$mustCallSuper
  @override
  void runBuild() {
    final ref = this.ref as $Ref<DownloadState, DownloadState>;
    final element =
        ref.element
            as $ClassProviderElement<
              AnyNotifier<DownloadState, DownloadState>,
              DownloadState,
              Object?,
              Object?
            >;
    element.handleCreate(ref, () => build(_$args));
  }
}

/// 다운로드된 팩 목록 프로바이더

@ProviderFor(downloadedPacks)
final downloadedPacksProvider = DownloadedPacksProvider._();

/// 다운로드된 팩 목록 프로바이더

final class DownloadedPacksProvider
    extends
        $FunctionalProvider<
          AsyncValue<List<String>>,
          List<String>,
          FutureOr<List<String>>
        >
    with $FutureModifier<List<String>>, $FutureProvider<List<String>> {
  /// 다운로드된 팩 목록 프로바이더
  DownloadedPacksProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'downloadedPacksProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$downloadedPacksHash();

  @$internal
  @override
  $FutureProviderElement<List<String>> $createElement(
    $ProviderPointer pointer,
  ) => $FutureProviderElement(pointer);

  @override
  FutureOr<List<String>> create(Ref ref) {
    return downloadedPacks(ref);
  }
}

String _$downloadedPacksHash() => r'a413a20fef0d93a836199891466d1c4e11fbd200';

/// 캐시된 이미지 총 용량 프로바이더

@ProviderFor(cachedImageSize)
final cachedImageSizeProvider = CachedImageSizeProvider._();

/// 캐시된 이미지 총 용량 프로바이더

final class CachedImageSizeProvider
    extends $FunctionalProvider<AsyncValue<int>, int, FutureOr<int>>
    with $FutureModifier<int>, $FutureProvider<int> {
  /// 캐시된 이미지 총 용량 프로바이더
  CachedImageSizeProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'cachedImageSizeProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$cachedImageSizeHash();

  @$internal
  @override
  $FutureProviderElement<int> $createElement($ProviderPointer pointer) =>
      $FutureProviderElement(pointer);

  @override
  FutureOr<int> create(Ref ref) {
    return cachedImageSize(ref);
  }
}

String _$cachedImageSizeHash() => r'a7d42ea4563c78964037c9b1c51dcd9fc5f793e3';
