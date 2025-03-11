"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'google/cloud/netapp/v1/common.proto')
_sym_db = _symbol_database.Default()
from .....google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#google/cloud/netapp/v1/common.proto\x12\x16google.cloud.netapp.v1\x1a\x1fgoogle/api/field_behavior.proto"\xb1\x01\n\x10LocationMetadata\x12K\n\x18supported_service_levels\x18\x01 \x03(\x0e2$.google.cloud.netapp.v1.ServiceLevelB\x03\xe0A\x03\x12P\n\x1asupported_flex_performance\x18\x02 \x03(\x0e2\'.google.cloud.netapp.v1.FlexPerformanceB\x03\xe0A\x03*_\n\x0cServiceLevel\x12\x1d\n\x19SERVICE_LEVEL_UNSPECIFIED\x10\x00\x12\x0b\n\x07PREMIUM\x10\x01\x12\x0b\n\x07EXTREME\x10\x02\x12\x0c\n\x08STANDARD\x10\x03\x12\x08\n\x04FLEX\x10\x04*n\n\x0fFlexPerformance\x12 \n\x1cFLEX_PERFORMANCE_UNSPECIFIED\x10\x00\x12\x1c\n\x18FLEX_PERFORMANCE_DEFAULT\x10\x01\x12\x1b\n\x17FLEX_PERFORMANCE_CUSTOM\x10\x02*U\n\x0eEncryptionType\x12\x1f\n\x1bENCRYPTION_TYPE_UNSPECIFIED\x10\x00\x12\x13\n\x0fSERVICE_MANAGED\x10\x01\x12\r\n\tCLOUD_KMS\x10\x02*T\n\x14DirectoryServiceType\x12&\n"DIRECTORY_SERVICE_TYPE_UNSPECIFIED\x10\x00\x12\x14\n\x10ACTIVE_DIRECTORY\x10\x01B\xad\x01\n\x1acom.google.cloud.netapp.v1B\x0bCommonProtoP\x01Z2cloud.google.com/go/netapp/apiv1/netapppb;netapppb\xaa\x02\x16Google.Cloud.NetApp.V1\xca\x02\x16Google\\Cloud\\NetApp\\V1\xea\x02\x19Google::Cloud::NetApp::V1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'google.cloud.netapp.v1.common_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x1acom.google.cloud.netapp.v1B\x0bCommonProtoP\x01Z2cloud.google.com/go/netapp/apiv1/netapppb;netapppb\xaa\x02\x16Google.Cloud.NetApp.V1\xca\x02\x16Google\\Cloud\\NetApp\\V1\xea\x02\x19Google::Cloud::NetApp::V1'
    _globals['_LOCATIONMETADATA'].fields_by_name['supported_service_levels']._loaded_options = None
    _globals['_LOCATIONMETADATA'].fields_by_name['supported_service_levels']._serialized_options = b'\xe0A\x03'
    _globals['_LOCATIONMETADATA'].fields_by_name['supported_flex_performance']._loaded_options = None
    _globals['_LOCATIONMETADATA'].fields_by_name['supported_flex_performance']._serialized_options = b'\xe0A\x03'
    _globals['_SERVICELEVEL']._serialized_start = 276
    _globals['_SERVICELEVEL']._serialized_end = 371
    _globals['_FLEXPERFORMANCE']._serialized_start = 373
    _globals['_FLEXPERFORMANCE']._serialized_end = 483
    _globals['_ENCRYPTIONTYPE']._serialized_start = 485
    _globals['_ENCRYPTIONTYPE']._serialized_end = 570
    _globals['_DIRECTORYSERVICETYPE']._serialized_start = 572
    _globals['_DIRECTORYSERVICETYPE']._serialized_end = 656
    _globals['_LOCATIONMETADATA']._serialized_start = 97
    _globals['_LOCATIONMETADATA']._serialized_end = 274