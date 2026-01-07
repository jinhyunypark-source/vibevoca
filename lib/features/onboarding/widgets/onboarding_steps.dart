import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../l10n/app_localizations.dart';
import 'package:gap/gap.dart';
import '../../../core/theme/app_colors.dart';
import '../providers/onboarding_provider.dart';
import 'selection_grid.dart';

class OnboardingSteps extends ConsumerStatefulWidget {
  const OnboardingSteps({super.key});

  @override
  ConsumerState<OnboardingSteps> createState() => _OnboardingStepsState();
}

class _OnboardingStepsState extends ConsumerState<OnboardingSteps> {
  int _currentStep = 0;
  String? _selectedRole;
  final List<String> _selectedInterests = [];

  void _nextStep() {
    setState(() {
      _currentStep++;
    });
  }

  void _submit() {
    if (_selectedRole == null) return;
    
    // Auto-generate a name for now since we removed text input
    // In a real app we might ask for nickname later or generate a cool handle
    final generatedName = "Player One"; 

    ref.read(onboardingControllerProvider.notifier).createPersona(
      name: generatedName,
      job: _selectedRole!,
      interests: _selectedInterests,
    );
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    
    // Role Options
    final roleOptions = [
      l10n.onboardingRoleMinor,
      l10n.onboardingRoleStudent,
      l10n.onboardingRoleWorker,
      l10n.onboardingRoleUnemployed,
    ];

    // Interest Options (Hardcoded for now, could be l10n strings too)
    final interestOptions = [
      "Travel", "Music", "Coding", "Sports", 
      "Art", "Business", "Gaming", "Food", 
      "Reading"
    ];

    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Step 1: Role Selection
          if (_currentStep == 0) ...[
            Text(
              l10n.onboardingQuestionRole,
              style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const Gap(40),
            SelectionGrid<String>(
              items: roleOptions,
              selectedItem: _selectedRole,
              labelBuilder: (item) => item,
              onSelect: (item) {
                setState(() {
                  _selectedRole = item;
                });
                Future.delayed(const Duration(milliseconds: 300), _nextStep);
              },
            ),
          ],

          // Step 2: Interest Selection
          if (_currentStep == 1) ...[
            Text(
              l10n.onboardingQuestionInterests,
              style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const Gap(40),
             Expanded(
               child: GridView.builder(
                 gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                   crossAxisCount: 3,
                   mainAxisSpacing: 10,
                   crossAxisSpacing: 10,
                   childAspectRatio: 1.0,
                 ),
                 itemCount: interestOptions.length,
                 itemBuilder: (context, index) {
                   final interest = interestOptions[index];
                   final isSelected = _selectedInterests.contains(interest);
                    return GestureDetector(
                      onTap: () {
                        setState(() {
                          if (isSelected) {
                            _selectedInterests.remove(interest);
                          } else {
                            _selectedInterests.add(interest);
                          }
                        });
                      },
                      child: AnimatedContainer(
                        duration: const Duration(milliseconds: 200),
                        decoration: BoxDecoration(
                          color: isSelected ? AppColors.primary : AppColors.surface,
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(
                            color: isSelected ? AppColors.accent : Colors.white10,
                            width: isSelected ? 2 : 1,
                          ),
                        ),
                        child: Center(
                          child: Text(
                            interest, 
                            style: TextStyle(
                              color: isSelected ? Colors.white : Colors.white70, 
                              fontWeight: FontWeight.bold
                            )
                          ),
                        ),
                      ),
                    );
                 },
               ),
             ),
             const Gap(20),
             ElevatedButton(
               onPressed: _selectedInterests.isNotEmpty ? _submit : null,
               style: ElevatedButton.styleFrom(
                 backgroundColor: AppColors.pass,
                 padding: const EdgeInsets.symmetric(vertical: 16),
                 shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
               ),
               child: Text(l10n.commonConfirm, style: const TextStyle(fontSize: 18, color: Colors.black, fontWeight: FontWeight.bold)),
             ),
          ],
        ],
      ),
    );
  }
}
