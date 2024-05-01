#import libraries
import requests
import random

def get_request_params():
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/73.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/73.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:75.0) Gecko/20100101 Firefox/75.0",
    ]    
    params = {
        "headers": {"User-Agent": random.choice(user_agents)},
    }
    return params

def fetch_html_requests(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            session    = requests.Session()
            req_params = get_request_params()
            response   = session.get(url, **req_params)
            response.raise_for_status()
            return response
    except (requests.HTTPError, requests.ConnectionError):
        return None