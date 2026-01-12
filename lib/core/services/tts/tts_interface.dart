
abstract class TTSInterface {
  Future<void> init();
  Future<void> speak(String text);
  Future<void> stop();
}
