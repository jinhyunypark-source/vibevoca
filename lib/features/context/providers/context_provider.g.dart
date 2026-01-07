// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'context_provider.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning

@ProviderFor(allContextOptions)
final allContextOptionsProvider = AllContextOptionsProvider._();

final class AllContextOptionsProvider
    extends
        $FunctionalProvider<
          AsyncValue<List<ContextItem>>,
          List<ContextItem>,
          FutureOr<List<ContextItem>>
        >
    with
        $FutureModifier<List<ContextItem>>,
        $FutureProvider<List<ContextItem>> {
  AllContextOptionsProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'allContextOptionsProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$allContextOptionsHash();

  @$internal
  @override
  $FutureProviderElement<List<ContextItem>> $createElement(
    $ProviderPointer pointer,
  ) => $FutureProviderElement(pointer);

  @override
  FutureOr<List<ContextItem>> create(Ref ref) {
    return allContextOptions(ref);
  }
}

String _$allContextOptionsHash() => r'e8a15020156885362749f17d27378fac3779308e';

@ProviderFor(SelectedContext)
final selectedContextProvider = SelectedContextProvider._();

final class SelectedContextProvider
    extends $NotifierProvider<SelectedContext, List<ContextItem>> {
  SelectedContextProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'selectedContextProvider',
        isAutoDispose: false,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$selectedContextHash();

  @$internal
  @override
  SelectedContext create() => SelectedContext();

  /// {@macro riverpod.override_with_value}
  Override overrideWithValue(List<ContextItem> value) {
    return $ProviderOverride(
      origin: this,
      providerOverride: $SyncValueProvider<List<ContextItem>>(value),
    );
  }
}

String _$selectedContextHash() => r'8e14e6cba7b824e853d86a589421c6fd6cd30432';

abstract class _$SelectedContext extends $Notifier<List<ContextItem>> {
  List<ContextItem> build();
  @$mustCallSuper
  @override
  void runBuild() {
    final ref = this.ref as $Ref<List<ContextItem>, List<ContextItem>>;
    final element =
        ref.element
            as $ClassProviderElement<
              AnyNotifier<List<ContextItem>, List<ContextItem>>,
              List<ContextItem>,
              Object?,
              Object?
            >;
    element.handleCreate(ref, build);
  }
}
