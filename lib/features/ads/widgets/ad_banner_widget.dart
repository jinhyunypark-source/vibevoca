import 'dart:io';
import 'package:flutter/material.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';
import 'package:flutter/foundation.dart'; // For kReleaseMode

class AdBannerWidget extends StatefulWidget {
  const AdBannerWidget({super.key});

  @override
  State<AdBannerWidget> createState() => _AdBannerWidgetState();
}

class _AdBannerWidgetState extends State<AdBannerWidget> {
  BannerAd? _bannerAd;
  bool _isLoaded = false;


  // TODO: Replace with your actual AdMob Ad Unit IDs
  // Android Production ID from AdMob Console
  static const String _androidProdId = 'ca-app-pub-1115530284517700/6956466526'; 
  // iOS Production ID from AdMob Console
  static const String _iosProdId = 'ca-app-pub-xxxxxxxxxxxxxxxx/zzzzzzzzzz'; 

  final String _adUnitId = Platform.isAndroid
      ? (kReleaseMode ? _androidProdId : 'ca-app-pub-3940256099942544/6300978111')
      : (kReleaseMode ? _iosProdId : 'ca-app-pub-3940256099942544/2934735716');

  @override
  void initState() {
    super.initState();
    _loadAd();
  }

  void _loadAd() {
    _bannerAd = BannerAd(
      adUnitId: _adUnitId,
      request: const AdRequest(),
      size: AdSize.banner, // Standard banner (320x50), or use AnchoredAdaptiveBannerAdSize for better fit
      listener: BannerAdListener(
        onAdLoaded: (ad) {
          print('✅ [AdMob] BannerAd loaded successfully: ${ad.responseInfo}');
          setState(() {
            _isLoaded = true;
          });
        },
        onAdFailedToLoad: (ad, err) {
          print('❌ [AdMob] BannerAd failed to load: code=${err.code}, message=${err.message}');
          print('❌ [AdMob] Error Domain: ${err.domain}');
          ad.dispose();
        },
        onAdOpened: (ad) => print('ℹ️ [AdMob] BannerAd opened'),
        onAdClosed: (ad) => print('ℹ️ [AdMob] BannerAd closed'),
      ),
    )..load();
  }

  @override
  void dispose() {
    _bannerAd?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_bannerAd == null || !_isLoaded) {
      return const SizedBox.shrink(); // Hide if not loaded
    }

    return SafeArea(
      top: false,
      child: Container(
        alignment: Alignment.center,
        width: _bannerAd!.size.width.toDouble(),
        height: _bannerAd!.size.height.toDouble(),
        child: AdWidget(ad: _bannerAd!),
      ),
    );
  }
}
