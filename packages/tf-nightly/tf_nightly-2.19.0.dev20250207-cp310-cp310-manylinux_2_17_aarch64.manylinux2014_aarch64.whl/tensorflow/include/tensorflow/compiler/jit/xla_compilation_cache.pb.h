// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/compiler/jit/xla_compilation_cache.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcompiler_2fjit_2fxla_5fcompilation_5fcache_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcompiler_2fjit_2fxla_5fcompilation_5fcache_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021009 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
#include "xla/service/hlo.pb.h"
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcompiler_2fjit_2fxla_5fcompilation_5fcache_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2fcompiler_2fjit_2fxla_5fcompilation_5fcache_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcompiler_2fjit_2fxla_5fcompilation_5fcache_2eproto;
namespace tensorflow {
class XlaSerializedCacheEntry;
struct XlaSerializedCacheEntryDefaultTypeInternal;
extern XlaSerializedCacheEntryDefaultTypeInternal _XlaSerializedCacheEntry_default_instance_;
class XlaSerializedCacheKey;
struct XlaSerializedCacheKeyDefaultTypeInternal;
extern XlaSerializedCacheKeyDefaultTypeInternal _XlaSerializedCacheKey_default_instance_;
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::tensorflow::XlaSerializedCacheEntry* Arena::CreateMaybeMessage<::tensorflow::XlaSerializedCacheEntry>(Arena*);
template<> ::tensorflow::XlaSerializedCacheKey* Arena::CreateMaybeMessage<::tensorflow::XlaSerializedCacheKey>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {

// ===================================================================

class XlaSerializedCacheKey final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.XlaSerializedCacheKey) */ {
 public:
  inline XlaSerializedCacheKey() : XlaSerializedCacheKey(nullptr) {}
  ~XlaSerializedCacheKey() override;
  explicit PROTOBUF_CONSTEXPR XlaSerializedCacheKey(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  XlaSerializedCacheKey(const XlaSerializedCacheKey& from);
  XlaSerializedCacheKey(XlaSerializedCacheKey&& from) noexcept
    : XlaSerializedCacheKey() {
    *this = ::std::move(from);
  }

  inline XlaSerializedCacheKey& operator=(const XlaSerializedCacheKey& from) {
    CopyFrom(from);
    return *this;
  }
  inline XlaSerializedCacheKey& operator=(XlaSerializedCacheKey&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const XlaSerializedCacheKey& default_instance() {
    return *internal_default_instance();
  }
  static inline const XlaSerializedCacheKey* internal_default_instance() {
    return reinterpret_cast<const XlaSerializedCacheKey*>(
               &_XlaSerializedCacheKey_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(XlaSerializedCacheKey& a, XlaSerializedCacheKey& b) {
    a.Swap(&b);
  }
  inline void Swap(XlaSerializedCacheKey* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(XlaSerializedCacheKey* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  XlaSerializedCacheKey* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<XlaSerializedCacheKey>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const XlaSerializedCacheKey& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const XlaSerializedCacheKey& from) {
    XlaSerializedCacheKey::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(XlaSerializedCacheKey* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.XlaSerializedCacheKey";
  }
  protected:
  explicit XlaSerializedCacheKey(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kDeviceTypeFieldNumber = 3,
    kPrefixFieldNumber = 4,
    kSignatureFingerprintFieldNumber = 1,
    kClusterFingerprintFieldNumber = 2,
    kCompiledUsingPjrtFieldNumber = 5,
  };
  // string device_type = 3;
  void clear_device_type();
  const std::string& device_type() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_device_type(ArgT0&& arg0, ArgT... args);
  std::string* mutable_device_type();
  PROTOBUF_NODISCARD std::string* release_device_type();
  void set_allocated_device_type(std::string* device_type);
  private:
  const std::string& _internal_device_type() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_device_type(const std::string& value);
  std::string* _internal_mutable_device_type();
  public:

  // string prefix = 4;
  void clear_prefix();
  const std::string& prefix() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_prefix(ArgT0&& arg0, ArgT... args);
  std::string* mutable_prefix();
  PROTOBUF_NODISCARD std::string* release_prefix();
  void set_allocated_prefix(std::string* prefix);
  private:
  const std::string& _internal_prefix() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_prefix(const std::string& value);
  std::string* _internal_mutable_prefix();
  public:

  // uint64 signature_fingerprint = 1;
  void clear_signature_fingerprint();
  uint64_t signature_fingerprint() const;
  void set_signature_fingerprint(uint64_t value);
  private:
  uint64_t _internal_signature_fingerprint() const;
  void _internal_set_signature_fingerprint(uint64_t value);
  public:

  // uint64 cluster_fingerprint = 2;
  void clear_cluster_fingerprint();
  uint64_t cluster_fingerprint() const;
  void set_cluster_fingerprint(uint64_t value);
  private:
  uint64_t _internal_cluster_fingerprint() const;
  void _internal_set_cluster_fingerprint(uint64_t value);
  public:

  // bool compiled_using_pjrt = 5;
  void clear_compiled_using_pjrt();
  bool compiled_using_pjrt() const;
  void set_compiled_using_pjrt(bool value);
  private:
  bool _internal_compiled_using_pjrt() const;
  void _internal_set_compiled_using_pjrt(bool value);
  public:

  // @@protoc_insertion_point(class_scope:tensorflow.XlaSerializedCacheKey)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr device_type_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr prefix_;
    uint64_t signature_fingerprint_;
    uint64_t cluster_fingerprint_;
    bool compiled_using_pjrt_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcompiler_2fjit_2fxla_5fcompilation_5fcache_2eproto;
};
// -------------------------------------------------------------------

class XlaSerializedCacheEntry final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.XlaSerializedCacheEntry) */ {
 public:
  inline XlaSerializedCacheEntry() : XlaSerializedCacheEntry(nullptr) {}
  ~XlaSerializedCacheEntry() override;
  explicit PROTOBUF_CONSTEXPR XlaSerializedCacheEntry(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  XlaSerializedCacheEntry(const XlaSerializedCacheEntry& from);
  XlaSerializedCacheEntry(XlaSerializedCacheEntry&& from) noexcept
    : XlaSerializedCacheEntry() {
    *this = ::std::move(from);
  }

  inline XlaSerializedCacheEntry& operator=(const XlaSerializedCacheEntry& from) {
    CopyFrom(from);
    return *this;
  }
  inline XlaSerializedCacheEntry& operator=(XlaSerializedCacheEntry&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const XlaSerializedCacheEntry& default_instance() {
    return *internal_default_instance();
  }
  static inline const XlaSerializedCacheEntry* internal_default_instance() {
    return reinterpret_cast<const XlaSerializedCacheEntry*>(
               &_XlaSerializedCacheEntry_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(XlaSerializedCacheEntry& a, XlaSerializedCacheEntry& b) {
    a.Swap(&b);
  }
  inline void Swap(XlaSerializedCacheEntry* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(XlaSerializedCacheEntry* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  XlaSerializedCacheEntry* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<XlaSerializedCacheEntry>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const XlaSerializedCacheEntry& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const XlaSerializedCacheEntry& from) {
    XlaSerializedCacheEntry::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(XlaSerializedCacheEntry* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.XlaSerializedCacheEntry";
  }
  protected:
  explicit XlaSerializedCacheEntry(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kExecutableFieldNumber = 3,
    kKeyFieldNumber = 1,
    kHloModuleFieldNumber = 2,
  };
  // bytes executable = 3;
  void clear_executable();
  const std::string& executable() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_executable(ArgT0&& arg0, ArgT... args);
  std::string* mutable_executable();
  PROTOBUF_NODISCARD std::string* release_executable();
  void set_allocated_executable(std::string* executable);
  private:
  const std::string& _internal_executable() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_executable(const std::string& value);
  std::string* _internal_mutable_executable();
  public:

  // .tensorflow.XlaSerializedCacheKey key = 1;
  bool has_key() const;
  private:
  bool _internal_has_key() const;
  public:
  void clear_key();
  const ::tensorflow::XlaSerializedCacheKey& key() const;
  PROTOBUF_NODISCARD ::tensorflow::XlaSerializedCacheKey* release_key();
  ::tensorflow::XlaSerializedCacheKey* mutable_key();
  void set_allocated_key(::tensorflow::XlaSerializedCacheKey* key);
  private:
  const ::tensorflow::XlaSerializedCacheKey& _internal_key() const;
  ::tensorflow::XlaSerializedCacheKey* _internal_mutable_key();
  public:
  void unsafe_arena_set_allocated_key(
      ::tensorflow::XlaSerializedCacheKey* key);
  ::tensorflow::XlaSerializedCacheKey* unsafe_arena_release_key();

  // .xla.HloModuleProto hlo_module = 2;
  bool has_hlo_module() const;
  private:
  bool _internal_has_hlo_module() const;
  public:
  void clear_hlo_module();
  const ::xla::HloModuleProto& hlo_module() const;
  PROTOBUF_NODISCARD ::xla::HloModuleProto* release_hlo_module();
  ::xla::HloModuleProto* mutable_hlo_module();
  void set_allocated_hlo_module(::xla::HloModuleProto* hlo_module);
  private:
  const ::xla::HloModuleProto& _internal_hlo_module() const;
  ::xla::HloModuleProto* _internal_mutable_hlo_module();
  public:
  void unsafe_arena_set_allocated_hlo_module(
      ::xla::HloModuleProto* hlo_module);
  ::xla::HloModuleProto* unsafe_arena_release_hlo_module();

  // @@protoc_insertion_point(class_scope:tensorflow.XlaSerializedCacheEntry)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr executable_;
    ::tensorflow::XlaSerializedCacheKey* key_;
    ::xla::HloModuleProto* hlo_module_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcompiler_2fjit_2fxla_5fcompilation_5fcache_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// XlaSerializedCacheKey

// uint64 signature_fingerprint = 1;
inline void XlaSerializedCacheKey::clear_signature_fingerprint() {
  _impl_.signature_fingerprint_ = uint64_t{0u};
}
inline uint64_t XlaSerializedCacheKey::_internal_signature_fingerprint() const {
  return _impl_.signature_fingerprint_;
}
inline uint64_t XlaSerializedCacheKey::signature_fingerprint() const {
  // @@protoc_insertion_point(field_get:tensorflow.XlaSerializedCacheKey.signature_fingerprint)
  return _internal_signature_fingerprint();
}
inline void XlaSerializedCacheKey::_internal_set_signature_fingerprint(uint64_t value) {
  
  _impl_.signature_fingerprint_ = value;
}
inline void XlaSerializedCacheKey::set_signature_fingerprint(uint64_t value) {
  _internal_set_signature_fingerprint(value);
  // @@protoc_insertion_point(field_set:tensorflow.XlaSerializedCacheKey.signature_fingerprint)
}

// uint64 cluster_fingerprint = 2;
inline void XlaSerializedCacheKey::clear_cluster_fingerprint() {
  _impl_.cluster_fingerprint_ = uint64_t{0u};
}
inline uint64_t XlaSerializedCacheKey::_internal_cluster_fingerprint() const {
  return _impl_.cluster_fingerprint_;
}
inline uint64_t XlaSerializedCacheKey::cluster_fingerprint() const {
  // @@protoc_insertion_point(field_get:tensorflow.XlaSerializedCacheKey.cluster_fingerprint)
  return _internal_cluster_fingerprint();
}
inline void XlaSerializedCacheKey::_internal_set_cluster_fingerprint(uint64_t value) {
  
  _impl_.cluster_fingerprint_ = value;
}
inline void XlaSerializedCacheKey::set_cluster_fingerprint(uint64_t value) {
  _internal_set_cluster_fingerprint(value);
  // @@protoc_insertion_point(field_set:tensorflow.XlaSerializedCacheKey.cluster_fingerprint)
}

// string device_type = 3;
inline void XlaSerializedCacheKey::clear_device_type() {
  _impl_.device_type_.ClearToEmpty();
}
inline const std::string& XlaSerializedCacheKey::device_type() const {
  // @@protoc_insertion_point(field_get:tensorflow.XlaSerializedCacheKey.device_type)
  return _internal_device_type();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void XlaSerializedCacheKey::set_device_type(ArgT0&& arg0, ArgT... args) {
 
 _impl_.device_type_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.XlaSerializedCacheKey.device_type)
}
inline std::string* XlaSerializedCacheKey::mutable_device_type() {
  std::string* _s = _internal_mutable_device_type();
  // @@protoc_insertion_point(field_mutable:tensorflow.XlaSerializedCacheKey.device_type)
  return _s;
}
inline const std::string& XlaSerializedCacheKey::_internal_device_type() const {
  return _impl_.device_type_.Get();
}
inline void XlaSerializedCacheKey::_internal_set_device_type(const std::string& value) {
  
  _impl_.device_type_.Set(value, GetArenaForAllocation());
}
inline std::string* XlaSerializedCacheKey::_internal_mutable_device_type() {
  
  return _impl_.device_type_.Mutable(GetArenaForAllocation());
}
inline std::string* XlaSerializedCacheKey::release_device_type() {
  // @@protoc_insertion_point(field_release:tensorflow.XlaSerializedCacheKey.device_type)
  return _impl_.device_type_.Release();
}
inline void XlaSerializedCacheKey::set_allocated_device_type(std::string* device_type) {
  if (device_type != nullptr) {
    
  } else {
    
  }
  _impl_.device_type_.SetAllocated(device_type, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.device_type_.IsDefault()) {
    _impl_.device_type_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.XlaSerializedCacheKey.device_type)
}

// string prefix = 4;
inline void XlaSerializedCacheKey::clear_prefix() {
  _impl_.prefix_.ClearToEmpty();
}
inline const std::string& XlaSerializedCacheKey::prefix() const {
  // @@protoc_insertion_point(field_get:tensorflow.XlaSerializedCacheKey.prefix)
  return _internal_prefix();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void XlaSerializedCacheKey::set_prefix(ArgT0&& arg0, ArgT... args) {
 
 _impl_.prefix_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.XlaSerializedCacheKey.prefix)
}
inline std::string* XlaSerializedCacheKey::mutable_prefix() {
  std::string* _s = _internal_mutable_prefix();
  // @@protoc_insertion_point(field_mutable:tensorflow.XlaSerializedCacheKey.prefix)
  return _s;
}
inline const std::string& XlaSerializedCacheKey::_internal_prefix() const {
  return _impl_.prefix_.Get();
}
inline void XlaSerializedCacheKey::_internal_set_prefix(const std::string& value) {
  
  _impl_.prefix_.Set(value, GetArenaForAllocation());
}
inline std::string* XlaSerializedCacheKey::_internal_mutable_prefix() {
  
  return _impl_.prefix_.Mutable(GetArenaForAllocation());
}
inline std::string* XlaSerializedCacheKey::release_prefix() {
  // @@protoc_insertion_point(field_release:tensorflow.XlaSerializedCacheKey.prefix)
  return _impl_.prefix_.Release();
}
inline void XlaSerializedCacheKey::set_allocated_prefix(std::string* prefix) {
  if (prefix != nullptr) {
    
  } else {
    
  }
  _impl_.prefix_.SetAllocated(prefix, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.prefix_.IsDefault()) {
    _impl_.prefix_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.XlaSerializedCacheKey.prefix)
}

// bool compiled_using_pjrt = 5;
inline void XlaSerializedCacheKey::clear_compiled_using_pjrt() {
  _impl_.compiled_using_pjrt_ = false;
}
inline bool XlaSerializedCacheKey::_internal_compiled_using_pjrt() const {
  return _impl_.compiled_using_pjrt_;
}
inline bool XlaSerializedCacheKey::compiled_using_pjrt() const {
  // @@protoc_insertion_point(field_get:tensorflow.XlaSerializedCacheKey.compiled_using_pjrt)
  return _internal_compiled_using_pjrt();
}
inline void XlaSerializedCacheKey::_internal_set_compiled_using_pjrt(bool value) {
  
  _impl_.compiled_using_pjrt_ = value;
}
inline void XlaSerializedCacheKey::set_compiled_using_pjrt(bool value) {
  _internal_set_compiled_using_pjrt(value);
  // @@protoc_insertion_point(field_set:tensorflow.XlaSerializedCacheKey.compiled_using_pjrt)
}

// -------------------------------------------------------------------

// XlaSerializedCacheEntry

// .tensorflow.XlaSerializedCacheKey key = 1;
inline bool XlaSerializedCacheEntry::_internal_has_key() const {
  return this != internal_default_instance() && _impl_.key_ != nullptr;
}
inline bool XlaSerializedCacheEntry::has_key() const {
  return _internal_has_key();
}
inline void XlaSerializedCacheEntry::clear_key() {
  if (GetArenaForAllocation() == nullptr && _impl_.key_ != nullptr) {
    delete _impl_.key_;
  }
  _impl_.key_ = nullptr;
}
inline const ::tensorflow::XlaSerializedCacheKey& XlaSerializedCacheEntry::_internal_key() const {
  const ::tensorflow::XlaSerializedCacheKey* p = _impl_.key_;
  return p != nullptr ? *p : reinterpret_cast<const ::tensorflow::XlaSerializedCacheKey&>(
      ::tensorflow::_XlaSerializedCacheKey_default_instance_);
}
inline const ::tensorflow::XlaSerializedCacheKey& XlaSerializedCacheEntry::key() const {
  // @@protoc_insertion_point(field_get:tensorflow.XlaSerializedCacheEntry.key)
  return _internal_key();
}
inline void XlaSerializedCacheEntry::unsafe_arena_set_allocated_key(
    ::tensorflow::XlaSerializedCacheKey* key) {
  if (GetArenaForAllocation() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.key_);
  }
  _impl_.key_ = key;
  if (key) {
    
  } else {
    
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:tensorflow.XlaSerializedCacheEntry.key)
}
inline ::tensorflow::XlaSerializedCacheKey* XlaSerializedCacheEntry::release_key() {
  
  ::tensorflow::XlaSerializedCacheKey* temp = _impl_.key_;
  _impl_.key_ = nullptr;
#ifdef PROTOBUF_FORCE_COPY_IN_RELEASE
  auto* old =  reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(temp);
  temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  if (GetArenaForAllocation() == nullptr) { delete old; }
#else  // PROTOBUF_FORCE_COPY_IN_RELEASE
  if (GetArenaForAllocation() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
#endif  // !PROTOBUF_FORCE_COPY_IN_RELEASE
  return temp;
}
inline ::tensorflow::XlaSerializedCacheKey* XlaSerializedCacheEntry::unsafe_arena_release_key() {
  // @@protoc_insertion_point(field_release:tensorflow.XlaSerializedCacheEntry.key)
  
  ::tensorflow::XlaSerializedCacheKey* temp = _impl_.key_;
  _impl_.key_ = nullptr;
  return temp;
}
inline ::tensorflow::XlaSerializedCacheKey* XlaSerializedCacheEntry::_internal_mutable_key() {
  
  if (_impl_.key_ == nullptr) {
    auto* p = CreateMaybeMessage<::tensorflow::XlaSerializedCacheKey>(GetArenaForAllocation());
    _impl_.key_ = p;
  }
  return _impl_.key_;
}
inline ::tensorflow::XlaSerializedCacheKey* XlaSerializedCacheEntry::mutable_key() {
  ::tensorflow::XlaSerializedCacheKey* _msg = _internal_mutable_key();
  // @@protoc_insertion_point(field_mutable:tensorflow.XlaSerializedCacheEntry.key)
  return _msg;
}
inline void XlaSerializedCacheEntry::set_allocated_key(::tensorflow::XlaSerializedCacheKey* key) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaForAllocation();
  if (message_arena == nullptr) {
    delete _impl_.key_;
  }
  if (key) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
        ::PROTOBUF_NAMESPACE_ID::Arena::InternalGetOwningArena(key);
    if (message_arena != submessage_arena) {
      key = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, key, submessage_arena);
    }
    
  } else {
    
  }
  _impl_.key_ = key;
  // @@protoc_insertion_point(field_set_allocated:tensorflow.XlaSerializedCacheEntry.key)
}

// .xla.HloModuleProto hlo_module = 2;
inline bool XlaSerializedCacheEntry::_internal_has_hlo_module() const {
  return this != internal_default_instance() && _impl_.hlo_module_ != nullptr;
}
inline bool XlaSerializedCacheEntry::has_hlo_module() const {
  return _internal_has_hlo_module();
}
inline const ::xla::HloModuleProto& XlaSerializedCacheEntry::_internal_hlo_module() const {
  const ::xla::HloModuleProto* p = _impl_.hlo_module_;
  return p != nullptr ? *p : reinterpret_cast<const ::xla::HloModuleProto&>(
      ::xla::_HloModuleProto_default_instance_);
}
inline const ::xla::HloModuleProto& XlaSerializedCacheEntry::hlo_module() const {
  // @@protoc_insertion_point(field_get:tensorflow.XlaSerializedCacheEntry.hlo_module)
  return _internal_hlo_module();
}
inline void XlaSerializedCacheEntry::unsafe_arena_set_allocated_hlo_module(
    ::xla::HloModuleProto* hlo_module) {
  if (GetArenaForAllocation() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.hlo_module_);
  }
  _impl_.hlo_module_ = hlo_module;
  if (hlo_module) {
    
  } else {
    
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:tensorflow.XlaSerializedCacheEntry.hlo_module)
}
inline ::xla::HloModuleProto* XlaSerializedCacheEntry::release_hlo_module() {
  
  ::xla::HloModuleProto* temp = _impl_.hlo_module_;
  _impl_.hlo_module_ = nullptr;
#ifdef PROTOBUF_FORCE_COPY_IN_RELEASE
  auto* old =  reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(temp);
  temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  if (GetArenaForAllocation() == nullptr) { delete old; }
#else  // PROTOBUF_FORCE_COPY_IN_RELEASE
  if (GetArenaForAllocation() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
#endif  // !PROTOBUF_FORCE_COPY_IN_RELEASE
  return temp;
}
inline ::xla::HloModuleProto* XlaSerializedCacheEntry::unsafe_arena_release_hlo_module() {
  // @@protoc_insertion_point(field_release:tensorflow.XlaSerializedCacheEntry.hlo_module)
  
  ::xla::HloModuleProto* temp = _impl_.hlo_module_;
  _impl_.hlo_module_ = nullptr;
  return temp;
}
inline ::xla::HloModuleProto* XlaSerializedCacheEntry::_internal_mutable_hlo_module() {
  
  if (_impl_.hlo_module_ == nullptr) {
    auto* p = CreateMaybeMessage<::xla::HloModuleProto>(GetArenaForAllocation());
    _impl_.hlo_module_ = p;
  }
  return _impl_.hlo_module_;
}
inline ::xla::HloModuleProto* XlaSerializedCacheEntry::mutable_hlo_module() {
  ::xla::HloModuleProto* _msg = _internal_mutable_hlo_module();
  // @@protoc_insertion_point(field_mutable:tensorflow.XlaSerializedCacheEntry.hlo_module)
  return _msg;
}
inline void XlaSerializedCacheEntry::set_allocated_hlo_module(::xla::HloModuleProto* hlo_module) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaForAllocation();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.hlo_module_);
  }
  if (hlo_module) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
        ::PROTOBUF_NAMESPACE_ID::Arena::InternalGetOwningArena(
                reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(hlo_module));
    if (message_arena != submessage_arena) {
      hlo_module = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, hlo_module, submessage_arena);
    }
    
  } else {
    
  }
  _impl_.hlo_module_ = hlo_module;
  // @@protoc_insertion_point(field_set_allocated:tensorflow.XlaSerializedCacheEntry.hlo_module)
}

// bytes executable = 3;
inline void XlaSerializedCacheEntry::clear_executable() {
  _impl_.executable_.ClearToEmpty();
}
inline const std::string& XlaSerializedCacheEntry::executable() const {
  // @@protoc_insertion_point(field_get:tensorflow.XlaSerializedCacheEntry.executable)
  return _internal_executable();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void XlaSerializedCacheEntry::set_executable(ArgT0&& arg0, ArgT... args) {
 
 _impl_.executable_.SetBytes(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.XlaSerializedCacheEntry.executable)
}
inline std::string* XlaSerializedCacheEntry::mutable_executable() {
  std::string* _s = _internal_mutable_executable();
  // @@protoc_insertion_point(field_mutable:tensorflow.XlaSerializedCacheEntry.executable)
  return _s;
}
inline const std::string& XlaSerializedCacheEntry::_internal_executable() const {
  return _impl_.executable_.Get();
}
inline void XlaSerializedCacheEntry::_internal_set_executable(const std::string& value) {
  
  _impl_.executable_.Set(value, GetArenaForAllocation());
}
inline std::string* XlaSerializedCacheEntry::_internal_mutable_executable() {
  
  return _impl_.executable_.Mutable(GetArenaForAllocation());
}
inline std::string* XlaSerializedCacheEntry::release_executable() {
  // @@protoc_insertion_point(field_release:tensorflow.XlaSerializedCacheEntry.executable)
  return _impl_.executable_.Release();
}
inline void XlaSerializedCacheEntry::set_allocated_executable(std::string* executable) {
  if (executable != nullptr) {
    
  } else {
    
  }
  _impl_.executable_.SetAllocated(executable, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.executable_.IsDefault()) {
    _impl_.executable_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.XlaSerializedCacheEntry.executable)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace tensorflow

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcompiler_2fjit_2fxla_5fcompilation_5fcache_2eproto
