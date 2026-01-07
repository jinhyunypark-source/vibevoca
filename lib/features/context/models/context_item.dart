import 'package:flutter/material.dart';
import 'package:freezed_annotation/freezed_annotation.dart';

part 'context_item.freezed.dart';
part 'context_item.g.dart';

enum ContextType { place, emotion, environment }

@freezed
abstract class ContextItem with _$ContextItem {
  const factory ContextItem({
    required String id,
    required String slug,
    required ContextType type,
    required String label,
    required String iconAsset, // Or iconData codepoint
  }) = _ContextItem;

  factory ContextItem.fromJson(Map<String, dynamic> json) => _$ContextItemFromJson(json);
}
