import random
from loguru import logger
from logger import Loger
import faker
import grpc
from concurrent import futures
import settings_pb2 as ship_proto
import settings_pb2_grpc as ship_grpc

GAlignment = ('Ally', 'Enemy')
GShipClass = ('Corvette', 'Frigate', 'Cruiser', 'Destroyer', 'Carrier', 'Dreadnought')
GShipsParameters = {
    "Corvette": {
        "length": [80, 250],
        "crew": [4, 10],
        "armed": True,
        "hostile": True
    },
    "Frigate": {
        "length": [300, 600],
        "crew": [10, 15],
        "armed": True,
        "hostile": False
    },
    "Cruiser": {
        "length": [500, 1000],
        "crew": [15, 30],
        "armed": True,
        "hostile": True
    },
    "Destroyer": {
        "length": [800, 2000],
        "crew": [50, 80],
        "armed": True,
        "hostile": False
    },
    "Carrier": {
        "length": [1000, 4000],
        "crew": [120, 250],
        "armed": False,
        "hostile": True
    },
    "Dreadnought": {
        "length": [5000, 20000],
        "crew": [300, 500],
        "armed": True,
        "hostile": True
    }
}


@Loger
def createData():
    global GAlignment, GShipClass, GShipsParameters
    fake = faker.Faker(['en_US'])
    officers = []
    statys = GAlignment[random.randint(0, 1)]
    officers_count = random.randint(0, 10) if statys == "Enemy" else random.randint(1, 10)
    for _ in range(officers_count):
        name = fake.name().split()
        officers.append({"first_name": name[0], "last_name": name[1], "rank": fake.job()})

    ship_class = ship_proto.ShipType.Name(random.randint(0, 5))
    ship_param = GShipsParameters[ship_class]
    data = ship_proto.Message(aligment=ship_proto.Aligment.Name(GAlignment.index(statys)),
                              name="Unknown" if statys == "Enemy" and random.randint(0, 1) else fake.name(),
                              classs=ship_class,
                              length=random.randint(ship_param['length'][0], ship_param['length'][1]),
                              crew_size=random.randint(ship_param['crew'][0], ship_param['crew'][1]),
                              armed=bool(random.randint(0, 1)),
                              officer=officers)
    return data


class GRPCServer(ship_grpc.GettingMessageServicer):
    def __init__(self, ):
        super().__init__()

    @Loger
    def SendMessage(self, request, context):
        for i in range(random.randint(1, 10)):
            yield createData()


@Loger
def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ship_grpc.add_GettingMessageServicer_to_server(GRPCServer(), server)
    server.add_insecure_port("[::]:1000")
    server.start()
    logger.warning("For stop server use CTRL+C")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(None)
        logger.info("Server is ended work")


if __name__ == "__main__":
    start_server()
