# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import service_pb2 as service__pb2


class AgentServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.click = channel.unary_unary(
        '/ai_flow.AgentService/click',
        request_serializer=service__pb2.RecordRequest.SerializeToString,
        response_deserializer=service__pb2.RecordResponse.FromString,
        )


class AgentServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def click(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AgentServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'click': grpc.unary_unary_rpc_method_handler(
          servicer.click,
          request_deserializer=service__pb2.RecordRequest.FromString,
          response_serializer=service__pb2.RecordResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ai_flow.AgentService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class InferenceServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.inference = channel.unary_unary(
        '/ai_flow.InferenceService/inference',
        request_serializer=service__pb2.RecordRequest.SerializeToString,
        response_deserializer=service__pb2.RecordResponse.FromString,
        )


class InferenceServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def inference(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_InferenceServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'inference': grpc.unary_unary_rpc_method_handler(
          servicer.inference,
          request_deserializer=service__pb2.RecordRequest.FromString,
          response_serializer=service__pb2.RecordResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ai_flow.InferenceService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
