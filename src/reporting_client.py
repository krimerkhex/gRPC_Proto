import sys
import grpc
import settings_pb2 as set_proto
import settings_pb2_grpc as set_grpc
from logger import Loger
from loguru import logger


@Loger
def sendRequest(coordinates):
    with grpc.insecure_channel("127.0.0.1:1000") as chanel:
        stub = set_grpc.GettingMessageStub(chanel)
        message = set_proto.Coordinate(point1=coordinates[0],
                                       point2=coordinates[1],
                                       point3=coordinates[2],
                                       point4=coordinates[3],
                                       point5=coordinates[4],
                                       point6=coordinates[5])
        for i in stub.SendMessage(message):
            print(i)


@Loger
def core():
    argc = sys.argv
    if len(argc) == 7:
        argc = argc[1:]
        sendRequest(list(map(float, argc)))
    else:
        logger.error("Bad args")


if __name__ == "__main__":
    core()
