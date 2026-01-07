import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../../core/theme/app_colors.dart';

enum DeckStatus { current, completed, locked }

class DeckBox extends StatefulWidget {
  final String title;
  final Color baseColor;
  final double progress; // 0.0 to 1.0 (0=New, 1=Mastered)
  final DeckStatus status;
  final VoidCallback onTap;
  final String? deckId;
  final String? iconAsset; 
  final double? width;
  final double? height;
  final bool compact; // To simplify UI for grid
  
  // Stats
  final int memorizedCount;
  final int reviewCount;
  final int totalCount;
  final bool isLastPlayed;

  const DeckBox({
    super.key,
    required this.title,
    required this.baseColor,
    required this.progress,
    required this.status,
    required this.onTap,
    this.deckId,
    this.iconAsset,
    this.width,
    this.height,
    this.compact = false,
    this.memorizedCount = 0,
    this.reviewCount = 0,
    this.totalCount = 0,
    this.isLastPlayed = false,
  });

  @override
  State<DeckBox> createState() => _DeckBoxState();
}

class _DeckBoxState extends State<DeckBox> with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: 4.seconds)..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  String? _getAssetPath() {
    if (widget.deckId == null) return null;
    const knownAssets = ['logic_clarity', 'emotion_depth', 'sensory_details', 'action_impact'];
    if (knownAssets.contains(widget.deckId)) {
        if (widget.deckId == 'logic_clarity') return 'assets/images/decks/logic.png';
        if (widget.deckId == 'emotion_depth') return 'assets/images/decks/emotion.png';
        if (widget.deckId == 'sensory_details') return 'assets/images/decks/sensory.png';
        if (widget.deckId == 'action_impact') return 'assets/images/decks/action.png';
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    // 1. Color Logic
    // Default: Grey
    // Active (Memorized > 0 OR Last Played): Theme Color
    final bool hasStarted = widget.memorizedCount > 0 || widget.isLastPlayed;
    final bool isCompleted = widget.memorizedCount > 0 && widget.memorizedCount == widget.totalCount;
    
    // If not started and not last played, use Grey. Otherwise use baseColor.
    Color displayColor = (!hasStarted) 
        ? Colors.grey.shade800 
        : widget.baseColor;
        
    // Completed overrides to Green? Prompt says: "If memorized > 0, use basic color. If complete, add badge."
    // It also says: "If deck icon green == total, complete." -> This implies color logic might be simpler.
    // "Basic color if memorized > 0".
    
    final assetPath = _getAssetPath();

    return GestureDetector(
      onTap: widget.onTap,
      // 1. Outer Animator: Handles Scale
      child: AnimatedContainer(
        duration: 300.ms,
        transform: widget.isLastPlayed 
          ? (Matrix4.identity()..scale(1.05)..translate(0.0, -5.0)) 
          : Matrix4.identity(),
        margin: widget.compact ? const EdgeInsets.all(4) : const EdgeInsets.symmetric(horizontal: 10, vertical: 20),
        width: widget.width,
        height: widget.height,
        
        // 2. Border Logic (Gold for Last Played)
        child: AnimatedBuilder(
          animation: _controller,
          builder: (context, child) {
            Gradient? borderGradient;
            Color borderColor = Colors.transparent;
            BoxShadow? shadow;

            if (widget.isLastPlayed) {
               // Gold Rotation
               borderGradient = LinearGradient(
                  colors: const [Color(0xFFFFE082), Color(0xFFB8860B), Color(0xFFFFD700), Color(0xFFF7F2E0), Color(0xFFFFE082)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  stops: const [0.0, 0.25, 0.5, 0.75, 1.0],
                  transform: GradientRotation(_controller.value * 2 * 3.14159),
               );
               shadow = BoxShadow(
                 color: const Color(0xFFFFD700).withOpacity(0.4),
                 blurRadius: widget.compact ? 10 : 25,
                 offset: const Offset(0, 4),
                 spreadRadius: 2,
               );
            } else {
               // Normal Border
               borderColor = Colors.white10;
            }

            return Container(
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(widget.compact ? 16 : 26),
                gradient: borderGradient,
                border: borderGradient == null ? Border.all(color: borderColor, width: 2) : null,
                boxShadow: shadow != null ? [shadow] : [],
              ),
              padding: EdgeInsets.all(widget.compact ? 2.0 : 4.0), // Border Width
              child: child, 
            );
          },
          // 3. Card Face
          child: Container(
            decoration: BoxDecoration(
              color: displayColor,
              image: assetPath != null 
                ? DecorationImage(
                    image: AssetImage(assetPath),
                    fit: BoxFit.cover,
                    colorFilter: !hasStarted
                       ? const ColorFilter.mode(Colors.grey, BlendMode.saturation) 
                       : ColorFilter.mode(Colors.black.withOpacity(0.3), BlendMode.darken),
                  ) 
                : null,
              borderRadius: BorderRadius.circular(widget.compact ? 14 : 23),
              gradient: assetPath == null ? LinearGradient(
                colors: [
                  displayColor,
                  displayColor.withOpacity(0.7),
                ],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ) : null,
            ),
            child: Stack(
              children: [
                if (assetPath != null)
                  Positioned.fill(
                    child: Container(
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(widget.compact ? 14 : 23),
                        gradient: LinearGradient(
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                          colors: [Colors.transparent, Colors.black.withOpacity(0.8)],
                          stops: const [0.5, 1.0],
                        ),
                      ),
                    ),
                  ),
                  
                // Overlay for Gray state handled by color/filter above

                // Content
                Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                       _buildDeckIcon(widget.iconAsset, size: widget.compact ? 32 : 50),
                      if (!widget.compact) ...[
                        const SizedBox(height: 20),
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 16.0),
                          child: Text(
                            widget.title, 
                            style: const TextStyle(
                              color: Colors.white, 
                              fontWeight: FontWeight.bold, 
                              fontSize: 22, 
                              letterSpacing: 1.2,
                              shadows: [Shadow(blurRadius: 10, color: Colors.black, offset: Offset(0, 2))],
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ),
                      ] else ...[
                        const SizedBox(height: 8),
                         // Compact Title
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 4.0),
                          child: Text(
                            widget.title, 
                            style: const TextStyle(
                              color: Colors.white, 
                              fontWeight: FontWeight.w600, 
                              fontSize: 12,
                              overflow: TextOverflow.ellipsis
                            ),
                            maxLines: 2,
                            textAlign: TextAlign.center,
                          ),
                        ),
                      ],
                      
                      // Stats Row (Small Numbers)
                      if (hasStarted) ...[
                         const SizedBox(height: 4),
                         Row(
                           mainAxisAlignment: MainAxisAlignment.center,
                           children: [
                             Text("${widget.memorizedCount}", style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
                             const Text(" / ", style: TextStyle(color: Colors.white30, fontSize: 10)),
                             Text("${widget.totalCount}", style: const TextStyle(color: Colors.white, fontSize: 10)),
                           ],
                         )
                      ]
                    ],
                  ),
                ),
                
                // Complete Badge
                if (isCompleted)
                  Positioned(
                    top: 8,
                    right: 8,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(
                        color: AppColors.pass,
                        borderRadius: BorderRadius.circular(4),
                        boxShadow: [
                           BoxShadow(color: Colors.black.withOpacity(0.3), blurRadius: 4)
                        ]
                      ),
                      child: const Text(
                        "COMPLETE",
                        style: TextStyle(color: Colors.white, fontSize: 8, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildDeckIcon(String? iconKey, {double size = 50}) {
    if (widget.progress >= 1.0) {
      return Icon(Icons.check_circle, size: size, color: Colors.white);
    }
    
    if (iconKey == null) {
       return Icon(Icons.layers, size: size, color: Colors.white.withOpacity(0.9));
    }

    // 1. Asset Image
    if (iconKey.startsWith('assets/')) {
        return Image.asset(iconKey, width: size + 10, height: size + 10);
    }

    // 2. Emoji
    if (iconKey.runes.length <= 2) {
       return Text(iconKey, style: TextStyle(fontSize: size));
    }

    // 3. Known Icon Keys (Mapping)
    // ... [Same mapping logic, just using local var for iconData] ...
    // To save space in tool output, assume mapping logic is here.
    // I need to copy the mapping logic or reference it. 
    // Since I'm replacing the whole file content or block, I must include it.
    // I will abbreviate for brevity if possible but for safety I should include common ones.
    
    // RE-INSERTING FULL MAPPING LOGIC FROM PREVIOUS FILE TO BE SAFE
    IconData? iconData;
    switch (iconKey) {
       // Communication
      case 'psychology': iconData = Icons.psychology; break;
      case 'record_voice_over': iconData = Icons.record_voice_over; break;
      case 'sentiment_satisfied': iconData = Icons.sentiment_satisfied; break;
      case 'short_text': iconData = Icons.short_text; break;
      case 'handshake': iconData = Icons.handshake; break;
      // Sense & Style
      case 'visibility': iconData = Icons.visibility; break;
      case 'hearing': iconData = Icons.hearing; break;
      case 'restaurant': iconData = Icons.restaurant; break;
      case 'air': iconData = Icons.air; break;
      case 'touch_app': iconData = Icons.touch_app; break;
      case 'palette': iconData = Icons.palette; break;
      // Intelligence & Judgment
      case 'lightbulb': iconData = Icons.lightbulb; break;
      case 'self_improvement': iconData = Icons.self_improvement; break;
      case 'tips_and_updates': iconData = Icons.tips_and_updates; break;
      case 'block': iconData = Icons.block; break;
      case 'help_outline': iconData = Icons.help_outline; break;
      // Relationships & Social
      case 'favorite': iconData = Icons.favorite; break;
      case 'groups': iconData = Icons.groups; break;
      case 'diversity_3': iconData = Icons.diversity_3; break;
      case 'remove_circle': iconData = Icons.remove_circle; break;
      case 'person': iconData = Icons.person; break;
      case 'diamond': iconData = Icons.diamond; break;
      // Change & Growth
      case 'trending_up': iconData = Icons.trending_up; break;
      case 'trending_down': iconData = Icons.trending_down; break;
      case 'autorenew': iconData = Icons.autorenew; break;
      case 'swap_vert': iconData = Icons.swap_vert; break;
      case 'replay': iconData = Icons.replay; break;
      // Difficulty & Complexity
      case 'fitness_center': iconData = Icons.fitness_center; break;
      case 'spa': iconData = Icons.spa; break;
      case 'hub': iconData = Icons.hub; break;
      case 'circle': iconData = Icons.circle; break;
      // Power & Authority
      case 'gavel': iconData = Icons.gavel; break;
      case 'volunteer_activism': iconData = Icons.volunteer_activism; break;
      case 'military_tech': iconData = Icons.military_tech; break;
      case 'diversity_1': iconData = Icons.diversity_1; break;
      // Size & Quantity
      case 'open_in_full': iconData = Icons.open_in_full; break;
      case 'close_fullscreen': iconData = Icons.close_fullscreen; break;
      case 'inventory_2': iconData = Icons.inventory_2; break;
      case 'inventory': iconData = Icons.inventory; break;
      case 'zoom_out_map': iconData = Icons.zoom_out_map; break;
      // Money & Finance
      case 'account_balance': iconData = Icons.account_balance; break;
      case 'money_off': iconData = Icons.money_off; break;
      case 'savings': iconData = Icons.savings; break;
      case 'sell': iconData = Icons.sell; break;
      case 'payments': iconData = Icons.payments; break;
      // Time & Duration
      case 'all_inclusive': iconData = Icons.all_inclusive; break;
      case 'hourglass_empty': iconData = Icons.hourglass_empty; break;
      case 'repeat': iconData = Icons.repeat; break;
      case 'speed': iconData = Icons.speed; break;
      case 'timeline': iconData = Icons.timeline; break;
      case 'schedule': iconData = Icons.schedule; break;
      // Legacy keys
      case 'fluency_delivery': iconData = Icons.record_voice_over; break;
      case 'logic_clarity': iconData = Icons.lightbulb; break;
      case 'emotion_depth': iconData = Icons.sentiment_satisfied_alt; break;
      case 'sensory_details': iconData = Icons.visibility; break;
      case 'action_impact': iconData = Icons.flash_on; break;
      case 'home': iconData = Icons.home; break;
      default: iconData = null;
    }

    if (iconData != null) {
      return Icon(iconData, size: size, color: Colors.white.withOpacity(0.9));
    }
    
    // 4. Fallback
    return Container(
      width: size + 10, height: size + 10,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        border: Border.all(color: Colors.white54, width: 2)
      ),
      child: Text(
        iconKey.substring(0, 1).toUpperCase(), 
        style: TextStyle(fontSize: size * 0.6, color: Colors.white, fontWeight: FontWeight.bold)
      ),
    );
  }
}
