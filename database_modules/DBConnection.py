import mysql.connector.pooling

# Create a connection pool
_connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="weather-gov-pool",
    pool_size=5,
    pool_reset_session=True,
    host="127.0.0.1",
    user="root",
    password="admin1234",
    database="weather-gov",
    charset="utf8"
)

def get_connection():
    # Get a connection from the pool
    connection = _connection_pool.get_connection()
    return connection