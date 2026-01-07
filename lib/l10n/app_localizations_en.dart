// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for English (`en`).
class AppLocalizationsEn extends AppLocalizations {
  AppLocalizationsEn([String locale = 'en']) : super(locale);

  @override
  String get appTitle => 'VibeVoca';

  @override
  String get onboardingQuestionRole => 'Who are you?';

  @override
  String get onboardingRoleMinor => 'Minor';

  @override
  String get onboardingRoleStudent => 'Student';

  @override
  String get onboardingRoleWorker => 'Worker';

  @override
  String get onboardingRoleUnemployed => 'Unemployed';

  @override
  String get onboardingQuestionInterests => 'What are your interests?';

  @override
  String get commonNext => 'Next';

  @override
  String get commonConfirm => 'Confirm';

  @override
  String get titleContextSelection => 'Context & Deck Collection';

  @override
  String get titleBattle => 'Word Battle';

  @override
  String get labelLockedDeck => 'LOCKED';

  @override
  String get labelReadyDeck => 'READY TO BATTLE';

  @override
  String get msgFillContext =>
      'Select context cards below to resonate with the decks.';

  @override
  String get titleSettings => 'Settings';

  @override
  String get menuEditProfile => 'Edit Profile';

  @override
  String get menuDashboard => 'Learning Dashboard';

  @override
  String get menuLogout => 'Logout';

  @override
  String get menuResetAll => 'Reset All Data';

  @override
  String get msgResetConfirm => 'Are you sure you want to reset all data?';

  @override
  String get commonCancel => 'Cancel';
}
