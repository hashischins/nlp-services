#! /bin/bash
python3.6 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. services/model/named_entity_recognition_rpc.proto
