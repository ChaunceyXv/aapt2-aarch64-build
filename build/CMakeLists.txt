cmake_minimum_required(VERSION 3.20)
project(aapt2-host CXX C)

# Sources are expected in <project>/src (fetched by build/build_aapt2.sh).
get_filename_component(AAPT2_BUILD_ROOT ${CMAKE_CURRENT_LIST_DIR} DIRECTORY)
set(SRC ${AAPT2_BUILD_ROOT}/src)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_compile_definitions(_FILE_OFFSET_BITS=64 _GNU_SOURCE)
add_compile_options(-include ${CMAKE_CURRENT_LIST_DIR}/host_defs.h)
add_compile_options(-fno-exceptions -fno-rtti -Wno-unused-parameter -Wno-missing-field-initializers -Wno-deprecated-declarations)

set(AAPT2_DIR ${SRC}/base/tools/aapt2)

# ---- host static deps ------------------------------------------------
add_library(libbase STATIC
    ${SRC}/libbase/abi_compatibility.cpp
    ${SRC}/libbase/chrono_utils.cpp
    ${SRC}/libbase/cmsg.cpp
    ${SRC}/libbase/file.cpp
    ${SRC}/libbase/hex.cpp
    ${SRC}/libbase/logging.cpp
    ${SRC}/libbase/mapped_file.cpp
    ${SRC}/libbase/parsebool.cpp
    ${SRC}/libbase/parsenetaddress.cpp
    ${SRC}/libbase/posix_strerror_r.cpp
    ${SRC}/libbase/process.cpp
    ${SRC}/libbase/properties.cpp
    ${SRC}/libbase/result.cpp
    ${SRC}/libbase/stringprintf.cpp
    ${SRC}/libbase/strings.cpp
    ${SRC}/libbase/threads.cpp
    ${SRC}/libbase/test_utils.cpp
    ${SRC}/libbase/errors_unix.cpp
)

add_library(libcutils STATIC
    ${SRC}/core/libcutils/android_get_control_file.cpp
    ${SRC}/core/libcutils/canned_fs_config.cpp
    ${SRC}/core/libcutils/config_utils.cpp
    ${SRC}/core/libcutils/fs.cpp
    ${SRC}/core/libcutils/fs_config.cpp
    ${SRC}/core/libcutils/hashmap.cpp
    ${SRC}/core/libcutils/iosched_policy.cpp
    ${SRC}/core/libcutils/load_file.cpp
    ${SRC}/core/libcutils/multiuser.cpp
    ${SRC}/core/libcutils/native_handle.cpp
    ${SRC}/core/libcutils/properties.cpp
    ${SRC}/core/libcutils/record_stream.cpp
    ${SRC}/core/libcutils/socket_inaddr_any_server_unix.cpp
    ${SRC}/core/libcutils/socket_local_client_unix.cpp
    ${SRC}/core/libcutils/socket_local_server_unix.cpp
    ${SRC}/core/libcutils/socket_network_client_unix.cpp
    ${SRC}/core/libcutils/sockets_unix.cpp
    ${SRC}/core/libcutils/sockets.cpp
    ${SRC}/core/libcutils/str_parms.cpp
    ${SRC}/core/libcutils/strlcpy.c
    ${SRC}/core/libcutils/android_reboot.cpp
    ${SRC}/core/libcutils/klog.cpp
    ${SRC}/core/libcutils/partition_utils.cpp
    ${SRC}/core/libcutils/qtaguid.cpp
    ${SRC}/core/libcutils/trace-dev.cpp
    ${SRC}/core/libcutils/uevent.cpp
)

add_library(libutils STATIC
    ${SRC}/core/libutils/FileMap.cpp
    ${SRC}/core/libutils/JenkinsHash.cpp
    ${SRC}/core/libutils/LightRefBase.cpp
    ${SRC}/core/libutils/NativeHandle.cpp
    ${SRC}/core/libutils/Printer.cpp
    ${SRC}/core/libutils/StopWatch.cpp
    ${SRC}/core/libutils/SystemClock.cpp
    ${SRC}/core/libutils/Threads.cpp
    ${SRC}/core/libutils/Timers.cpp
    ${SRC}/core/libutils/Tokenizer.cpp
    ${SRC}/core/libutils/misc.cpp
    ${SRC}/core/libutils/Trace.cpp
    ${SRC}/core/libutils/Looper.cpp
    ${SRC}/core/libutils/binder/Errors.cpp
    ${SRC}/core/libutils/binder/RefBase.cpp
    ${SRC}/core/libutils/binder/SharedBuffer.cpp
    ${SRC}/core/libutils/binder/String16.cpp
    ${SRC}/core/libutils/binder/String8.cpp
    ${SRC}/core/libutils/binder/StrongPointer.cpp
    ${SRC}/core/libutils/binder/Unicode.cpp
    ${SRC}/core/libutils/binder/VectorImpl.cpp
)

add_library(liblog STATIC
    ${SRC}/logging/liblog/log_event_list.cpp
    ${SRC}/logging/liblog/log_event_write.cpp
    ${SRC}/logging/liblog/logger_name.cpp
    ${SRC}/logging/liblog/logger_read.cpp
    ${SRC}/logging/liblog/logger_write.cpp
    ${SRC}/logging/liblog/properties.cpp
    ${SRC}/logging/liblog/logprint.cpp
    ${SRC}/logging/liblog/event_tag_map.cpp
    ${SRC}/logging/liblog/log_time.cpp
    ${SRC}/logging/liblog/pmsg_reader.cpp
    ${SRC}/logging/liblog/pmsg_writer.cpp
    ${SRC}/logging/liblog/logd_reader.cpp
    ${SRC}/logging/liblog/logd_writer.cpp
)
target_compile_definitions(liblog PRIVATE
    LIBLOG_LOG_TAG=1006 _XOPEN_SOURCE=700 FAKE_LOG_DEVICE=1
    SNET_EVENT_LOG_TAG=1397638686 ANDROID_DEBUGGABLE=0
)

add_library(libandroidfw STATIC
    ${SRC}/base/libs/androidfw/ApkAssets.cpp
    ${SRC}/base/libs/androidfw/ApkParsing.cpp
    ${SRC}/base/libs/androidfw/Asset.cpp
    ${SRC}/base/libs/androidfw/AssetDir.cpp
    ${SRC}/base/libs/androidfw/AssetManager.cpp
    ${SRC}/base/libs/androidfw/AssetManager2.cpp
    ${SRC}/base/libs/androidfw/AssetsProvider.cpp
    ${SRC}/base/libs/androidfw/AttributeResolution.cpp
    ${SRC}/base/libs/androidfw/BigBuffer.cpp
    ${SRC}/base/libs/androidfw/BigBufferStream.cpp
    ${SRC}/base/libs/androidfw/ChunkIterator.cpp
    ${SRC}/base/libs/androidfw/ConfigDescription.cpp
    ${SRC}/base/libs/androidfw/FileStream.cpp
    ${SRC}/base/libs/androidfw/Idmap.cpp
    ${SRC}/base/libs/androidfw/LoadedArsc.cpp
    ${SRC}/base/libs/androidfw/Locale.cpp
    ${SRC}/base/libs/androidfw/LocaleData.cpp
    ${SRC}/base/libs/androidfw/misc.cpp
    ${SRC}/base/libs/androidfw/NinePatch.cpp
    ${SRC}/base/libs/androidfw/ObbFile.cpp
    ${SRC}/base/libs/androidfw/PosixUtils.cpp
    ${SRC}/base/libs/androidfw/Png.cpp
    ${SRC}/base/libs/androidfw/PngChunkFilter.cpp
    ${SRC}/base/libs/androidfw/PngCrunch.cpp
    ${SRC}/base/libs/androidfw/ResourceTimer.cpp
    ${SRC}/base/libs/androidfw/ResourceTypes.cpp
    ${SRC}/base/libs/androidfw/ResourceUtils.cpp
    ${SRC}/base/libs/androidfw/StreamingZipInflater.cpp
    ${SRC}/base/libs/androidfw/StringPool.cpp
    ${SRC}/base/libs/androidfw/TypeWrappers.cpp
    ${SRC}/base/libs/androidfw/Util.cpp
    ${SRC}/base/libs/androidfw/ZipFileRO.cpp
    ${SRC}/base/libs/androidfw/ZipUtils.cpp
    ${SRC}/base/libs/androidfw/PathUtils.cpp
)
target_compile_definitions(libandroidfw PRIVATE STATIC_ANDROIDFW_FOR_TOOLS)

add_library(libziparchive STATIC
    ${SRC}/libziparchive/zip_archive.cc
    ${SRC}/libziparchive/zip_archive_stream_entry.cc
    ${SRC}/libziparchive/zip_cd_entry_map.cc
    ${SRC}/libziparchive/zip_writer.cc
    ${SRC}/libziparchive/zip_error.cpp
    ${SRC}/libziparchive/incfs_support/signal_handling.cpp
)
target_compile_definitions(libziparchive PRIVATE
    ZLIB_CONST _FILE_OFFSET_BITS=64 ZIPARCHIVE_DISABLE_CALLBACK_API=1
)

add_library(libbuildversion STATIC
    ${SRC}/soong/cc/libbuildversion/libbuildversion.cpp
)
target_include_directories(libbuildversion PRIVATE ${SRC}/soong/cc/libbuildversion/include)

# ---- selinux / sepol / incfs ----------------------------------------
set(HOST_SELINUX_STUB ${CMAKE_CURRENT_LIST_DIR}/host_selinux_stub.c)
add_library(libsepol STATIC
    ${SRC}/selinux/libsepol/src/assertion.c
    ${SRC}/selinux/libsepol/src/avrule_block.c
    ${SRC}/selinux/libsepol/src/avtab.c
    ${SRC}/selinux/libsepol/src/boolean_record.c
    ${SRC}/selinux/libsepol/src/booleans.c
    ${SRC}/selinux/libsepol/src/conditional.c
    ${SRC}/selinux/libsepol/src/constraint.c
    ${SRC}/selinux/libsepol/src/context.c
    ${SRC}/selinux/libsepol/src/context_record.c
    ${SRC}/selinux/libsepol/src/debug.c
    ${SRC}/selinux/libsepol/src/ebitmap.c
    ${SRC}/selinux/libsepol/src/expand.c
    ${SRC}/selinux/libsepol/src/handle.c
    ${SRC}/selinux/libsepol/src/hashtab.c
    ${SRC}/selinux/libsepol/src/hierarchy.c
    ${SRC}/selinux/libsepol/src/iface_record.c
    ${SRC}/selinux/libsepol/src/interfaces.c
    ${SRC}/selinux/libsepol/src/kernel_to_cil.c
    ${SRC}/selinux/libsepol/src/kernel_to_common.c
    ${SRC}/selinux/libsepol/src/kernel_to_conf.c
    ${SRC}/selinux/libsepol/src/link.c
    ${SRC}/selinux/libsepol/src/mls.c
    ${SRC}/selinux/libsepol/src/module.c
    ${SRC}/selinux/libsepol/src/module_to_cil.c
    ${SRC}/selinux/libsepol/src/node_record.c
    ${SRC}/selinux/libsepol/src/nodes.c
    ${SRC}/selinux/libsepol/src/optimize.c
    ${SRC}/selinux/libsepol/src/polcaps.c
    ${SRC}/selinux/libsepol/src/policydb.c
    ${SRC}/selinux/libsepol/src/policydb_convert.c
    ${SRC}/selinux/libsepol/src/policydb_public.c
    ${SRC}/selinux/libsepol/src/policydb_validate.c
    ${SRC}/selinux/libsepol/src/port_record.c
    ${SRC}/selinux/libsepol/src/ports.c
    ${SRC}/selinux/libsepol/src/services.c
    ${SRC}/selinux/libsepol/src/sidtab.c
    ${SRC}/selinux/libsepol/src/symtab.c
    ${SRC}/selinux/libsepol/src/user_record.c
    ${SRC}/selinux/libsepol/src/users.c
    ${SRC}/selinux/libsepol/src/util.c
    ${SRC}/selinux/libsepol/src/write.c
    ${SRC}/selinux/libsepol/cil/src/android.c
    ${SRC}/selinux/libsepol/cil/src/cil_binary.c
    ${SRC}/selinux/libsepol/cil/src/cil_build_ast.c
    ${SRC}/selinux/libsepol/cil/src/cil.c
    ${SRC}/selinux/libsepol/cil/src/cil_copy_ast.c
    ${SRC}/selinux/libsepol/cil/src/cil_find.c
    ${SRC}/selinux/libsepol/cil/src/cil_fqn.c
    ${SRC}/selinux/libsepol/cil/src/cil_list.c
    ${SRC}/selinux/libsepol/cil/src/cil_log.c
    ${SRC}/selinux/libsepol/cil/src/cil_mem.c
    ${SRC}/selinux/libsepol/cil/src/cil_parser.c
    ${SRC}/selinux/libsepol/cil/src/cil_policy.c
    ${SRC}/selinux/libsepol/cil/src/cil_post.c
    ${SRC}/selinux/libsepol/cil/src/cil_reset_ast.c
    ${SRC}/selinux/libsepol/cil/src/cil_resolve_ast.c
    ${SRC}/selinux/libsepol/cil/src/cil_stack.c
    ${SRC}/selinux/libsepol/cil/src/cil_strpool.c
    ${SRC}/selinux/libsepol/cil/src/cil_symtab.c
    ${SRC}/selinux/libsepol/cil/src/cil_tree.c
    ${SRC}/selinux/libsepol/cil/src/cil_verify.c
    ${SRC}/selinux/libsepol/cil/src/cil_write_ast.c
)
set_source_files_properties(${SRC}/selinux/libsepol/cil/src/cil_lexer.l PROPERTIES LANGUAGE C)
add_custom_command(
    OUTPUT ${CMAKE_BINARY_DIR}/cil_lexer.c
    COMMAND flex -o ${CMAKE_BINARY_DIR}/cil_lexer.c ${SRC}/selinux/libsepol/cil/src/cil_lexer.l
    DEPENDS ${SRC}/selinux/libsepol/cil/src/cil_lexer.l
)
target_sources(libsepol PRIVATE ${CMAKE_BINARY_DIR}/cil_lexer.c)
target_compile_definitions(libsepol PRIVATE HAVE_REALLOCARRAY _GNU_SOURCE)
target_include_directories(libsepol PUBLIC
    ${SRC}/selinux/libselinux/include
    ${SRC}/selinux/libsepol/include
    ${SRC}/selinux/libsepol/src
    ${SRC}/selinux/libsepol/cil/include
    ${SRC}/selinux/libsepol/cil/src
)

add_library(libselinux STATIC
    ${SRC}/selinux/libselinux/src/android/android_seapp.c
    ${HOST_SELINUX_STUB}
    ${SRC}/selinux/libselinux/src/avc.c
    ${SRC}/selinux/libselinux/src/avc_internal.c
    ${SRC}/selinux/libselinux/src/avc_sidtab.c
    ${SRC}/selinux/libselinux/src/booleans.c
    ${SRC}/selinux/libselinux/src/callbacks.c
    ${SRC}/selinux/libselinux/src/canonicalize_context.c
    ${SRC}/selinux/libselinux/src/checkAccess.c
    ${SRC}/selinux/libselinux/src/check_context.c
    ${SRC}/selinux/libselinux/src/compute_av.c
    ${SRC}/selinux/libselinux/src/compute_create.c
    ${SRC}/selinux/libselinux/src/compute_member.c
    ${SRC}/selinux/libselinux/src/context.c
    ${SRC}/selinux/libselinux/src/deny_unknown.c
    ${SRC}/selinux/libselinux/src/disable.c
    ${SRC}/selinux/libselinux/src/enabled.c
    ${SRC}/selinux/libselinux/src/fgetfilecon.c
    ${SRC}/selinux/libselinux/src/freecon.c
    ${SRC}/selinux/libselinux/src/fsetfilecon.c
    ${SRC}/selinux/libselinux/src/get_initial_context.c
    ${SRC}/selinux/libselinux/src/getenforce.c
    ${SRC}/selinux/libselinux/src/getfilecon.c
    ${SRC}/selinux/libselinux/src/getpeercon.c
    ${SRC}/selinux/libselinux/src/init.c
    ${SRC}/selinux/libselinux/src/label.c
    ${SRC}/selinux/libselinux/src/label_backends_android.c
    ${SRC}/selinux/libselinux/src/label_file.c
    ${SRC}/selinux/libselinux/src/label_support.c
    ${SRC}/selinux/libselinux/src/lgetfilecon.c
    ${SRC}/selinux/libselinux/src/load_policy.c
    ${SRC}/selinux/libselinux/src/lsetfilecon.c
    ${SRC}/selinux/libselinux/src/mapping.c
    ${SRC}/selinux/libselinux/src/matchpathcon.c
    ${SRC}/selinux/libselinux/src/policyvers.c
    ${SRC}/selinux/libselinux/src/procattr.c
    ${SRC}/selinux/libselinux/src/regex.c
    ${SRC}/selinux/libselinux/src/reject_unknown.c
    ${SRC}/selinux/libselinux/src/selinux_internal.c
    ${SRC}/selinux/libselinux/src/sestatus.c
    ${SRC}/selinux/libselinux/src/setenforce.c
    ${SRC}/selinux/libselinux/src/setfilecon.c
    ${SRC}/selinux/libselinux/src/setrans_client.c
    ${SRC}/selinux/libselinux/src/sha1.c
    ${SRC}/selinux/libselinux/src/stringrep.c
)
target_compile_definitions(libselinux PRIVATE
    AUDITD_LOG_TAG=1003 _GNU_SOURCE HOST USE_PCRE2
    DISABLE_SETRANS DISABLE_BOOL NO_MEDIA_BACKEND NO_X_BACKEND NO_DB_BACKEND
    PCRE2_CODE_UNIT_WIDTH=8
)
target_include_directories(libselinux PUBLIC
    ${SRC}/selinux/libselinux/include
    ${SRC}/selinux/libsepol/include
    ${SRC}/core/libcutils/include
    ${SRC}/core/libpackagelistparser/include
    ${SRC}/logging/liblog/include
    ${SRC}/pcre/include
)
target_include_directories(libselinux PRIVATE
    ${SRC}/selinux/libselinux/src
)

add_library(libincfs STATIC
    ${SRC}/incremental_delivery/incfs/incfs.cpp
    ${SRC}/incremental_delivery/incfs/MountRegistry.cpp
    ${SRC}/incremental_delivery/incfs/path.cpp
    ${SRC}/incremental_delivery/incfs/util/map_ptr.cpp
    ${SRC}/incremental_delivery/sysprop/IncrementalProperties.sysprop.cpp
)
target_include_directories(libincfs PUBLIC
    ${SRC}/incremental_delivery/incfs/include
    ${SRC}/incremental_delivery/incfs/util/include
    ${SRC}/incremental_delivery/sysprop
    ${SRC}/incremental_delivery/incfs/kernel-headers
    ${SRC}/libbase/include
    ${SRC}/core/libutils/include
    ${SRC}/selinux/libselinux/include
    ${SRC}/logging/liblog/include
)

set(AAPT2_DEPS
    ${SRC}/base/tools/aapt2
    ${SRC}/core/include
    ${SRC}/core/libsystem/include
    ${SRC}/core/libutils/include
    ${SRC}/core/libprocessgroup/include
    ${SRC}/core/libvndksupport/include
    ${SRC}/core/libcutils/include
    ${SRC}/logging/liblog/include
    ${SRC}/libbase/include
    ${SRC}/native/include
    ${SRC}/native/libs/binder/include
    ${SRC}/base/libs/androidfw/include
    ${SRC}/base/libs/androidfw/include_pathutils
    ${SRC}/libziparchive/include
    ${SRC}/libziparchive/incfs_support/include
    ${SRC}/incremental_delivery/incfs/util/include
    ${SRC}/incremental_delivery/incfs/kernel-headers
    ${SRC}/base/cmds/idmap2/libidmap2_policies/include
    ${SRC}/soong/cc/libbuildversion/include
    /usr/src/googletest/googletest/include
)
foreach(tgt libbase libcutils libutils liblog libandroidfw libziparchive)
    target_include_directories(${tgt} PRIVATE ${AAPT2_DEPS})
endforeach()

# ---- proto generation (system protoc 3.21) --------------------------
set(AAPT2_PROTO_TARGETS)
file(GLOB AAPT2_PROTOS ${AAPT2_DIR}/*.proto)
foreach(p ${AAPT2_PROTOS})
    get_filename_component(w ${p} NAME_WE)
    add_custom_command(
        OUTPUT ${AAPT2_DIR}/${w}.pb.cc ${AAPT2_DIR}/${w}.pb.h
        COMMAND protoc -I ${AAPT2_DIR} --cpp_out=${AAPT2_DIR} ${w}.proto
        DEPENDS ${p}
        WORKING_DIRECTORY ${AAPT2_DIR}
        COMMENT "protoc ${w}"
    )
    list(APPEND AAPT2_PROTO_SRC ${AAPT2_DIR}/${w}.pb.cc)
    list(APPEND AAPT2_PROTO_HDRS ${AAPT2_DIR}/${w}.pb.h)
endforeach()
add_custom_target(protogen DEPENDS ${AAPT2_PROTO_SRC} ${AAPT2_PROTO_HDRS})

# ---- libaapt2 --------------------------------------------------------
add_library(libaapt2 STATIC
    ${AAPT2_DIR}/compile/IdAssigner.cpp
    ${AAPT2_DIR}/compile/InlineXmlFormatParser.cpp
    ${AAPT2_DIR}/compile/PseudolocaleGenerator.cpp
    ${AAPT2_DIR}/compile/Pseudolocalizer.cpp
    ${AAPT2_DIR}/compile/XmlIdCollector.cpp
    ${AAPT2_DIR}/configuration/ConfigurationParser.cpp
    ${AAPT2_DIR}/dump/DumpManifest.cpp
    ${AAPT2_DIR}/filter/AbiFilter.cpp
    ${AAPT2_DIR}/filter/ConfigFilter.cpp
    ${AAPT2_DIR}/format/Archive.cpp
    ${AAPT2_DIR}/format/Container.cpp
    ${AAPT2_DIR}/format/binary/BinaryResourceParser.cpp
    ${AAPT2_DIR}/format/binary/ResChunkPullParser.cpp
    ${AAPT2_DIR}/format/binary/ResEntryWriter.cpp
    ${AAPT2_DIR}/format/binary/TableFlattener.cpp
    ${AAPT2_DIR}/format/binary/XmlFlattener.cpp
    ${AAPT2_DIR}/format/proto/ProtoDeserialize.cpp
    ${AAPT2_DIR}/format/proto/ProtoSerialize.cpp
    ${AAPT2_DIR}/io/File.cpp
    ${AAPT2_DIR}/io/FileSystem.cpp
    ${AAPT2_DIR}/io/StringStream.cpp
    ${AAPT2_DIR}/io/Util.cpp
    ${AAPT2_DIR}/io/ZipArchive.cpp
    ${AAPT2_DIR}/link/AutoVersioner.cpp
    ${AAPT2_DIR}/link/FeatureFlagsFilter.cpp
    ${AAPT2_DIR}/link/ManifestFixer.cpp
    ${AAPT2_DIR}/link/NoDefaultResourceRemover.cpp
    ${AAPT2_DIR}/link/PrivateAttributeMover.cpp
    ${AAPT2_DIR}/link/ReferenceLinker.cpp
    ${AAPT2_DIR}/link/ResourceExcluder.cpp
    ${AAPT2_DIR}/link/TableMerger.cpp
    ${AAPT2_DIR}/link/XmlCompatVersioner.cpp
    ${AAPT2_DIR}/link/XmlNamespaceRemover.cpp
    ${AAPT2_DIR}/link/XmlReferenceLinker.cpp
    ${AAPT2_DIR}/optimize/MultiApkGenerator.cpp
    ${AAPT2_DIR}/optimize/ResourceDeduper.cpp
    ${AAPT2_DIR}/optimize/ResourceFilter.cpp
    ${AAPT2_DIR}/optimize/Obfuscator.cpp
    ${AAPT2_DIR}/optimize/VersionCollapser.cpp
    ${AAPT2_DIR}/process/ProductFilter.cpp
    ${AAPT2_DIR}/process/SymbolTable.cpp
    ${AAPT2_DIR}/split/TableSplitter.cpp
    ${AAPT2_DIR}/text/Printer.cpp
    ${AAPT2_DIR}/text/Unicode.cpp
    ${AAPT2_DIR}/text/Utf8Iterator.cpp
    ${AAPT2_DIR}/util/Files.cpp
    ${AAPT2_DIR}/util/Util.cpp
    ${AAPT2_DIR}/Debug.cpp
    ${AAPT2_DIR}/DominatorTree.cpp
    ${AAPT2_DIR}/java/AnnotationProcessor.cpp
    ${AAPT2_DIR}/java/ClassDefinition.cpp
    ${AAPT2_DIR}/java/JavaClassGenerator.cpp
    ${AAPT2_DIR}/java/ManifestClassGenerator.cpp
    ${AAPT2_DIR}/java/ProguardRules.cpp
    ${AAPT2_DIR}/LoadedApk.cpp
    ${AAPT2_DIR}/Resource.cpp
    ${AAPT2_DIR}/ResourceParser.cpp
    ${AAPT2_DIR}/ResourceTable.cpp
    ${AAPT2_DIR}/ResourceUtils.cpp
    ${AAPT2_DIR}/ResourceValues.cpp
    ${AAPT2_DIR}/SdkConstants.cpp
    ${AAPT2_DIR}/trace/TraceBuffer.cpp
    ${AAPT2_DIR}/xml/XmlActionExecutor.cpp
    ${AAPT2_DIR}/xml/XmlDom.cpp
    ${AAPT2_DIR}/xml/XmlPullParser.cpp
    ${AAPT2_DIR}/xml/XmlUtil.cpp
    ${AAPT2_DIR}/ValueTransformer.cpp
    ${AAPT2_PROTO_SRC}
)
target_include_directories(libaapt2 PRIVATE ${AAPT2_DEPS})

# ---- aapt2 executable -------------------------------------------------
add_executable(aapt2
    ${AAPT2_DIR}/Main.cpp
    ${AAPT2_DIR}/cmd/ApkInfo.cpp
    ${AAPT2_DIR}/cmd/Command.cpp
    ${AAPT2_DIR}/cmd/Compile.cpp
    ${AAPT2_DIR}/cmd/Convert.cpp
    ${AAPT2_DIR}/cmd/Diff.cpp
    ${AAPT2_DIR}/cmd/Dump.cpp
    ${AAPT2_DIR}/cmd/Link.cpp
    ${AAPT2_DIR}/cmd/Optimize.cpp
    ${AAPT2_DIR}/cmd/Util.cpp
)
target_include_directories(aapt2 PRIVATE ${AAPT2_DEPS})
target_link_libraries(aapt2 PRIVATE
    libaapt2 libbuildversion libandroidfw libziparchive libincfs libselinux libsepol
    libutils libcutils liblog libbase
    protobuf expat png z fmt icuuc icui18n icudata pcre2-8
    crypto pthread
)
