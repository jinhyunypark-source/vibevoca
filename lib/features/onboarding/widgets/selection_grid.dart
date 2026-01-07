import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../../core/theme/app_colors.dart';

class SelectionGrid<T> extends StatelessWidget {
  final List<T> items;
  final T? selectedItem;
  final String? Function(T) labelBuilder;
  final void Function(T) onSelect;
  final int crossAxisCount;

  const SelectionGrid({
    super.key,
    required this.items,
    this.selectedItem,
    required this.labelBuilder,
    required this.onSelect,
    this.crossAxisCount = 2,
  });

  @override
  Widget build(BuildContext context) {
    return GridView.builder(
      physics: const NeverScrollableScrollPhysics(),
      shrinkWrap: true,
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: crossAxisCount,
        mainAxisSpacing: 16,
        crossAxisSpacing: 16,
        childAspectRatio: 1.0,
      ),
      itemCount: items.length,
      itemBuilder: (context, index) {
        final item = items[index];
        final isSelected = selectedItem == item;
        return GestureDetector(
          onTap: () => onSelect(item),
          child: AnimatedContainer(
            duration: 200.ms,
            decoration: BoxDecoration(
              color: isSelected ? AppColors.primary : AppColors.surface,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(
                color: isSelected ? AppColors.accent : Colors.white10,
                width: isSelected ? 3 : 1,
              ),
              boxShadow: isSelected
                  ? [
                      BoxShadow(
                        color: AppColors.primary.withOpacity(0.5),
                        blurRadius: 15,
                        spreadRadius: 2,
                      )
                    ]
                  : [],
            ),
            child: Center(
              child: Text(
                labelBuilder(item) ?? '',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: isSelected ? Colors.white : Colors.white70,
                ),
                textAlign: TextAlign.center,
              ),
            ),
          ),
        ).animate().fadeIn(delay: (index * 100).ms).scale();
      },
    );
  }
}
