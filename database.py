from mysql import connector
# from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy import text


load_dotenv()


class MySQLDatabase:
    def __init__(self) -> None:
        self.__host = os.getenv('HOST')
        self.__username = os.getenv('MYSQL_USER')
        self.__password = os.getenv('MYSQL_PASSWORD')
        self.__database = os.getenv('MYSQL_DATABASE')
        self.__port = os.getenv('PORT')
        self.conn = self._connect()
    
    def _connect(self):
        return connector.connect(
            # f"mysql+mysql-connector-python://{self.__username}:{self.__password}@db:{self.__port}/{self.__database}"
            user=self.__username,
            password=self.__password,
            host=self.__host,
            port=self.__port,
            database=self.__database,
            ssl_disabled=True
        )
    
    def test_connection(self):
        conn_result = ''

        try:
            self.conn.execute(text('SHOW TABLES'))
            conn_result = 'Connected successfully'
        except Exception as e:
            conn_result = f'Connection failed. Error: {e}'

        return {'Database conection status': conn_result}
    
    def query(self, query: str) -> str:
        try:
            result = self.conn.execute(text(query)).fetchall()
        except Exception as e:
            pass
        finally:
            self.conn.close()
            return result
