from flask import Flask
import os
import psycopg2

app = Flask(__name__)

@app.route("/hello")
def hello():
    try:
        db_host = os.environ.get("DB_HOST")
        db_name = os.environ.get("DB_NAME")
        db_user = os.environ.get("DB_USER")
        db_password = os.environ.get("DB_PASSWORD")

        conn = psycopg2.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_password
        )

        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        cur.close()
        conn.close()

        return f"✅ Hello from Flask Midterm! Connected to PostgreSQL {version[0]}"
    except Exception as e:
        return f"❌ PostgreSQL connection failed: {str(e)}"
