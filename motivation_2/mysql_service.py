from mysql.connector import Error
from mysql.connector import pooling


class MysqlService:

    def __init__(self, host, port, database, user, password, pool_name='mission_push_lambda', pool_size=5):

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

        try:
            self.connection_pool = pooling.MySQLConnectionPool(pool_name=pool_name,
                                                               pool_size=pool_size,
                                                               pool_reset_session=True,
                                                               host=self.host,
                                                               port=self.port,
                                                               database=self.database,
                                                               user=self.user,
                                                               password=self.password)

        except Error as e:
            raise Exception(f"Error while connecting to MySQL using Connection pool: {e}") from e

    def get_push_token(self):
        with self.connection_pool.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                try:
                    sql = f"""
                    SELECT p.push_token, p.sound 
                    FROM push p 
                    JOIN users u ON u.id = p.user_id
                    JOIN alert_setting als ON als.device_id = p.device_id
                    WHERE als.luck_message = 'CHECKED';
                    """
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
                except Error as e:
                    raise Exception(f"Error in MysqlService.get_mission_push: {e}") from e
