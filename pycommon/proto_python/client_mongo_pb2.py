# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: client_mongo.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import service as _service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_pb2 as common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='client_mongo.proto',
  package='alpha.server',
  syntax='proto3',
  serialized_pb=_b('\n\x12\x63lient_mongo.proto\x12\x0c\x61lpha.server\x1a\x0c\x63ommon.proto\"s\n\x0e\x46indDocRequest\x12\x13\n\x0b\x63\x61llback_id\x18\x01 \x01(\x05\x12\n\n\x02\x64\x62\x18\x02 \x01(\t\x12\x12\n\ncollection\x18\x03 \x01(\t\x12\r\n\x05query\x18\x04 \x01(\t\x12\x0e\n\x06\x66ields\x18\x05 \x01(\t\x12\r\n\x05limit\x18\x06 \x01(\t\"c\n\x10UpdateDocRequest\x12\x13\n\x0b\x63\x61llback_id\x18\x01 \x01(\x05\x12\n\n\x02\x64\x62\x18\x02 \x01(\t\x12\x12\n\ncollection\x18\x03 \x01(\t\x12\r\n\x05query\x18\x04 \x01(\t\x12\x0b\n\x03\x64oc\x18\x05 \x01(\t\"T\n\x10InsertDocRequest\x12\x13\n\x0b\x63\x61llback_id\x18\x01 \x01(\x05\x12\n\n\x02\x64\x62\x18\x02 \x01(\t\x12\x12\n\ncollection\x18\x03 \x01(\t\x12\x0b\n\x03\x64oc\x18\x04 \x01(\t\"A\n\x0c\x46indDocReply\x12\x13\n\x0b\x63\x61llback_id\x18\x01 \x01(\x05\x12\x0e\n\x06status\x18\x02 \x01(\x08\x12\x0c\n\x04\x64ocs\x18\x03 \x01(\t\"5\n\x0eUpdateDocReply\x12\x13\n\x0b\x63\x61llback_id\x18\x01 \x01(\x05\x12\x0e\n\x06status\x18\x02 \x01(\x08\"H\n\x0eInsertDocReply\x12\x13\n\x0b\x63\x61llback_id\x18\x01 \x01(\x05\x12\x0e\n\x06status\x18\x02 \x01(\x08\x12\x11\n\tinsert_id\x18\x03 \x01(\t2\xe4\x02\n\nIDBService\x12H\n\x0e\x63onnect_server\x12\".alpha.server.ConnectServerRequest\x1a\x12.alpha.server.Void\x12\x41\n\x0e\x65ntity_message\x12\x1b.alpha.server.EntityMessage\x1a\x12.alpha.server.Void\x12?\n\x0b\x64\x62_find_doc\x12\x1c.alpha.server.FindDocRequest\x1a\x12.alpha.server.Void\x12\x43\n\rdb_update_doc\x12\x1e.alpha.server.UpdateDocRequest\x1a\x12.alpha.server.Void\x12\x43\n\rdb_insert_doc\x12\x1e.alpha.server.InsertDocRequest\x1a\x12.alpha.server.Void2\xf3\x02\n\x10IDBClientService\x12\x45\n\rconnect_reply\x12 .alpha.server.ConnectServerReply\x1a\x12.alpha.server.Void\x12\x41\n\x0e\x65ntity_message\x12\x1b.alpha.server.EntityMessage\x1a\x12.alpha.server.Void\x12\x43\n\x11\x64\x62_find_doc_reply\x12\x1a.alpha.server.FindDocReply\x1a\x12.alpha.server.Void\x12G\n\x13\x64o_update_doc_reply\x12\x1c.alpha.server.UpdateDocReply\x1a\x12.alpha.server.Void\x12G\n\x13\x64o_insert_doc_reply\x12\x1c.alpha.server.InsertDocReply\x1a\x12.alpha.server.VoidB\x03\x90\x01\x01\x62\x06proto3')
  ,
  dependencies=[common__pb2.DESCRIPTOR,])




_FINDDOCREQUEST = _descriptor.Descriptor(
  name='FindDocRequest',
  full_name='alpha.server.FindDocRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='callback_id', full_name='alpha.server.FindDocRequest.callback_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='db', full_name='alpha.server.FindDocRequest.db', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='collection', full_name='alpha.server.FindDocRequest.collection', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='query', full_name='alpha.server.FindDocRequest.query', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fields', full_name='alpha.server.FindDocRequest.fields', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='limit', full_name='alpha.server.FindDocRequest.limit', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=50,
  serialized_end=165,
)


_UPDATEDOCREQUEST = _descriptor.Descriptor(
  name='UpdateDocRequest',
  full_name='alpha.server.UpdateDocRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='callback_id', full_name='alpha.server.UpdateDocRequest.callback_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='db', full_name='alpha.server.UpdateDocRequest.db', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='collection', full_name='alpha.server.UpdateDocRequest.collection', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='query', full_name='alpha.server.UpdateDocRequest.query', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='doc', full_name='alpha.server.UpdateDocRequest.doc', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=167,
  serialized_end=266,
)


_INSERTDOCREQUEST = _descriptor.Descriptor(
  name='InsertDocRequest',
  full_name='alpha.server.InsertDocRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='callback_id', full_name='alpha.server.InsertDocRequest.callback_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='db', full_name='alpha.server.InsertDocRequest.db', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='collection', full_name='alpha.server.InsertDocRequest.collection', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='doc', full_name='alpha.server.InsertDocRequest.doc', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=268,
  serialized_end=352,
)


_FINDDOCREPLY = _descriptor.Descriptor(
  name='FindDocReply',
  full_name='alpha.server.FindDocReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='callback_id', full_name='alpha.server.FindDocReply.callback_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='alpha.server.FindDocReply.status', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='docs', full_name='alpha.server.FindDocReply.docs', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=354,
  serialized_end=419,
)


_UPDATEDOCREPLY = _descriptor.Descriptor(
  name='UpdateDocReply',
  full_name='alpha.server.UpdateDocReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='callback_id', full_name='alpha.server.UpdateDocReply.callback_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='alpha.server.UpdateDocReply.status', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=421,
  serialized_end=474,
)


_INSERTDOCREPLY = _descriptor.Descriptor(
  name='InsertDocReply',
  full_name='alpha.server.InsertDocReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='callback_id', full_name='alpha.server.InsertDocReply.callback_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='alpha.server.InsertDocReply.status', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='insert_id', full_name='alpha.server.InsertDocReply.insert_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=476,
  serialized_end=548,
)

DESCRIPTOR.message_types_by_name['FindDocRequest'] = _FINDDOCREQUEST
DESCRIPTOR.message_types_by_name['UpdateDocRequest'] = _UPDATEDOCREQUEST
DESCRIPTOR.message_types_by_name['InsertDocRequest'] = _INSERTDOCREQUEST
DESCRIPTOR.message_types_by_name['FindDocReply'] = _FINDDOCREPLY
DESCRIPTOR.message_types_by_name['UpdateDocReply'] = _UPDATEDOCREPLY
DESCRIPTOR.message_types_by_name['InsertDocReply'] = _INSERTDOCREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FindDocRequest = _reflection.GeneratedProtocolMessageType('FindDocRequest', (_message.Message,), dict(
  DESCRIPTOR = _FINDDOCREQUEST,
  __module__ = 'client_mongo_pb2'
  # @@protoc_insertion_point(class_scope:alpha.server.FindDocRequest)
  ))
_sym_db.RegisterMessage(FindDocRequest)

UpdateDocRequest = _reflection.GeneratedProtocolMessageType('UpdateDocRequest', (_message.Message,), dict(
  DESCRIPTOR = _UPDATEDOCREQUEST,
  __module__ = 'client_mongo_pb2'
  # @@protoc_insertion_point(class_scope:alpha.server.UpdateDocRequest)
  ))
_sym_db.RegisterMessage(UpdateDocRequest)

InsertDocRequest = _reflection.GeneratedProtocolMessageType('InsertDocRequest', (_message.Message,), dict(
  DESCRIPTOR = _INSERTDOCREQUEST,
  __module__ = 'client_mongo_pb2'
  # @@protoc_insertion_point(class_scope:alpha.server.InsertDocRequest)
  ))
_sym_db.RegisterMessage(InsertDocRequest)

FindDocReply = _reflection.GeneratedProtocolMessageType('FindDocReply', (_message.Message,), dict(
  DESCRIPTOR = _FINDDOCREPLY,
  __module__ = 'client_mongo_pb2'
  # @@protoc_insertion_point(class_scope:alpha.server.FindDocReply)
  ))
_sym_db.RegisterMessage(FindDocReply)

UpdateDocReply = _reflection.GeneratedProtocolMessageType('UpdateDocReply', (_message.Message,), dict(
  DESCRIPTOR = _UPDATEDOCREPLY,
  __module__ = 'client_mongo_pb2'
  # @@protoc_insertion_point(class_scope:alpha.server.UpdateDocReply)
  ))
_sym_db.RegisterMessage(UpdateDocReply)

InsertDocReply = _reflection.GeneratedProtocolMessageType('InsertDocReply', (_message.Message,), dict(
  DESCRIPTOR = _INSERTDOCREPLY,
  __module__ = 'client_mongo_pb2'
  # @@protoc_insertion_point(class_scope:alpha.server.InsertDocReply)
  ))
_sym_db.RegisterMessage(InsertDocReply)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\220\001\001'))

_IDBSERVICE = _descriptor.ServiceDescriptor(
  name='IDBService',
  full_name='alpha.server.IDBService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=551,
  serialized_end=907,
  methods=[
  _descriptor.MethodDescriptor(
    name='connect_server',
    full_name='alpha.server.IDBService.connect_server',
    index=0,
    containing_service=None,
    input_type=common__pb2._CONNECTSERVERREQUEST,
    output_type=common__pb2._VOID,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='entity_message',
    full_name='alpha.server.IDBService.entity_message',
    index=1,
    containing_service=None,
    input_type=common__pb2._ENTITYMESSAGE,
    output_type=common__pb2._VOID,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='db_find_doc',
    full_name='alpha.server.IDBService.db_find_doc',
    index=2,
    containing_service=None,
    input_type=_FINDDOCREQUEST,
    output_type=common__pb2._VOID,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='db_update_doc',
    full_name='alpha.server.IDBService.db_update_doc',
    index=3,
    containing_service=None,
    input_type=_UPDATEDOCREQUEST,
    output_type=common__pb2._VOID,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='db_insert_doc',
    full_name='alpha.server.IDBService.db_insert_doc',
    index=4,
    containing_service=None,
    input_type=_INSERTDOCREQUEST,
    output_type=common__pb2._VOID,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_IDBSERVICE)

DESCRIPTOR.services_by_name['IDBService'] = _IDBSERVICE


_IDBCLIENTSERVICE = _descriptor.ServiceDescriptor(
  name='IDBClientService',
  full_name='alpha.server.IDBClientService',
  file=DESCRIPTOR,
  index=1,
  options=None,
  serialized_start=910,
  serialized_end=1281,
  methods=[
  _descriptor.MethodDescriptor(
    name='connect_reply',
    full_name='alpha.server.IDBClientService.connect_reply',
    index=0,
    containing_service=None,
    input_type=common__pb2._CONNECTSERVERREPLY,
    output_type=common__pb2._VOID,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='entity_message',
    full_name='alpha.server.IDBClientService.entity_message',
    index=1,
    containing_service=None,
    input_type=common__pb2._ENTITYMESSAGE,
    output_type=common__pb2._VOID,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='db_find_doc_reply',
    full_name='alpha.server.IDBClientService.db_find_doc_reply',
    index=2,
    containing_service=None,
    input_type=_FINDDOCREPLY,
    output_type=common__pb2._VOID,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='do_update_doc_reply',
    full_name='alpha.server.IDBClientService.do_update_doc_reply',
    index=3,
    containing_service=None,
    input_type=_UPDATEDOCREPLY,
    output_type=common__pb2._VOID,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='do_insert_doc_reply',
    full_name='alpha.server.IDBClientService.do_insert_doc_reply',
    index=4,
    containing_service=None,
    input_type=_INSERTDOCREPLY,
    output_type=common__pb2._VOID,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_IDBCLIENTSERVICE)

DESCRIPTOR.services_by_name['IDBClientService'] = _IDBCLIENTSERVICE

IDBService = service_reflection.GeneratedServiceType('IDBService', (_service.Service,), dict(
  DESCRIPTOR = _IDBSERVICE,
  __module__ = 'client_mongo_pb2'
  ))

IDBService_Stub = service_reflection.GeneratedServiceStubType('IDBService_Stub', (IDBService,), dict(
  DESCRIPTOR = _IDBSERVICE,
  __module__ = 'client_mongo_pb2'
  ))


IDBClientService = service_reflection.GeneratedServiceType('IDBClientService', (_service.Service,), dict(
  DESCRIPTOR = _IDBCLIENTSERVICE,
  __module__ = 'client_mongo_pb2'
  ))

IDBClientService_Stub = service_reflection.GeneratedServiceStubType('IDBClientService_Stub', (IDBClientService,), dict(
  DESCRIPTOR = _IDBCLIENTSERVICE,
  __module__ = 'client_mongo_pb2'
  ))


# @@protoc_insertion_point(module_scope)
