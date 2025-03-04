# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import service as _service
from google.protobuf import service_reflection
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='service.proto',
  package='ai_flow',
  syntax='proto3',
  serialized_options=_b('\220\001\001'),
  serialized_pb=_b('\n\rservice.proto\x12\x07\x61i_flow\"\x1f\n\rRecordRequest\x12\x0e\n\x06record\x18\x01 \x01(\t\" \n\x0eRecordResponse\x12\x0e\n\x06record\x18\x01 \x01(\t2J\n\x0c\x41gentService\x12:\n\x05\x63lick\x12\x16.ai_flow.RecordRequest\x1a\x17.ai_flow.RecordResponse\"\x00\x32R\n\x10InferenceService\x12>\n\tinference\x12\x16.ai_flow.RecordRequest\x1a\x17.ai_flow.RecordResponse\"\x00\x42\x03\x90\x01\x01\x62\x06proto3')
)




_RECORDREQUEST = _descriptor.Descriptor(
  name='RecordRequest',
  full_name='ai_flow.RecordRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='record', full_name='ai_flow.RecordRequest.record', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=26,
  serialized_end=57,
)


_RECORDRESPONSE = _descriptor.Descriptor(
  name='RecordResponse',
  full_name='ai_flow.RecordResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='record', full_name='ai_flow.RecordResponse.record', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=59,
  serialized_end=91,
)

DESCRIPTOR.message_types_by_name['RecordRequest'] = _RECORDREQUEST
DESCRIPTOR.message_types_by_name['RecordResponse'] = _RECORDRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RecordRequest = _reflection.GeneratedProtocolMessageType('RecordRequest', (_message.Message,), {
  'DESCRIPTOR' : _RECORDREQUEST,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:ai_flow.RecordRequest)
  })
_sym_db.RegisterMessage(RecordRequest)

RecordResponse = _reflection.GeneratedProtocolMessageType('RecordResponse', (_message.Message,), {
  'DESCRIPTOR' : _RECORDRESPONSE,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:ai_flow.RecordResponse)
  })
_sym_db.RegisterMessage(RecordResponse)


DESCRIPTOR._options = None

_AGENTSERVICE = _descriptor.ServiceDescriptor(
  name='AgentService',
  full_name='ai_flow.AgentService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=93,
  serialized_end=167,
  methods=[
  _descriptor.MethodDescriptor(
    name='click',
    full_name='ai_flow.AgentService.click',
    index=0,
    containing_service=None,
    input_type=_RECORDREQUEST,
    output_type=_RECORDRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_AGENTSERVICE)

DESCRIPTOR.services_by_name['AgentService'] = _AGENTSERVICE


_INFERENCESERVICE = _descriptor.ServiceDescriptor(
  name='InferenceService',
  full_name='ai_flow.InferenceService',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  serialized_start=169,
  serialized_end=251,
  methods=[
  _descriptor.MethodDescriptor(
    name='inference',
    full_name='ai_flow.InferenceService.inference',
    index=0,
    containing_service=None,
    input_type=_RECORDREQUEST,
    output_type=_RECORDRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_INFERENCESERVICE)

DESCRIPTOR.services_by_name['InferenceService'] = _INFERENCESERVICE

AgentService = service_reflection.GeneratedServiceType('AgentService', (_service.Service,), dict(
  DESCRIPTOR = _AGENTSERVICE,
  __module__ = 'service_pb2'
  ))

AgentService_Stub = service_reflection.GeneratedServiceStubType('AgentService_Stub', (AgentService,), dict(
  DESCRIPTOR = _AGENTSERVICE,
  __module__ = 'service_pb2'
  ))


InferenceService = service_reflection.GeneratedServiceType('InferenceService', (_service.Service,), dict(
  DESCRIPTOR = _INFERENCESERVICE,
  __module__ = 'service_pb2'
  ))

InferenceService_Stub = service_reflection.GeneratedServiceStubType('InferenceService_Stub', (InferenceService,), dict(
  DESCRIPTOR = _INFERENCESERVICE,
  __module__ = 'service_pb2'
  ))


# @@protoc_insertion_point(module_scope)
