import argparse
import json
import grpc
import settings_pb2 as set_proto
import settings_pb2_grpc as set_grpc
from logger import Loger
from loguru import logger
from pydantic import BaseModel, ValidationError, model_validator
from reporting_server import GAlignment, GShipClass, GShipsParameters
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


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


@Loger
def output_response(coordinates):
    for response in select_from_table(coordinates):
        print("{")
        print(f"""\t"agliment": {response[2]}""")
        print(f"""\t"name": {response[3]}""")
        print(f"""\t"class": {response[4]}""")
        print(f"""\t"length": {response[5]}""")
        print(f"""\t"crew_size": {response[6]}""")
        print(f"""\t"armed": {response[7]}""")
        print("""\t"officers": [""", end="")
        for value in response[8]:
            print(
                f"""{{"first_name": {value['first_name']}, "last_name": {value['last_name']}, "rank": {value['rank']}}}""",
                end="")
        print("]")
        print("}")


def parse_officers(officer):
    temp = []
    for value in officer:
        temp.append(dict(first_name=value.first_name, last_name=value.last_name, rank=value.rank.replace('\'', ' ')))
    return json.dumps(temp)


def validation_response(data: list[set_proto.Message], cords):
    if len(select_from_table(cords)) == 0:
        for response in data:
            try:
                officers = [{'first_name': value.first_name, 'last_name': value.last_name, 'rank': value.rank} for value
                            in
                            response.officer]
                Ship(aligment=response.aligment,
                     name=response.name,
                     classs=response.classs,
                     length=response.length,
                     crew=response.crew_size,
                     armed=response.armed,
                     officers=officers)
                officers = parse_officers(response.officer)
                insert_into_table(response, cords, officers)
            except ValidationError as e:
                logger.error("server gave bad value", e)
    # output_response(cords)


def send_request(coordinates, str_cords):
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
        validation_response(data, str_cords)


def parser_officers(aligment):
    response = select_from_table_officers(aligment)
    data: list = []
    for list_officers in response:
        for officer in list_officers[0]:
            data.append(officer)
    return data


def search_traitors():
    ally: list = parser_officers('Ally')
    enemy: list = parser_officers('Enemy')
    traitors: list = []
    for ally_officer in ally:
        if ally_officer in enemy:
            traitors.append(ally_officer)
    for officer in traitors:
        print(f"Traitor: {officer}")
    else:
        print("Traitors don't found")


def send_request_r_all(request):
    try:
        conn = psycopg2.connect(host='127.0.0.1', port='5432', user='postgres', password='user', dbname="galaxy_store")
        cursor = conn.cursor()
        cursor.execute(request)
        return cursor.fetchall()
    except Exception as e:
        logger.exception(e)


def send_request_r_one(request):
    try:
        conn = psycopg2.connect(host='127.0.0.1', port='5432', user='postgres', password='user', dbname="galaxy_store")
        cursor = conn.cursor()
        cursor.execute(request)
        return cursor.fetchone()
    except Exception as e:
        logger.exception(e)


def send_request_without_r(request):
    try:
        conn = psycopg2.connect(host='127.0.0.1', port='5432', user='postgres', password='user', dbname="galaxy_store")
        cursor = conn.cursor()
        cursor.execute(request)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.exception(e)


def select_from_table(coordinates: str):
    requests = f"""select * from Ships where Coordinates = '{coordinates}';"""
    return send_request_r_all(requests)


def select_from_table_officers(aligment):
    requests = f"""select officers from Ships where Aligments = '{aligment}';"""
    return send_request_r_all(requests)


def insert_into_table(message: set_proto.Message, coordinates: str, officers):
    requests = f"""insert into Ships (Coordinates, Aligments, Name, ShipType, Lenght, Crew_Size, Armed, Officers)
    values ('{coordinates}', '{GAlignment[message.aligment]}', '{message.name}', '{GShipClass[message.classs]}',
    {message.length}, {message.crew_size}, {message.armed}, '{officers}');"""
    send_request_without_r(requests)


def create_table():
    try:
        conn = psycopg2.connect(host='127.0.0.1', port='5432', user='postgres', password='user', dbname="galaxy_store")
        cursor = conn.cursor()
        requests = f"""create table Ships
        (
            ID serial unique primary key, 
            Coordinates text not null,
            Aligments text not null,
            Name text not null,
            ShipType text not null,
            Lenght float not null,
            Crew_Size float not null,
            Armed bool not null,
            Officers jsonb not null
        );"""
        cursor.execute(requests)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        pass


def create_database():
    try:
        conn = psycopg2.connect(host='127.0.0.1', port='5432', user='postgres', password='user')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        requests = f"""create database galaxy_store;"""
        cursor.execute(requests)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        pass


def check_postgres_connection() -> bool:
    flag: bool = True
    try:
        conn = psycopg2.connect(host='127.0.0.1', port='5432', user='postgres', password='user')
        conn.close()
    except Exception as e:
        logger.exception(e)
        flag = False
    return flag


def init_parser(parser: argparse.ArgumentParser):
    parser.add_argument('command', choices=['scan', 'list_traitors'], help='Command to execute')
    parser.add_argument('coordinates', nargs='*', type=float, help='Coordinates for scan command')
    return parser.parse_args()


def core():
    if check_postgres_connection():
        create_database()
        create_table()
        args = init_parser(argparse.ArgumentParser(""))
        cords = '_'.join(list(map(str, args.coordinates)))
        if args.command == 'scan':
            if len(args.coordinates) == 6:
                send_request(args.coordinates, cords)
            else:
                logger.error(
                    'Invalid number of coordinates. Please provide latitude and longitude. Work\'s only for 6 coords')
        elif args.command == 'list_traitors':
            search_traitors()
    else:
        logger.error("Postgres server don't enable")


if __name__ == "__main__":
    core()
