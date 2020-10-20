import json
import pandas
import requests

def get_data(url):

    initial_request = requests.request("GET", url)
    request_json = initial_request.json()   
    runs_json = request_json["data"]["runs"]

    return runs_json

def transform_data(runs_json):

    #clean up headers; renaming optimization
    df = pandas.json_normalize(runs_json)

    df["video"] = df["run.videos.links"]
    df["video"] = df.video.apply(pandas.Series)
    df["video"] = df.video.apply(pandas.Series)

    df["times"] = df["run.times.primary_t"]
    

    FIELDS = ["run.weblink", "video", "run.date", "times"]
    print(df[FIELDS].head(5))

def generate_url(game, category, run_count):

    return f"https://www.speedrun.com/api/v1/leaderboards/{game}/category/{category}?top={run_count}"


def main():

    print()
    print("RUN START")
    print()

    # get data
    url = generate_url("smw", "96_Exit", "5")

    runs_json = get_data(url)

    # transform data
    transform_data(runs_json)

    # get data
    url = url = generate_url("oot", "100", "5")

    runs_json = get_data(url)

    #transform data
    transform_data(runs_json)

    print()
    print("RUN END")


if __name__ == "__main__":
    main()

