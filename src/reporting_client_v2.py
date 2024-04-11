import sys
import grpc
import settings_pb2 as set_proto
import settings_pb2_grpc as set_grpc
from logger import Loger
from loguru import logger
from pydantic import BaseModel, ValidationError, model_validator
from reporting_server import GAlignment, GShipClass, GShipsParameters


class Ship(BaseModel):
    aligment: int
    name: str
    classs: int
    length: float
    crew: int
    armed: bool
    officers: list[dict[str, str]]

    @model_validator(mode='after')
    def validation(self):
        data = GShipsParameters[GShipClass[self.classs]]
        aligment = bool(GAlignment[self.aligment])
        hostile = aligment if data["hostile"] is False else True
        armed = data['armed'] == self.armed if data["armed"] is False else True
        length = data['length'][0] <= self.length <= data['length'][1]
        crew = data["crew"][0] <= self.crew <= data["crew"][1]
        if hostile and length and crew and armed:
            return self
        else:
            raise ValueError(
                f"""Ship have parameters not for his class""")


def output_response(response: set_proto.Message):
    print("{")
    print(f"""\t"agliment": {GAlignment[response.aligment]}""")
    print(f"""\t"name": {response.name}""")
    print(f"""\t"class": {GShipClass[response.classs]}""")
    print(f"""\t"length": {response.length}""")
    print(f"""\t"crew_size": {response.crew_size}""")
    print("""\t"officers": [""", end="")
    for value in response.officer:
        print(f"""{{"first_name": {value.first_name}, "last_name": {value.last_name}, "rank": {value.rank}}}""", end="")
    print("]")
    print("}")


def validation_response(data: list[set_proto.Message]):
    for response in data:
        try:
            officers = [{'first_name': value.first_name, 'last_name': value.last_name, 'rank': value.rank} for value in
                        response.officer]
            Ship(aligment=response.aligment,
                 name=response.name,
                 classs=response.classs,
                 length=response.length,
                 crew=response.crew_size,
                 armed=response.armed,
                 officers=officers)
            output_response(response)
        except ValidationError as e:
            logger.error("server gave bad value", e)


def send_request(coordinates):
    with grpc.insecure_channel("127.0.0.1:1000") as chanel:
        stub = set_grpc.GettingMessageStub(chanel)
        message = set_proto.Coordinate(point1=coordinates[0],
                                       point2=coordinates[1],
                                       point3=coordinates[2],
                                       point4=coordinates[3],
                                       point5=coordinates[4],
                                       point6=coordinates[5])
        data: list[set_proto.Message] = []
        for i in stub.SendMessage(message):
            data.append(i)
        validation_response(data)


def core():
    argc = sys.argv
    if len(argc) == 7:
        argc = argc[1:]
        send_request(list(map(float, argc)))
    else:
        logger.error("Bad args")


if __name__ == "__main__":
    core()
