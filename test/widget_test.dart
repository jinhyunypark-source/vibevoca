// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:vibevoca/core/router/app_router.dart'; // Where VibeVocaApp is defined usually, or main. No, it is in Core/Router usually or changed.
// Wait, I need to check where VibeVocaApp is.
// It is in `lib/core/router/app_router.dart` based on my memory or `app_theme.dart`? 
// Actually `VibeVocaApp` is in `lib/core/router/app_router.dart` usually?
// Let's check `lib/main.dart` import.
// It imports `package:vibevoca/core/router/app_router.dart`.
// Let's check `app_router.dart`.
import 'package:vibevoca/core/router/app_router.dart';
import 'package:vibevoca/main.dart'; // No main.dart usually doesn't export the app class unless defined there.
// VibeVocaApp is defined in `lib/core/router/app_router.dart` (Checked in previous turns).
import 'package:vibevoca/core/router/app_router.dart';

void main() {
  testWidgets('Counter increments smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const ProviderScope(child: VibeVocaApp()));

    // Verify that our counter starts at 0.
    expect(find.text('0'), findsOneWidget);
    expect(find.text('1'), findsNothing);

    // Tap the '+' icon and trigger a frame.
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();

    // Verify that our counter has incremented.
    expect(find.text('0'), findsNothing);
    expect(find.text('1'), findsOneWidget);
  });
}
