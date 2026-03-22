import os
import time
from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


def check_db_connection():
    retries = int(os.getenv("DB_CONNECT_RETRIES", "10"))
    delay_seconds = float(os.getenv("DB_CONNECT_DELAY", "1"))
    last_error = "No se pudo establecer conexion"

    for attempt in range(retries):
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "mysql"),
                port=int(os.getenv("DB_PORT", "3306")),
                user=os.getenv("DB_USER", "appuser"),
                password=os.getenv("DB_PASSWORD", "apppassword"),
                database=os.getenv("DB_NAME", "appdb"),
            )
            if connection.is_connected():
                connection.close()
                return True, "Conexion a MySQL exitosa"
            last_error = "No se pudo establecer conexion"
        except Error as err:
            last_error = str(err)

        if attempt < retries - 1:
            time.sleep(delay_seconds)

    return False, f"Error de conexion: {last_error}"


@app.route("/")
def hello():
    ok, message = check_db_connection()
    return jsonify(
        {
            "message": "Hola Mundo",
            "mysql_connected": ok,
            "mysql_status": message,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
