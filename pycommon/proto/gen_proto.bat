protoc.exe --python_out=../proto_python echo_test.proto common.proto client_server.proto client_mongo.proto
protoc.exe --cpp_out=../../client/proto common.proto client_server.proto echo_test.proto