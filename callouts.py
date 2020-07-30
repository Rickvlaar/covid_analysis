import requests


# Gets data from supplied endpoint and returns the json
def get_covid_stats(url):
    try:
        stats_response = requests.get(url)
        if stats_response.status_code == 200:
            return stats_response.json()
    except:
        return None
