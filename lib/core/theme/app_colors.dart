import 'package:flutter/material.dart';

class AppColors {
  // Brand Colors
  static const Color primary = Color(0xFF6C5CE7); // Deep Purple
  static const Color accent = Color(0xFFA29BFE); // Light Purple
  
  // Semantic Colors (PRD Specified)
  static const Color pass = Color(0xFF2ECC71); // Green
  static const Color fail = Color(0xFFE74C3C); // Red
  static const Color warning = Color(0xFFF1C40F); // Yellow/Gold
  
  // Background Colors
  static const Color background = Color(0xFF13111A); // Very Dark Purple/Black
  static const Color surface = Color(0xFF1E1B29); // Slightly lighter for cards
  static const Color surfaceHighlight = Color(0xFF2D2B3B);
  
  // Text Colors
  static const Color textPrimary = Color(0xFFFFFFFF);
  static const Color textSecondary = Color(0xFFB2BEC3);
  static const Color textTertiary = Color(0xFF636E72);

  // Gradients
  static const LinearGradient premiumGradient = LinearGradient(
    colors: [Color(0xFF6C5CE7), Color(0xFFA29BFE)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
  
  static const LinearGradient goldGradient = LinearGradient(
    colors: [Color(0xFFF1C40F), Color(0xFFF39C12)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
}
