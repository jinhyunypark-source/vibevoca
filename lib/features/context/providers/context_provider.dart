import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../profile/models/job_interest_model.dart';
import '../models/context_item.dart';
import 'deck_collection_provider.dart'; // for repo provider
import '../repositories/supabase_repository.dart';

part 'context_provider.g.dart';
// ... (imports)

@riverpod
Future<List<ContextItem>> allContextOptions(Ref ref) async {
  final repo = ref.watch(supabaseRepositoryProvider);
  final interests = await repo.getInterests(category: 'vibe');
  
  return interests.map((i) {
    // Determine type from tags
    ContextType type = ContextType.place; // Default
    if (i.tags.contains('emotion')) type = ContextType.emotion;
    if (i.tags.contains('environment')) type = ContextType.environment;

    return ContextItem(
      id: i.id, 
      slug: i.code, // Map code -> slug
      type: type, 
      label: i.labelEn, // Or labelKo depending on locale
      iconAsset: i.icon ?? 'help_outline'
    );
  }).toList();
}

// State to track selected items (Multi-select, max 3)
@Riverpod(keepAlive: true)
class SelectedContext extends _$SelectedContext {
  @override
  List<ContextItem> build() {
    return [];
  }

  void toggle(ContextItem item) {
    if (state.contains(item)) {
       state = state.where((i) => i.id != item.id).toList();
    } else {
       if (state.length < 3) {
         state = [...state, item];
       }
    }
  }

  bool get isComplete => state.isNotEmpty;
}
