// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'onboarding_provider.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning

@ProviderFor(OnboardingController)
final onboardingControllerProvider = OnboardingControllerProvider._();

final class OnboardingControllerProvider
    extends $AsyncNotifierProvider<OnboardingController, Persona?> {
  OnboardingControllerProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'onboardingControllerProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$onboardingControllerHash();

  @$internal
  @override
  OnboardingController create() => OnboardingController();
}

String _$onboardingControllerHash() =>
    r'062c24ab08b8e2f54bee42f95bb398b3a711d0cb';

abstract class _$OnboardingController extends $AsyncNotifier<Persona?> {
  FutureOr<Persona?> build();
  @$mustCallSuper
  @override
  void runBuild() {
    final ref = this.ref as $Ref<AsyncValue<Persona?>, Persona?>;
    final element =
        ref.element
            as $ClassProviderElement<
              AnyNotifier<AsyncValue<Persona?>, Persona?>,
              AsyncValue<Persona?>,
              Object?,
              Object?
            >;
    element.handleCreate(ref, build);
  }
}
