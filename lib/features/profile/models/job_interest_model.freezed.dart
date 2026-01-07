// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'job_interest_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$InterestModel {

 String get id; String get category;// job, hobby, vibe
 String get code;@JsonKey(name: 'label_en') String get labelEn;@JsonKey(name: 'label_ko') String get labelKo; String? get icon; String? get color; List<String> get tags;@JsonKey(name: 'order_index') int get orderIndex;
/// Create a copy of InterestModel
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$InterestModelCopyWith<InterestModel> get copyWith => _$InterestModelCopyWithImpl<InterestModel>(this as InterestModel, _$identity);

  /// Serializes this InterestModel to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is InterestModel&&(identical(other.id, id) || other.id == id)&&(identical(other.category, category) || other.category == category)&&(identical(other.code, code) || other.code == code)&&(identical(other.labelEn, labelEn) || other.labelEn == labelEn)&&(identical(other.labelKo, labelKo) || other.labelKo == labelKo)&&(identical(other.icon, icon) || other.icon == icon)&&(identical(other.color, color) || other.color == color)&&const DeepCollectionEquality().equals(other.tags, tags)&&(identical(other.orderIndex, orderIndex) || other.orderIndex == orderIndex));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,category,code,labelEn,labelKo,icon,color,const DeepCollectionEquality().hash(tags),orderIndex);

@override
String toString() {
  return 'InterestModel(id: $id, category: $category, code: $code, labelEn: $labelEn, labelKo: $labelKo, icon: $icon, color: $color, tags: $tags, orderIndex: $orderIndex)';
}


}

/// @nodoc
abstract mixin class $InterestModelCopyWith<$Res>  {
  factory $InterestModelCopyWith(InterestModel value, $Res Function(InterestModel) _then) = _$InterestModelCopyWithImpl;
@useResult
$Res call({
 String id, String category, String code,@JsonKey(name: 'label_en') String labelEn,@JsonKey(name: 'label_ko') String labelKo, String? icon, String? color, List<String> tags,@JsonKey(name: 'order_index') int orderIndex
});




}
/// @nodoc
class _$InterestModelCopyWithImpl<$Res>
    implements $InterestModelCopyWith<$Res> {
  _$InterestModelCopyWithImpl(this._self, this._then);

  final InterestModel _self;
  final $Res Function(InterestModel) _then;

/// Create a copy of InterestModel
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? category = null,Object? code = null,Object? labelEn = null,Object? labelKo = null,Object? icon = freezed,Object? color = freezed,Object? tags = null,Object? orderIndex = null,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,category: null == category ? _self.category : category // ignore: cast_nullable_to_non_nullable
as String,code: null == code ? _self.code : code // ignore: cast_nullable_to_non_nullable
as String,labelEn: null == labelEn ? _self.labelEn : labelEn // ignore: cast_nullable_to_non_nullable
as String,labelKo: null == labelKo ? _self.labelKo : labelKo // ignore: cast_nullable_to_non_nullable
as String,icon: freezed == icon ? _self.icon : icon // ignore: cast_nullable_to_non_nullable
as String?,color: freezed == color ? _self.color : color // ignore: cast_nullable_to_non_nullable
as String?,tags: null == tags ? _self.tags : tags // ignore: cast_nullable_to_non_nullable
as List<String>,orderIndex: null == orderIndex ? _self.orderIndex : orderIndex // ignore: cast_nullable_to_non_nullable
as int,
  ));
}

}


/// Adds pattern-matching-related methods to [InterestModel].
extension InterestModelPatterns on InterestModel {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _InterestModel value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _InterestModel() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _InterestModel value)  $default,){
final _that = this;
switch (_that) {
case _InterestModel():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _InterestModel value)?  $default,){
final _that = this;
switch (_that) {
case _InterestModel() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id,  String category,  String code, @JsonKey(name: 'label_en')  String labelEn, @JsonKey(name: 'label_ko')  String labelKo,  String? icon,  String? color,  List<String> tags, @JsonKey(name: 'order_index')  int orderIndex)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _InterestModel() when $default != null:
return $default(_that.id,_that.category,_that.code,_that.labelEn,_that.labelKo,_that.icon,_that.color,_that.tags,_that.orderIndex);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id,  String category,  String code, @JsonKey(name: 'label_en')  String labelEn, @JsonKey(name: 'label_ko')  String labelKo,  String? icon,  String? color,  List<String> tags, @JsonKey(name: 'order_index')  int orderIndex)  $default,) {final _that = this;
switch (_that) {
case _InterestModel():
return $default(_that.id,_that.category,_that.code,_that.labelEn,_that.labelKo,_that.icon,_that.color,_that.tags,_that.orderIndex);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id,  String category,  String code, @JsonKey(name: 'label_en')  String labelEn, @JsonKey(name: 'label_ko')  String labelKo,  String? icon,  String? color,  List<String> tags, @JsonKey(name: 'order_index')  int orderIndex)?  $default,) {final _that = this;
switch (_that) {
case _InterestModel() when $default != null:
return $default(_that.id,_that.category,_that.code,_that.labelEn,_that.labelKo,_that.icon,_that.color,_that.tags,_that.orderIndex);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _InterestModel implements InterestModel {
  const _InterestModel({required this.id, this.category = 'job', required this.code, @JsonKey(name: 'label_en') required this.labelEn, @JsonKey(name: 'label_ko') required this.labelKo, this.icon, this.color, final  List<String> tags = const [], @JsonKey(name: 'order_index') this.orderIndex = 0}): _tags = tags;
  factory _InterestModel.fromJson(Map<String, dynamic> json) => _$InterestModelFromJson(json);

@override final  String id;
@override@JsonKey() final  String category;
// job, hobby, vibe
@override final  String code;
@override@JsonKey(name: 'label_en') final  String labelEn;
@override@JsonKey(name: 'label_ko') final  String labelKo;
@override final  String? icon;
@override final  String? color;
 final  List<String> _tags;
@override@JsonKey() List<String> get tags {
  if (_tags is EqualUnmodifiableListView) return _tags;
  // ignore: implicit_dynamic_type
  return EqualUnmodifiableListView(_tags);
}

@override@JsonKey(name: 'order_index') final  int orderIndex;

/// Create a copy of InterestModel
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$InterestModelCopyWith<_InterestModel> get copyWith => __$InterestModelCopyWithImpl<_InterestModel>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$InterestModelToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _InterestModel&&(identical(other.id, id) || other.id == id)&&(identical(other.category, category) || other.category == category)&&(identical(other.code, code) || other.code == code)&&(identical(other.labelEn, labelEn) || other.labelEn == labelEn)&&(identical(other.labelKo, labelKo) || other.labelKo == labelKo)&&(identical(other.icon, icon) || other.icon == icon)&&(identical(other.color, color) || other.color == color)&&const DeepCollectionEquality().equals(other._tags, _tags)&&(identical(other.orderIndex, orderIndex) || other.orderIndex == orderIndex));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,category,code,labelEn,labelKo,icon,color,const DeepCollectionEquality().hash(_tags),orderIndex);

@override
String toString() {
  return 'InterestModel(id: $id, category: $category, code: $code, labelEn: $labelEn, labelKo: $labelKo, icon: $icon, color: $color, tags: $tags, orderIndex: $orderIndex)';
}


}

/// @nodoc
abstract mixin class _$InterestModelCopyWith<$Res> implements $InterestModelCopyWith<$Res> {
  factory _$InterestModelCopyWith(_InterestModel value, $Res Function(_InterestModel) _then) = __$InterestModelCopyWithImpl;
@override @useResult
$Res call({
 String id, String category, String code,@JsonKey(name: 'label_en') String labelEn,@JsonKey(name: 'label_ko') String labelKo, String? icon, String? color, List<String> tags,@JsonKey(name: 'order_index') int orderIndex
});




}
/// @nodoc
class __$InterestModelCopyWithImpl<$Res>
    implements _$InterestModelCopyWith<$Res> {
  __$InterestModelCopyWithImpl(this._self, this._then);

  final _InterestModel _self;
  final $Res Function(_InterestModel) _then;

/// Create a copy of InterestModel
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? category = null,Object? code = null,Object? labelEn = null,Object? labelKo = null,Object? icon = freezed,Object? color = freezed,Object? tags = null,Object? orderIndex = null,}) {
  return _then(_InterestModel(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,category: null == category ? _self.category : category // ignore: cast_nullable_to_non_nullable
as String,code: null == code ? _self.code : code // ignore: cast_nullable_to_non_nullable
as String,labelEn: null == labelEn ? _self.labelEn : labelEn // ignore: cast_nullable_to_non_nullable
as String,labelKo: null == labelKo ? _self.labelKo : labelKo // ignore: cast_nullable_to_non_nullable
as String,icon: freezed == icon ? _self.icon : icon // ignore: cast_nullable_to_non_nullable
as String?,color: freezed == color ? _self.color : color // ignore: cast_nullable_to_non_nullable
as String?,tags: null == tags ? _self._tags : tags // ignore: cast_nullable_to_non_nullable
as List<String>,orderIndex: null == orderIndex ? _self.orderIndex : orderIndex // ignore: cast_nullable_to_non_nullable
as int,
  ));
}


}

// dart format on
