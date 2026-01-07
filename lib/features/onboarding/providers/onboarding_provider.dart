import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:uuid/uuid.dart';
import '../models/persona.dart';

part 'onboarding_provider.g.dart';

@riverpod
class OnboardingController extends _$OnboardingController {
  @override
  FutureOr<Persona?> build() {
    return null;
  }

  Future<void> createPersona({
    required String name,
    required String job,
    required List<String> interests,
  }) async {
    state = const AsyncValue.loading();

    // Mock AI Generation delay
    await Future.delayed(const Duration(seconds: 2));

    // Mock AI Logic: Generate a cool title based on inputs
    String title = "The Novice Adventurer";
    if (interests.contains("Sports")) {
      title = "The Energetic Striker";
    } else if (interests.contains("Reading")) {
      title = "The Wise Scholar";
    } else if (job.toLowerCase().contains("developer")) {
      title = "The Code Weaver";
    }

    final newPersona = Persona(
      id: const Uuid().v4(),
      name: name,
      job: job,
      interests: interests,
      title: title,
    );

    state = AsyncValue.data(newPersona);
  }
}
