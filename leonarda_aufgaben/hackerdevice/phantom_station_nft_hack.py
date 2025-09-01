import grpc
import api_pb2
import api_pb2_grpc

def read_secret_station_data():
    with grpc.insecure_channel('10.255.255.254:2028') as channel:
        stub = api_pb2_grpc.HackingDeviceServerStub(channel)

        request = api_pb2.Void()

        response = stub.read_secret_station_data(request)

        print("Received data:")
        for item in response.data:
            print(item)


if __name__ == '__main__':
    read_secret_station_data()