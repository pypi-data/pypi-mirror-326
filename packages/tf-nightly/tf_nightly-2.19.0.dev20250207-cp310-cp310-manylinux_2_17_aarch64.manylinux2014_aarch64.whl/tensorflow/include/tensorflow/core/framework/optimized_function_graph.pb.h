// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/framework/optimized_function_graph.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fframework_2foptimized_5ffunction_5fgraph_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fframework_2foptimized_5ffunction_5fgraph_2eproto

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
#include <google/protobuf/map.h>  // IWYU pragma: export
#include <google/protobuf/map_entry.h>
#include <google/protobuf/map_field_inl.h>
#include <google/protobuf/generated_enum_reflection.h>
#include <google/protobuf/unknown_field_set.h>
#include "tensorflow/core/framework/graph.pb.h"
#include "tensorflow/core/framework/types.pb.h"
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcore_2fframework_2foptimized_5ffunction_5fgraph_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2fcore_2fframework_2foptimized_5ffunction_5fgraph_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcore_2fframework_2foptimized_5ffunction_5fgraph_2eproto;
namespace tensorflow {
class OptimizedFunctionGraph;
struct OptimizedFunctionGraphDefaultTypeInternal;
extern OptimizedFunctionGraphDefaultTypeInternal _OptimizedFunctionGraph_default_instance_;
class OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse;
struct OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUseDefaultTypeInternal;
extern OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUseDefaultTypeInternal _OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse_default_instance_;
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::tensorflow::OptimizedFunctionGraph* Arena::CreateMaybeMessage<::tensorflow::OptimizedFunctionGraph>(Arena*);
template<> ::tensorflow::OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse* Arena::CreateMaybeMessage<::tensorflow::OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {

enum OptimizedFunctionGraph_OptimizationSource : int {
  OptimizedFunctionGraph_OptimizationSource_SOURCE_UNSPECIFIED = 0,
  OptimizedFunctionGraph_OptimizationSource_AOT = 1,
  OptimizedFunctionGraph_OptimizationSource_JIT = 2,
  OptimizedFunctionGraph_OptimizationSource_OptimizedFunctionGraph_OptimizationSource_INT_MIN_SENTINEL_DO_NOT_USE_ = std::numeric_limits<int32_t>::min(),
  OptimizedFunctionGraph_OptimizationSource_OptimizedFunctionGraph_OptimizationSource_INT_MAX_SENTINEL_DO_NOT_USE_ = std::numeric_limits<int32_t>::max()
};
bool OptimizedFunctionGraph_OptimizationSource_IsValid(int value);
constexpr OptimizedFunctionGraph_OptimizationSource OptimizedFunctionGraph_OptimizationSource_OptimizationSource_MIN = OptimizedFunctionGraph_OptimizationSource_SOURCE_UNSPECIFIED;
constexpr OptimizedFunctionGraph_OptimizationSource OptimizedFunctionGraph_OptimizationSource_OptimizationSource_MAX = OptimizedFunctionGraph_OptimizationSource_JIT;
constexpr int OptimizedFunctionGraph_OptimizationSource_OptimizationSource_ARRAYSIZE = OptimizedFunctionGraph_OptimizationSource_OptimizationSource_MAX + 1;

const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor* OptimizedFunctionGraph_OptimizationSource_descriptor();
template<typename T>
inline const std::string& OptimizedFunctionGraph_OptimizationSource_Name(T enum_t_value) {
  static_assert(::std::is_same<T, OptimizedFunctionGraph_OptimizationSource>::value ||
    ::std::is_integral<T>::value,
    "Incorrect type passed to function OptimizedFunctionGraph_OptimizationSource_Name.");
  return ::PROTOBUF_NAMESPACE_ID::internal::NameOfEnum(
    OptimizedFunctionGraph_OptimizationSource_descriptor(), enum_t_value);
}
inline bool OptimizedFunctionGraph_OptimizationSource_Parse(
    ::PROTOBUF_NAMESPACE_ID::ConstStringParam name, OptimizedFunctionGraph_OptimizationSource* value) {
  return ::PROTOBUF_NAMESPACE_ID::internal::ParseNamedEnum<OptimizedFunctionGraph_OptimizationSource>(
    OptimizedFunctionGraph_OptimizationSource_descriptor(), name, value);
}
// ===================================================================

class OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse : public ::PROTOBUF_NAMESPACE_ID::internal::MapEntry<OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse, 
    std::string, std::string,
    ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::TYPE_STRING,
    ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::TYPE_STRING> {
public:
  typedef ::PROTOBUF_NAMESPACE_ID::internal::MapEntry<OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse, 
    std::string, std::string,
    ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::TYPE_STRING,
    ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::TYPE_STRING> SuperType;
  OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse();
  explicit PROTOBUF_CONSTEXPR OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse(
      ::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);
  explicit OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  void MergeFrom(const OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse& other);
  static const OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse* internal_default_instance() { return reinterpret_cast<const OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse*>(&_OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse_default_instance_); }
  static bool ValidateKey(std::string* s) {
    return ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::VerifyUtf8String(s->data(), static_cast<int>(s->size()), ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::PARSE, "tensorflow.OptimizedFunctionGraph.NodeNameToControlRetEntry.key");
 }
  static bool ValidateValue(std::string* s) {
    return ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::VerifyUtf8String(s->data(), static_cast<int>(s->size()), ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::PARSE, "tensorflow.OptimizedFunctionGraph.NodeNameToControlRetEntry.value");
 }
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;
  friend struct ::TableStruct_tensorflow_2fcore_2fframework_2foptimized_5ffunction_5fgraph_2eproto;
};

// -------------------------------------------------------------------

class OptimizedFunctionGraph final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.OptimizedFunctionGraph) */ {
 public:
  inline OptimizedFunctionGraph() : OptimizedFunctionGraph(nullptr) {}
  ~OptimizedFunctionGraph() override;
  explicit PROTOBUF_CONSTEXPR OptimizedFunctionGraph(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  OptimizedFunctionGraph(const OptimizedFunctionGraph& from);
  OptimizedFunctionGraph(OptimizedFunctionGraph&& from) noexcept
    : OptimizedFunctionGraph() {
    *this = ::std::move(from);
  }

  inline OptimizedFunctionGraph& operator=(const OptimizedFunctionGraph& from) {
    CopyFrom(from);
    return *this;
  }
  inline OptimizedFunctionGraph& operator=(OptimizedFunctionGraph&& from) noexcept {
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
  static const OptimizedFunctionGraph& default_instance() {
    return *internal_default_instance();
  }
  static inline const OptimizedFunctionGraph* internal_default_instance() {
    return reinterpret_cast<const OptimizedFunctionGraph*>(
               &_OptimizedFunctionGraph_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(OptimizedFunctionGraph& a, OptimizedFunctionGraph& b) {
    a.Swap(&b);
  }
  inline void Swap(OptimizedFunctionGraph* other) {
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
  void UnsafeArenaSwap(OptimizedFunctionGraph* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  OptimizedFunctionGraph* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<OptimizedFunctionGraph>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const OptimizedFunctionGraph& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const OptimizedFunctionGraph& from) {
    OptimizedFunctionGraph::MergeImpl(*this, from);
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
  void InternalSwap(OptimizedFunctionGraph* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.OptimizedFunctionGraph";
  }
  protected:
  explicit OptimizedFunctionGraph(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  private:
  static void ArenaDtor(void* object);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------


  typedef OptimizedFunctionGraph_OptimizationSource OptimizationSource;
  static constexpr OptimizationSource SOURCE_UNSPECIFIED =
    OptimizedFunctionGraph_OptimizationSource_SOURCE_UNSPECIFIED;
  static constexpr OptimizationSource AOT =
    OptimizedFunctionGraph_OptimizationSource_AOT;
  static constexpr OptimizationSource JIT =
    OptimizedFunctionGraph_OptimizationSource_JIT;
  static inline bool OptimizationSource_IsValid(int value) {
    return OptimizedFunctionGraph_OptimizationSource_IsValid(value);
  }
  static constexpr OptimizationSource OptimizationSource_MIN =
    OptimizedFunctionGraph_OptimizationSource_OptimizationSource_MIN;
  static constexpr OptimizationSource OptimizationSource_MAX =
    OptimizedFunctionGraph_OptimizationSource_OptimizationSource_MAX;
  static constexpr int OptimizationSource_ARRAYSIZE =
    OptimizedFunctionGraph_OptimizationSource_OptimizationSource_ARRAYSIZE;
  static inline const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor*
  OptimizationSource_descriptor() {
    return OptimizedFunctionGraph_OptimizationSource_descriptor();
  }
  template<typename T>
  static inline const std::string& OptimizationSource_Name(T enum_t_value) {
    static_assert(::std::is_same<T, OptimizationSource>::value ||
      ::std::is_integral<T>::value,
      "Incorrect type passed to function OptimizationSource_Name.");
    return OptimizedFunctionGraph_OptimizationSource_Name(enum_t_value);
  }
  static inline bool OptimizationSource_Parse(::PROTOBUF_NAMESPACE_ID::ConstStringParam name,
      OptimizationSource* value) {
    return OptimizedFunctionGraph_OptimizationSource_Parse(name, value);
  }

  // accessors -------------------------------------------------------

  enum : int {
    kNodeNameToControlRetFieldNumber = 3,
    kRetTypesFieldNumber = 4,
    kNameFieldNumber = 1,
    kFunctionGraphFieldNumber = 2,
    kNumReturnNodesFieldNumber = 5,
    kSourceFieldNumber = 7,
    kOptimizationTimeUsecsFieldNumber = 8,
  };
  // map<string, string> node_name_to_control_ret = 3;
  int node_name_to_control_ret_size() const;
  private:
  int _internal_node_name_to_control_ret_size() const;
  public:
  void clear_node_name_to_control_ret();
  private:
  const ::PROTOBUF_NAMESPACE_ID::Map< std::string, std::string >&
      _internal_node_name_to_control_ret() const;
  ::PROTOBUF_NAMESPACE_ID::Map< std::string, std::string >*
      _internal_mutable_node_name_to_control_ret();
  public:
  const ::PROTOBUF_NAMESPACE_ID::Map< std::string, std::string >&
      node_name_to_control_ret() const;
  ::PROTOBUF_NAMESPACE_ID::Map< std::string, std::string >*
      mutable_node_name_to_control_ret();

  // repeated .tensorflow.DataType ret_types = 4;
  int ret_types_size() const;
  private:
  int _internal_ret_types_size() const;
  public:
  void clear_ret_types();
  private:
  ::tensorflow::DataType _internal_ret_types(int index) const;
  void _internal_add_ret_types(::tensorflow::DataType value);
  ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>* _internal_mutable_ret_types();
  public:
  ::tensorflow::DataType ret_types(int index) const;
  void set_ret_types(int index, ::tensorflow::DataType value);
  void add_ret_types(::tensorflow::DataType value);
  const ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>& ret_types() const;
  ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>* mutable_ret_types();

  // string name = 1;
  void clear_name();
  const std::string& name() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_name(ArgT0&& arg0, ArgT... args);
  std::string* mutable_name();
  PROTOBUF_NODISCARD std::string* release_name();
  void set_allocated_name(std::string* name);
  private:
  const std::string& _internal_name() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_name(const std::string& value);
  std::string* _internal_mutable_name();
  public:

  // .tensorflow.GraphDef function_graph = 2;
  bool has_function_graph() const;
  private:
  bool _internal_has_function_graph() const;
  public:
  void clear_function_graph();
  const ::tensorflow::GraphDef& function_graph() const;
  PROTOBUF_NODISCARD ::tensorflow::GraphDef* release_function_graph();
  ::tensorflow::GraphDef* mutable_function_graph();
  void set_allocated_function_graph(::tensorflow::GraphDef* function_graph);
  private:
  const ::tensorflow::GraphDef& _internal_function_graph() const;
  ::tensorflow::GraphDef* _internal_mutable_function_graph();
  public:
  void unsafe_arena_set_allocated_function_graph(
      ::tensorflow::GraphDef* function_graph);
  ::tensorflow::GraphDef* unsafe_arena_release_function_graph();

  // uint32 num_return_nodes = 5;
  void clear_num_return_nodes();
  uint32_t num_return_nodes() const;
  void set_num_return_nodes(uint32_t value);
  private:
  uint32_t _internal_num_return_nodes() const;
  void _internal_set_num_return_nodes(uint32_t value);
  public:

  // optional .tensorflow.OptimizedFunctionGraph.OptimizationSource source = 7;
  bool has_source() const;
  private:
  bool _internal_has_source() const;
  public:
  void clear_source();
  ::tensorflow::OptimizedFunctionGraph_OptimizationSource source() const;
  void set_source(::tensorflow::OptimizedFunctionGraph_OptimizationSource value);
  private:
  ::tensorflow::OptimizedFunctionGraph_OptimizationSource _internal_source() const;
  void _internal_set_source(::tensorflow::OptimizedFunctionGraph_OptimizationSource value);
  public:

  // optional uint64 optimization_time_usecs = 8;
  bool has_optimization_time_usecs() const;
  private:
  bool _internal_has_optimization_time_usecs() const;
  public:
  void clear_optimization_time_usecs();
  uint64_t optimization_time_usecs() const;
  void set_optimization_time_usecs(uint64_t value);
  private:
  uint64_t _internal_optimization_time_usecs() const;
  void _internal_set_optimization_time_usecs(uint64_t value);
  public:

  // @@protoc_insertion_point(class_scope:tensorflow.OptimizedFunctionGraph)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::HasBits<1> _has_bits_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
    ::PROTOBUF_NAMESPACE_ID::internal::MapField<
        OptimizedFunctionGraph_NodeNameToControlRetEntry_DoNotUse,
        std::string, std::string,
        ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::TYPE_STRING,
        ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::TYPE_STRING> node_name_to_control_ret_;
    ::PROTOBUF_NAMESPACE_ID::RepeatedField<int> ret_types_;
    mutable std::atomic<int> _ret_types_cached_byte_size_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr name_;
    ::tensorflow::GraphDef* function_graph_;
    uint32_t num_return_nodes_;
    int source_;
    uint64_t optimization_time_usecs_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcore_2fframework_2foptimized_5ffunction_5fgraph_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// -------------------------------------------------------------------

// OptimizedFunctionGraph

// string name = 1;
inline void OptimizedFunctionGraph::clear_name() {
  _impl_.name_.ClearToEmpty();
}
inline const std::string& OptimizedFunctionGraph::name() const {
  // @@protoc_insertion_point(field_get:tensorflow.OptimizedFunctionGraph.name)
  return _internal_name();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void OptimizedFunctionGraph::set_name(ArgT0&& arg0, ArgT... args) {
 
 _impl_.name_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.OptimizedFunctionGraph.name)
}
inline std::string* OptimizedFunctionGraph::mutable_name() {
  std::string* _s = _internal_mutable_name();
  // @@protoc_insertion_point(field_mutable:tensorflow.OptimizedFunctionGraph.name)
  return _s;
}
inline const std::string& OptimizedFunctionGraph::_internal_name() const {
  return _impl_.name_.Get();
}
inline void OptimizedFunctionGraph::_internal_set_name(const std::string& value) {
  
  _impl_.name_.Set(value, GetArenaForAllocation());
}
inline std::string* OptimizedFunctionGraph::_internal_mutable_name() {
  
  return _impl_.name_.Mutable(GetArenaForAllocation());
}
inline std::string* OptimizedFunctionGraph::release_name() {
  // @@protoc_insertion_point(field_release:tensorflow.OptimizedFunctionGraph.name)
  return _impl_.name_.Release();
}
inline void OptimizedFunctionGraph::set_allocated_name(std::string* name) {
  if (name != nullptr) {
    
  } else {
    
  }
  _impl_.name_.SetAllocated(name, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.name_.IsDefault()) {
    _impl_.name_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.OptimizedFunctionGraph.name)
}

// .tensorflow.GraphDef function_graph = 2;
inline bool OptimizedFunctionGraph::_internal_has_function_graph() const {
  return this != internal_default_instance() && _impl_.function_graph_ != nullptr;
}
inline bool OptimizedFunctionGraph::has_function_graph() const {
  return _internal_has_function_graph();
}
inline const ::tensorflow::GraphDef& OptimizedFunctionGraph::_internal_function_graph() const {
  const ::tensorflow::GraphDef* p = _impl_.function_graph_;
  return p != nullptr ? *p : reinterpret_cast<const ::tensorflow::GraphDef&>(
      ::tensorflow::_GraphDef_default_instance_);
}
inline const ::tensorflow::GraphDef& OptimizedFunctionGraph::function_graph() const {
  // @@protoc_insertion_point(field_get:tensorflow.OptimizedFunctionGraph.function_graph)
  return _internal_function_graph();
}
inline void OptimizedFunctionGraph::unsafe_arena_set_allocated_function_graph(
    ::tensorflow::GraphDef* function_graph) {
  if (GetArenaForAllocation() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.function_graph_);
  }
  _impl_.function_graph_ = function_graph;
  if (function_graph) {
    
  } else {
    
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:tensorflow.OptimizedFunctionGraph.function_graph)
}
inline ::tensorflow::GraphDef* OptimizedFunctionGraph::release_function_graph() {
  
  ::tensorflow::GraphDef* temp = _impl_.function_graph_;
  _impl_.function_graph_ = nullptr;
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
inline ::tensorflow::GraphDef* OptimizedFunctionGraph::unsafe_arena_release_function_graph() {
  // @@protoc_insertion_point(field_release:tensorflow.OptimizedFunctionGraph.function_graph)
  
  ::tensorflow::GraphDef* temp = _impl_.function_graph_;
  _impl_.function_graph_ = nullptr;
  return temp;
}
inline ::tensorflow::GraphDef* OptimizedFunctionGraph::_internal_mutable_function_graph() {
  
  if (_impl_.function_graph_ == nullptr) {
    auto* p = CreateMaybeMessage<::tensorflow::GraphDef>(GetArenaForAllocation());
    _impl_.function_graph_ = p;
  }
  return _impl_.function_graph_;
}
inline ::tensorflow::GraphDef* OptimizedFunctionGraph::mutable_function_graph() {
  ::tensorflow::GraphDef* _msg = _internal_mutable_function_graph();
  // @@protoc_insertion_point(field_mutable:tensorflow.OptimizedFunctionGraph.function_graph)
  return _msg;
}
inline void OptimizedFunctionGraph::set_allocated_function_graph(::tensorflow::GraphDef* function_graph) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaForAllocation();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.function_graph_);
  }
  if (function_graph) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
        ::PROTOBUF_NAMESPACE_ID::Arena::InternalGetOwningArena(
                reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(function_graph));
    if (message_arena != submessage_arena) {
      function_graph = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, function_graph, submessage_arena);
    }
    
  } else {
    
  }
  _impl_.function_graph_ = function_graph;
  // @@protoc_insertion_point(field_set_allocated:tensorflow.OptimizedFunctionGraph.function_graph)
}

// map<string, string> node_name_to_control_ret = 3;
inline int OptimizedFunctionGraph::_internal_node_name_to_control_ret_size() const {
  return _impl_.node_name_to_control_ret_.size();
}
inline int OptimizedFunctionGraph::node_name_to_control_ret_size() const {
  return _internal_node_name_to_control_ret_size();
}
inline void OptimizedFunctionGraph::clear_node_name_to_control_ret() {
  _impl_.node_name_to_control_ret_.Clear();
}
inline const ::PROTOBUF_NAMESPACE_ID::Map< std::string, std::string >&
OptimizedFunctionGraph::_internal_node_name_to_control_ret() const {
  return _impl_.node_name_to_control_ret_.GetMap();
}
inline const ::PROTOBUF_NAMESPACE_ID::Map< std::string, std::string >&
OptimizedFunctionGraph::node_name_to_control_ret() const {
  // @@protoc_insertion_point(field_map:tensorflow.OptimizedFunctionGraph.node_name_to_control_ret)
  return _internal_node_name_to_control_ret();
}
inline ::PROTOBUF_NAMESPACE_ID::Map< std::string, std::string >*
OptimizedFunctionGraph::_internal_mutable_node_name_to_control_ret() {
  return _impl_.node_name_to_control_ret_.MutableMap();
}
inline ::PROTOBUF_NAMESPACE_ID::Map< std::string, std::string >*
OptimizedFunctionGraph::mutable_node_name_to_control_ret() {
  // @@protoc_insertion_point(field_mutable_map:tensorflow.OptimizedFunctionGraph.node_name_to_control_ret)
  return _internal_mutable_node_name_to_control_ret();
}

// repeated .tensorflow.DataType ret_types = 4;
inline int OptimizedFunctionGraph::_internal_ret_types_size() const {
  return _impl_.ret_types_.size();
}
inline int OptimizedFunctionGraph::ret_types_size() const {
  return _internal_ret_types_size();
}
inline void OptimizedFunctionGraph::clear_ret_types() {
  _impl_.ret_types_.Clear();
}
inline ::tensorflow::DataType OptimizedFunctionGraph::_internal_ret_types(int index) const {
  return static_cast< ::tensorflow::DataType >(_impl_.ret_types_.Get(index));
}
inline ::tensorflow::DataType OptimizedFunctionGraph::ret_types(int index) const {
  // @@protoc_insertion_point(field_get:tensorflow.OptimizedFunctionGraph.ret_types)
  return _internal_ret_types(index);
}
inline void OptimizedFunctionGraph::set_ret_types(int index, ::tensorflow::DataType value) {
  _impl_.ret_types_.Set(index, value);
  // @@protoc_insertion_point(field_set:tensorflow.OptimizedFunctionGraph.ret_types)
}
inline void OptimizedFunctionGraph::_internal_add_ret_types(::tensorflow::DataType value) {
  _impl_.ret_types_.Add(value);
}
inline void OptimizedFunctionGraph::add_ret_types(::tensorflow::DataType value) {
  _internal_add_ret_types(value);
  // @@protoc_insertion_point(field_add:tensorflow.OptimizedFunctionGraph.ret_types)
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>&
OptimizedFunctionGraph::ret_types() const {
  // @@protoc_insertion_point(field_list:tensorflow.OptimizedFunctionGraph.ret_types)
  return _impl_.ret_types_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>*
OptimizedFunctionGraph::_internal_mutable_ret_types() {
  return &_impl_.ret_types_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>*
OptimizedFunctionGraph::mutable_ret_types() {
  // @@protoc_insertion_point(field_mutable_list:tensorflow.OptimizedFunctionGraph.ret_types)
  return _internal_mutable_ret_types();
}

// uint32 num_return_nodes = 5;
inline void OptimizedFunctionGraph::clear_num_return_nodes() {
  _impl_.num_return_nodes_ = 0u;
}
inline uint32_t OptimizedFunctionGraph::_internal_num_return_nodes() const {
  return _impl_.num_return_nodes_;
}
inline uint32_t OptimizedFunctionGraph::num_return_nodes() const {
  // @@protoc_insertion_point(field_get:tensorflow.OptimizedFunctionGraph.num_return_nodes)
  return _internal_num_return_nodes();
}
inline void OptimizedFunctionGraph::_internal_set_num_return_nodes(uint32_t value) {
  
  _impl_.num_return_nodes_ = value;
}
inline void OptimizedFunctionGraph::set_num_return_nodes(uint32_t value) {
  _internal_set_num_return_nodes(value);
  // @@protoc_insertion_point(field_set:tensorflow.OptimizedFunctionGraph.num_return_nodes)
}

// optional .tensorflow.OptimizedFunctionGraph.OptimizationSource source = 7;
inline bool OptimizedFunctionGraph::_internal_has_source() const {
  bool value = (_impl_._has_bits_[0] & 0x00000001u) != 0;
  return value;
}
inline bool OptimizedFunctionGraph::has_source() const {
  return _internal_has_source();
}
inline void OptimizedFunctionGraph::clear_source() {
  _impl_.source_ = 0;
  _impl_._has_bits_[0] &= ~0x00000001u;
}
inline ::tensorflow::OptimizedFunctionGraph_OptimizationSource OptimizedFunctionGraph::_internal_source() const {
  return static_cast< ::tensorflow::OptimizedFunctionGraph_OptimizationSource >(_impl_.source_);
}
inline ::tensorflow::OptimizedFunctionGraph_OptimizationSource OptimizedFunctionGraph::source() const {
  // @@protoc_insertion_point(field_get:tensorflow.OptimizedFunctionGraph.source)
  return _internal_source();
}
inline void OptimizedFunctionGraph::_internal_set_source(::tensorflow::OptimizedFunctionGraph_OptimizationSource value) {
  _impl_._has_bits_[0] |= 0x00000001u;
  _impl_.source_ = value;
}
inline void OptimizedFunctionGraph::set_source(::tensorflow::OptimizedFunctionGraph_OptimizationSource value) {
  _internal_set_source(value);
  // @@protoc_insertion_point(field_set:tensorflow.OptimizedFunctionGraph.source)
}

// optional uint64 optimization_time_usecs = 8;
inline bool OptimizedFunctionGraph::_internal_has_optimization_time_usecs() const {
  bool value = (_impl_._has_bits_[0] & 0x00000002u) != 0;
  return value;
}
inline bool OptimizedFunctionGraph::has_optimization_time_usecs() const {
  return _internal_has_optimization_time_usecs();
}
inline void OptimizedFunctionGraph::clear_optimization_time_usecs() {
  _impl_.optimization_time_usecs_ = uint64_t{0u};
  _impl_._has_bits_[0] &= ~0x00000002u;
}
inline uint64_t OptimizedFunctionGraph::_internal_optimization_time_usecs() const {
  return _impl_.optimization_time_usecs_;
}
inline uint64_t OptimizedFunctionGraph::optimization_time_usecs() const {
  // @@protoc_insertion_point(field_get:tensorflow.OptimizedFunctionGraph.optimization_time_usecs)
  return _internal_optimization_time_usecs();
}
inline void OptimizedFunctionGraph::_internal_set_optimization_time_usecs(uint64_t value) {
  _impl_._has_bits_[0] |= 0x00000002u;
  _impl_.optimization_time_usecs_ = value;
}
inline void OptimizedFunctionGraph::set_optimization_time_usecs(uint64_t value) {
  _internal_set_optimization_time_usecs(value);
  // @@protoc_insertion_point(field_set:tensorflow.OptimizedFunctionGraph.optimization_time_usecs)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace tensorflow

PROTOBUF_NAMESPACE_OPEN

template <> struct is_proto_enum< ::tensorflow::OptimizedFunctionGraph_OptimizationSource> : ::std::true_type {};
template <>
inline const EnumDescriptor* GetEnumDescriptor< ::tensorflow::OptimizedFunctionGraph_OptimizationSource>() {
  return ::tensorflow::OptimizedFunctionGraph_OptimizationSource_descriptor();
}

PROTOBUF_NAMESPACE_CLOSE

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fframework_2foptimized_5ffunction_5fgraph_2eproto
