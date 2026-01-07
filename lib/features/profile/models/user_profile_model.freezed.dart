// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'user_profile_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$UserProfileModel {

 String get id; String? get role;// Unified interest_ids now contains both jobs and interests
@JsonKey(name: 'interest_ids') List<String> get interestIds;@JsonKey(name: 'last_played_deck_id') String? get lastPlayedDeckId;@JsonKey(name: 'completed_deck_ids') List<String> get completedDeckIds;
/// Create a copy of UserProfileModel
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$UserProfileModelCopyWith<UserProfileModel> get copyWith => _$UserProfileModelCopyWithImpl<UserProfileModel>(this as UserProfileModel, _$identity);

  /// Serializes this UserProfileModel to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is UserProfileModel&&(identical(other.id, id) || other.id == id)&&(identical(other.role, role) || other.role == role)&&const DeepCollectionEquality().equals(other.interestIds, interestIds)&&(identical(other.lastPlayedDeckId, lastPlayedDeckId) || other.lastPlayedDeckId == lastPlayedDeckId)&&const DeepCollectionEquality().equals(other.completedDeckIds, completedDeckIds));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,role,const DeepCollectionEquality().hash(interestIds),lastPlayedDeckId,const DeepCollectionEquality().hash(completedDeckIds));

@override
String toString() {
  return 'UserProfileModel(id: $id, role: $role, interestIds: $interestIds, lastPlayedDeckId: $lastPlayedDeckId, completedDeckIds: $completedDeckIds)';
}


}

/// @nodoc
abstract mixin class $UserProfileModelCopyWith<$Res>  {
  factory $UserProfileModelCopyWith(UserProfileModel value, $Res Function(UserProfileModel) _then) = _$UserProfileModelCopyWithImpl;
@useResult
$Res call({
 String id, String? role,@JsonKey(name: 'interest_ids') List<String> interestIds,@JsonKey(name: 'last_played_deck_id') String? lastPlayedDeckId,@JsonKey(name: 'completed_deck_ids') List<String> completedDeckIds
});




}
/// @nodoc
class _$UserProfileModelCopyWithImpl<$Res>
    implements $UserProfileModelCopyWith<$Res> {
  _$UserProfileModelCopyWithImpl(this._self, this._then);

  final UserProfileModel _self;
  final $Res Function(UserProfileModel) _then;

/// Create a copy of UserProfileModel
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? role = freezed,Object? interestIds = null,Object? lastPlayedDeckId = freezed,Object? completedDeckIds = null,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,role: freezed == role ? _self.role : role // ignore: cast_nullable_to_non_nullable
as String?,interestIds: null == interestIds ? _self.interestIds : interestIds // ignore: cast_nullable_to_non_nullable
as List<String>,lastPlayedDeckId: freezed == lastPlayedDeckId ? _self.lastPlayedDeckId : lastPlayedDeckId // ignore: cast_nullable_to_non_nullable
as String?,completedDeckIds: null == completedDeckIds ? _self.completedDeckIds : completedDeckIds // ignore: cast_nullable_to_non_nullable
as List<String>,
  ));
}

}


/// Adds pattern-matching-related methods to [UserProfileModel].
extension UserProfileModelPatterns on UserProfileModel {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _UserProfileModel value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _UserProfileModel() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _UserProfileModel value)  $default,){
final _that = this;
switch (_that) {
case _UserProfileModel():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _UserProfileModel value)?  $default,){
final _that = this;
switch (_that) {
case _UserProfileModel() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id,  String? role, @JsonKey(name: 'interest_ids')  List<String> interestIds, @JsonKey(name: 'last_played_deck_id')  String? lastPlayedDeckId, @JsonKey(name: 'completed_deck_ids')  List<String> completedDeckIds)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _UserProfileModel() when $default != null:
return $default(_that.id,_that.role,_that.interestIds,_that.lastPlayedDeckId,_that.completedDeckIds);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id,  String? role, @JsonKey(name: 'interest_ids')  List<String> interestIds, @JsonKey(name: 'last_played_deck_id')  String? lastPlayedDeckId, @JsonKey(name: 'completed_deck_ids')  List<String> completedDeckIds)  $default,) {final _that = this;
switch (_that) {
case _UserProfileModel():
return $default(_that.id,_that.role,_that.interestIds,_that.lastPlayedDeckId,_that.completedDeckIds);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id,  String? role, @JsonKey(name: 'interest_ids')  List<String> interestIds, @JsonKey(name: 'last_played_deck_id')  String? lastPlayedDeckId, @JsonKey(name: 'completed_deck_ids')  List<String> completedDeckIds)?  $default,) {final _that = this;
switch (_that) {
case _UserProfileModel() when $default != null:
return $default(_that.id,_that.role,_that.interestIds,_that.lastPlayedDeckId,_that.completedDeckIds);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _UserProfileModel implements UserProfileModel {
  const _UserProfileModel({required this.id, this.role, @JsonKey(name: 'interest_ids') final  List<String> interestIds = const [], @JsonKey(name: 'last_played_deck_id') this.lastPlayedDeckId, @JsonKey(name: 'completed_deck_ids') final  List<String> completedDeckIds = const []}): _interestIds = interestIds,_completedDeckIds = completedDeckIds;
  factory _UserProfileModel.fromJson(Map<String, dynamic> json) => _$UserProfileModelFromJson(json);

@override final  String id;
@override final  String? role;
// Unified interest_ids now contains both jobs and interests
 final  List<String> _interestIds;
// Unified interest_ids now contains both jobs and interests
@override@JsonKey(name: 'interest_ids') List<String> get interestIds {
  if (_interestIds is EqualUnmodifiableListView) return _interestIds;
  // ignore: implicit_dynamic_type
  return EqualUnmodifiableListView(_interestIds);
}

@override@JsonKey(name: 'last_played_deck_id') final  String? lastPlayedDeckId;
 final  List<String> _completedDeckIds;
@override@JsonKey(name: 'completed_deck_ids') List<String> get completedDeckIds {
  if (_completedDeckIds is EqualUnmodifiableListView) return _completedDeckIds;
  // ignore: implicit_dynamic_type
  return EqualUnmodifiableListView(_completedDeckIds);
}


/// Create a copy of UserProfileModel
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$UserProfileModelCopyWith<_UserProfileModel> get copyWith => __$UserProfileModelCopyWithImpl<_UserProfileModel>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$UserProfileModelToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _UserProfileModel&&(identical(other.id, id) || other.id == id)&&(identical(other.role, role) || other.role == role)&&const DeepCollectionEquality().equals(other._interestIds, _interestIds)&&(identical(other.lastPlayedDeckId, lastPlayedDeckId) || other.lastPlayedDeckId == lastPlayedDeckId)&&const DeepCollectionEquality().equals(other._completedDeckIds, _completedDeckIds));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,role,const DeepCollectionEquality().hash(_interestIds),lastPlayedDeckId,const DeepCollectionEquality().hash(_completedDeckIds));

@override
String toString() {
  return 'UserProfileModel(id: $id, role: $role, interestIds: $interestIds, lastPlayedDeckId: $lastPlayedDeckId, completedDeckIds: $completedDeckIds)';
}


}

/// @nodoc
abstract mixin class _$UserProfileModelCopyWith<$Res> implements $UserProfileModelCopyWith<$Res> {
  factory _$UserProfileModelCopyWith(_UserProfileModel value, $Res Function(_UserProfileModel) _then) = __$UserProfileModelCopyWithImpl;
@override @useResult
$Res call({
 String id, String? role,@JsonKey(name: 'interest_ids') List<String> interestIds,@JsonKey(name: 'last_played_deck_id') String? lastPlayedDeckId,@JsonKey(name: 'completed_deck_ids') List<String> completedDeckIds
});




}
/// @nodoc
class __$UserProfileModelCopyWithImpl<$Res>
    implements _$UserProfileModelCopyWith<$Res> {
  __$UserProfileModelCopyWithImpl(this._self, this._then);

  final _UserProfileModel _self;
  final $Res Function(_UserProfileModel) _then;

/// Create a copy of UserProfileModel
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? role = freezed,Object? interestIds = null,Object? lastPlayedDeckId = freezed,Object? completedDeckIds = null,}) {
  return _then(_UserProfileModel(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,role: freezed == role ? _self.role : role // ignore: cast_nullable_to_non_nullable
as String?,interestIds: null == interestIds ? _self._interestIds : interestIds // ignore: cast_nullable_to_non_nullable
as List<String>,lastPlayedDeckId: freezed == lastPlayedDeckId ? _self.lastPlayedDeckId : lastPlayedDeckId // ignore: cast_nullable_to_non_nullable
as String?,completedDeckIds: null == completedDeckIds ? _self._completedDeckIds : completedDeckIds // ignore: cast_nullable_to_non_nullable
as List<String>,
  ));
}


}

// dart format on
