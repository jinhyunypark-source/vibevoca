import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'tts/sherpa_tts_service.dart';
import 'tts/tts_interface.dart';

part 'tts_service.g.dart';

// Expose the interface
@Riverpod(keepAlive: true)
TTSInterface ttsService(Ref ref) {
  return SherpaTTSService();
}
