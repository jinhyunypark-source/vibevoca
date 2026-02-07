import 'dart:io';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../../core/services/tts_service.dart';
import '../../../core/utils/material_icons_mapper.dart';
import '../../../core/theme/app_colors.dart';
import '../models/word_card_model.dart';
import 'generative_card_background.dart';
import '../../context/providers/image_pack_provider.dart';

class FlashCard extends ConsumerStatefulWidget {
  final WordCardModel card;
  final String? deckIcon;
  final void Function(DismissDirection)? onSwipe;
  const FlashCard({super.key, required this.card, this.deckIcon, this.onSwipe});

  @override
  ConsumerState<FlashCard> createState() => _FlashCardState();
}

class _FlashCardState extends ConsumerState<FlashCard> with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _animation;
  bool _isFlipped = false;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: 400.ms);
    _animation = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOutBack),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _flip() {
    if (_isFlipped) {
      _controller.reverse();
    } else {
      _controller.forward();
    }
    _isFlipped = !_isFlipped;
  }
  
  void _speak(String text) {
    if (text.isNotEmpty) {
      ref.read(ttsServiceProvider).speak(text);
    }
  }

  /// 번들 데모 이미지 경로 (assets/word_images_demo/)
  String _getWordImagePath() {
    return 'assets/word_images_demo/${widget.card.id}.jpg';
  }

  /// 이미지 소스 해결 결과
  /// [type]: 'file' (로컬 캐시), 'asset' (번들), 'none' (없음)
  /// [path]: 이미지 경로 (type이 'none'이면 null)
  Future<({String type, String? path})> _resolveImageSource() async {
    final cardId = widget.card.id;

    // 1. 로컬 캐시 확인 (다운로드된 이미지)
    final imagePackService = ref.read(imagePackServiceProvider);
    final localPath = await imagePackService.getLocalImagePath(cardId);
    if (localPath != null) {
      return (type: 'file', path: localPath);
    }

    // 2. 번들 에셋 확인 (데모 카테고리)
    final demoPath = _getWordImagePath();
    final hasBundledAsset = await imagePackService.checkBundledAssetExists(demoPath);
    if (hasBundledAsset) {
      return (type: 'asset', path: demoPath);
    }

    // 3. 이미지 없음
    return (type: 'none', path: null);
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _flip,
      child: AnimatedBuilder(
        animation: _animation,
        builder: (context, child) {
          final angle = _animation.value * pi;
          final isBackVisible = angle >= pi / 2;
          
          final transform = Matrix4.identity()
            ..setEntry(3, 2, 0.001) // Perspective
            ..rotateY(angle);

          return Transform(
            transform: transform,
            alignment: Alignment.center,
            child: isBackVisible 
              ? Transform(
                  alignment: Alignment.center,
                  transform: Matrix4.identity()..rotateY(pi), // Flip back to be readable
                  child: _buildBack(),
                ) 
              : _buildFront(),
          );
        },
      ),
    );
  }

  double _overscrollAccumulator = 0.0;
  double _dragDistance = 0.0;

  Widget _buildWatermarkIcon() {
    final iconKey = widget.deckIcon;
    if (iconKey != null && iconKey.startsWith('assets/')) {
       return Image.asset(iconKey, width: 200, height: 200, fit: BoxFit.contain);
    }
    // Fallback Icons
    IconData iconData = Icons.style; // Default deck icon
    if (iconKey == 'fluency_delivery') iconData = Icons.record_voice_over;
    if (iconKey == 'emotion_depth') iconData = Icons.sentiment_satisfied_alt;
    
    return Icon(iconData, size: 200, color: Colors.white);
  }

  Widget _buildZonedPage({
    required Widget topContent,
    required Widget middleContent, // This will be scrollable
    required Widget bottomContent,
  }) {
    return Column(
      children: [
        // Top Zone (Swipe Down Region) - 20% height
        Expanded(
          flex: 2, 
          child: Container(
             color: Colors.transparent, 
             width: double.infinity,
             padding: const EdgeInsets.only(top: 16),
             alignment: Alignment.topCenter,
             child: FittedBox(
               fit: BoxFit.scaleDown,
               child: topContent,
             ),
          ),
        ),
        
        // Middle Zone (Scroll Region) - 60% height
        Expanded(
          flex: 6,
          child: NotificationListener<OverscrollNotification>(
            onNotification: (notification) {
               if (notification.metrics.axis != Axis.vertical) return false;
               _overscrollAccumulator += notification.overscroll;
               const double threshold = 50.0;
               if (_overscrollAccumulator < -threshold) {
                  _overscrollAccumulator = 0; widget.onSwipe?.call(DismissDirection.down);
               } else if (_overscrollAccumulator > threshold) {
                  _overscrollAccumulator = 0; widget.onSwipe?.call(DismissDirection.up);
               }
               return false;
            },
            child: NotificationListener<ScrollEndNotification>(
              onNotification: (_) { _overscrollAccumulator = 0; return false; },
              child: SingleChildScrollView(
                physics: const BouncingScrollPhysics(),
                child: middleContent,
              ),
            ),
          ),
        ),
        
        // Bottom Zone (Swipe Up Region) - 20% height
        Expanded(
          flex: 2,
          child: Container(
            color: Colors.transparent,
            width: double.infinity,
            padding: const EdgeInsets.only(bottom: 16),
            alignment: Alignment.bottomCenter,
            child: FittedBox(
              fit: BoxFit.scaleDown,
              child: bottomContent,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildFront() {
    final imagePath = _getWordImagePath();

    return Container(
      decoration: BoxDecoration(
        color: Colors.white, // White Theme: Background
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: Colors.transparent, width: 0), // White Theme: Seamless Border
        boxShadow: const [BoxShadow(color: Colors.black12, blurRadius: 10, offset: Offset(0, 4))],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(22),
        child: Stack(
          children: [
            // Main Column Layout
            Column(
              children: [
                // 1. Top Section: Word & Speaker
                Expanded(
                  flex: 3,
                  child: Container(
                    alignment: Alignment.center,
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Flexible(
                          child: FittedBox(
                            fit: BoxFit.scaleDown,
                            child: Text(
                              widget.card.word,
                              textAlign: TextAlign.center,
                              style: const TextStyle(
                                fontSize: 42,
                                fontWeight: FontWeight.bold,
                                color: Colors.black87, // White Theme: Dark Text
                                letterSpacing: 1.0,
                                shadows: []
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        GestureDetector(
                          onTap: () => _speak(widget.card.word),
                          child: Container(
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.1), 
                              shape: BoxShape.circle
                            ),
                            child: const Icon(Icons.volume_up_rounded, color: AppColors.primary, size: 28), // White Theme: Primary Color Icon
                          ),
                        )
                      ],
                    ),
                  ),
                ),

                // 2. Middle Section: Framed Image
                Expanded(
                  flex: 5,
                  child: Center(
                    child: Container(
                      width: 280,
                      height: 280,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(24),
                        border: Border.all(color: Colors.white, width: 4), // White Theme: White Frame (Seamless)
                        boxShadow: [
                          BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 15, offset: const Offset(0, 8))
                        ],
                      ),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(20),
                        child: FutureBuilder<({String type, String? path})>(
                          future: _resolveImageSource(),
                          builder: (context, snapshot) {
                            if (!snapshot.hasData) {
                              // Loading state
                              return const Center(child: CircularProgressIndicator());
                            }

                            final source = snapshot.data!;
                            switch (source.type) {
                              case 'file':
                                // 로컬 캐시 이미지 (다운로드됨)
                                return Image.file(File(source.path!), fit: BoxFit.contain);
                              case 'asset':
                                // 번들 에셋 이미지 (데모 카테고리)
                                return Image.asset(source.path!, fit: BoxFit.contain);
                              default:
                                // 이미지 없음 - GenerativeCardBackground
                                return GenerativeCardBackground(word: widget.card.word, baseColor: AppColors.primary);
                            }
                          },
                        ),
                      ),
                    ),
                  ),
                ),

                // 3. Bottom Section: Interaction Hints
                Expanded(
                  flex: 3,
                  child: Container(
                    padding: const EdgeInsets.only(bottom: 20),
                    alignment: Alignment.bottomCenter,
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text("탭 해서 뜻보기", style: TextStyle(fontSize: 15, color: Colors.grey[600], fontWeight: FontWeight.w500)), // White Theme: Darker Hint
                        const SizedBox(height: 16),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.keyboard_arrow_up, color: AppColors.fail, size: 32),
                            const SizedBox(width: 8),
                            Text("암기장", style: TextStyle(color: AppColors.fail, fontSize: 22, fontWeight: FontWeight.bold)),
                            const SizedBox(width: 40),
                            Text("암기완료", style: TextStyle(color: AppColors.pass, fontSize: 22, fontWeight: FontWeight.bold)),
                            const SizedBox(width: 8),
                            Icon(Icons.keyboard_arrow_down, color: AppColors.pass, size: 32),
                          ],
                        ),
                        const SizedBox(height: 20),
                      ],
                    ),
                  ),
                ),
              ],
            ),

            // Fail Count Badge (Overlay)
            if (widget.card.failCount > 0)
              Positioned(
                top: 20, right: 20,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: AppColors.fail, 
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 4, offset: Offset(0, 2))]
                  ),
                  child: Text("+${widget.card.failCount}", style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
                ),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildBack() {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.surfaceHighlight,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: AppColors.primary, width: 2),
        boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 10, offset: Offset(0, 4))],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(22),
        child: Stack(
          children: [
            Positioned(
                left: -30, top: -30,
                child: Icon(Icons.translate, size: 150, color: Colors.white.withOpacity(0.03)),
            ),
            
            Positioned.fill(
              child: _buildZonedPage(
                topContent: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Flexible(
                        child: Text(
                          widget.card.word,
                          style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AppColors.accent),
                          textAlign: TextAlign.center,
                        ),
                      ),
                      const SizedBox(width: 8),
                      GestureDetector(
                        onTap: () => _speak(widget.card.word),
                        child: const Icon(Icons.volume_up_rounded, color: AppColors.accent, size: 20),
                      ),
                    ],
                  ),
                ),
                middleContent: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24.0),
                  child: Column(
                    children: [
                      const SizedBox(height: 10),
                      Text(
                        widget.card.meaning,
                        style: const TextStyle(fontSize: 20, color: Colors.white),
                        textAlign: TextAlign.center,
                      ),
                      const Divider(color: Colors.white24, height: 40),
                      
                      // Sentence Logic: Prioritize Vibe Sentences. If empty, fallback to exampleSentence.
                      if (widget.card.vibeSentences.isNotEmpty) ...[
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                            decoration: BoxDecoration(color: AppColors.primary.withOpacity(0.2), borderRadius: BorderRadius.circular(6)),
                            child: const Text("Vibe Context", style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 12)),
                          ),
                          const SizedBox(height: 12),
                          ...widget.card.vibeSentences.map((info) => _buildSentenceWithSpeaker(info.sentence, iconName: info.icon)),
                      ] else ...[
                          _buildSentenceWithSpeaker(widget.card.exampleSentence),
                      ],
                       const SizedBox(height: 20),
                    ],
                  ),
                ),
                bottomContent: Padding(
                  padding: const EdgeInsets.only(bottom: 20.0),
                  child: Text(
                     "탭 해서 뒤집기",
                     style: TextStyle(fontSize: 16, color: Colors.white.withOpacity(0.5), fontWeight: FontWeight.w500),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSentenceWithSpeaker(String text, {String? iconName}) {
     return Padding(
       padding: const EdgeInsets.only(bottom: 16.0),
       child: Column(
         children: [
            if (iconName != null)
               Padding(
                 padding: const EdgeInsets.only(bottom: 4),
                 child: Icon(MaterialIconsMapper.getIcon(iconName), size: 20, color: AppColors.primary.withOpacity(0.8)),
               ),
            Text(
              "\"$text\"",
              style: const TextStyle(fontSize: 16, color: Colors.white, height: 1.4, fontStyle: FontStyle.italic),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 4),
            GestureDetector(
              onTap: () => _speak(text),
              child: Container(
                padding: const EdgeInsets.all(8), // Touch target
                child: const Icon(Icons.volume_up_rounded, color: Colors.white54, size: 20),
              ),
            ),
         ],
       ),
     );
  }
}
