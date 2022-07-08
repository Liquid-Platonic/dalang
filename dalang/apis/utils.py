import requests

from dalang.config.config import ACCESS_TOKEN, API_URL


def query_and_get_results(endpoint, query, headers):
    r = requests.post(endpoint, json={"query": query}, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"Query failed to run with a {r.status_code}.")


def get_genres(endpoint, headers):
    query = """
    query {
        __type(name: "AudioAnalysisV6GenreTags"){
            name
            enumValues {
                name
            }
        }
    }
    """
    results = query_and_get_results(endpoint, query, headers)
    return _get_values_from_enum_query(results)


def get_moods(endpoint, headers):
    query = """
    query {
        __type(name: "AudioAnalysisV6MoodTags"){
            name
            enumValues {
                name
            }
        }
    }
    """
    results = query_and_get_results(endpoint, query, headers)
    return _get_values_from_enum_query(results)


def _get_values_from_enum_query(query_results):
    values = query_results["data"]["__type"]["enumValues"]
    return [value["name"] for value in values]


def get_moods_advanced(endpoint, headers):
    query = """
    query {
        __type(name: "AudioAnalysisV6MoodAdvancedTags"){
            name
            enumValues {
                name
            }
        }
    }
    """
    values = query_and_get_results(endpoint, query, headers)
    return _get_values_from_enum_query(values)


if __name__ == "__main__":
    endpoint = API_URL
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    print(get_genres(endpoint, headers))
    print(get_moods(endpoint, headers))
    print(get_moods_advanced(endpoint, headers))
