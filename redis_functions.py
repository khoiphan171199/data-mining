from collections import Counter

import redis


def create_dict(my_list) -> dict:
    return {i: 1 for i in my_list}


def convert_dict(my_dict) -> dict:
    return dict([i, int(j)] for i, j in my_dict.items())


def save_tag(r: redis.Redis, tag: str, keywords) -> None:
    try:
        existing = r.hgetall(tag)
        if existing:
            updated = Counter(convert_dict(existing)) + Counter(create_dict(keywords))
            r.hmset(tag, updated)

        else:
            r.hmset(tag, create_dict(keywords))

    except Exception as e:
        print("error saving tag data to redis database: ")
        print(e)

    return None
