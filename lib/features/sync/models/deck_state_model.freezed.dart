// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'deck_state_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$DeckState {

 String get deckId; String get userId; int get totalCount; int get memorizedCount; int get remindCount; List<CardState> get cardStates;// Resume Logic
 String? get lastViewedCardId;// Local-only flag to track if this needs syncing
@JsonKey(includeToJson: false, includeFromJson: false) bool get isDirty;// Timestamp for when it was last modified locally
@JsonKey(includeToJson: false, includeFromJson: false) DateTime? get lastChangedAt;// DB Timestamps
 DateTime? get updatedAt;
/// Create a copy of DeckState
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$DeckStateCopyWith<DeckState> get copyWith => _$DeckStateCopyWithImpl<DeckState>(this as DeckState, _$identity);

  /// Serializes this DeckState to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is DeckState&&(identical(other.deckId, deckId) || other.deckId == deckId)&&(identical(other.userId, userId) || other.userId == userId)&&(identical(other.totalCount, totalCount) || other.totalCount == totalCount)&&(identical(other.memorizedCount, memorizedCount) || other.memorizedCount == memorizedCount)&&(identical(other.remindCount, remindCount) || other.remindCount == remindCount)&&const DeepCollectionEquality().equals(other.cardStates, cardStates)&&(identical(other.lastViewedCardId, lastViewedCardId) || other.lastViewedCardId == lastViewedCardId)&&(identical(other.isDirty, isDirty) || other.isDirty == isDirty)&&(identical(other.lastChangedAt, lastChangedAt) || other.lastChangedAt == lastChangedAt)&&(identical(other.updatedAt, updatedAt) || other.updatedAt == updatedAt));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,deckId,userId,totalCount,memorizedCount,remindCount,const DeepCollectionEquality().hash(cardStates),lastViewedCardId,isDirty,lastChangedAt,updatedAt);

@override
String toString() {
  return 'DeckState(deckId: $deckId, userId: $userId, totalCount: $totalCount, memorizedCount: $memorizedCount, remindCount: $remindCount, cardStates: $cardStates, lastViewedCardId: $lastViewedCardId, isDirty: $isDirty, lastChangedAt: $lastChangedAt, updatedAt: $updatedAt)';
}


}

/// @nodoc
abstract mixin class $DeckStateCopyWith<$Res>  {
  factory $DeckStateCopyWith(DeckState value, $Res Function(DeckState) _then) = _$DeckStateCopyWithImpl;
@useResult
$Res call({
 String deckId, String userId, int totalCount, int memorizedCount, int remindCount, List<CardState> cardStates, String? lastViewedCardId,@JsonKey(includeToJson: false, includeFromJson: false) bool isDirty,@JsonKey(includeToJson: false, includeFromJson: false) DateTime? lastChangedAt, DateTime? updatedAt
});




}
/// @nodoc
class _$DeckStateCopyWithImpl<$Res>
    implements $DeckStateCopyWith<$Res> {
  _$DeckStateCopyWithImpl(this._self, this._then);

  final DeckState _self;
  final $Res Function(DeckState) _then;

/// Create a copy of DeckState
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? deckId = null,Object? userId = null,Object? totalCount = null,Object? memorizedCount = null,Object? remindCount = null,Object? cardStates = null,Object? lastViewedCardId = freezed,Object? isDirty = null,Object? lastChangedAt = freezed,Object? updatedAt = freezed,}) {
  return _then(_self.copyWith(
deckId: null == deckId ? _self.deckId : deckId // ignore: cast_nullable_to_non_nullable
as String,userId: null == userId ? _self.userId : userId // ignore: cast_nullable_to_non_nullable
as String,totalCount: null == totalCount ? _self.totalCount : totalCount // ignore: cast_nullable_to_non_nullable
as int,memorizedCount: null == memorizedCount ? _self.memorizedCount : memorizedCount // ignore: cast_nullable_to_non_nullable
as int,remindCount: null == remindCount ? _self.remindCount : remindCount // ignore: cast_nullable_to_non_nullable
as int,cardStates: null == cardStates ? _self.cardStates : cardStates // ignore: cast_nullable_to_non_nullable
as List<CardState>,lastViewedCardId: freezed == lastViewedCardId ? _self.lastViewedCardId : lastViewedCardId // ignore: cast_nullable_to_non_nullable
as String?,isDirty: null == isDirty ? _self.isDirty : isDirty // ignore: cast_nullable_to_non_nullable
as bool,lastChangedAt: freezed == lastChangedAt ? _self.lastChangedAt : lastChangedAt // ignore: cast_nullable_to_non_nullable
as DateTime?,updatedAt: freezed == updatedAt ? _self.updatedAt : updatedAt // ignore: cast_nullable_to_non_nullable
as DateTime?,
  ));
}

}


/// Adds pattern-matching-related methods to [DeckState].
extension DeckStatePatterns on DeckState {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _DeckState value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _DeckState() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _DeckState value)  $default,){
final _that = this;
switch (_that) {
case _DeckState():
return $default(_that);}
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _DeckState value)?  $default,){
final _that = this;
switch (_that) {
case _DeckState() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String deckId,  String userId,  int totalCount,  int memorizedCount,  int remindCount,  List<CardState> cardStates,  String? lastViewedCardId, @JsonKey(includeToJson: false, includeFromJson: false)  bool isDirty, @JsonKey(includeToJson: false, includeFromJson: false)  DateTime? lastChangedAt,  DateTime? updatedAt)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _DeckState() when $default != null:
return $default(_that.deckId,_that.userId,_that.totalCount,_that.memorizedCount,_that.remindCount,_that.cardStates,_that.lastViewedCardId,_that.isDirty,_that.lastChangedAt,_that.updatedAt);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String deckId,  String userId,  int totalCount,  int memorizedCount,  int remindCount,  List<CardState> cardStates,  String? lastViewedCardId, @JsonKey(includeToJson: false, includeFromJson: false)  bool isDirty, @JsonKey(includeToJson: false, includeFromJson: false)  DateTime? lastChangedAt,  DateTime? updatedAt)  $default,) {final _that = this;
switch (_that) {
case _DeckState():
return $default(_that.deckId,_that.userId,_that.totalCount,_that.memorizedCount,_that.remindCount,_that.cardStates,_that.lastViewedCardId,_that.isDirty,_that.lastChangedAt,_that.updatedAt);}
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String deckId,  String userId,  int totalCount,  int memorizedCount,  int remindCount,  List<CardState> cardStates,  String? lastViewedCardId, @JsonKey(includeToJson: false, includeFromJson: false)  bool isDirty, @JsonKey(includeToJson: false, includeFromJson: false)  DateTime? lastChangedAt,  DateTime? updatedAt)?  $default,) {final _that = this;
switch (_that) {
case _DeckState() when $default != null:
return $default(_that.deckId,_that.userId,_that.totalCount,_that.memorizedCount,_that.remindCount,_that.cardStates,_that.lastViewedCardId,_that.isDirty,_that.lastChangedAt,_that.updatedAt);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _DeckState implements DeckState {
  const _DeckState({required this.deckId, required this.userId, this.totalCount = 0, this.memorizedCount = 0, this.remindCount = 0, final  List<CardState> cardStates = const [], this.lastViewedCardId, @JsonKey(includeToJson: false, includeFromJson: false) this.isDirty = false, @JsonKey(includeToJson: false, includeFromJson: false) this.lastChangedAt, this.updatedAt}): _cardStates = cardStates;
  factory _DeckState.fromJson(Map<String, dynamic> json) => _$DeckStateFromJson(json);

@override final  String deckId;
@override final  String userId;
@override@JsonKey() final  int totalCount;
@override@JsonKey() final  int memorizedCount;
@override@JsonKey() final  int remindCount;
 final  List<CardState> _cardStates;
@override@JsonKey() List<CardState> get cardStates {
  if (_cardStates is EqualUnmodifiableListView) return _cardStates;
  // ignore: implicit_dynamic_type
  return EqualUnmodifiableListView(_cardStates);
}

// Resume Logic
@override final  String? lastViewedCardId;
// Local-only flag to track if this needs syncing
@override@JsonKey(includeToJson: false, includeFromJson: false) final  bool isDirty;
// Timestamp for when it was last modified locally
@override@JsonKey(includeToJson: false, includeFromJson: false) final  DateTime? lastChangedAt;
// DB Timestamps
@override final  DateTime? updatedAt;

/// Create a copy of DeckState
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$DeckStateCopyWith<_DeckState> get copyWith => __$DeckStateCopyWithImpl<_DeckState>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$DeckStateToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _DeckState&&(identical(other.deckId, deckId) || other.deckId == deckId)&&(identical(other.userId, userId) || other.userId == userId)&&(identical(other.totalCount, totalCount) || other.totalCount == totalCount)&&(identical(other.memorizedCount, memorizedCount) || other.memorizedCount == memorizedCount)&&(identical(other.remindCount, remindCount) || other.remindCount == remindCount)&&const DeepCollectionEquality().equals(other._cardStates, _cardStates)&&(identical(other.lastViewedCardId, lastViewedCardId) || other.lastViewedCardId == lastViewedCardId)&&(identical(other.isDirty, isDirty) || other.isDirty == isDirty)&&(identical(other.lastChangedAt, lastChangedAt) || other.lastChangedAt == lastChangedAt)&&(identical(other.updatedAt, updatedAt) || other.updatedAt == updatedAt));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,deckId,userId,totalCount,memorizedCount,remindCount,const DeepCollectionEquality().hash(_cardStates),lastViewedCardId,isDirty,lastChangedAt,updatedAt);

@override
String toString() {
  return 'DeckState(deckId: $deckId, userId: $userId, totalCount: $totalCount, memorizedCount: $memorizedCount, remindCount: $remindCount, cardStates: $cardStates, lastViewedCardId: $lastViewedCardId, isDirty: $isDirty, lastChangedAt: $lastChangedAt, updatedAt: $updatedAt)';
}


}

/// @nodoc
abstract mixin class _$DeckStateCopyWith<$Res> implements $DeckStateCopyWith<$Res> {
  factory _$DeckStateCopyWith(_DeckState value, $Res Function(_DeckState) _then) = __$DeckStateCopyWithImpl;
@override @useResult
$Res call({
 String deckId, String userId, int totalCount, int memorizedCount, int remindCount, List<CardState> cardStates, String? lastViewedCardId,@JsonKey(includeToJson: false, includeFromJson: false) bool isDirty,@JsonKey(includeToJson: false, includeFromJson: false) DateTime? lastChangedAt, DateTime? updatedAt
});




}
/// @nodoc
class __$DeckStateCopyWithImpl<$Res>
    implements _$DeckStateCopyWith<$Res> {
  __$DeckStateCopyWithImpl(this._self, this._then);

  final _DeckState _self;
  final $Res Function(_DeckState) _then;

/// Create a copy of DeckState
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? deckId = null,Object? userId = null,Object? totalCount = null,Object? memorizedCount = null,Object? remindCount = null,Object? cardStates = null,Object? lastViewedCardId = freezed,Object? isDirty = null,Object? lastChangedAt = freezed,Object? updatedAt = freezed,}) {
  return _then(_DeckState(
deckId: null == deckId ? _self.deckId : deckId // ignore: cast_nullable_to_non_nullable
as String,userId: null == userId ? _self.userId : userId // ignore: cast_nullable_to_non_nullable
as String,totalCount: null == totalCount ? _self.totalCount : totalCount // ignore: cast_nullable_to_non_nullable
as int,memorizedCount: null == memorizedCount ? _self.memorizedCount : memorizedCount // ignore: cast_nullable_to_non_nullable
as int,remindCount: null == remindCount ? _self.remindCount : remindCount // ignore: cast_nullable_to_non_nullable
as int,cardStates: null == cardStates ? _self._cardStates : cardStates // ignore: cast_nullable_to_non_nullable
as List<CardState>,lastViewedCardId: freezed == lastViewedCardId ? _self.lastViewedCardId : lastViewedCardId // ignore: cast_nullable_to_non_nullable
as String?,isDirty: null == isDirty ? _self.isDirty : isDirty // ignore: cast_nullable_to_non_nullable
as bool,lastChangedAt: freezed == lastChangedAt ? _self.lastChangedAt : lastChangedAt // ignore: cast_nullable_to_non_nullable
as DateTime?,updatedAt: freezed == updatedAt ? _self.updatedAt : updatedAt // ignore: cast_nullable_to_non_nullable
as DateTime?,
  ));
}


}


/// @nodoc
mixin _$CardState {

 String get id;/// 'new', 'review', 'memorized'
@JsonKey(name: 's') String get status;/// Remind Count
@JsonKey(name: 'rc') int get remindCount;/// Re-memorize Count (or Memory Count)
@JsonKey(name: 'mc') int get stepCount;
/// Create a copy of CardState
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$CardStateCopyWith<CardState> get copyWith => _$CardStateCopyWithImpl<CardState>(this as CardState, _$identity);

  /// Serializes this CardState to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is CardState&&(identical(other.id, id) || other.id == id)&&(identical(other.status, status) || other.status == status)&&(identical(other.remindCount, remindCount) || other.remindCount == remindCount)&&(identical(other.stepCount, stepCount) || other.stepCount == stepCount));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,status,remindCount,stepCount);

@override
String toString() {
  return 'CardState(id: $id, status: $status, remindCount: $remindCount, stepCount: $stepCount)';
}


}

/// @nodoc
abstract mixin class $CardStateCopyWith<$Res>  {
  factory $CardStateCopyWith(CardState value, $Res Function(CardState) _then) = _$CardStateCopyWithImpl;
@useResult
$Res call({
 String id,@JsonKey(name: 's') String status,@JsonKey(name: 'rc') int remindCount,@JsonKey(name: 'mc') int stepCount
});




}
/// @nodoc
class _$CardStateCopyWithImpl<$Res>
    implements $CardStateCopyWith<$Res> {
  _$CardStateCopyWithImpl(this._self, this._then);

  final CardState _self;
  final $Res Function(CardState) _then;

/// Create a copy of CardState
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? status = null,Object? remindCount = null,Object? stepCount = null,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,remindCount: null == remindCount ? _self.remindCount : remindCount // ignore: cast_nullable_to_non_nullable
as int,stepCount: null == stepCount ? _self.stepCount : stepCount // ignore: cast_nullable_to_non_nullable
as int,
  ));
}

}


/// Adds pattern-matching-related methods to [CardState].
extension CardStatePatterns on CardState {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _CardState value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _CardState() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _CardState value)  $default,){
final _that = this;
switch (_that) {
case _CardState():
return $default(_that);}
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _CardState value)?  $default,){
final _that = this;
switch (_that) {
case _CardState() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 's')  String status, @JsonKey(name: 'rc')  int remindCount, @JsonKey(name: 'mc')  int stepCount)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _CardState() when $default != null:
return $default(_that.id,_that.status,_that.remindCount,_that.stepCount);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 's')  String status, @JsonKey(name: 'rc')  int remindCount, @JsonKey(name: 'mc')  int stepCount)  $default,) {final _that = this;
switch (_that) {
case _CardState():
return $default(_that.id,_that.status,_that.remindCount,_that.stepCount);}
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id, @JsonKey(name: 's')  String status, @JsonKey(name: 'rc')  int remindCount, @JsonKey(name: 'mc')  int stepCount)?  $default,) {final _that = this;
switch (_that) {
case _CardState() when $default != null:
return $default(_that.id,_that.status,_that.remindCount,_that.stepCount);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _CardState implements CardState {
  const _CardState({required this.id, @JsonKey(name: 's') required this.status, @JsonKey(name: 'rc') this.remindCount = 0, @JsonKey(name: 'mc') this.stepCount = 0});
  factory _CardState.fromJson(Map<String, dynamic> json) => _$CardStateFromJson(json);

@override final  String id;
/// 'new', 'review', 'memorized'
@override@JsonKey(name: 's') final  String status;
/// Remind Count
@override@JsonKey(name: 'rc') final  int remindCount;
/// Re-memorize Count (or Memory Count)
@override@JsonKey(name: 'mc') final  int stepCount;

/// Create a copy of CardState
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$CardStateCopyWith<_CardState> get copyWith => __$CardStateCopyWithImpl<_CardState>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$CardStateToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _CardState&&(identical(other.id, id) || other.id == id)&&(identical(other.status, status) || other.status == status)&&(identical(other.remindCount, remindCount) || other.remindCount == remindCount)&&(identical(other.stepCount, stepCount) || other.stepCount == stepCount));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,status,remindCount,stepCount);

@override
String toString() {
  return 'CardState(id: $id, status: $status, remindCount: $remindCount, stepCount: $stepCount)';
}


}

/// @nodoc
abstract mixin class _$CardStateCopyWith<$Res> implements $CardStateCopyWith<$Res> {
  factory _$CardStateCopyWith(_CardState value, $Res Function(_CardState) _then) = __$CardStateCopyWithImpl;
@override @useResult
$Res call({
 String id,@JsonKey(name: 's') String status,@JsonKey(name: 'rc') int remindCount,@JsonKey(name: 'mc') int stepCount
});




}
/// @nodoc
class __$CardStateCopyWithImpl<$Res>
    implements _$CardStateCopyWith<$Res> {
  __$CardStateCopyWithImpl(this._self, this._then);

  final _CardState _self;
  final $Res Function(_CardState) _then;

/// Create a copy of CardState
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? status = null,Object? remindCount = null,Object? stepCount = null,}) {
  return _then(_CardState(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,remindCount: null == remindCount ? _self.remindCount : remindCount // ignore: cast_nullable_to_non_nullable
as int,stepCount: null == stepCount ? _self.stepCount : stepCount // ignore: cast_nullable_to_non_nullable
as int,
  ));
}


}

// dart format on
