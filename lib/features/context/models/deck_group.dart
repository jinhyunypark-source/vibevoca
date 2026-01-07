import 'package:flutter/material.dart';

class DeckGroup {
  final String id;
  final String title; // English ID/Title
  final String titleKo; // Korean Title
  final Color color;
  final double progress;
  final String? icon;
  final int totalCards;

  const DeckGroup({
    required this.id,
    required this.title,
    required this.titleKo,
    required this.color,
    required this.progress,
    this.icon,
    this.totalCards = 0,
  });
}
