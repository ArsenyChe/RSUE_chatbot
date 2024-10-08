import psycopg2
from os import getenv
from dotenv import load_dotenv

load_dotenv()

try:
    connection = psycopg2.connect(
        host = getenv('HOST'),
        user = getenv('USER'),
        password = getenv('PASS'),
        database = getenv('DB_NAME_MESSAGE')
    )
    print(f'[INFO] PostgreSQL connect DB_NAME_MESSAGE')
except Exception as e:
    print(f'[INFO] PostgreSQL {e}')

async def add_message(chat_id: int, message_id: int, question_text: str, answer_text: str, formatted_date: str) -> None:
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO message (
                    chat_id, 
                    message_id, 
                    message_question_text, 
                    message_answer_text, 
                    formatted_date) 
                VALUES (%s,%s,%s,%s,TO_DATE(%s, 'YYYY-MM-DD'));""",
                (chat_id,
                message_id, 
                question_text, 
                answer_text, 
                formatted_date))
            connection.commit()
    except Exception as e:
        print(f'[INFO] PostgreSQL add_message {e}')

async def update_message(evaluation_response: bool, chat_id: int, message_id: int) -> None:
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """UPDATE message 
                SET evaluation_response = %s
                WHERE chat_id = %s 
                AND message_id = %s;""",
                (evaluation_response,
                chat_id,
                message_id))
            connection.commit()
    except Exception as e:
        print(f'[INFO] PostgreSQL update_message {e}')

async def show_questions(date: str, to_date: str, evaluation_response: bool):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT message_question_text FROM message
                WHERE (evaluation_response IS NULL OR evaluation_response = %s) AND (formatted_date BETWEEN %s AND %s)""",
                (evaluation_response,
                date,
                to_date))
            connection.commit()
            return cursor.fetchall()
    except Exception as e:
        print(f'[INFO] PostgreSQL update_message {e}')