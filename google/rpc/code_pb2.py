# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/rpc/code.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/rpc/code.proto',
  package='google.rpc',
  syntax='proto3',
  serialized_options=b'\n\016com.google.rpcB\tCodeProtoP\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x15google/rpc/code.proto\x12\ngoogle.rpc*\xb7\x02\n\x04\x43ode\x12\x06\n\x02OK\x10\x00\x12\r\n\tCANCELLED\x10\x01\x12\x0b\n\x07UNKNOWN\x10\x02\x12\x14\n\x10INVALID_ARGUMENT\x10\x03\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x04\x12\r\n\tNOT_FOUND\x10\x05\x12\x12\n\x0e\x41LREADY_EXISTS\x10\x06\x12\x15\n\x11PERMISSION_DENIED\x10\x07\x12\x13\n\x0fUNAUTHENTICATED\x10\x10\x12\x16\n\x12RESOURCE_EXHAUSTED\x10\x08\x12\x17\n\x13\x46\x41ILED_PRECONDITION\x10\t\x12\x0b\n\x07\x41\x42ORTED\x10\n\x12\x10\n\x0cOUT_OF_RANGE\x10\x0b\x12\x11\n\rUNIMPLEMENTED\x10\x0c\x12\x0c\n\x08INTERNAL\x10\r\x12\x0f\n\x0bUNAVAILABLE\x10\x0e\x12\r\n\tDATA_LOSS\x10\x0f\x42\x1d\n\x0e\x63om.google.rpcB\tCodeProtoP\x01\x62\x06proto3'
)

_CODE = _descriptor.EnumDescriptor(
  name='Code',
  full_name='google.rpc.Code',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OK', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CANCELLED', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_ARGUMENT', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DEADLINE_EXCEEDED', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_FOUND', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ALREADY_EXISTS', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PERMISSION_DENIED', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNAUTHENTICATED', index=8, number=16,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RESOURCE_EXHAUSTED', index=9, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FAILED_PRECONDITION', index=10, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ABORTED', index=11, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OUT_OF_RANGE', index=12, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNIMPLEMENTED', index=13, number=12,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INTERNAL', index=14, number=13,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNAVAILABLE', index=15, number=14,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATA_LOSS', index=16, number=15,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=38,
  serialized_end=349,
)
_sym_db.RegisterEnumDescriptor(_CODE)

Code = enum_type_wrapper.EnumTypeWrapper(_CODE)
OK = 0
CANCELLED = 1
UNKNOWN = 2
INVALID_ARGUMENT = 3
DEADLINE_EXCEEDED = 4
NOT_FOUND = 5
ALREADY_EXISTS = 6
PERMISSION_DENIED = 7
UNAUTHENTICATED = 16
RESOURCE_EXHAUSTED = 8
FAILED_PRECONDITION = 9
ABORTED = 10
OUT_OF_RANGE = 11
UNIMPLEMENTED = 12
INTERNAL = 13
UNAVAILABLE = 14
DATA_LOSS = 15


DESCRIPTOR.enum_types_by_name['Code'] = _CODE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
