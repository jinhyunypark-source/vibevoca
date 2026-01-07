import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_colors.dart';
import '../providers/onboarding_provider.dart';

class OnboardingForm extends ConsumerStatefulWidget {
  const OnboardingForm({super.key});

  @override
  ConsumerState<OnboardingForm> createState() => _OnboardingFormState();
}

class _OnboardingFormState extends ConsumerState<OnboardingForm> {
  final _nameController = TextEditingController();
  final _jobController = TextEditingController();
  final List<String> _selectedInterests = [];
  
  final List<String> _availableInterests = [
    "Travel", "Music", "Coding", "Sports", "Art", "Business", "Gaming", "Food"
  ];

  void _submit() {
    if (_nameController.text.isEmpty || _jobController.text.isEmpty) return;
    
    ref.read(onboardingControllerProvider.notifier).createPersona(
      name: _nameController.text,
      job: _jobController.text,
      interests: _selectedInterests,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Text(
            "Who are you?",
            style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 40),
          TextField(
            controller: _nameController,
            decoration: InputDecoration(
              labelText: "Name",
              filled: true,
              fillColor: AppColors.surface,
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
            ),
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _jobController,
             decoration: InputDecoration(
              labelText: "Job / Role",
              filled: true,
              fillColor: AppColors.surface,
               border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
            ),
          ),
          const SizedBox(height: 24),
          const Text("Interests", style: TextStyle(fontSize: 18, color: Colors.grey)),
          const SizedBox(height: 12),
          Wrap(
            spacing: 8,
            children: _availableInterests.map((interest) {
              final isSelected = _selectedInterests.contains(interest);
              return FilterChip(
                label: Text(interest),
                selected: isSelected,
                selectedColor: AppColors.primary,
                checkmarkColor: Colors.white,
                labelStyle: TextStyle(
                  color: isSelected ? Colors.white : Colors.white70
                ),
                backgroundColor: AppColors.surface,
                onSelected: (selected) {
                  setState(() {
                    if (selected) {
                      _selectedInterests.add(interest);
                    } else {
                      _selectedInterests.remove(interest);
                    }
                  });
                },
              );
            }).toList(),
          ),
          const Spacer(),
          ElevatedButton(
            onPressed: _submit,
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primary,
              padding: const EdgeInsets.symmetric(vertical: 16),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            ),
            child: const Text("Create Persona", style: TextStyle(fontSize: 18, color: Colors.white, fontWeight: FontWeight.bold)),
          ),
          const SizedBox(height: 20),
        ],
      ),
    );
  }
}
