import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel


class product(BaseModel):
    def __getitem__(self, key):
        return getattr(self, key)

    name: str
    price: int


app = FastAPI()
return_state = "Query executed"


@app.put("/")
async def insert_product(product_info: product):
    try:
        config = {"user": "test", "password": "sample", "host": "localhost", "database": "test"}
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(prepared=True)

        sql_select = "SELECT COUNT(id) from test_1 WHERE name=(%s) and price=(%s)"
        json_data = product_info.__dict__
        data = (json_data.get("name"), json_data.get("price"))

        cursor.execute(sql_select, data)
        rows = cursor.fetchall()
        count = rows[0][0]

        if 0 == count:
            # sql_insert_dict = "INSERT INTO test_1 VALUES (%(name)s, %(price)s)"
            # data_dict = {"name": "Hotel", "price": "24600"}

            sql_insert = "INSERT INTO test_1 (Name,Price) VALUES (%s, %s)"

            cursor.execute(sql_insert, data)
            connection.commit()

    except mysql.connector.Error as error:
        print("Query Failed {}".format(error))
        return_state = "Query failed"
    finally:
        cursor.close()
        connection.close()

    return return_state