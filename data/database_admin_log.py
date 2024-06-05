import psycopg2
from os import getenv
from dotenv import load_dotenv

load_dotenv()

try:
    connection = psycopg2.connect(
        host = getenv('HOST'),
        user = getenv('USER'),
        password = getenv('PASS'),
        database = getenv('DB_NAME_ADMIN')
    )
    print(f'[INFO] PostgreSQL connect DB_NAME_ADMIN')
except Exception as e:
    print(f'[INFO] PostgreSQL {e}')

async def add_admin(username: str, phone_number: str, email: str, name: str, surname: str, patronymic: str) -> None:
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO administrators (
                    username, 
                    phone_number, 
                    email, 
                    name, 
                    surname,
                    patronymic) 
                VALUES (%s,%s,%s,%s,%s,%s);""",
                (username,
                phone_number, 
                email, 
                name, 
                surname,
                patronymic))
            connection.commit()
    except Exception as e:
        print(f'[INFO] PostgreSQL add_admin {e}')

async def delete_admin(username: str) -> None:
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """ DELETE FROM administrators WHERE username = %s;""",
                (username,))
            connection.commit()
    except Exception as e:
        print(f'[INFO] PostgreSQL delete_admin {e}')

async def add_log(administrator_username: str, action: str, date_time: str) -> None:
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO logs (
                    administrator_username, 
                    action, 
                    date_time) 
                VALUES (%s,%s,%s);""",
                (administrator_username,
                action, 
                date_time))
            connection.commit()
    except Exception as e:
        print(f'[INFO] PostgreSQL add_log {e}')