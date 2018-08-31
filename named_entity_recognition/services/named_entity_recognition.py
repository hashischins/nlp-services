import base64
import sys
import logging
import grpc
import concurrent.futures as futures
import services.common
from nltk import word_tokenize, pos_tag, ne_chunk


# Importing the generated codes from buildproto.sh
import services.model.named_entity_recognition_rpc_pb2_grpc as grpc_bt_grpc
from services.model.named_entity_recognition_rpc_pb2 import OutputMessage

logging.basicConfig(
    level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger('named_entity_recognition')


'''
Simple arithmetic services to test the Snet Daemon (gRPC), dApp and/or Snet-CLI.
The user must provide the method (arithmetic operation) and
two numeric inputs: "a" and "b".

e.g:
With dApp:  'method': mul
            'params': {"a": 12.0, "b": 77.0}
Resulting:  response:
                value: 924.0


Full snet-cli cmd:
$ snet client call mul '{"a":12.0, "b":77.0}'

Result:
(Transaction info)
Signing job...

Read call params from cmdline...

Calling services...

    response:
        value: 924.0
'''


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class ShowMessageServicer(grpc_bt_grpc.ShowMessageServicer):

    def __init__(self):
        # Just for debugging purpose.
        log.debug("ShowMessageServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def show(self, request, context):
        # In our case, request is a InputMessage() object (from .proto file)
        self.value = request.value

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()

        self.result.value = "Processed => " + self.value
        # log.debug('add({},{})={}'.format(self.a, self.b, self.result.value))
        return self.result


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class TokenizeMessageServicer(grpc_bt_grpc.TokenizeMessageServicer):

    def __init__(self):
        # Just for debugging purpose.
        log.debug("TokenizeMessageServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def tokenize(self, request, context):
        # In our case, request is a InputMessage() object (from .proto file)
        self.value = request.value
        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()

        # Base64 decoding
        sentence = base64.b64decode(self.value).decode('utf-8')

        # Sentence tokenizing
        tokenized_sentence = word_tokenize(sentence)

        # Encoding result
        resultBase64 = base64.b64encode(str(tokenized_sentence).encode('utf-8'))

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()
        self.result.value = resultBase64
        # log.debug('add({},{})={}'.format(self.a, self.b, self.result.value))
        return self.result


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class TagMessageServicer(grpc_bt_grpc.TaggingMessageServicer):

    def __init__(self):
        # Just for debugging purpose.
        log.debug("TagMessageServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def tag(self, request, context):
        # In our case, request is a InputMessage() object (from .proto file)
        self.value = request.value
        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()

        # Base64 decoding
        sentence = base64.b64decode(self.value).decode('utf-8')

        # Sentence tokenizing
        tokenized_sentence = word_tokenize(sentence)

        # Sentence taggning
        tagged_sentence = pos_tag(tokenized_sentence)

        # Encoding result
        resultBase64 = base64.b64encode(str(tagged_sentence).encode('utf-8'))

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()
        self.result.value = resultBase64
        # log.debug('add({},{})={}'.format(self.a, self.b, self.result.value))
        return self.result


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class ChunkMessageServicer(grpc_bt_grpc.ChunkMessageServicer):

    def __init__(self):
        # Just for debugging purpose.
        log.debug("ChunkMessageServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def chunk(self, request, context):
        # In our case, request is a InputMessage() object (from .proto file)
        self.value = request.value
        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()

        # Base64 decoding
        sentence = base64.b64decode(self.value).decode('utf-8')

        # Sentence tokenizing
        tokenized_sentence = word_tokenize(sentence)

        # Sentence taggning
        tagged_sentence = pos_tag(tokenized_sentence)

        # Sentence chunking
        chunked_sentence = ne_chunk(tagged_sentence)

        # Encoding result
        resultBase64 = base64.b64encode(str(chunked_sentence).encode('utf-8'))

        # To respond we need to create a OutputMessage() object (from .proto file)
        self.result = OutputMessage()
        self.result.value = resultBase64
        # log.debug('add({},{})={}'.format(self.a, self.b, self.result.value))
        return self.result


# The gRPC serve function.
#
# Params:
# max_workers: pool of threads to execute calls asynchronously
# port: gRPC server port
#
# Add all your classes to the server here.
# (from generated .py files by protobuf compiler)
def serve(max_workers=10, port=7777):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    grpc_bt_grpc.add_ShowMessageServicer_to_server(ShowMessageServicer(), server)
    grpc_bt_grpc.add_TokenizeMessageServicer_to_server(TokenizeMessageServicer(), server)
    grpc_bt_grpc.add_TaggingMessageServicer_to_server(TagMessageServicer(), server)
    grpc_bt_grpc.add_ChunkMessageServicer_to_server(ChunkMessageServicer(), server)
    server.add_insecure_port('[::]:{}'.format(port))
    return server


if __name__ == '__main__':
    '''
    Runs the gRPC server to communicate with the Snet Daemon.
    '''
    parser = services.common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    services.common.main_loop(serve, args)
