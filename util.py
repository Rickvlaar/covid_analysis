from config import Endpoints
import concurrent.futures
import callouts


def refresh_data_files():
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for key, value in Endpoints.__dict__.items():
            if not key.startswith('_'):
                executor.submit(write_response_to_file, key, value)


def write_response_to_file(filename, endpoint):
    new_file = open(file='data_files/' + filename + '.json', mode='wb')
    data = callouts.get_covid_stats(endpoint)
    new_file.write(data)
    new_file.close()
