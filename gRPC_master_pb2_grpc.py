# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import gRPC_master_pb2 as gRPC__master__pb2


class gRPC_masterStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.add_node = channel.unary_unary(
                '/gRPC_master/add_node',
                request_serializer=gRPC__master__pb2.Request.SerializeToString,
                response_deserializer=gRPC__master__pb2.ReturnedMessage.FromString,
                )
        self.remove_node = channel.unary_unary(
                '/gRPC_master/remove_node',
                request_serializer=gRPC__master__pb2.Request.SerializeToString,
                response_deserializer=gRPC__master__pb2.ReturnedMessage.FromString,
                )
        self.get_workers = channel.unary_unary(
                '/gRPC_master/get_workers',
                request_serializer=gRPC__master__pb2.Request.SerializeToString,
                response_deserializer=gRPC__master__pb2.ListedServers.FromString,
                )


class gRPC_masterServicer(object):
    """Missing associated documentation comment in .proto file."""

    def add_node(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def remove_node(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_workers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_gRPC_masterServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'add_node': grpc.unary_unary_rpc_method_handler(
                    servicer.add_node,
                    request_deserializer=gRPC__master__pb2.Request.FromString,
                    response_serializer=gRPC__master__pb2.ReturnedMessage.SerializeToString,
            ),
            'remove_node': grpc.unary_unary_rpc_method_handler(
                    servicer.remove_node,
                    request_deserializer=gRPC__master__pb2.Request.FromString,
                    response_serializer=gRPC__master__pb2.ReturnedMessage.SerializeToString,
            ),
            'get_workers': grpc.unary_unary_rpc_method_handler(
                    servicer.get_workers,
                    request_deserializer=gRPC__master__pb2.Request.FromString,
                    response_serializer=gRPC__master__pb2.ListedServers.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'gRPC_master', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class gRPC_master(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def add_node(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gRPC_master/add_node',
            gRPC__master__pb2.Request.SerializeToString,
            gRPC__master__pb2.ReturnedMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def remove_node(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gRPC_master/remove_node',
            gRPC__master__pb2.Request.SerializeToString,
            gRPC__master__pb2.ReturnedMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_workers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/gRPC_master/get_workers',
            gRPC__master__pb2.Request.SerializeToString,
            gRPC__master__pb2.ListedServers.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
