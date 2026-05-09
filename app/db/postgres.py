import psycopg2

conn = psycopg2.connect(
    dbname="rag_db", user="postgres", password="your_password", host="localhost"
)
