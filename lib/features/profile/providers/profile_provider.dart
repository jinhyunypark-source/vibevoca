import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:vibevoca/features/context/repositories/supabase_repository.dart';
import 'package:vibevoca/features/context/providers/deck_collection_provider.dart';
import 'package:vibevoca/features/sync/services/session_service.dart'; // Added for Guest Support
import 'package:vibevoca/features/profile/models/job_interest_model.dart';
import 'package:vibevoca/features/profile/models/user_profile_model.dart';
import 'package:vibevoca/features/auth/providers/auth_provider.dart';

part 'profile_provider.g.dart';

@riverpod
Future<List<InterestModel>> interests(Ref ref) async {
  final repo = ref.watch(supabaseRepositoryProvider);
  return repo.getInterests();
}

@riverpod
Future<UserProfileModel?> userProfile(Ref ref) async {
  final user = ref.watch(authProvider).value;
  // If user is logged in, fetch from Supabase
  if (user != null) {
    final repo = ref.watch(supabaseRepositoryProvider);
    return repo.getProfile(user.id);
  }
  
  // If Guest, fetch from SessionService (Local)
  // We need to watch specific updates or just rely on invalidation?
  // Since SessionService is not a notifier, we rely on invalidation calls.
  return ref.read(sessionServiceProvider).getProfile();
}

@Riverpod(keepAlive: true)
class ProfileController extends _$ProfileController {
  @override
  FutureOr<void> build() {}

  Future<void> saveProfile({
    List<String>? interestIds,
  }) async {
    final user = ref.read(authProvider).value;
    
    // GUEST HANDLING
    if (user == null) {
       // Persist strictly to local storage
       // We create a temporary profile object if needed or update existing
       final currentProfile = ref.read(sessionServiceProvider).getProfile();
       final updatedProfile = currentProfile?.copyWith(
          interestIds: interestIds ?? [],
       ) ?? UserProfileModel(
          id: 'guest',
          interestIds: interestIds ?? [],
          lastPlayedDeckId: null,
          completedDeckIds: [],
       );
       
       ref.read(sessionServiceProvider).updateProfileLocal(updatedProfile);
       
       // Manually force refresh of userProfileProvider for guests? 
       // userProfileProvider depends on authProvider value which is null.
       // We need to update userProfileProvider to read from SessionService if user is null.
       ref.invalidate(userProfileProvider);
       return;
    }

    // AUTHENTICATED HANDLING
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      await ref.read(supabaseRepositoryProvider).updateProfile(
        userId: user.id,
        interestIds: interestIds,
      );
      // Invalidate profile provider to re-fetch
      ref.invalidate(userProfileProvider);
    });
  }

  Future<void> updateLastPlayedDeck(String deckId) async {
    final user = ref.read(authProvider).value;
    if (user == null) return;
    
    // Optimistic update or just wait? 
    // Wait is better to ensure "shine" happens on return with correct data.
    await ref.read(supabaseRepositoryProvider).updateLastPlayedDeck(user.id, deckId);
    ref.invalidate(userProfileProvider);
  }
}
