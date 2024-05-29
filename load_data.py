import pandas as pd
import redis

from redis_functions import convert_dict


def load_tag(tag_dict: dict, df: pd.DataFrame) -> pd.DataFrame:
    tag_dict = convert_dict(tag_dict)
    tag_series = pd.Series(tag_dict)

    return pd.concat([df, tag_series.to_frame().T], ignore_index=True)


def convert_to_probability(df: pd.DataFrame) -> pd.DataFrame:
    for i, row in df.iterrows():
        max = row.max()
        for j, value in row.items():
            if value == 0:
                continue
            df.at[i, j] = value / max

    return df


r = redis.StrictRedis(
    host="localhost", port=6379, charset="utf-8", decode_responses=True
)

all_keywords = []

for tag in r.keys():
    keywords = r.hgetall(tag)
    for keyword in keywords:
        all_keywords.append(keyword)

df = pd.DataFrame([], columns=all_keywords)
df = df.loc[:, ~df.columns.duplicated()].copy()

for tag in r.keys():
    tag_dict = r.hgetall(tag)
    df = load_tag(tag_dict, df)

df = df.fillna(0)
df["Keyword"] = r.keys()
df = df.set_index("Keyword")
df = df.T

df.to_csv("data_unconverted.csv")

df = convert_to_probability(df)
df.to_csv("data.csv")
