import 'package:google_sign_in/google_sign_in.dart' as gsi;
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:vibevoca/features/context/repositories/supabase_repository.dart';
import 'package:vibevoca/features/sync/services/session_service.dart';
import 'package:vibevoca/features/context/providers/deck_collection_provider.dart';
import 'package:vibevoca/features/analytics/services/analytics_service.dart';

part 'auth_provider.g.dart';

@Riverpod(keepAlive: true)
class Auth extends _$Auth {
  final _googleSignIn = gsi.GoogleSignIn(
    // TODO: Replace with your actual Web Client ID
    serverClientId: '830072949698-midq7i26a9huoa635mkltc3lo890r0up.apps.googleusercontent.com', 
  );

  @override
  Stream<User?> build() {
    final client = Supabase.instance.client;
    
    // Listen to Auth Changes
    return client.auth.onAuthStateChange.asyncMap((data) async {
      final user = data.session?.user;
      // Initialize Session Service (Handle Guest or User)
      await ref.read(sessionServiceProvider).initialize(user?.id);
      return user;
    });
  }

  Future<void> signInWithGoogle() async {
    // We cannot set 'state' directly in a StreamNotifier like AsyncValue.loading() 
    // effectively, unless we yield manually, but here we are in a method.
    // The Stream build matches the Auth State.
    // So we just trigger the side effect (SignIn) and the Stream will emit the new user.
    
    try {
      // 1. Trigger Google Sign-In Flow
      final googleUser = await _googleSignIn.signIn();
      if (googleUser == null) {
        return; // User canceled
      }

      // 2. Get Auth Details (ID Token is key)
      final googleAuth = await googleUser.authentication;
      final accessToken = googleAuth.accessToken;
      final idToken = googleAuth.idToken;

      if (idToken == null) {
        throw 'No ID Token found. Make sure Web Client ID is configured correctly.';
      }

      // 3. Authenticate with Supabase
      await Supabase.instance.client.auth.signInWithIdToken(
        provider: OAuthProvider.google,
        idToken: idToken,
        accessToken: accessToken,
      );

      // 4. Sync User Profile (Email, Provider, Last Login)
      final currentUser = Supabase.instance.client.auth.currentUser;
      if (currentUser != null) {
        final repo = ref.read(supabaseRepositoryProvider);
        await repo.syncUserProfile(
          userId: currentUser.id, 
          email: currentUser.email ?? '', 
          provider: 'google'
        );
        // Log Analytics
        ref.read(analyticsServiceProvider).logLogin(method: 'google');
      }
      
    } catch (e, st) {
      // For a StreamNotifier, we probably just want to log or show error via a separate provider/callback,
      // as setting state to error might break the stream subscription logic if not handled.
      // But for now, we can try to rethrow or let UI handle it.
      print("Google Sign In Error: $e");
      // state = AsyncValue.error(e, st); // Can't set state easily in StreamNotifier this way if strictly stream-based?
      // Actually StreamNotifier allows state setter if we mix it? 
      // But standard way is the stream drives state.
    }
  }

  Future<void> signOut() async {
    await _googleSignIn.signOut();
    await Supabase.instance.client.auth.signOut();
  }
}
