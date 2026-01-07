// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'supabase_models.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$VocabCategory {

 String get id; String get title;@JsonKey(name: 'title_ko') String? get titleKo; String? get description;@JsonKey(name: 'image_url') String? get imageUrl; String? get icon; String get color;
/// Create a copy of VocabCategory
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$VocabCategoryCopyWith<VocabCategory> get copyWith => _$VocabCategoryCopyWithImpl<VocabCategory>(this as VocabCategory, _$identity);

  /// Serializes this VocabCategory to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is VocabCategory&&(identical(other.id, id) || other.id == id)&&(identical(other.title, title) || other.title == title)&&(identical(other.titleKo, titleKo) || other.titleKo == titleKo)&&(identical(other.description, description) || other.description == description)&&(identical(other.imageUrl, imageUrl) || other.imageUrl == imageUrl)&&(identical(other.icon, icon) || other.icon == icon)&&(identical(other.color, color) || other.color == color));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,title,titleKo,description,imageUrl,icon,color);

@override
String toString() {
  return 'VocabCategory(id: $id, title: $title, titleKo: $titleKo, description: $description, imageUrl: $imageUrl, icon: $icon, color: $color)';
}


}

/// @nodoc
abstract mixin class $VocabCategoryCopyWith<$Res>  {
  factory $VocabCategoryCopyWith(VocabCategory value, $Res Function(VocabCategory) _then) = _$VocabCategoryCopyWithImpl;
@useResult
$Res call({
 String id, String title,@JsonKey(name: 'title_ko') String? titleKo, String? description,@JsonKey(name: 'image_url') String? imageUrl, String? icon, String color
});




}
/// @nodoc
class _$VocabCategoryCopyWithImpl<$Res>
    implements $VocabCategoryCopyWith<$Res> {
  _$VocabCategoryCopyWithImpl(this._self, this._then);

  final VocabCategory _self;
  final $Res Function(VocabCategory) _then;

/// Create a copy of VocabCategory
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? title = null,Object? titleKo = freezed,Object? description = freezed,Object? imageUrl = freezed,Object? icon = freezed,Object? color = null,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,title: null == title ? _self.title : title // ignore: cast_nullable_to_non_nullable
as String,titleKo: freezed == titleKo ? _self.titleKo : titleKo // ignore: cast_nullable_to_non_nullable
as String?,description: freezed == description ? _self.description : description // ignore: cast_nullable_to_non_nullable
as String?,imageUrl: freezed == imageUrl ? _self.imageUrl : imageUrl // ignore: cast_nullable_to_non_nullable
as String?,icon: freezed == icon ? _self.icon : icon // ignore: cast_nullable_to_non_nullable
as String?,color: null == color ? _self.color : color // ignore: cast_nullable_to_non_nullable
as String,
  ));
}

}


/// Adds pattern-matching-related methods to [VocabCategory].
extension VocabCategoryPatterns on VocabCategory {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _VocabCategory value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _VocabCategory() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _VocabCategory value)  $default,){
final _that = this;
switch (_that) {
case _VocabCategory():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _VocabCategory value)?  $default,){
final _that = this;
switch (_that) {
case _VocabCategory() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id,  String title, @JsonKey(name: 'title_ko')  String? titleKo,  String? description, @JsonKey(name: 'image_url')  String? imageUrl,  String? icon,  String color)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _VocabCategory() when $default != null:
return $default(_that.id,_that.title,_that.titleKo,_that.description,_that.imageUrl,_that.icon,_that.color);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id,  String title, @JsonKey(name: 'title_ko')  String? titleKo,  String? description, @JsonKey(name: 'image_url')  String? imageUrl,  String? icon,  String color)  $default,) {final _that = this;
switch (_that) {
case _VocabCategory():
return $default(_that.id,_that.title,_that.titleKo,_that.description,_that.imageUrl,_that.icon,_that.color);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id,  String title, @JsonKey(name: 'title_ko')  String? titleKo,  String? description, @JsonKey(name: 'image_url')  String? imageUrl,  String? icon,  String color)?  $default,) {final _that = this;
switch (_that) {
case _VocabCategory() when $default != null:
return $default(_that.id,_that.title,_that.titleKo,_that.description,_that.imageUrl,_that.icon,_that.color);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _VocabCategory implements VocabCategory {
  const _VocabCategory({required this.id, required this.title, @JsonKey(name: 'title_ko') this.titleKo, this.description, @JsonKey(name: 'image_url') this.imageUrl, this.icon, this.color = '#4A90E2'});
  factory _VocabCategory.fromJson(Map<String, dynamic> json) => _$VocabCategoryFromJson(json);

@override final  String id;
@override final  String title;
@override@JsonKey(name: 'title_ko') final  String? titleKo;
@override final  String? description;
@override@JsonKey(name: 'image_url') final  String? imageUrl;
@override final  String? icon;
@override@JsonKey() final  String color;

/// Create a copy of VocabCategory
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$VocabCategoryCopyWith<_VocabCategory> get copyWith => __$VocabCategoryCopyWithImpl<_VocabCategory>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$VocabCategoryToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _VocabCategory&&(identical(other.id, id) || other.id == id)&&(identical(other.title, title) || other.title == title)&&(identical(other.titleKo, titleKo) || other.titleKo == titleKo)&&(identical(other.description, description) || other.description == description)&&(identical(other.imageUrl, imageUrl) || other.imageUrl == imageUrl)&&(identical(other.icon, icon) || other.icon == icon)&&(identical(other.color, color) || other.color == color));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,title,titleKo,description,imageUrl,icon,color);

@override
String toString() {
  return 'VocabCategory(id: $id, title: $title, titleKo: $titleKo, description: $description, imageUrl: $imageUrl, icon: $icon, color: $color)';
}


}

/// @nodoc
abstract mixin class _$VocabCategoryCopyWith<$Res> implements $VocabCategoryCopyWith<$Res> {
  factory _$VocabCategoryCopyWith(_VocabCategory value, $Res Function(_VocabCategory) _then) = __$VocabCategoryCopyWithImpl;
@override @useResult
$Res call({
 String id, String title,@JsonKey(name: 'title_ko') String? titleKo, String? description,@JsonKey(name: 'image_url') String? imageUrl, String? icon, String color
});




}
/// @nodoc
class __$VocabCategoryCopyWithImpl<$Res>
    implements _$VocabCategoryCopyWith<$Res> {
  __$VocabCategoryCopyWithImpl(this._self, this._then);

  final _VocabCategory _self;
  final $Res Function(_VocabCategory) _then;

/// Create a copy of VocabCategory
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? title = null,Object? titleKo = freezed,Object? description = freezed,Object? imageUrl = freezed,Object? icon = freezed,Object? color = null,}) {
  return _then(_VocabCategory(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,title: null == title ? _self.title : title // ignore: cast_nullable_to_non_nullable
as String,titleKo: freezed == titleKo ? _self.titleKo : titleKo // ignore: cast_nullable_to_non_nullable
as String?,description: freezed == description ? _self.description : description // ignore: cast_nullable_to_non_nullable
as String?,imageUrl: freezed == imageUrl ? _self.imageUrl : imageUrl // ignore: cast_nullable_to_non_nullable
as String?,icon: freezed == icon ? _self.icon : icon // ignore: cast_nullable_to_non_nullable
as String?,color: null == color ? _self.color : color // ignore: cast_nullable_to_non_nullable
as String,
  ));
}


}


/// @nodoc
mixin _$VocabDeck {

 String get id;@JsonKey(name: 'category_id') String get categoryId; String get title;@JsonKey(name: 'title_ko') String? get titleKo;@JsonKey(name: 'order_index') int get orderIndex; String get color; String? get icon;@JsonKey(readValue: _readCardCount) int get cardCount;
/// Create a copy of VocabDeck
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$VocabDeckCopyWith<VocabDeck> get copyWith => _$VocabDeckCopyWithImpl<VocabDeck>(this as VocabDeck, _$identity);

  /// Serializes this VocabDeck to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is VocabDeck&&(identical(other.id, id) || other.id == id)&&(identical(other.categoryId, categoryId) || other.categoryId == categoryId)&&(identical(other.title, title) || other.title == title)&&(identical(other.titleKo, titleKo) || other.titleKo == titleKo)&&(identical(other.orderIndex, orderIndex) || other.orderIndex == orderIndex)&&(identical(other.color, color) || other.color == color)&&(identical(other.icon, icon) || other.icon == icon)&&(identical(other.cardCount, cardCount) || other.cardCount == cardCount));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,categoryId,title,titleKo,orderIndex,color,icon,cardCount);

@override
String toString() {
  return 'VocabDeck(id: $id, categoryId: $categoryId, title: $title, titleKo: $titleKo, orderIndex: $orderIndex, color: $color, icon: $icon, cardCount: $cardCount)';
}


}

/// @nodoc
abstract mixin class $VocabDeckCopyWith<$Res>  {
  factory $VocabDeckCopyWith(VocabDeck value, $Res Function(VocabDeck) _then) = _$VocabDeckCopyWithImpl;
@useResult
$Res call({
 String id,@JsonKey(name: 'category_id') String categoryId, String title,@JsonKey(name: 'title_ko') String? titleKo,@JsonKey(name: 'order_index') int orderIndex, String color, String? icon,@JsonKey(readValue: _readCardCount) int cardCount
});




}
/// @nodoc
class _$VocabDeckCopyWithImpl<$Res>
    implements $VocabDeckCopyWith<$Res> {
  _$VocabDeckCopyWithImpl(this._self, this._then);

  final VocabDeck _self;
  final $Res Function(VocabDeck) _then;

/// Create a copy of VocabDeck
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? categoryId = null,Object? title = null,Object? titleKo = freezed,Object? orderIndex = null,Object? color = null,Object? icon = freezed,Object? cardCount = null,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,categoryId: null == categoryId ? _self.categoryId : categoryId // ignore: cast_nullable_to_non_nullable
as String,title: null == title ? _self.title : title // ignore: cast_nullable_to_non_nullable
as String,titleKo: freezed == titleKo ? _self.titleKo : titleKo // ignore: cast_nullable_to_non_nullable
as String?,orderIndex: null == orderIndex ? _self.orderIndex : orderIndex // ignore: cast_nullable_to_non_nullable
as int,color: null == color ? _self.color : color // ignore: cast_nullable_to_non_nullable
as String,icon: freezed == icon ? _self.icon : icon // ignore: cast_nullable_to_non_nullable
as String?,cardCount: null == cardCount ? _self.cardCount : cardCount // ignore: cast_nullable_to_non_nullable
as int,
  ));
}

}


/// Adds pattern-matching-related methods to [VocabDeck].
extension VocabDeckPatterns on VocabDeck {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _VocabDeck value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _VocabDeck() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _VocabDeck value)  $default,){
final _that = this;
switch (_that) {
case _VocabDeck():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _VocabDeck value)?  $default,){
final _that = this;
switch (_that) {
case _VocabDeck() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 'category_id')  String categoryId,  String title, @JsonKey(name: 'title_ko')  String? titleKo, @JsonKey(name: 'order_index')  int orderIndex,  String color,  String? icon, @JsonKey(readValue: _readCardCount)  int cardCount)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _VocabDeck() when $default != null:
return $default(_that.id,_that.categoryId,_that.title,_that.titleKo,_that.orderIndex,_that.color,_that.icon,_that.cardCount);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 'category_id')  String categoryId,  String title, @JsonKey(name: 'title_ko')  String? titleKo, @JsonKey(name: 'order_index')  int orderIndex,  String color,  String? icon, @JsonKey(readValue: _readCardCount)  int cardCount)  $default,) {final _that = this;
switch (_that) {
case _VocabDeck():
return $default(_that.id,_that.categoryId,_that.title,_that.titleKo,_that.orderIndex,_that.color,_that.icon,_that.cardCount);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id, @JsonKey(name: 'category_id')  String categoryId,  String title, @JsonKey(name: 'title_ko')  String? titleKo, @JsonKey(name: 'order_index')  int orderIndex,  String color,  String? icon, @JsonKey(readValue: _readCardCount)  int cardCount)?  $default,) {final _that = this;
switch (_that) {
case _VocabDeck() when $default != null:
return $default(_that.id,_that.categoryId,_that.title,_that.titleKo,_that.orderIndex,_that.color,_that.icon,_that.cardCount);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _VocabDeck implements VocabDeck {
  const _VocabDeck({required this.id, @JsonKey(name: 'category_id') required this.categoryId, required this.title, @JsonKey(name: 'title_ko') this.titleKo, @JsonKey(name: 'order_index') this.orderIndex = 0, this.color = '#FF5733', this.icon, @JsonKey(readValue: _readCardCount) this.cardCount = 0});
  factory _VocabDeck.fromJson(Map<String, dynamic> json) => _$VocabDeckFromJson(json);

@override final  String id;
@override@JsonKey(name: 'category_id') final  String categoryId;
@override final  String title;
@override@JsonKey(name: 'title_ko') final  String? titleKo;
@override@JsonKey(name: 'order_index') final  int orderIndex;
@override@JsonKey() final  String color;
@override final  String? icon;
@override@JsonKey(readValue: _readCardCount) final  int cardCount;

/// Create a copy of VocabDeck
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$VocabDeckCopyWith<_VocabDeck> get copyWith => __$VocabDeckCopyWithImpl<_VocabDeck>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$VocabDeckToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _VocabDeck&&(identical(other.id, id) || other.id == id)&&(identical(other.categoryId, categoryId) || other.categoryId == categoryId)&&(identical(other.title, title) || other.title == title)&&(identical(other.titleKo, titleKo) || other.titleKo == titleKo)&&(identical(other.orderIndex, orderIndex) || other.orderIndex == orderIndex)&&(identical(other.color, color) || other.color == color)&&(identical(other.icon, icon) || other.icon == icon)&&(identical(other.cardCount, cardCount) || other.cardCount == cardCount));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,categoryId,title,titleKo,orderIndex,color,icon,cardCount);

@override
String toString() {
  return 'VocabDeck(id: $id, categoryId: $categoryId, title: $title, titleKo: $titleKo, orderIndex: $orderIndex, color: $color, icon: $icon, cardCount: $cardCount)';
}


}

/// @nodoc
abstract mixin class _$VocabDeckCopyWith<$Res> implements $VocabDeckCopyWith<$Res> {
  factory _$VocabDeckCopyWith(_VocabDeck value, $Res Function(_VocabDeck) _then) = __$VocabDeckCopyWithImpl;
@override @useResult
$Res call({
 String id,@JsonKey(name: 'category_id') String categoryId, String title,@JsonKey(name: 'title_ko') String? titleKo,@JsonKey(name: 'order_index') int orderIndex, String color, String? icon,@JsonKey(readValue: _readCardCount) int cardCount
});




}
/// @nodoc
class __$VocabDeckCopyWithImpl<$Res>
    implements _$VocabDeckCopyWith<$Res> {
  __$VocabDeckCopyWithImpl(this._self, this._then);

  final _VocabDeck _self;
  final $Res Function(_VocabDeck) _then;

/// Create a copy of VocabDeck
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? categoryId = null,Object? title = null,Object? titleKo = freezed,Object? orderIndex = null,Object? color = null,Object? icon = freezed,Object? cardCount = null,}) {
  return _then(_VocabDeck(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,categoryId: null == categoryId ? _self.categoryId : categoryId // ignore: cast_nullable_to_non_nullable
as String,title: null == title ? _self.title : title // ignore: cast_nullable_to_non_nullable
as String,titleKo: freezed == titleKo ? _self.titleKo : titleKo // ignore: cast_nullable_to_non_nullable
as String?,orderIndex: null == orderIndex ? _self.orderIndex : orderIndex // ignore: cast_nullable_to_non_nullable
as int,color: null == color ? _self.color : color // ignore: cast_nullable_to_non_nullable
as String,icon: freezed == icon ? _self.icon : icon // ignore: cast_nullable_to_non_nullable
as String?,cardCount: null == cardCount ? _self.cardCount : cardCount // ignore: cast_nullable_to_non_nullable
as int,
  ));
}


}


/// @nodoc
mixin _$VocabCard {

 String get id;@JsonKey(name: 'deck_id') String get deckId;@JsonKey(name: 'front_text') String get frontText;@JsonKey(name: 'back_text') String get backText;@JsonKey(name: 'example_sentences') List<String> get exampleSentences;@JsonKey(name: 'audio_url') String? get audioUrl;
/// Create a copy of VocabCard
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$VocabCardCopyWith<VocabCard> get copyWith => _$VocabCardCopyWithImpl<VocabCard>(this as VocabCard, _$identity);

  /// Serializes this VocabCard to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is VocabCard&&(identical(other.id, id) || other.id == id)&&(identical(other.deckId, deckId) || other.deckId == deckId)&&(identical(other.frontText, frontText) || other.frontText == frontText)&&(identical(other.backText, backText) || other.backText == backText)&&const DeepCollectionEquality().equals(other.exampleSentences, exampleSentences)&&(identical(other.audioUrl, audioUrl) || other.audioUrl == audioUrl));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,deckId,frontText,backText,const DeepCollectionEquality().hash(exampleSentences),audioUrl);

@override
String toString() {
  return 'VocabCard(id: $id, deckId: $deckId, frontText: $frontText, backText: $backText, exampleSentences: $exampleSentences, audioUrl: $audioUrl)';
}


}

/// @nodoc
abstract mixin class $VocabCardCopyWith<$Res>  {
  factory $VocabCardCopyWith(VocabCard value, $Res Function(VocabCard) _then) = _$VocabCardCopyWithImpl;
@useResult
$Res call({
 String id,@JsonKey(name: 'deck_id') String deckId,@JsonKey(name: 'front_text') String frontText,@JsonKey(name: 'back_text') String backText,@JsonKey(name: 'example_sentences') List<String> exampleSentences,@JsonKey(name: 'audio_url') String? audioUrl
});




}
/// @nodoc
class _$VocabCardCopyWithImpl<$Res>
    implements $VocabCardCopyWith<$Res> {
  _$VocabCardCopyWithImpl(this._self, this._then);

  final VocabCard _self;
  final $Res Function(VocabCard) _then;

/// Create a copy of VocabCard
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? deckId = null,Object? frontText = null,Object? backText = null,Object? exampleSentences = null,Object? audioUrl = freezed,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,deckId: null == deckId ? _self.deckId : deckId // ignore: cast_nullable_to_non_nullable
as String,frontText: null == frontText ? _self.frontText : frontText // ignore: cast_nullable_to_non_nullable
as String,backText: null == backText ? _self.backText : backText // ignore: cast_nullable_to_non_nullable
as String,exampleSentences: null == exampleSentences ? _self.exampleSentences : exampleSentences // ignore: cast_nullable_to_non_nullable
as List<String>,audioUrl: freezed == audioUrl ? _self.audioUrl : audioUrl // ignore: cast_nullable_to_non_nullable
as String?,
  ));
}

}


/// Adds pattern-matching-related methods to [VocabCard].
extension VocabCardPatterns on VocabCard {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _VocabCard value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _VocabCard() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _VocabCard value)  $default,){
final _that = this;
switch (_that) {
case _VocabCard():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _VocabCard value)?  $default,){
final _that = this;
switch (_that) {
case _VocabCard() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 'deck_id')  String deckId, @JsonKey(name: 'front_text')  String frontText, @JsonKey(name: 'back_text')  String backText, @JsonKey(name: 'example_sentences')  List<String> exampleSentences, @JsonKey(name: 'audio_url')  String? audioUrl)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _VocabCard() when $default != null:
return $default(_that.id,_that.deckId,_that.frontText,_that.backText,_that.exampleSentences,_that.audioUrl);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id, @JsonKey(name: 'deck_id')  String deckId, @JsonKey(name: 'front_text')  String frontText, @JsonKey(name: 'back_text')  String backText, @JsonKey(name: 'example_sentences')  List<String> exampleSentences, @JsonKey(name: 'audio_url')  String? audioUrl)  $default,) {final _that = this;
switch (_that) {
case _VocabCard():
return $default(_that.id,_that.deckId,_that.frontText,_that.backText,_that.exampleSentences,_that.audioUrl);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id, @JsonKey(name: 'deck_id')  String deckId, @JsonKey(name: 'front_text')  String frontText, @JsonKey(name: 'back_text')  String backText, @JsonKey(name: 'example_sentences')  List<String> exampleSentences, @JsonKey(name: 'audio_url')  String? audioUrl)?  $default,) {final _that = this;
switch (_that) {
case _VocabCard() when $default != null:
return $default(_that.id,_that.deckId,_that.frontText,_that.backText,_that.exampleSentences,_that.audioUrl);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _VocabCard implements VocabCard {
  const _VocabCard({required this.id, @JsonKey(name: 'deck_id') required this.deckId, @JsonKey(name: 'front_text') required this.frontText, @JsonKey(name: 'back_text') required this.backText, @JsonKey(name: 'example_sentences') final  List<String> exampleSentences = const [], @JsonKey(name: 'audio_url') this.audioUrl}): _exampleSentences = exampleSentences;
  factory _VocabCard.fromJson(Map<String, dynamic> json) => _$VocabCardFromJson(json);

@override final  String id;
@override@JsonKey(name: 'deck_id') final  String deckId;
@override@JsonKey(name: 'front_text') final  String frontText;
@override@JsonKey(name: 'back_text') final  String backText;
 final  List<String> _exampleSentences;
@override@JsonKey(name: 'example_sentences') List<String> get exampleSentences {
  if (_exampleSentences is EqualUnmodifiableListView) return _exampleSentences;
  // ignore: implicit_dynamic_type
  return EqualUnmodifiableListView(_exampleSentences);
}

@override@JsonKey(name: 'audio_url') final  String? audioUrl;

/// Create a copy of VocabCard
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$VocabCardCopyWith<_VocabCard> get copyWith => __$VocabCardCopyWithImpl<_VocabCard>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$VocabCardToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _VocabCard&&(identical(other.id, id) || other.id == id)&&(identical(other.deckId, deckId) || other.deckId == deckId)&&(identical(other.frontText, frontText) || other.frontText == frontText)&&(identical(other.backText, backText) || other.backText == backText)&&const DeepCollectionEquality().equals(other._exampleSentences, _exampleSentences)&&(identical(other.audioUrl, audioUrl) || other.audioUrl == audioUrl));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,deckId,frontText,backText,const DeepCollectionEquality().hash(_exampleSentences),audioUrl);

@override
String toString() {
  return 'VocabCard(id: $id, deckId: $deckId, frontText: $frontText, backText: $backText, exampleSentences: $exampleSentences, audioUrl: $audioUrl)';
}


}

/// @nodoc
abstract mixin class _$VocabCardCopyWith<$Res> implements $VocabCardCopyWith<$Res> {
  factory _$VocabCardCopyWith(_VocabCard value, $Res Function(_VocabCard) _then) = __$VocabCardCopyWithImpl;
@override @useResult
$Res call({
 String id,@JsonKey(name: 'deck_id') String deckId,@JsonKey(name: 'front_text') String frontText,@JsonKey(name: 'back_text') String backText,@JsonKey(name: 'example_sentences') List<String> exampleSentences,@JsonKey(name: 'audio_url') String? audioUrl
});




}
/// @nodoc
class __$VocabCardCopyWithImpl<$Res>
    implements _$VocabCardCopyWith<$Res> {
  __$VocabCardCopyWithImpl(this._self, this._then);

  final _VocabCard _self;
  final $Res Function(_VocabCard) _then;

/// Create a copy of VocabCard
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? deckId = null,Object? frontText = null,Object? backText = null,Object? exampleSentences = null,Object? audioUrl = freezed,}) {
  return _then(_VocabCard(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,deckId: null == deckId ? _self.deckId : deckId // ignore: cast_nullable_to_non_nullable
as String,frontText: null == frontText ? _self.frontText : frontText // ignore: cast_nullable_to_non_nullable
as String,backText: null == backText ? _self.backText : backText // ignore: cast_nullable_to_non_nullable
as String,exampleSentences: null == exampleSentences ? _self._exampleSentences : exampleSentences // ignore: cast_nullable_to_non_nullable
as List<String>,audioUrl: freezed == audioUrl ? _self.audioUrl : audioUrl // ignore: cast_nullable_to_non_nullable
as String?,
  ));
}


}


/// @nodoc
mixin _$VocabContext {

 String get id; String get type;// place, emotion, environment
 String get slug; String get label; String? get icon;@JsonKey(name: 'prompt_description') String? get promptDescription;
/// Create a copy of VocabContext
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$VocabContextCopyWith<VocabContext> get copyWith => _$VocabContextCopyWithImpl<VocabContext>(this as VocabContext, _$identity);

  /// Serializes this VocabContext to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is VocabContext&&(identical(other.id, id) || other.id == id)&&(identical(other.type, type) || other.type == type)&&(identical(other.slug, slug) || other.slug == slug)&&(identical(other.label, label) || other.label == label)&&(identical(other.icon, icon) || other.icon == icon)&&(identical(other.promptDescription, promptDescription) || other.promptDescription == promptDescription));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,type,slug,label,icon,promptDescription);

@override
String toString() {
  return 'VocabContext(id: $id, type: $type, slug: $slug, label: $label, icon: $icon, promptDescription: $promptDescription)';
}


}

/// @nodoc
abstract mixin class $VocabContextCopyWith<$Res>  {
  factory $VocabContextCopyWith(VocabContext value, $Res Function(VocabContext) _then) = _$VocabContextCopyWithImpl;
@useResult
$Res call({
 String id, String type, String slug, String label, String? icon,@JsonKey(name: 'prompt_description') String? promptDescription
});




}
/// @nodoc
class _$VocabContextCopyWithImpl<$Res>
    implements $VocabContextCopyWith<$Res> {
  _$VocabContextCopyWithImpl(this._self, this._then);

  final VocabContext _self;
  final $Res Function(VocabContext) _then;

/// Create a copy of VocabContext
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? type = null,Object? slug = null,Object? label = null,Object? icon = freezed,Object? promptDescription = freezed,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,type: null == type ? _self.type : type // ignore: cast_nullable_to_non_nullable
as String,slug: null == slug ? _self.slug : slug // ignore: cast_nullable_to_non_nullable
as String,label: null == label ? _self.label : label // ignore: cast_nullable_to_non_nullable
as String,icon: freezed == icon ? _self.icon : icon // ignore: cast_nullable_to_non_nullable
as String?,promptDescription: freezed == promptDescription ? _self.promptDescription : promptDescription // ignore: cast_nullable_to_non_nullable
as String?,
  ));
}

}


/// Adds pattern-matching-related methods to [VocabContext].
extension VocabContextPatterns on VocabContext {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _VocabContext value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _VocabContext() when $default != null:
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

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _VocabContext value)  $default,){
final _that = this;
switch (_that) {
case _VocabContext():
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _VocabContext value)?  $default,){
final _that = this;
switch (_that) {
case _VocabContext() when $default != null:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id,  String type,  String slug,  String label,  String? icon, @JsonKey(name: 'prompt_description')  String? promptDescription)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _VocabContext() when $default != null:
return $default(_that.id,_that.type,_that.slug,_that.label,_that.icon,_that.promptDescription);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id,  String type,  String slug,  String label,  String? icon, @JsonKey(name: 'prompt_description')  String? promptDescription)  $default,) {final _that = this;
switch (_that) {
case _VocabContext():
return $default(_that.id,_that.type,_that.slug,_that.label,_that.icon,_that.promptDescription);case _:
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id,  String type,  String slug,  String label,  String? icon, @JsonKey(name: 'prompt_description')  String? promptDescription)?  $default,) {final _that = this;
switch (_that) {
case _VocabContext() when $default != null:
return $default(_that.id,_that.type,_that.slug,_that.label,_that.icon,_that.promptDescription);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _VocabContext implements VocabContext {
  const _VocabContext({required this.id, required this.type, required this.slug, required this.label, this.icon, @JsonKey(name: 'prompt_description') this.promptDescription});
  factory _VocabContext.fromJson(Map<String, dynamic> json) => _$VocabContextFromJson(json);

@override final  String id;
@override final  String type;
// place, emotion, environment
@override final  String slug;
@override final  String label;
@override final  String? icon;
@override@JsonKey(name: 'prompt_description') final  String? promptDescription;

/// Create a copy of VocabContext
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$VocabContextCopyWith<_VocabContext> get copyWith => __$VocabContextCopyWithImpl<_VocabContext>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$VocabContextToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _VocabContext&&(identical(other.id, id) || other.id == id)&&(identical(other.type, type) || other.type == type)&&(identical(other.slug, slug) || other.slug == slug)&&(identical(other.label, label) || other.label == label)&&(identical(other.icon, icon) || other.icon == icon)&&(identical(other.promptDescription, promptDescription) || other.promptDescription == promptDescription));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,type,slug,label,icon,promptDescription);

@override
String toString() {
  return 'VocabContext(id: $id, type: $type, slug: $slug, label: $label, icon: $icon, promptDescription: $promptDescription)';
}


}

/// @nodoc
abstract mixin class _$VocabContextCopyWith<$Res> implements $VocabContextCopyWith<$Res> {
  factory _$VocabContextCopyWith(_VocabContext value, $Res Function(_VocabContext) _then) = __$VocabContextCopyWithImpl;
@override @useResult
$Res call({
 String id, String type, String slug, String label, String? icon,@JsonKey(name: 'prompt_description') String? promptDescription
});




}
/// @nodoc
class __$VocabContextCopyWithImpl<$Res>
    implements _$VocabContextCopyWith<$Res> {
  __$VocabContextCopyWithImpl(this._self, this._then);

  final _VocabContext _self;
  final $Res Function(_VocabContext) _then;

/// Create a copy of VocabContext
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? type = null,Object? slug = null,Object? label = null,Object? icon = freezed,Object? promptDescription = freezed,}) {
  return _then(_VocabContext(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,type: null == type ? _self.type : type // ignore: cast_nullable_to_non_nullable
as String,slug: null == slug ? _self.slug : slug // ignore: cast_nullable_to_non_nullable
as String,label: null == label ? _self.label : label // ignore: cast_nullable_to_non_nullable
as String,icon: freezed == icon ? _self.icon : icon // ignore: cast_nullable_to_non_nullable
as String?,promptDescription: freezed == promptDescription ? _self.promptDescription : promptDescription // ignore: cast_nullable_to_non_nullable
as String?,
  ));
}


}

// dart format on
