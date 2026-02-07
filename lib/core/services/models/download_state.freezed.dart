// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'download_state.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;
/// @nodoc
mixin _$DownloadState {





@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is DownloadState);
}


@override
int get hashCode => runtimeType.hashCode;

@override
String toString() {
  return 'DownloadState()';
}


}

/// @nodoc
class $DownloadStateCopyWith<$Res>  {
$DownloadStateCopyWith(DownloadState _, $Res Function(DownloadState) __);
}


/// Adds pattern-matching-related methods to [DownloadState].
extension DownloadStatePatterns on DownloadState {
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

@optionalTypeArgs TResult maybeMap<TResult extends Object?>({TResult Function( NotDownloaded value)?  notDownloaded,TResult Function( Downloading value)?  downloading,TResult Function( Downloaded value)?  downloaded,TResult Function( DownloadError value)?  error,required TResult orElse(),}){
final _that = this;
switch (_that) {
case NotDownloaded() when notDownloaded != null:
return notDownloaded(_that);case Downloading() when downloading != null:
return downloading(_that);case Downloaded() when downloaded != null:
return downloaded(_that);case DownloadError() when error != null:
return error(_that);case _:
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

@optionalTypeArgs TResult map<TResult extends Object?>({required TResult Function( NotDownloaded value)  notDownloaded,required TResult Function( Downloading value)  downloading,required TResult Function( Downloaded value)  downloaded,required TResult Function( DownloadError value)  error,}){
final _that = this;
switch (_that) {
case NotDownloaded():
return notDownloaded(_that);case Downloading():
return downloading(_that);case Downloaded():
return downloaded(_that);case DownloadError():
return error(_that);}
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

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>({TResult? Function( NotDownloaded value)?  notDownloaded,TResult? Function( Downloading value)?  downloading,TResult? Function( Downloaded value)?  downloaded,TResult? Function( DownloadError value)?  error,}){
final _that = this;
switch (_that) {
case NotDownloaded() when notDownloaded != null:
return notDownloaded(_that);case Downloading() when downloading != null:
return downloading(_that);case Downloaded() when downloaded != null:
return downloaded(_that);case DownloadError() when error != null:
return error(_that);case _:
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

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>({TResult Function()?  notDownloaded,TResult Function( double progress)?  downloading,TResult Function()?  downloaded,TResult Function( String message)?  error,required TResult orElse(),}) {final _that = this;
switch (_that) {
case NotDownloaded() when notDownloaded != null:
return notDownloaded();case Downloading() when downloading != null:
return downloading(_that.progress);case Downloaded() when downloaded != null:
return downloaded();case DownloadError() when error != null:
return error(_that.message);case _:
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

@optionalTypeArgs TResult when<TResult extends Object?>({required TResult Function()  notDownloaded,required TResult Function( double progress)  downloading,required TResult Function()  downloaded,required TResult Function( String message)  error,}) {final _that = this;
switch (_that) {
case NotDownloaded():
return notDownloaded();case Downloading():
return downloading(_that.progress);case Downloaded():
return downloaded();case DownloadError():
return error(_that.message);}
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

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>({TResult? Function()?  notDownloaded,TResult? Function( double progress)?  downloading,TResult? Function()?  downloaded,TResult? Function( String message)?  error,}) {final _that = this;
switch (_that) {
case NotDownloaded() when notDownloaded != null:
return notDownloaded();case Downloading() when downloading != null:
return downloading(_that.progress);case Downloaded() when downloaded != null:
return downloaded();case DownloadError() when error != null:
return error(_that.message);case _:
  return null;

}
}

}

/// @nodoc


class NotDownloaded implements DownloadState {
  const NotDownloaded();
  






@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is NotDownloaded);
}


@override
int get hashCode => runtimeType.hashCode;

@override
String toString() {
  return 'DownloadState.notDownloaded()';
}


}




/// @nodoc


class Downloading implements DownloadState {
  const Downloading(this.progress);
  

 final  double progress;

/// Create a copy of DownloadState
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$DownloadingCopyWith<Downloading> get copyWith => _$DownloadingCopyWithImpl<Downloading>(this, _$identity);



@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is Downloading&&(identical(other.progress, progress) || other.progress == progress));
}


@override
int get hashCode => Object.hash(runtimeType,progress);

@override
String toString() {
  return 'DownloadState.downloading(progress: $progress)';
}


}

/// @nodoc
abstract mixin class $DownloadingCopyWith<$Res> implements $DownloadStateCopyWith<$Res> {
  factory $DownloadingCopyWith(Downloading value, $Res Function(Downloading) _then) = _$DownloadingCopyWithImpl;
@useResult
$Res call({
 double progress
});




}
/// @nodoc
class _$DownloadingCopyWithImpl<$Res>
    implements $DownloadingCopyWith<$Res> {
  _$DownloadingCopyWithImpl(this._self, this._then);

  final Downloading _self;
  final $Res Function(Downloading) _then;

/// Create a copy of DownloadState
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') $Res call({Object? progress = null,}) {
  return _then(Downloading(
null == progress ? _self.progress : progress // ignore: cast_nullable_to_non_nullable
as double,
  ));
}


}

/// @nodoc


class Downloaded implements DownloadState {
  const Downloaded();
  






@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is Downloaded);
}


@override
int get hashCode => runtimeType.hashCode;

@override
String toString() {
  return 'DownloadState.downloaded()';
}


}




/// @nodoc


class DownloadError implements DownloadState {
  const DownloadError(this.message);
  

 final  String message;

/// Create a copy of DownloadState
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$DownloadErrorCopyWith<DownloadError> get copyWith => _$DownloadErrorCopyWithImpl<DownloadError>(this, _$identity);



@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is DownloadError&&(identical(other.message, message) || other.message == message));
}


@override
int get hashCode => Object.hash(runtimeType,message);

@override
String toString() {
  return 'DownloadState.error(message: $message)';
}


}

/// @nodoc
abstract mixin class $DownloadErrorCopyWith<$Res> implements $DownloadStateCopyWith<$Res> {
  factory $DownloadErrorCopyWith(DownloadError value, $Res Function(DownloadError) _then) = _$DownloadErrorCopyWithImpl;
@useResult
$Res call({
 String message
});




}
/// @nodoc
class _$DownloadErrorCopyWithImpl<$Res>
    implements $DownloadErrorCopyWith<$Res> {
  _$DownloadErrorCopyWithImpl(this._self, this._then);

  final DownloadError _self;
  final $Res Function(DownloadError) _then;

/// Create a copy of DownloadState
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') $Res call({Object? message = null,}) {
  return _then(DownloadError(
null == message ? _self.message : message // ignore: cast_nullable_to_non_nullable
as String,
  ));
}


}

// dart format on
