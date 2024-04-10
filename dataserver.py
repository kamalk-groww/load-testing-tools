from fastapi import FastAPI
import pandas as pd
import json

app = FastAPI()

filename = "sample2.csv" # update as per your requirements
chunksize = 3 # update as per your requirements


def get_data_using_generators():
    while True:
        for chunk in pd.read_csv(filename, chunksize=chunksize, skiprows=1):
            data = []
            for _, row in chunk.iterrows():
                data.append(json.loads(row.iloc[1]))

            yield data

gen = get_data_using_generators()
@app.get("/get_chunk")
async def get_chunk():
    return next(gen)