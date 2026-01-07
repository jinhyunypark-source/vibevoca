// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'persona.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$Persona {

 String get id; String get name; String get job; List<String> get interests; String get title;
/// Create a copy of Persona
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$PersonaCopyWith<Persona> get copyWith => _$PersonaCopyWithImpl<Persona>(this as Persona, _$identity);

  /// Serializes this Persona to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is Persona&&(identical(other.id, id) || other.id == id)&&(identical(other.name, name) || other.name == name)&&(identical(other.job, job) || other.job == job)&&const DeepCollectionEquality().equals(other.interests, interests)&&(identical(other.title, title) || other.title == title));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,name,job,const DeepCollectionEquality().hash(interests),title);

@override
String toString() {
  return 'Persona(id: $id, name: $name, job: $job, interests: $interests, title: $title)';
}


}

/// @nodoc
abstract mixin class $PersonaCopyWith<$Res>  {
  factory $PersonaCopyWith(Persona value, $Res Function(Persona) _then) = _$PersonaCopyWithImpl;
@useResult
$Res call({
 String id, String name, String job, List<String> interests, String title
});




}
/// @nodoc
class _$PersonaCopyWithImpl<$Res>
    implements $PersonaCopyWith<$Res> {
  _$PersonaCopyWithImpl(this._self, this._then);

  final Persona _self;
  final $Res Function(Persona) _then;

/// Create a copy of Persona
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? name = null,Object? job = null,Object? interests = null,Object? title = null,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,name: null == name ? _self.name : name // ignore: cast_nullable_to_non_nullable
as String,job: null == job ? _self.job : job // ignore: cast_nullable_to_non_nullable
as String,interests: null == interests ? _self.interests : interests // ignore: cast_nullable_to_non_nullable
as List<String>,title: null == title ? _self.title : title // ignore: cast_nullable_to_non_nullable
as String,
  ));
}

}


/// Adds pattern-matching-related methods to [Persona].
extension PersonaPatterns on Persona {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _Persona value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _Persona() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _Persona value)  $default,){
final _that = this;
switch (_that) {
case _Persona():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _Persona value)?  $default,){
final _that = this;
switch (_that) {
case _Persona() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id,  String name,  String job,  List<String> interests,  String title)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _Persona() when $default != null:
return $default(_that.id,_that.name,_that.job,_that.interests,_that.title);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id,  String name,  String job,  List<String> interests,  String title)  $default,) {final _that = this;
switch (_that) {
case _Persona():
return $default(_that.id,_that.name,_that.job,_that.interests,_that.title);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id,  String name,  String job,  List<String> interests,  String title)?  $default,) {final _that = this;
switch (_that) {
case _Persona() when $default != null:
return $default(_that.id,_that.name,_that.job,_that.interests,_that.title);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _Persona implements Persona {
  const _Persona({required this.id, required this.name, required this.job, required final  List<String> interests, required this.title}): _interests = interests;
  factory _Persona.fromJson(Map<String, dynamic> json) => _$PersonaFromJson(json);

@override final  String id;
@override final  String name;
@override final  String job;
 final  List<String> _interests;
@override List<String> get interests {
  if (_interests is EqualUnmodifiableListView) return _interests;
  // ignore: implicit_dynamic_type
  return EqualUnmodifiableListView(_interests);
}

@override final  String title;

/// Create a copy of Persona
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$PersonaCopyWith<_Persona> get copyWith => __$PersonaCopyWithImpl<_Persona>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$PersonaToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _Persona&&(identical(other.id, id) || other.id == id)&&(identical(other.name, name) || other.name == name)&&(identical(other.job, job) || other.job == job)&&const DeepCollectionEquality().equals(other._interests, _interests)&&(identical(other.title, title) || other.title == title));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,name,job,const DeepCollectionEquality().hash(_interests),title);

@override
String toString() {
  return 'Persona(id: $id, name: $name, job: $job, interests: $interests, title: $title)';
}


}

/// @nodoc
abstract mixin class _$PersonaCopyWith<$Res> implements $PersonaCopyWith<$Res> {
  factory _$PersonaCopyWith(_Persona value, $Res Function(_Persona) _then) = __$PersonaCopyWithImpl;
@override @useResult
$Res call({
 String id, String name, String job, List<String> interests, String title
});




}
/// @nodoc
class __$PersonaCopyWithImpl<$Res>
    implements _$PersonaCopyWith<$Res> {
  __$PersonaCopyWithImpl(this._self, this._then);

  final _Persona _self;
  final $Res Function(_Persona) _then;

/// Create a copy of Persona
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? name = null,Object? job = null,Object? interests = null,Object? title = null,}) {
  return _then(_Persona(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,name: null == name ? _self.name : name // ignore: cast_nullable_to_non_nullable
as String,job: null == job ? _self.job : job // ignore: cast_nullable_to_non_nullable
as String,interests: null == interests ? _self._interests : interests // ignore: cast_nullable_to_non_nullable
as List<String>,title: null == title ? _self.title : title // ignore: cast_nullable_to_non_nullable
as String,
  ));
}


}

// dart format on
