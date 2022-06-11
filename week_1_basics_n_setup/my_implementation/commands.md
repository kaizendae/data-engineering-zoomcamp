`docker run -it -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi" -p 4444:5432 -v my_taxi_data:/var/lib/postgresql/data postgres:13`

`python3 ingest_data.py --user=root --password=root --host=localhost --port=4444 --database=ny_taxi --table=yellow_taxi_data --url=https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2022-01.parquet `

`docker run --network host taxi_ingest:001  --user=root --password=root --host=localhost --port=4444 --database=ny_taxi --table=yellow_taxi_data --url=https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2022-01.parquet`

# install google cloud sdk 
1. `brew tap homebrew/cask`
2. `brew --cask install google-cloud-sdk`
3. `gcloud version`
4. `gcloud auth login`