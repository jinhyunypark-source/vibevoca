// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'battle_provider.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning

@ProviderFor(BattleController)
final battleControllerProvider = BattleControllerFamily._();

final class BattleControllerProvider
    extends $AsyncNotifierProvider<BattleController, BattleSessionState> {
  BattleControllerProvider._({
    required BattleControllerFamily super.from,
    required String super.argument,
  }) : super(
         retry: null,
         name: r'battleControllerProvider',
         isAutoDispose: true,
         dependencies: null,
         $allTransitiveDependencies: null,
       );

  @override
  String debugGetCreateSourceHash() => _$battleControllerHash();

  @override
  String toString() {
    return r'battleControllerProvider'
        ''
        '($argument)';
  }

  @$internal
  @override
  BattleController create() => BattleController();

  @override
  bool operator ==(Object other) {
    return other is BattleControllerProvider && other.argument == argument;
  }

  @override
  int get hashCode {
    return argument.hashCode;
  }
}

String _$battleControllerHash() => r'a8b2b098f5d7d38b3cca88aa1970d066f29e010b';

final class BattleControllerFamily extends $Family
    with
        $ClassFamilyOverride<
          BattleController,
          AsyncValue<BattleSessionState>,
          BattleSessionState,
          FutureOr<BattleSessionState>,
          String
        > {
  BattleControllerFamily._()
    : super(
        retry: null,
        name: r'battleControllerProvider',
        dependencies: null,
        $allTransitiveDependencies: null,
        isAutoDispose: true,
      );

  BattleControllerProvider call(String deckId) =>
      BattleControllerProvider._(argument: deckId, from: this);

  @override
  String toString() => r'battleControllerProvider';
}

abstract class _$BattleController extends $AsyncNotifier<BattleSessionState> {
  late final _$args = ref.$arg as String;
  String get deckId => _$args;

  FutureOr<BattleSessionState> build(String deckId);
  @$mustCallSuper
  @override
  void runBuild() {
    final ref =
        this.ref as $Ref<AsyncValue<BattleSessionState>, BattleSessionState>;
    final element =
        ref.element
            as $ClassProviderElement<
              AnyNotifier<AsyncValue<BattleSessionState>, BattleSessionState>,
              AsyncValue<BattleSessionState>,
              Object?,
              Object?
            >;
    element.handleCreate(ref, () => build(_$args));
  }
}
