import json
import numpy
import pandas
import requests
import datetime

run_num = 5

def get_data(url):

    initial_request = requests.request("GET", url)
    request_json = initial_request.json()   
    runs_json = request_json["data"]["runs"]

    return runs_json

def transform_data(runs_json):

    df = setup_data(runs_json)

    FIELDS = ["weblink", "video", "date", "times", "world_record"]
    record = None

    for index, row in df.iterrows():

        if record is None:
            record = row.at["times"]
            df.loc[index, 'world_record'] = True
        
        elif row.at["times"] < record:
            record = row.at["times"]
            df.loc[index, 'world_record'] = True
        else:
            df.loc[index, 'world_record'] = False

    for index, row in df.iterrows():
        df.loc[index, 'times'] = float(df.loc[index, 'times'])
        df.loc[index, 'times'] = str(datetime.timedelta(seconds = df.loc[index, 'times']))

    visible_run_num = 30

    filtered_df = df.loc[df['world_record'] == True]  

    print(filtered_df[FIELDS].head(visible_run_num))

def setup_data(runs_json):

    df = pandas.json_normalize(runs_json)
    
    df["video"] = df["run.videos.links"]
    del df["run.videos.links"]
    df["times"] = df["run.times.primary_t"]
    del df["run.times.primary_t"]
    df["weblink"] = df["run.weblink"]
    del df["run.weblink"]
    df["date"] = df["run.date"]
    del df["run.date"]

    df["video"] = df.video.apply(pandas.Series)
    df["video"] = df.video.apply(pandas.Series)

    df["world_record"] = numpy.nan

    df = df.sort_values("date")

    return df


def generate_url(game, category, run_count):

    return f"https://www.speedrun.com/api/v1/leaderboards/{game}/category/{category}?top={run_count}"


def main():

    print()
    print("RUN START")
    print()
    
    run_num = 300

    # get data
    url = generate_url("smw", "96_Exit", run_num)

    runs_json = get_data(url)

    # transform data
    transform_data(runs_json)

    # get data
    url = generate_url("oot", "100", run_num)

    runs_json = get_data(url)

    #transform data
    transform_data(runs_json)

    print()
    print("RUN END")


if __name__ == "__main__":
    main()

