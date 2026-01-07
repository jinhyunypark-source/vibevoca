import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_en.dart';
import 'app_localizations_ko.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'l10n/app_localizations.dart';
///
/// return MaterialApp(
///   localizationsDelegates: AppLocalizations.localizationsDelegates,
///   supportedLocales: AppLocalizations.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```yaml
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # Rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the AppLocalizations.supportedLocales
/// property.
abstract class AppLocalizations {
  AppLocalizations(String locale)
    : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates =
      <LocalizationsDelegate<dynamic>>[
        delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
      ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('en'),
    Locale('ko'),
  ];

  /// No description provided for @appTitle.
  ///
  /// In ko, this message translates to:
  /// **'VibeVoca'**
  String get appTitle;

  /// No description provided for @onboardingQuestionRole.
  ///
  /// In ko, this message translates to:
  /// **'당신은 어떤 사람입니까?'**
  String get onboardingQuestionRole;

  /// No description provided for @onboardingRoleMinor.
  ///
  /// In ko, this message translates to:
  /// **'미성년'**
  String get onboardingRoleMinor;

  /// No description provided for @onboardingRoleStudent.
  ///
  /// In ko, this message translates to:
  /// **'대학생'**
  String get onboardingRoleStudent;

  /// No description provided for @onboardingRoleWorker.
  ///
  /// In ko, this message translates to:
  /// **'직장인'**
  String get onboardingRoleWorker;

  /// No description provided for @onboardingRoleUnemployed.
  ///
  /// In ko, this message translates to:
  /// **'무직'**
  String get onboardingRoleUnemployed;

  /// No description provided for @onboardingQuestionInterests.
  ///
  /// In ko, this message translates to:
  /// **'어떤 것에 관심이 있나요?'**
  String get onboardingQuestionInterests;

  /// No description provided for @commonNext.
  ///
  /// In ko, this message translates to:
  /// **'다음'**
  String get commonNext;

  /// No description provided for @commonConfirm.
  ///
  /// In ko, this message translates to:
  /// **'확인'**
  String get commonConfirm;

  /// No description provided for @titleContextSelection.
  ///
  /// In ko, this message translates to:
  /// **'상황 및 덱 컬렉션'**
  String get titleContextSelection;

  /// No description provided for @titleBattle.
  ///
  /// In ko, this message translates to:
  /// **'단어 암기 배틀'**
  String get titleBattle;

  /// No description provided for @labelLockedDeck.
  ///
  /// In ko, this message translates to:
  /// **'잠금'**
  String get labelLockedDeck;

  /// No description provided for @labelReadyDeck.
  ///
  /// In ko, this message translates to:
  /// **'전투 준비'**
  String get labelReadyDeck;

  /// No description provided for @msgFillContext.
  ///
  /// In ko, this message translates to:
  /// **'아래 상황 카드를 선택하여 덱을 공명시키세요.'**
  String get msgFillContext;

  /// No description provided for @titleSettings.
  ///
  /// In ko, this message translates to:
  /// **'설정'**
  String get titleSettings;

  /// No description provided for @menuEditProfile.
  ///
  /// In ko, this message translates to:
  /// **'프로필 수정'**
  String get menuEditProfile;

  /// No description provided for @menuDashboard.
  ///
  /// In ko, this message translates to:
  /// **'학습 현황'**
  String get menuDashboard;

  /// No description provided for @menuLogout.
  ///
  /// In ko, this message translates to:
  /// **'로그아웃'**
  String get menuLogout;

  /// No description provided for @menuResetAll.
  ///
  /// In ko, this message translates to:
  /// **'전체 초기화'**
  String get menuResetAll;

  /// No description provided for @msgResetConfirm.
  ///
  /// In ko, this message translates to:
  /// **'정말로 모든 데이터를 초기화 하시겠습니까?'**
  String get msgResetConfirm;

  /// No description provided for @commonCancel.
  ///
  /// In ko, this message translates to:
  /// **'취소'**
  String get commonCancel;
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(lookupAppLocalizations(locale));
  }

  @override
  bool isSupported(Locale locale) =>
      <String>['en', 'ko'].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {
  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'en':
      return AppLocalizationsEn();
    case 'ko':
      return AppLocalizationsKo();
  }

  throw FlutterError(
    'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
    'an issue with the localizations generation tool. Please file an issue '
    'on GitHub with a reproducible sample app and the gen-l10n configuration '
    'that was used.',
  );
}
