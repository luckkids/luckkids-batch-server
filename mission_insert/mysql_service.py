from mysql.connector import Error
from mysql.connector import pooling


class MysqlService:

    def __init__(self, host, port, database, user, password, pool_name='mission_insert_batch', pool_size=2):

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

    def bulk_insert(self, records):
        if not records:
            return

        connection = None
        cursor = None

        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()

            columns = ', '.join(records[0].keys())
            placeholders = ', '.join(['%s'] * len(records[0]))
            query = f"INSERT IGNORE INTO mission_outcome ({columns}) VALUES ({placeholders})"

            values = [list(record.values()) for record in records]
            cursor.executemany(query, values)
            connection.commit()

        except Exception as e:
            if connection:
                connection.rollback()
            raise Exception(f"Error in MysqlService.bulk_insert: {e}") from e

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_mission(self):
        with self.connection_pool.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                try:
                    sql = "SELECT id FROM mission WHERE mission_active = 'TRUE' AND deleted_date IS NULL"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
                except Error as e:
                    raise Exception(f"Error in MysqlService.get_mission: {e}") from e
