// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'profile_provider.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning

@ProviderFor(interests)
final interestsProvider = InterestsProvider._();

final class InterestsProvider
    extends
        $FunctionalProvider<
          AsyncValue<List<InterestModel>>,
          List<InterestModel>,
          FutureOr<List<InterestModel>>
        >
    with
        $FutureModifier<List<InterestModel>>,
        $FutureProvider<List<InterestModel>> {
  InterestsProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'interestsProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$interestsHash();

  @$internal
  @override
  $FutureProviderElement<List<InterestModel>> $createElement(
    $ProviderPointer pointer,
  ) => $FutureProviderElement(pointer);

  @override
  FutureOr<List<InterestModel>> create(Ref ref) {
    return interests(ref);
  }
}

String _$interestsHash() => r'78c9f174baf3a40e2078782a8615bd84f8459512';

@ProviderFor(userProfile)
final userProfileProvider = UserProfileProvider._();

final class UserProfileProvider
    extends
        $FunctionalProvider<
          AsyncValue<UserProfileModel?>,
          UserProfileModel?,
          FutureOr<UserProfileModel?>
        >
    with
        $FutureModifier<UserProfileModel?>,
        $FutureProvider<UserProfileModel?> {
  UserProfileProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'userProfileProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$userProfileHash();

  @$internal
  @override
  $FutureProviderElement<UserProfileModel?> $createElement(
    $ProviderPointer pointer,
  ) => $FutureProviderElement(pointer);

  @override
  FutureOr<UserProfileModel?> create(Ref ref) {
    return userProfile(ref);
  }
}

String _$userProfileHash() => r'74ec92d1107ab5d08c45fe8791e0db92a34cb1a9';

@ProviderFor(ProfileController)
final profileControllerProvider = ProfileControllerProvider._();

final class ProfileControllerProvider
    extends $AsyncNotifierProvider<ProfileController, void> {
  ProfileControllerProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'profileControllerProvider',
        isAutoDispose: false,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$profileControllerHash();

  @$internal
  @override
  ProfileController create() => ProfileController();
}

String _$profileControllerHash() => r'6e742a16875a9bc801179a0e62974e50eb8a2327';

abstract class _$ProfileController extends $AsyncNotifier<void> {
  FutureOr<void> build();
  @$mustCallSuper
  @override
  void runBuild() {
    final ref = this.ref as $Ref<AsyncValue<void>, void>;
    final element =
        ref.element
            as $ClassProviderElement<
              AnyNotifier<AsyncValue<void>, void>,
              AsyncValue<void>,
              Object?,
              Object?
            >;
    element.handleCreate(ref, build);
  }
}
