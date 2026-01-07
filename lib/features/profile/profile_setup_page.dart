import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:gap/gap.dart';
import 'package:go_router/go_router.dart';
import 'package:vibevoca/core/theme/app_colors.dart';
import 'package:vibevoca/features/profile/providers/profile_provider.dart';
import 'package:vibevoca/features/profile/models/job_interest_model.dart';

class ProfileSetupPage extends ConsumerStatefulWidget {
  const ProfileSetupPage({super.key});

  @override
  ConsumerState<ProfileSetupPage> createState() => _ProfileSetupPageState();
}

class _ProfileSetupPageState extends ConsumerState<ProfileSetupPage> {
  final List<String> _selectedInterestIds = [];
  bool _isInitialized = false;

  @override
  void initState() {
    super.initState();
  }

  void _onSave(List<InterestModel> allOptions) async {
    // Validation: Check if at least one 'job' category item is selected
    final jobOptions = allOptions.where((e) => e.category == 'job').map((e) => e.id).toSet();
    final hasJob = _selectedInterestIds.any((id) => jobOptions.contains(id));

    if (!hasJob) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select your occupation')),
      );
      return;
    }
    
    await ref.read(profileControllerProvider.notifier).saveProfile(
      interestIds: _selectedInterestIds,
    );
    
    if (mounted) {
       if (context.canPop()) context.pop();
       else context.go('/context-selection'); 
    }
  }

  @override
  Widget build(BuildContext context) {
    // Only fetch interestsProvider (unified)
    final allOptionsAsync = ref.watch(interestsProvider);
    final userProfileAsync = ref.watch(userProfileProvider);
    final isSaving = ref.watch(profileControllerProvider).isLoading;

    // Load initial data once when available
    if (!_isInitialized && userProfileAsync.value != null) {
      // Use microtask to avoid calling setState during build
      Future.microtask(() {
        if (mounted && !_isInitialized) {
          setState(() {
            _selectedInterestIds.addAll(userProfileAsync.value!.interestIds);
            _isInitialized = true;
          });
        }
      });
    }

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        title: const Text("Your Profile"),
        leading: IconButton( 
            icon: const Icon(Icons.close),
             onPressed: () {
               if (context.canPop()) context.pop();
               else context.go('/context-selection'); 
             },
        ),
      ),
      body: SafeArea(
        child: allOptionsAsync.when(
          data: (allOptions) {
            final jobs = allOptions.where((e) => e.category == 'job').toList();
            final interests = allOptions.where((e) => e.category == 'hobby').toList();

            return Column(
              children: [
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 24),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Gap(24),
                        const Text(
                          "맞춤형 예문을 위해\n당신에 대해 조금더 알려주세요.",
                          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white, height: 1.3),
                        ).animate().fadeIn().moveY(begin: 10, end: 0),
                        
                        const Gap(8),
                        const Text(
                          "Tell us about yourself",
                          style: TextStyle(fontSize: 14, color: Colors.white70),
                        ).animate().fadeIn(delay: 100.ms),
                        
                        const Gap(24),
      
                        // 1. Job Selection (Auto-sized, usually small)
                        const Text("Occupation", style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold)),
                        const Gap(12),
                        _buildGrid(
                          items: jobs, 
                          isMultiSelect: false,
                          selectedIds: _selectedInterestIds,
                          onSelect: (id, selected) {
                            setState(() {
                               _selectedInterestIds.removeWhere((pid) => jobs.any((j) => j.id == pid));
                               if (selected) _selectedInterestIds.add(id);
                             });
                          }
                        ),
      
                        const Gap(24),
      
                        // 2. Interest Selection (Expanded & Scrollable)
                        const Text("Interests", style: TextStyle(color: AppColors.accent, fontWeight: FontWeight.bold)),
                        const Gap(12),
                        Expanded(
                          child: _buildScrollableGrid(
                            items: interests, 
                            isMultiSelect: true,
                            selectedIds: _selectedInterestIds,
                            onSelect: (id, selected) {
                               setState(() {
                                 if (selected) _selectedInterestIds.add(id);
                                 else _selectedInterestIds.remove(id);
                               });
                            }
                          ),
                        ),
                      ],
                    ),
                  ),
                ),

                // Save Button (Fixed at bottom)
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(24),
                  decoration: const BoxDecoration(
                    color: AppColors.background,
                    boxShadow: [
                      BoxShadow(color: Colors.black26, blurRadius: 10, offset: Offset(0, -5))
                    ]
                  ),
                  child: ElevatedButton(
                    onPressed: isSaving ? null : () => _onSave(allOptions),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                    child: isSaving 
                      ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2))
                      : const Text("저장하고 계속", style: TextStyle(color: Colors.black, fontSize: 16, fontWeight: FontWeight.bold)),
                  ),
                ).animate().fadeIn(delay: 300.ms).moveY(begin: 20, end: 0),
              ],
            );
          },
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (err, _) => Center(child: Text('Error: $err', style: const TextStyle(color: Colors.red))),
        ),
      ),
    );
  }

  Widget _buildScrollableGrid({
    required List<InterestModel> items,
    required bool isMultiSelect,
    required List<String> selectedIds,
    required Function(String, bool) onSelect,
  }) {
    final activeColor = isMultiSelect ? AppColors.accent : AppColors.primary;

    return GridView.builder(
      physics: const BouncingScrollPhysics(), // Allow scrolling
      padding: const EdgeInsets.only(bottom: 20),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 3,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
        childAspectRatio: 1.1, 
      ),
      itemCount: items.length,
      itemBuilder: (context, index) {
        final item = items[index];
        final isSelected = selectedIds.contains(item.id);

        return GestureDetector(
          onTap: () => onSelect(item.id, !isSelected),
          child: AnimatedContainer(
            duration: 200.ms,
            decoration: BoxDecoration(
              color: isSelected ? activeColor : AppColors.surface,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: isSelected ? activeColor : Colors.white10,
                width: 2,
              ),
            ),
            padding: const EdgeInsets.all(8),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  _getIconData(item.icon),
                  color: isSelected ? Colors.black : Colors.white70,
                  size: 28,
                ),
                const Gap(8),
                Text(
                  item.labelKo,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: isSelected ? Colors.black : Colors.white,
                    fontSize: 12,
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildGrid({
    required List<InterestModel> items,
    required bool isMultiSelect,
    required List<String> selectedIds,
    required Function(String, bool) onSelect,
  }) {
    // Determine color based on type
    final activeColor = isMultiSelect ? AppColors.accent : AppColors.primary;

    return GridView.builder(
      physics: const NeverScrollableScrollPhysics(),
      shrinkWrap: true,
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 3,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
        childAspectRatio: 1.1, // Adjust for card shape
      ),
      itemCount: items.length,
      itemBuilder: (context, index) {
        final item = items[index];
        final isSelected = selectedIds.contains(item.id);

        return GestureDetector(
          onTap: () => onSelect(item.id, !isSelected), // Toggle for multi, Select for single (handled by parent)
          child: AnimatedContainer(
            duration: 200.ms,
            decoration: BoxDecoration(
              color: isSelected ? activeColor : AppColors.surface,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: isSelected ? activeColor : Colors.white10,
                width: 2,
              ),
            ),
            padding: const EdgeInsets.all(8),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  _getIconData(item.icon),
                  color: isSelected ? Colors.black : Colors.white70,
                  size: 28,
                ),
                const Gap(8),
                Text(
                  item.labelKo, // Use Korean label
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: isSelected ? Colors.black : Colors.white,
                    fontSize: 12,
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  IconData _getIconData(String? iconName) {
    if (iconName == null) return Icons.help_outline;
    switch (iconName) {
      case 'school': return Icons.school;
      case 'code': return Icons.code;
      case 'brush': return Icons.brush;
      case 'business_center': return Icons.business_center;
      case 'laptop_mac': return Icons.laptop_mac;
      case 'person': return Icons.person;
      case 'flight': return Icons.flight;
      case 'trending_up': return Icons.trending_up;
      case 'memory': return Icons.memory;
      case 'palette': return Icons.palette;
      case 'theater_comedy': return Icons.theater_comedy;
      case 'restaurant': return Icons.restaurant;
      case 'local_cafe': return Icons.local_cafe;
      case 'import_contacts': return Icons.import_contacts;
      default: return Icons.category;
    }
  }
}
