import 'dart:math';
import 'package:flutter/material.dart';

class GenerativeCardBackground extends StatelessWidget {
  final String word;
  final Color baseColor;

  const GenerativeCardBackground({
    super.key,
    required this.word,
    required this.baseColor,
  });

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      painter: _GenerativePainter(word, baseColor),
      child: Container(),
    );
  }
}

class _GenerativePainter extends CustomPainter {
  final String seed;
  final Color baseColor;

  _GenerativePainter(this.seed, this.baseColor);

  @override
  void paint(Canvas canvas, Size size) {
    final int hash = seed.hashCode;
    final Random random = Random(hash);

    // Background filler
    // Slightly darken or lighten the base color for the background
    final Paint bgPaint = Paint()..color = baseColor.withOpacity(0.1);
    final Rect rect = Rect.fromLTWH(0, 0, size.width, size.height);
    canvas.drawRect(rect, bgPaint);

    final Paint shapePaint = Paint()
      ..style = PaintingStyle.fill
      ..strokeCap = StrokeCap.round;

    // Draw 3-5 random geometric shapes
    final int shapeCount = 3 + random.nextInt(3); 
    
    for (int i = 0; i < shapeCount; i++) {
        // Vary color slightly
        final double opacity = 0.05 + random.nextDouble() * 0.1;
        final Color shapeColor = Color.fromARGB(
          (255 * opacity).toInt(),
          baseColor.red + random.nextInt(50) - 25,
          baseColor.green + random.nextInt(50) - 25,
          baseColor.blue + random.nextInt(50) - 25,
        ).withOpacity(opacity); // Ensure valid opacity

        shapePaint.color = shapeColor;

        final double cx = random.nextDouble() * size.width;
        final double cy = random.nextDouble() * size.height;
        final double radius = 50 + random.nextDouble() * 150;
        
        // Randomly choose shape: Circle, RoundedRect, or Line
        final int type = random.nextInt(3);
        
        if (type == 0) {
           canvas.drawCircle(Offset(cx, cy), radius, shapePaint);
        } else if (type == 1) {
           canvas.drawRRect(
             RRect.fromRectAndRadius(
               Rect.fromCenter(center: Offset(cx, cy), width: radius * 1.5, height: radius),
               const Radius.circular(20),
             ), 
             shapePaint
           );
        } else {
           shapePaint.strokeWidth = 20 + random.nextDouble() * 40;
           shapePaint.style = PaintingStyle.stroke;
           final double endX = cx + (random.nextBool() ? 100 : -100);
           final double endY = cy + (random.nextBool() ? 100 : -100);
           canvas.drawLine(Offset(cx, cy), Offset(endX, endY), shapePaint);
           shapePaint.style = PaintingStyle.fill; // Reset
        }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
