import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/widgets.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:path_provider/path_provider.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../auth/providers/auth_provider.dart';
import '../models/deck_state_model.dart';
import '../../profile/models/user_profile_model.dart';
import '../../context/providers/deck_collection_provider.dart'; // For supabaseRepositoryProvider

final sessionServiceProvider = Provider.autoDispose<SessionService>((ref) {
  final link = ref.keepAlive();
  final service = SessionService(Supabase.instance.client, ref);
  // Initialize immediately (will load guest or previous session)
  // But AuthProvider listener will re-init on change.
  // Actually, we should probably lazy load or let AuthProvider handle it?
  // Let's safe-guard by letting it be ready to handle calls.
  return service;
  ref.onDispose(() {
    service.dispose();
  });
  return service;
});

class SessionService with WidgetsBindingObserver {
  final SupabaseClient _client;
  final Ref _ref;
  
  String get _currentUserId {
    return _ref.read(authProvider).value?.id ?? kGuestUserId;
  }
  
  // Constants
  static const String kGuestUserId = 'guest_local_user';
  
  // State
  Map<String, DeckState> _deckCache = {};
  UserProfileModel? _profileCache;
  // List<String> _selectedContextIds = []; // TODO: Implement Context Sync

  Timer? _autoSaveTimer;

  SessionService(this._client, this._ref) {
    _autoSaveTimer = Timer.periodic(const Duration(minutes: 5), (timer) {
      saveToDisk();
      debugPrint("SessionService: Auto-saving to disk (Timer)");
    });
    WidgetsBinding.instance.addObserver(this);
  }

  void dispose() {
    _autoSaveTimer?.cancel();
    WidgetsBinding.instance.removeObserver(this);
    saveToDisk();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.paused) {
      debugPrint("SessionService: App Paused -> Saving to disk...");
      saveToDisk();
    }
  }

  Future<File> get _localFile async {
    final directory = await getApplicationDocumentsDirectory();
    return File('${directory.path}/user_session_v1.json');
  }

  // --- Initialization ---

  Future<void> initialize([String? userId]) async {
    final targetId = userId ?? _currentUserId;
    try {
      final file = await _localFile;
      if (await file.exists()) {
        final content = await file.readAsString();
        final Map<String, dynamic> json = jsonDecode(content);
        
        // 1. Verify User (if userId changed, maybe reset? For now assume session matches file or overwrite)
         // Actually we should check if json['userId'] == userId if we store it.
        
        // 2. Load Progress
        if (json['progress'] != null) {
          final List<dynamic> progressList = json['progress'];
          _deckCache.clear();
          for (var item in progressList) {
             final d = DeckState.fromJson(item);
             // Allow loading if it matches targetId OR if it's data we want to keep?
             // For now, strict match to avoid mixing users if multiple people use device.
             // But if we want to migrate Guest -> User, we might need logic here.
             // Simplest: Load if matches.
             if (d.userId == targetId) {
                _deckCache[d.deckId] = d;
             }
             // Migration Hack: If we are a real user, but found guest data?
             // Maybe we should allow merge later. For now, strict match.
          }
        }
        
        // 3. Load Profile
        if (json['profile'] != null) {
          try {
             _profileCache = UserProfileModel.fromJson(json['profile']);
          } catch(e) {
             debugPrint("SessionService: Failed to parse cached profile: $e");
          }
        }

        debugPrint("SessionService: Session loaded (Decks: ${_deckCache.length}, Profile: ${_profileCache != null})");
      } else {
        debugPrint("SessionService: No local session found.");
      }
    } catch (e) {
      debugPrint("SessionService: Error loading session: $e");
    }
  }
  
  // --- Profile Management ---
  
  UserProfileModel? getProfile() => _profileCache;
  
  void updateProfileLocal(UserProfileModel profile) {
    _profileCache = profile;
    saveToDisk(); // Immediate save optional, but good for safety
  }

  // --- Progress Management (Logic from ProgressSyncService) ---

  DeckState? getDeckState(String deckId) => _deckCache[deckId];

  void updateCardProgress(String deckId, String cardId, String status, {bool incrementRemind = false, int? forceRemindCount}) {
     final userId = _currentUserId;
     // if (userId == null) return; // Removed null check for guest support

     var deck = _deckCache[deckId];
     if (deck == null) {
       deck = DeckState(deckId: deckId, userId: userId, cardStates: [], isDirty: true);
     }

     final List<CardState> newCards = List.from(deck.cardStates);
     final idx = newCards.indexWhere((c) => c.id == cardId);
     
     if (idx != -1) {
       final old = newCards[idx];
       int newRemind = old.remindCount;
       if (forceRemindCount != null) {
          newRemind = forceRemindCount;
       } else if (incrementRemind) {
          newRemind = old.remindCount + 1;
       }
       
       newCards[idx] = old.copyWith(
         status: status,
         remindCount: newRemind,
       );
     } else {
       newCards.add(CardState(id: cardId, status: status, remindCount: forceRemindCount ?? (incrementRemind ? 1 : 0)));
     }

     final memorized = newCards.where((c) => c.status == 'memorized').length;
     final reminded = newCards.fold(0, (sum, c) => sum + c.remindCount);

     _deckCache[deckId] = deck.copyWith(
       cardStates: newCards,
       memorizedCount: memorized,
       remindCount: reminded,
       totalCount: newCards.length,
       isDirty: true,
       lastChangedAt: DateTime.now(),
     );
  }
  
  void updateLastViewedCard(String deckId, String cardId) {
     final userId = _currentUserId;
     // if (userId == null) return;

     var deck = _deckCache[deckId];
     if (deck == null) {
       deck = DeckState(deckId: deckId, userId: userId, cardStates: [], isDirty: true, lastViewedCardId: cardId);
     }

     _deckCache[deckId] = deck.copyWith(
       lastViewedCardId: cardId,
       isDirty: true,
       lastChangedAt: DateTime.now(),
     );
  }
  
  Future<void> resetDeckProgress(String deckId) async {
     final userId = _currentUserId;
     // if (userId == null) return;

     final deck = _deckCache[deckId];
     if (deck == null) return;

     final newCards = deck.cardStates.map((c) => c.copyWith(status: 'new')).toList();

     _deckCache[deckId] = deck.copyWith(
       cardStates: newCards,
       memorizedCount: 0,
       lastChangedAt: DateTime.now(),
       isDirty: true,
     );
     
     await saveToDisk();
  }

  // --- Persistence & Backup ---

  Future<void> saveToDisk() async {
     try {
       final file = await _localFile;
       
       final data = {
         'progress': _deckCache.values.map((d) => d.toJson()).toList(),
         'profile': _profileCache?.toJson(),
         'updated_at': DateTime.now().toIso8601String(),
       };
       
       await file.writeAsString(jsonEncode(data));
       debugPrint("SessionService: Saved to local disk.");
     } catch (e) {
       debugPrint("SessionService: Failed to save to disk: $e");
     }
  }

  Future<void> backupToCloud() async {
     final userId = _ref.read(authProvider).value?.id;
     if (userId == null) throw Exception("User not logged in");

     await saveToDisk();

     final data = {
       'progress': _deckCache.values.map((d) => d.toJson()).toList(),
       'profile': _profileCache?.toJson(),
       'last_backup_at': DateTime.now().toIso8601String(),
     };

     debugPrint("SessionService: Backing up session to Cloud...");
     try {
       await _client.from('user_backups').upsert({
         'user_id': userId,
         'backup_data': data,
         'updated_at': DateTime.now().toIso8601String(),
       }, onConflict: 'user_id');
       debugPrint("SessionService: Backup successful.");
     } catch (e) {
       debugPrint("SessionService: Backup failed: $e");
       rethrow; 
     }
  }

  Future<void> restoreFromCloud() async {
    final userId = _ref.read(authProvider).value?.id;
    if (userId == null) throw Exception("User not logged in");

    debugPrint("SessionService: Restoring from Cloud...");

    try {
      final response = await _client
          .from('user_backups')
          .select()
          .eq('user_id', userId)
          .maybeSingle(); 
      
      if (response == null) throw Exception("No backup found.");
      
      final Map<String, dynamic> backupData = response['backup_data'];
      
      // Restore Progress
      if (backupData['progress'] != null) {
        _deckCache.clear();
        for (var item in (backupData['progress'] as List)) {
           final d = DeckState.fromJson(item);
           _deckCache[d.deckId] = d;
        }
      }
      
      // Restore Profile
      if (backupData['profile'] != null) {
         _profileCache = UserProfileModel.fromJson(backupData['profile']);
      }
      
      await saveToDisk();
      debugPrint("SessionService: Restored session.");
    } catch (e) {
      debugPrint("SessionService: Restore failed: $e");
      rethrow;
    }
  }

  Future<void> clearLocalData() async {
    _deckCache.clear();
    _profileCache = null;
    final file = await _localFile;
    if (await file.exists()) {
      await file.delete();
    }
    debugPrint("SessionService: Local data cleared.");
  }

  Future<void> resetAllData() async {
     final userId = _currentUserId;
     // if (userId == null) return;
     
     // 1. Reset Cloud Data via Repository
     // (Lazy read to avoid circular dependency if any, though Repo is independent)
     final repo = _ref.read(supabaseRepositoryProvider);
     await repo.resetProfile(userId);
     
     // 2. Clear Local Data
     await clearLocalData();
  }
  // --- Review Mode Support ---

  List<({String deckId, String cardId, int failCount})> getAllReviewCandidates() {
     final candidates = <({String deckId, String cardId, int failCount})>[];
     
     for (var deck in _deckCache.values) {
        for (var card in deck.cardStates) {
           // Include if Remind Count > 0 
           // (Status might be 'review' or even 'new' if count set? Usually 'review')
           if (card.remindCount > 0) {
              candidates.add((deckId: deck.deckId, cardId: card.id, failCount: card.remindCount));
           }
        }
     }
     
     // Sort by Fail Count DESC (Highest priority first)
     candidates.sort((a,b) => b.failCount.compareTo(a.failCount));
     return candidates;
  }
}
