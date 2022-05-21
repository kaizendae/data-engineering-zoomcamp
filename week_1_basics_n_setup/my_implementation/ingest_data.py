import pandas as pd
from time import time
import argparse
from sqlalchemy import create_engine
from os import system
# user, password, host, port, database, nametable name, csv_url



def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    database = params.database
    table = params.table
    url = params.url
    file_name = 'data'

    # download dataset
    system(f"wget {url} -O {file_name}")
    df = pd.read_parquet(file_name)
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    df = pd.read_parquet(file_name, engine="fastparquet")

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.to_sql(name=table, con=engine, if_exists='append')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest data into postgres')
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='username for postgres')
    parser.add_argument('--host', help='username for postgres')
    parser.add_argument('--port', help='username for postgres')
    parser.add_argument('--database', help='username for postgres')
    parser.add_argument('--table', help='username for postgres')
    parser.add_argument('--url', help='username for postgres')
    args = parser.parse_args()
    # print(args.accumulate(args.integers))
    main(args)




# from sqlalchemy import create_engine
# engine = create_engine('postgresql://root:root@localhost:4444/ny_taxi')
# engine.connect()

# df_iter = pd.read_csv('yellow_tripdata_2022-01.csv', iterator=True, chunksize=100000)
# df = next(df_iter)
# df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
# df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

# while True:
#     s = time()
#     df = next(df_iter)
#     df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
#     df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
#     df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
#     e = time()
#     print('inserted in %.3f' %(e - s))
# https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2022-01.parquet