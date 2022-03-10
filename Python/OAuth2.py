'''
Author - Ajin & Anant
Desc - This is a server side python program. If you call it with an agent number,
        the program should be able to send you agent information as a json payload
'''
from fastapi import FastAPI
import logging
from databricks import sql
import os

app = FastAPI()
logging.getLogger('databricks.sql').setLevel(logging.DEBUG)

@app.get('/')
def example():
    return('hello')

@app.get('/index')
def index():
    text = "Welcome to this test page"
    return text 
    
@app.get('/index/{agent_number}')
def get_agent_data():
    with sql.connect(server_hostname="int-nml.cloud.databricks.com",
                 http_path="sql/protocolv1/o/0/1012-131129-jail177",
                 access_token="dapi720a0573021803b5214b0f321f98e0cc") as connection:
      with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM default.aa LIMIT 2")
        result = cursor.fetchall()
        data = json.dumps(result)
        print(data)

if __name__ == "__main__":
    app.debug = True