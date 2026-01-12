// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'word_card_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$WordCardModel {

 String get id; String get word; String get meaning; String get exampleSentence;// "AI Generated" context
 List<VibeDisplayInfo> get vibeSentences; bool get isMemorized; int get failCount; String? get originalDeckId;
/// Create a copy of WordCardModel
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$WordCardModelCopyWith<WordCardModel> get copyWith => _$WordCardModelCopyWithImpl<WordCardModel>(this as WordCardModel, _$identity);

  /// Serializes this WordCardModel to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is WordCardModel&&(identical(other.id, id) || other.id == id)&&(identical(other.word, word) || other.word == word)&&(identical(other.meaning, meaning) || other.meaning == meaning)&&(identical(other.exampleSentence, exampleSentence) || other.exampleSentence == exampleSentence)&&const DeepCollectionEquality().equals(other.vibeSentences, vibeSentences)&&(identical(other.isMemorized, isMemorized) || other.isMemorized == isMemorized)&&(identical(other.failCount, failCount) || other.failCount == failCount)&&(identical(other.originalDeckId, originalDeckId) || other.originalDeckId == originalDeckId));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,word,meaning,exampleSentence,const DeepCollectionEquality().hash(vibeSentences),isMemorized,failCount,originalDeckId);

@override
String toString() {
  return 'WordCardModel(id: $id, word: $word, meaning: $meaning, exampleSentence: $exampleSentence, vibeSentences: $vibeSentences, isMemorized: $isMemorized, failCount: $failCount, originalDeckId: $originalDeckId)';
}


}

/// @nodoc
abstract mixin class $WordCardModelCopyWith<$Res>  {
  factory $WordCardModelCopyWith(WordCardModel value, $Res Function(WordCardModel) _then) = _$WordCardModelCopyWithImpl;
@useResult
$Res call({
 String id, String word, String meaning, String exampleSentence, List<VibeDisplayInfo> vibeSentences, bool isMemorized, int failCount, String? originalDeckId
});




}
/// @nodoc
class _$WordCardModelCopyWithImpl<$Res>
    implements $WordCardModelCopyWith<$Res> {
  _$WordCardModelCopyWithImpl(this._self, this._then);

  final WordCardModel _self;
  final $Res Function(WordCardModel) _then;

/// Create a copy of WordCardModel
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? word = null,Object? meaning = null,Object? exampleSentence = null,Object? vibeSentences = null,Object? isMemorized = null,Object? failCount = null,Object? originalDeckId = freezed,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,word: null == word ? _self.word : word // ignore: cast_nullable_to_non_nullable
as String,meaning: null == meaning ? _self.meaning : meaning // ignore: cast_nullable_to_non_nullable
as String,exampleSentence: null == exampleSentence ? _self.exampleSentence : exampleSentence // ignore: cast_nullable_to_non_nullable
as String,vibeSentences: null == vibeSentences ? _self.vibeSentences : vibeSentences // ignore: cast_nullable_to_non_nullable
as List<VibeDisplayInfo>,isMemorized: null == isMemorized ? _self.isMemorized : isMemorized // ignore: cast_nullable_to_non_nullable
as bool,failCount: null == failCount ? _self.failCount : failCount // ignore: cast_nullable_to_non_nullable
as int,originalDeckId: freezed == originalDeckId ? _self.originalDeckId : originalDeckId // ignore: cast_nullable_to_non_nullable
as String?,
  ));
}

}


/// Adds pattern-matching-related methods to [WordCardModel].
extension WordCardModelPatterns on WordCardModel {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _WordCardModel value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _WordCardModel() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _WordCardModel value)  $default,){
final _that = this;
switch (_that) {
case _WordCardModel():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _WordCardModel value)?  $default,){
final _that = this;
switch (_that) {
case _WordCardModel() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id,  String word,  String meaning,  String exampleSentence,  List<VibeDisplayInfo> vibeSentences,  bool isMemorized,  int failCount,  String? originalDeckId)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _WordCardModel() when $default != null:
return $default(_that.id,_that.word,_that.meaning,_that.exampleSentence,_that.vibeSentences,_that.isMemorized,_that.failCount,_that.originalDeckId);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id,  String word,  String meaning,  String exampleSentence,  List<VibeDisplayInfo> vibeSentences,  bool isMemorized,  int failCount,  String? originalDeckId)  $default,) {final _that = this;
switch (_that) {
case _WordCardModel():
return $default(_that.id,_that.word,_that.meaning,_that.exampleSentence,_that.vibeSentences,_that.isMemorized,_that.failCount,_that.originalDeckId);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id,  String word,  String meaning,  String exampleSentence,  List<VibeDisplayInfo> vibeSentences,  bool isMemorized,  int failCount,  String? originalDeckId)?  $default,) {final _that = this;
switch (_that) {
case _WordCardModel() when $default != null:
return $default(_that.id,_that.word,_that.meaning,_that.exampleSentence,_that.vibeSentences,_that.isMemorized,_that.failCount,_that.originalDeckId);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _WordCardModel implements WordCardModel {
  const _WordCardModel({required this.id, required this.word, required this.meaning, required this.exampleSentence, final  List<VibeDisplayInfo> vibeSentences = const [], this.isMemorized = false, this.failCount = 0, this.originalDeckId}): _vibeSentences = vibeSentences;
  factory _WordCardModel.fromJson(Map<String, dynamic> json) => _$WordCardModelFromJson(json);

@override final  String id;
@override final  String word;
@override final  String meaning;
@override final  String exampleSentence;
// "AI Generated" context
 final  List<VibeDisplayInfo> _vibeSentences;
// "AI Generated" context
@override@JsonKey() List<VibeDisplayInfo> get vibeSentences {
  if (_vibeSentences is EqualUnmodifiableListView) return _vibeSentences;
  // ignore: implicit_dynamic_type
  return EqualUnmodifiableListView(_vibeSentences);
}

@override@JsonKey() final  bool isMemorized;
@override@JsonKey() final  int failCount;
@override final  String? originalDeckId;

/// Create a copy of WordCardModel
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$WordCardModelCopyWith<_WordCardModel> get copyWith => __$WordCardModelCopyWithImpl<_WordCardModel>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$WordCardModelToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _WordCardModel&&(identical(other.id, id) || other.id == id)&&(identical(other.word, word) || other.word == word)&&(identical(other.meaning, meaning) || other.meaning == meaning)&&(identical(other.exampleSentence, exampleSentence) || other.exampleSentence == exampleSentence)&&const DeepCollectionEquality().equals(other._vibeSentences, _vibeSentences)&&(identical(other.isMemorized, isMemorized) || other.isMemorized == isMemorized)&&(identical(other.failCount, failCount) || other.failCount == failCount)&&(identical(other.originalDeckId, originalDeckId) || other.originalDeckId == originalDeckId));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,word,meaning,exampleSentence,const DeepCollectionEquality().hash(_vibeSentences),isMemorized,failCount,originalDeckId);

@override
String toString() {
  return 'WordCardModel(id: $id, word: $word, meaning: $meaning, exampleSentence: $exampleSentence, vibeSentences: $vibeSentences, isMemorized: $isMemorized, failCount: $failCount, originalDeckId: $originalDeckId)';
}


}

/// @nodoc
abstract mixin class _$WordCardModelCopyWith<$Res> implements $WordCardModelCopyWith<$Res> {
  factory _$WordCardModelCopyWith(_WordCardModel value, $Res Function(_WordCardModel) _then) = __$WordCardModelCopyWithImpl;
@override @useResult
$Res call({
 String id, String word, String meaning, String exampleSentence, List<VibeDisplayInfo> vibeSentences, bool isMemorized, int failCount, String? originalDeckId
});




}
/// @nodoc
class __$WordCardModelCopyWithImpl<$Res>
    implements _$WordCardModelCopyWith<$Res> {
  __$WordCardModelCopyWithImpl(this._self, this._then);

  final _WordCardModel _self;
  final $Res Function(_WordCardModel) _then;

/// Create a copy of WordCardModel
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? word = null,Object? meaning = null,Object? exampleSentence = null,Object? vibeSentences = null,Object? isMemorized = null,Object? failCount = null,Object? originalDeckId = freezed,}) {
  return _then(_WordCardModel(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,word: null == word ? _self.word : word // ignore: cast_nullable_to_non_nullable
as String,meaning: null == meaning ? _self.meaning : meaning // ignore: cast_nullable_to_non_nullable
as String,exampleSentence: null == exampleSentence ? _self.exampleSentence : exampleSentence // ignore: cast_nullable_to_non_nullable
as String,vibeSentences: null == vibeSentences ? _self._vibeSentences : vibeSentences // ignore: cast_nullable_to_non_nullable
as List<VibeDisplayInfo>,isMemorized: null == isMemorized ? _self.isMemorized : isMemorized // ignore: cast_nullable_to_non_nullable
as bool,failCount: null == failCount ? _self.failCount : failCount // ignore: cast_nullable_to_non_nullable
as int,originalDeckId: freezed == originalDeckId ? _self.originalDeckId : originalDeckId // ignore: cast_nullable_to_non_nullable
as String?,
  ));
}


}


/// @nodoc
mixin _$VibeDisplayInfo {

 String get sentence; String? get icon;// Material Icon name string
 String? get tagName;
/// Create a copy of VibeDisplayInfo
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$VibeDisplayInfoCopyWith<VibeDisplayInfo> get copyWith => _$VibeDisplayInfoCopyWithImpl<VibeDisplayInfo>(this as VibeDisplayInfo, _$identity);

  /// Serializes this VibeDisplayInfo to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is VibeDisplayInfo&&(identical(other.sentence, sentence) || other.sentence == sentence)&&(identical(other.icon, icon) || other.icon == icon)&&(identical(other.tagName, tagName) || other.tagName == tagName));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,sentence,icon,tagName);

@override
String toString() {
  return 'VibeDisplayInfo(sentence: $sentence, icon: $icon, tagName: $tagName)';
}


}

/// @nodoc
abstract mixin class $VibeDisplayInfoCopyWith<$Res>  {
  factory $VibeDisplayInfoCopyWith(VibeDisplayInfo value, $Res Function(VibeDisplayInfo) _then) = _$VibeDisplayInfoCopyWithImpl;
@useResult
$Res call({
 String sentence, String? icon, String? tagName
});




}
/// @nodoc
class _$VibeDisplayInfoCopyWithImpl<$Res>
    implements $VibeDisplayInfoCopyWith<$Res> {
  _$VibeDisplayInfoCopyWithImpl(this._self, this._then);

  final VibeDisplayInfo _self;
  final $Res Function(VibeDisplayInfo) _then;

/// Create a copy of VibeDisplayInfo
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? sentence = null,Object? icon = freezed,Object? tagName = freezed,}) {
  return _then(_self.copyWith(
sentence: null == sentence ? _self.sentence : sentence // ignore: cast_nullable_to_non_nullable
as String,icon: freezed == icon ? _self.icon : icon // ignore: cast_nullable_to_non_nullable
as String?,tagName: freezed == tagName ? _self.tagName : tagName // ignore: cast_nullable_to_non_nullable
as String?,
  ));
}

}


/// Adds pattern-matching-related methods to [VibeDisplayInfo].
extension VibeDisplayInfoPatterns on VibeDisplayInfo {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _VibeDisplayInfo value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _VibeDisplayInfo() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _VibeDisplayInfo value)  $default,){
final _that = this;
switch (_that) {
case _VibeDisplayInfo():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _VibeDisplayInfo value)?  $default,){
final _that = this;
switch (_that) {
case _VibeDisplayInfo() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String sentence,  String? icon,  String? tagName)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _VibeDisplayInfo() when $default != null:
return $default(_that.sentence,_that.icon,_that.tagName);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String sentence,  String? icon,  String? tagName)  $default,) {final _that = this;
switch (_that) {
case _VibeDisplayInfo():
return $default(_that.sentence,_that.icon,_that.tagName);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String sentence,  String? icon,  String? tagName)?  $default,) {final _that = this;
switch (_that) {
case _VibeDisplayInfo() when $default != null:
return $default(_that.sentence,_that.icon,_that.tagName);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _VibeDisplayInfo implements VibeDisplayInfo {
  const _VibeDisplayInfo({required this.sentence, this.icon, this.tagName});
  factory _VibeDisplayInfo.fromJson(Map<String, dynamic> json) => _$VibeDisplayInfoFromJson(json);

@override final  String sentence;
@override final  String? icon;
// Material Icon name string
@override final  String? tagName;

/// Create a copy of VibeDisplayInfo
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$VibeDisplayInfoCopyWith<_VibeDisplayInfo> get copyWith => __$VibeDisplayInfoCopyWithImpl<_VibeDisplayInfo>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$VibeDisplayInfoToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _VibeDisplayInfo&&(identical(other.sentence, sentence) || other.sentence == sentence)&&(identical(other.icon, icon) || other.icon == icon)&&(identical(other.tagName, tagName) || other.tagName == tagName));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,sentence,icon,tagName);

@override
String toString() {
  return 'VibeDisplayInfo(sentence: $sentence, icon: $icon, tagName: $tagName)';
}


}

/// @nodoc
abstract mixin class _$VibeDisplayInfoCopyWith<$Res> implements $VibeDisplayInfoCopyWith<$Res> {
  factory _$VibeDisplayInfoCopyWith(_VibeDisplayInfo value, $Res Function(_VibeDisplayInfo) _then) = __$VibeDisplayInfoCopyWithImpl;
@override @useResult
$Res call({
 String sentence, String? icon, String? tagName
});




}
/// @nodoc
class __$VibeDisplayInfoCopyWithImpl<$Res>
    implements _$VibeDisplayInfoCopyWith<$Res> {
  __$VibeDisplayInfoCopyWithImpl(this._self, this._then);

  final _VibeDisplayInfo _self;
  final $Res Function(_VibeDisplayInfo) _then;

/// Create a copy of VibeDisplayInfo
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? sentence = null,Object? icon = freezed,Object? tagName = freezed,}) {
  return _then(_VibeDisplayInfo(
sentence: null == sentence ? _self.sentence : sentence // ignore: cast_nullable_to_non_nullable
as String,icon: freezed == icon ? _self.icon : icon // ignore: cast_nullable_to_non_nullable
as String?,tagName: freezed == tagName ? _self.tagName : tagName // ignore: cast_nullable_to_non_nullable
as String?,
  ));
}


}

// dart format on
