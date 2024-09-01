import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


connection = psycopg2.connect(
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT"),
    database=os.environ.get("DB_NAME"),
)
cursor = connection.cursor()

# get user and all metrics/intereactions

cursor.execute(
    """SELECT u.id, u.name, u.email, u.role, u.age, u.music_genre
    FROM users u"""
)

user = cursor.fetchall()
for u in user:
    print("Name:", u[1])
    print("Email:", u[3])
    print("id:", u[0])
    print("\n")
