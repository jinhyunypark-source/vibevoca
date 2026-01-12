import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/services.dart';
import 'package:path_provider/path_provider.dart';
import 'package:sherpa_onnx/sherpa_onnx.dart' as sherpa;
import 'package:audioplayers/audioplayers.dart';
import 'package:archive/archive.dart';
import 'package:path/path.dart' as p;
import 'tts_interface.dart';

class SherpaTTSService implements TTSInterface {
  sherpa.OfflineTts? _tts;
  final AudioPlayer _player = AudioPlayer();
  bool _isInitialized = false;
  
  // Model Constants
  static const _modelDirName = 'vits-piper-en_US-amy-low';
  static const _modelAssetName = 'en_US-amy-low.onnx';
  static const _tokensAssetName = 'tokens.txt';
  static const _espeakZipName = 'espeak-ng-data.zip';

  @override
  Future<void> init() async {
    if (_isInitialized) return;

    // Initialize global bindings first (Required for new sherpa_onnx versions)
    sherpa.initBindings();

    final docDir = await getApplicationDocumentsDirectory();
    final baseDir = Directory('${docDir.path}/sherpa_models/$_modelDirName');

    if (!baseDir.existsSync()) {
      await baseDir.create(recursive: true);
    }
    
    final modelPath = '${baseDir.path}/$_modelAssetName';
    final tokensPath = '${baseDir.path}/$_tokensAssetName';
    final espeakDataDir = '${baseDir.path}/espeak-ng-data';
    final espeakZipPath = '${baseDir.path}/$_espeakZipName';

    // 1. Copy Model & Tokens
    await _copyAsset('assets/sherpa_models/$_modelDirName/$_modelAssetName', modelPath);
    await _copyAsset('assets/sherpa_models/$_modelDirName/$_tokensAssetName', tokensPath);
    
    // 2. Extract espeak-ng-data if needed
    if (!Directory(espeakDataDir).existsSync()) {
        try {
            print("📦 SherpaTTSService: Extracting espeak-ng-data...");
            await _copyAsset('assets/sherpa_models/$_modelDirName/$_espeakZipName', espeakZipPath);
            
            final bytes = File(espeakZipPath).readAsBytesSync();
            final archive = ZipDecoder().decodeBytes(bytes);
            
            for (final file in archive) {
              final filename = file.name;
              if (file.isFile) {
                final data = file.content as List<int>;
                File('${baseDir.path}/$filename')
                  ..createSync(recursive: true)
                  ..writeAsBytesSync(data);
              } else {
                Directory('${baseDir.path}/$filename').create(recursive: true);
              }
            }
            print("✅ SherpaTTSService: Extraction complete.");
        } catch(e) {
            print("❌ SherpaTTSService: Extraction failed: $e");
        }
    }

    final config = sherpa.OfflineTtsConfig(
      model: sherpa.OfflineTtsModelConfig(
        vits: sherpa.OfflineTtsVitsModelConfig(
          model: modelPath,
          tokens: tokensPath,
          dataDir: espeakDataDir,
        ),
        provider: 'cpu',
        numThreads: 1,
        debug: true,
      ),
      ruleFsts: '',
    );

    try {
      _tts = sherpa.OfflineTts(config);
      _isInitialized = true;
      // Set audio context for iOS/Android if needed via AudioPlayer, 
      // but usually AudioPlayer handles it.
      await _player.setAudioContext(AudioContext(
        iOS: AudioContextIOS(
           category: AVAudioSessionCategory.playback,
        ),
        android: AudioContextAndroid(
           usageType: AndroidUsageType.media,
           contentType: AndroidContentType.speech,
           audioFocus: AndroidAudioFocus.gain,
        ),
      ));
      
      print("🔊 SherpaTTSService: Engine Initialized");
    } catch (e) {
      print("❌ SherpaTTSService: Engine Init failed: $e");
    }
  }

  Future<void> _copyAsset(String assetPath, String targetPath) async {
    if (File(targetPath).existsSync()) return;
    try {
      final data = await rootBundle.load(assetPath);
      final bytes = data.buffer.asUint8List();
      await File(targetPath).writeAsBytes(bytes, flush: true);
    } catch (e) {
      print("❌ Failed to copy asset $assetPath: $e");
    }
  }

  @override
  Future<void> speak(String text) async {
    if (!_isInitialized || _tts == null) {
      await init();
    }
    
    // Filter logic update: 
    // If text contains Korean, strip the Korean parts (likely in parentheses) and speak the English part.
    String textToSpeak = text;
    if (RegExp(r'[가-힣]').hasMatch(text)) {
       // Remove content inside parentheses if it contains Korean, e.g. " (주책없이...)"
       textToSpeak = text.replaceAll(RegExp(r'\([^)]*[가-힣]+[^)]*\)'), '');
       // Remove any remaining Korean characters
       textToSpeak = textToSpeak.replaceAll(RegExp(r'[가-힣]'), '');
       textToSpeak = textToSpeak.trim();
    }

    if (textToSpeak.isEmpty) {
       print("🔇 SherpaTTSService: No speakable English text found.");
       return;
    }
    
    print("🔊 SherpaTTSService: Generating audio for '$textToSpeak'...");
    
    try {
      // 1. Generate Audio
      // API updated: text is likely a named parameter or signature changed.
      // Assuming named based on "0 allowed, but 1 found" error implies no positional args.
      final generated = _tts!.generate(text: textToSpeak, sid: 0, speed: 1.0);
      
      // 2. Save to WAV file
      // AudioPlayer plays files reliably. Sherpa generates raw PCM samples (Float32).
      // We need to convert Float32 samples to Int16 PCM for standard WAV, 
      // or check if sherpa provides wav writer.
      // Wait, sherpa_onnx dart package has `sherpa.writeWave`? 
      // Checking package docs... usually `sherpa_onnx` provides a helper or we write it manually.
      // The `OfflineTtsGeneratedAudio` has `save(String filename)`.
      
      final dir = await getTemporaryDirectory();
      final tempPath = '${dir.path}/tts_output.wav';
      
      // Manual WAV writing
      final success = await _writeWavFile(
         path: tempPath, 
         samples: generated.samples, 
         sampleRate: generated.sampleRate
      );
      
      if (success) {
         // 3. Play Audio
         await _player.play(DeviceFileSource(tempPath));
         print("🔊 SherpaTTSService: Playing...");
      } else {
         print("❌ SherpaTTSService: Failed to save WAV file.");
      }

    } catch (e) {
      print("❌ SherpaTTSService: Processing failed: $e");
    }
  }

  // Helper to write WAV file from Float32 samples
  Future<bool> _writeWavFile({
    required String path, 
    required Float32List samples, 
    required int sampleRate
  }) async {
    try {
      final file = File(path);
      final int numSamples = samples.length;
      final int numChannels = 1; 
      final int byteRate = sampleRate * numChannels * 2; // 16-bit
      final int blockAlign = numChannels * 2; 
      final int bitsPerSample = 16;
      
      final int dataSize = numSamples * 2;
      final int chunkSize = 36 + dataSize;
      
      final buffer = BytesBuilder();
      
      // RIFF chunk
      _writeString(buffer, 'RIFF');
      _writeInt32(buffer, chunkSize);
      _writeString(buffer, 'WAVE');
      
      // fmt chunk
      _writeString(buffer, 'fmt ');
      _writeInt32(buffer, 16); // Subchunk1Size (16 for PCM)
      _writeInt16(buffer, 1);  // AudioFormat (1 = PCM)
      _writeInt16(buffer, numChannels);
      _writeInt32(buffer, sampleRate);
      _writeInt32(buffer, byteRate);
      _writeInt16(buffer, blockAlign);
      _writeInt16(buffer, bitsPerSample);
      
      // data chunk
      _writeString(buffer, 'data');
      _writeInt32(buffer, dataSize);
      
      // Write samples (convert Float32 -1.0..1.0 to Int16)
      for (final sample in samples) {
        var value = (sample * 32767).toInt();
        if (value > 32767) value = 32767;
        if (value < -32768) value = -32768;
        _writeInt16(buffer, value);
      }
      
      await file.writeAsBytes(buffer.toBytes(), flush: true);
      return true;
    } catch(e) {
      print("❌ Error writing WAV: $e");
      return false;
    }
  }

  void _writeString(BytesBuilder buffer, String s) {
    buffer.add(s.codeUnits);
  }

  void _writeInt32(BytesBuilder buffer, int value) {
    buffer.addByte(value & 0xff);
    buffer.addByte((value >> 8) & 0xff);
    buffer.addByte((value >> 16) & 0xff);
    buffer.addByte((value >> 24) & 0xff);
  }

  void _writeInt16(BytesBuilder buffer, int value) {
    buffer.addByte(value & 0xff);
    buffer.addByte((value >> 8) & 0xff);
  }

  @override
  Future<void> stop() async {
    await _player.stop();
  }
}
