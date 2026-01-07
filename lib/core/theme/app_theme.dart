import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'app_colors.dart';

class AppTheme {
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: AppColors.background,
      primaryColor: AppColors.primary,
      
      // Text Theme
      textTheme: GoogleFonts.outfitTextTheme(ThemeData.dark().textTheme).apply(
        bodyColor: AppColors.textPrimary,
        displayColor: AppColors.textPrimary,
      ),
      
      // Color Scheme
      colorScheme: const ColorScheme.dark(
        primary: AppColors.primary,
        secondary: AppColors.accent,
        surface: AppColors.surface,
        error: AppColors.fail,
        onSurface: AppColors.textPrimary,
      ),

      // Card Theme
      // cardTheme: CardTheme(
      //   color: AppColors.surface,
      //   elevation: 8,
      //   shape: RoundedRectangleBorder(
      //     borderRadius: BorderRadius.circular(20),
      //   ),
      // ),
      
      // AppBar Theme
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
      ),
    );
  }
}
