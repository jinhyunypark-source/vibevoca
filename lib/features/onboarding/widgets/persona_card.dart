import 'package:flutter/material.dart';
import '../../../core/theme/app_colors.dart';
import '../../onboarding/models/persona.dart';
import 'package:flutter_animate/flutter_animate.dart';

class PersonaCard extends StatelessWidget {
  final Persona persona;
  final VoidCallback? onTap;

  const PersonaCard({super.key, required this.persona, this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 300,
        height: 480,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(24),
          gradient: const LinearGradient(
            colors: [Color(0xFF2C3A47), Color(0xFF13111A)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
          border: Border.all(color: AppColors.accent, width: 2),
          boxShadow: [
             BoxShadow(
              color: AppColors.primary.withOpacity(0.5),
              blurRadius: 20,
              spreadRadius: 2,
            )
          ],
        ),
        child: Stack(
          children: [
            // "Image" Placeholder Area
            Positioned(
              top: 20,
              left: 20,
              right: 20,
              height: 250,
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.black38,
                  borderRadius: BorderRadius.circular(16),
                  // image: const DecorationImage(
                  //   image: NetworkImage('https://placeholder.com/300x400'), 
                  //   fit: BoxFit.cover,
                  // ),
                ),
                child: const Center(
                  child: Icon(Icons.person, size: 80, color: Colors.white24),
                ),
              ),
            ),
            
            // Text Content
            Positioned(
              bottom: 40,
              left: 20,
              right: 20,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    persona.title.toUpperCase(),
                    style: const TextStyle(
                      fontFamily: 'Cinzel', // Or similar "fantasy" font if available, fallback to default
                      color: AppColors.warning,
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.2,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 12),
                  Text(
                    persona.name,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    "${persona.job} • ${persona.interests.join(', ')}",
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.7),
                      fontSize: 14,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
            
             // Rarity Gem (Decorative)
             Positioned(
               top: 260, // Overlapping image bottom
               left: 0, 
               right: 0,
               child: Center(
                 child: Container(
                   width: 30,
                   height: 30,
                   decoration: BoxDecoration(
                     color: AppColors.primary,
                     shape: BoxShape.circle,
                     border: Border.all(color: Colors.white, width: 2),
                     boxShadow: [
                       BoxShadow(color: AppColors.primary.withOpacity(0.8), blurRadius: 10)
                     ],
                   ),
                 ),
               ),
             )
          ],
        ),
      ).animate().fadeIn().scale(duration: 600.ms, curve: Curves.easeOutBack),
    );
  }
}
