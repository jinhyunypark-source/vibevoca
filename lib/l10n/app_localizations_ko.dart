// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Korean (`ko`).
class AppLocalizationsKo extends AppLocalizations {
  AppLocalizationsKo([String locale = 'ko']) : super(locale);

  @override
  String get appTitle => 'VibeVoca';

  @override
  String get onboardingQuestionRole => '당신은 어떤 사람입니까?';

  @override
  String get onboardingRoleMinor => '미성년';

  @override
  String get onboardingRoleStudent => '대학생';

  @override
  String get onboardingRoleWorker => '직장인';

  @override
  String get onboardingRoleUnemployed => '무직';

  @override
  String get onboardingQuestionInterests => '어떤 것에 관심이 있나요?';

  @override
  String get commonNext => '다음';

  @override
  String get commonConfirm => '확인';

  @override
  String get titleContextSelection => '상황 및 덱 컬렉션';

  @override
  String get titleBattle => '단어 암기 배틀';

  @override
  String get labelLockedDeck => '잠금';

  @override
  String get labelReadyDeck => '전투 준비';

  @override
  String get msgFillContext => '아래 상황 카드를 선택하여 덱을 공명시키세요.';

  @override
  String get titleSettings => '설정';

  @override
  String get menuEditProfile => '프로필 수정';

  @override
  String get menuDashboard => '학습 현황';

  @override
  String get menuLogout => '로그아웃';

  @override
  String get menuResetAll => '전체 초기화';

  @override
  String get msgResetConfirm => '정말로 모든 데이터를 초기화 하시겠습니까?';

  @override
  String get commonCancel => '취소';
}
