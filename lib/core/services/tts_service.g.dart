// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'tts_service.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning

@ProviderFor(ttsService)
final ttsServiceProvider = TtsServiceProvider._();

final class TtsServiceProvider
    extends $FunctionalProvider<TTSInterface, TTSInterface, TTSInterface>
    with $Provider<TTSInterface> {
  TtsServiceProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'ttsServiceProvider',
        isAutoDispose: false,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$ttsServiceHash();

  @$internal
  @override
  $ProviderElement<TTSInterface> $createElement($ProviderPointer pointer) =>
      $ProviderElement(pointer);

  @override
  TTSInterface create(Ref ref) {
    return ttsService(ref);
  }

  /// {@macro riverpod.override_with_value}
  Override overrideWithValue(TTSInterface value) {
    return $ProviderOverride(
      origin: this,
      providerOverride: $SyncValueProvider<TTSInterface>(value),
    );
  }
}

String _$ttsServiceHash() => r'5f4c34d655529777ed229e7fbb272c2b4d2cb9dd';
