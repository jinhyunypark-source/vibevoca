// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'context_item.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$ContextItem {

 String get id; String get slug; ContextType get type; String get label; String get iconAsset;
/// Create a copy of ContextItem
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$ContextItemCopyWith<ContextItem> get copyWith => _$ContextItemCopyWithImpl<ContextItem>(this as ContextItem, _$identity);

  /// Serializes this ContextItem to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is ContextItem&&(identical(other.id, id) || other.id == id)&&(identical(other.slug, slug) || other.slug == slug)&&(identical(other.type, type) || other.type == type)&&(identical(other.label, label) || other.label == label)&&(identical(other.iconAsset, iconAsset) || other.iconAsset == iconAsset));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,slug,type,label,iconAsset);

@override
String toString() {
  return 'ContextItem(id: $id, slug: $slug, type: $type, label: $label, iconAsset: $iconAsset)';
}


}

/// @nodoc
abstract mixin class $ContextItemCopyWith<$Res>  {
  factory $ContextItemCopyWith(ContextItem value, $Res Function(ContextItem) _then) = _$ContextItemCopyWithImpl;
@useResult
$Res call({
 String id, String slug, ContextType type, String label, String iconAsset
});




}
/// @nodoc
class _$ContextItemCopyWithImpl<$Res>
    implements $ContextItemCopyWith<$Res> {
  _$ContextItemCopyWithImpl(this._self, this._then);

  final ContextItem _self;
  final $Res Function(ContextItem) _then;

/// Create a copy of ContextItem
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? slug = null,Object? type = null,Object? label = null,Object? iconAsset = null,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,slug: null == slug ? _self.slug : slug // ignore: cast_nullable_to_non_nullable
as String,type: null == type ? _self.type : type // ignore: cast_nullable_to_non_nullable
as ContextType,label: null == label ? _self.label : label // ignore: cast_nullable_to_non_nullable
as String,iconAsset: null == iconAsset ? _self.iconAsset : iconAsset // ignore: cast_nullable_to_non_nullable
as String,
  ));
}

}


/// Adds pattern-matching-related methods to [ContextItem].
extension ContextItemPatterns on ContextItem {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _ContextItem value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _ContextItem() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _ContextItem value)  $default,){
final _that = this;
switch (_that) {
case _ContextItem():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _ContextItem value)?  $default,){
final _that = this;
switch (_that) {
case _ContextItem() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id,  String slug,  ContextType type,  String label,  String iconAsset)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _ContextItem() when $default != null:
return $default(_that.id,_that.slug,_that.type,_that.label,_that.iconAsset);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id,  String slug,  ContextType type,  String label,  String iconAsset)  $default,) {final _that = this;
switch (_that) {
case _ContextItem():
return $default(_that.id,_that.slug,_that.type,_that.label,_that.iconAsset);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id,  String slug,  ContextType type,  String label,  String iconAsset)?  $default,) {final _that = this;
switch (_that) {
case _ContextItem() when $default != null:
return $default(_that.id,_that.slug,_that.type,_that.label,_that.iconAsset);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _ContextItem implements ContextItem {
  const _ContextItem({required this.id, required this.slug, required this.type, required this.label, required this.iconAsset});
  factory _ContextItem.fromJson(Map<String, dynamic> json) => _$ContextItemFromJson(json);

@override final  String id;
@override final  String slug;
@override final  ContextType type;
@override final  String label;
@override final  String iconAsset;

/// Create a copy of ContextItem
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$ContextItemCopyWith<_ContextItem> get copyWith => __$ContextItemCopyWithImpl<_ContextItem>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$ContextItemToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _ContextItem&&(identical(other.id, id) || other.id == id)&&(identical(other.slug, slug) || other.slug == slug)&&(identical(other.type, type) || other.type == type)&&(identical(other.label, label) || other.label == label)&&(identical(other.iconAsset, iconAsset) || other.iconAsset == iconAsset));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,slug,type,label,iconAsset);

@override
String toString() {
  return 'ContextItem(id: $id, slug: $slug, type: $type, label: $label, iconAsset: $iconAsset)';
}


}

/// @nodoc
abstract mixin class _$ContextItemCopyWith<$Res> implements $ContextItemCopyWith<$Res> {
  factory _$ContextItemCopyWith(_ContextItem value, $Res Function(_ContextItem) _then) = __$ContextItemCopyWithImpl;
@override @useResult
$Res call({
 String id, String slug, ContextType type, String label, String iconAsset
});




}
/// @nodoc
class __$ContextItemCopyWithImpl<$Res>
    implements _$ContextItemCopyWith<$Res> {
  __$ContextItemCopyWithImpl(this._self, this._then);

  final _ContextItem _self;
  final $Res Function(_ContextItem) _then;

/// Create a copy of ContextItem
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? slug = null,Object? type = null,Object? label = null,Object? iconAsset = null,}) {
  return _then(_ContextItem(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,slug: null == slug ? _self.slug : slug // ignore: cast_nullable_to_non_nullable
as String,type: null == type ? _self.type : type // ignore: cast_nullable_to_non_nullable
as ContextType,label: null == label ? _self.label : label // ignore: cast_nullable_to_non_nullable
as String,iconAsset: null == iconAsset ? _self.iconAsset : iconAsset // ignore: cast_nullable_to_non_nullable
as String,
  ));
}


}

// dart format on
