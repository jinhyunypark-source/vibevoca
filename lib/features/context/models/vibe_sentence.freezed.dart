// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'vibe_sentence.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$VibeSentence {

@JsonKey(name: 'card_id') String get cardId;@JsonKey(name: 'sentence_en') String get sentenceEn;@JsonKey(name: 'sentence_ko') String? get sentenceKo; List<String> get tags;
/// Create a copy of VibeSentence
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$VibeSentenceCopyWith<VibeSentence> get copyWith => _$VibeSentenceCopyWithImpl<VibeSentence>(this as VibeSentence, _$identity);

  /// Serializes this VibeSentence to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is VibeSentence&&(identical(other.cardId, cardId) || other.cardId == cardId)&&(identical(other.sentenceEn, sentenceEn) || other.sentenceEn == sentenceEn)&&(identical(other.sentenceKo, sentenceKo) || other.sentenceKo == sentenceKo)&&const DeepCollectionEquality().equals(other.tags, tags));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,cardId,sentenceEn,sentenceKo,const DeepCollectionEquality().hash(tags));

@override
String toString() {
  return 'VibeSentence(cardId: $cardId, sentenceEn: $sentenceEn, sentenceKo: $sentenceKo, tags: $tags)';
}


}

/// @nodoc
abstract mixin class $VibeSentenceCopyWith<$Res>  {
  factory $VibeSentenceCopyWith(VibeSentence value, $Res Function(VibeSentence) _then) = _$VibeSentenceCopyWithImpl;
@useResult
$Res call({
@JsonKey(name: 'card_id') String cardId,@JsonKey(name: 'sentence_en') String sentenceEn,@JsonKey(name: 'sentence_ko') String? sentenceKo, List<String> tags
});




}
/// @nodoc
class _$VibeSentenceCopyWithImpl<$Res>
    implements $VibeSentenceCopyWith<$Res> {
  _$VibeSentenceCopyWithImpl(this._self, this._then);

  final VibeSentence _self;
  final $Res Function(VibeSentence) _then;

/// Create a copy of VibeSentence
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? cardId = null,Object? sentenceEn = null,Object? sentenceKo = freezed,Object? tags = null,}) {
  return _then(_self.copyWith(
cardId: null == cardId ? _self.cardId : cardId // ignore: cast_nullable_to_non_nullable
as String,sentenceEn: null == sentenceEn ? _self.sentenceEn : sentenceEn // ignore: cast_nullable_to_non_nullable
as String,sentenceKo: freezed == sentenceKo ? _self.sentenceKo : sentenceKo // ignore: cast_nullable_to_non_nullable
as String?,tags: null == tags ? _self.tags : tags // ignore: cast_nullable_to_non_nullable
as List<String>,
  ));
}

}


/// Adds pattern-matching-related methods to [VibeSentence].
extension VibeSentencePatterns on VibeSentence {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _VibeSentence value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _VibeSentence() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _VibeSentence value)  $default,){
final _that = this;
switch (_that) {
case _VibeSentence():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _VibeSentence value)?  $default,){
final _that = this;
switch (_that) {
case _VibeSentence() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function(@JsonKey(name: 'card_id')  String cardId, @JsonKey(name: 'sentence_en')  String sentenceEn, @JsonKey(name: 'sentence_ko')  String? sentenceKo,  List<String> tags)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _VibeSentence() when $default != null:
return $default(_that.cardId,_that.sentenceEn,_that.sentenceKo,_that.tags);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function(@JsonKey(name: 'card_id')  String cardId, @JsonKey(name: 'sentence_en')  String sentenceEn, @JsonKey(name: 'sentence_ko')  String? sentenceKo,  List<String> tags)  $default,) {final _that = this;
switch (_that) {
case _VibeSentence():
return $default(_that.cardId,_that.sentenceEn,_that.sentenceKo,_that.tags);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function(@JsonKey(name: 'card_id')  String cardId, @JsonKey(name: 'sentence_en')  String sentenceEn, @JsonKey(name: 'sentence_ko')  String? sentenceKo,  List<String> tags)?  $default,) {final _that = this;
switch (_that) {
case _VibeSentence() when $default != null:
return $default(_that.cardId,_that.sentenceEn,_that.sentenceKo,_that.tags);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _VibeSentence implements VibeSentence {
  const _VibeSentence({@JsonKey(name: 'card_id') required this.cardId, @JsonKey(name: 'sentence_en') required this.sentenceEn, @JsonKey(name: 'sentence_ko') this.sentenceKo, required final  List<String> tags}): _tags = tags;
  factory _VibeSentence.fromJson(Map<String, dynamic> json) => _$VibeSentenceFromJson(json);

@override@JsonKey(name: 'card_id') final  String cardId;
@override@JsonKey(name: 'sentence_en') final  String sentenceEn;
@override@JsonKey(name: 'sentence_ko') final  String? sentenceKo;
 final  List<String> _tags;
@override List<String> get tags {
  if (_tags is EqualUnmodifiableListView) return _tags;
  // ignore: implicit_dynamic_type
  return EqualUnmodifiableListView(_tags);
}


/// Create a copy of VibeSentence
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$VibeSentenceCopyWith<_VibeSentence> get copyWith => __$VibeSentenceCopyWithImpl<_VibeSentence>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$VibeSentenceToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _VibeSentence&&(identical(other.cardId, cardId) || other.cardId == cardId)&&(identical(other.sentenceEn, sentenceEn) || other.sentenceEn == sentenceEn)&&(identical(other.sentenceKo, sentenceKo) || other.sentenceKo == sentenceKo)&&const DeepCollectionEquality().equals(other._tags, _tags));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,cardId,sentenceEn,sentenceKo,const DeepCollectionEquality().hash(_tags));

@override
String toString() {
  return 'VibeSentence(cardId: $cardId, sentenceEn: $sentenceEn, sentenceKo: $sentenceKo, tags: $tags)';
}


}

/// @nodoc
abstract mixin class _$VibeSentenceCopyWith<$Res> implements $VibeSentenceCopyWith<$Res> {
  factory _$VibeSentenceCopyWith(_VibeSentence value, $Res Function(_VibeSentence) _then) = __$VibeSentenceCopyWithImpl;
@override @useResult
$Res call({
@JsonKey(name: 'card_id') String cardId,@JsonKey(name: 'sentence_en') String sentenceEn,@JsonKey(name: 'sentence_ko') String? sentenceKo, List<String> tags
});




}
/// @nodoc
class __$VibeSentenceCopyWithImpl<$Res>
    implements _$VibeSentenceCopyWith<$Res> {
  __$VibeSentenceCopyWithImpl(this._self, this._then);

  final _VibeSentence _self;
  final $Res Function(_VibeSentence) _then;

/// Create a copy of VibeSentence
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? cardId = null,Object? sentenceEn = null,Object? sentenceKo = freezed,Object? tags = null,}) {
  return _then(_VibeSentence(
cardId: null == cardId ? _self.cardId : cardId // ignore: cast_nullable_to_non_nullable
as String,sentenceEn: null == sentenceEn ? _self.sentenceEn : sentenceEn // ignore: cast_nullable_to_non_nullable
as String,sentenceKo: freezed == sentenceKo ? _self.sentenceKo : sentenceKo // ignore: cast_nullable_to_non_nullable
as String?,tags: null == tags ? _self._tags : tags // ignore: cast_nullable_to_non_nullable
as List<String>,
  ));
}


}

// dart format on
