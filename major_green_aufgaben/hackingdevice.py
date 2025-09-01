import grpc
import api_pb2
import api_pb2_grpc


def run():
    with grpc.insecure_channel("10.255.255.254:2028") as channel:
        stub = api_pb2_grpc.HackingDeviceServerStub(channel)

        request = api_pb2.Void()

        try:
            response = stub.read_secret_station_data(request)
            print("Received data:", response.data)

        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()} - {e.details()}")

if __name__ == '__main__':
    run()
