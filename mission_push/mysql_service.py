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

    def get_mission_push(self, kst_date, kst_time):
        with self.connection_pool.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                try:

                    sql = f"""
                    SELECT m.description, m.alert_time, p.push_token 
                    FROM mission m 
                    JOIN push p ON m.user_id = p.user_id 
                    JOIN alert_setting a ON p.device_id = a.device_id AND a.mission = 'CHECKED' 
                    WHERE m.alert_status = 'CHECKED' 
                        AND m.alert_time <= '{kst_time}' 
                        AND m.push_date != '{kst_date}' 
                        AND m.deleted_date IS NULL;
                    """
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
                except Error as e:
                    raise Exception(f"Error in MysqlService.get_mission_push: {e}") from e
