import requests


def put(url, headers, body):
    try:
        return requests.put(url, json=body, headers=headers)
    except Exception as e:
        print('Something happened...{}'.format(e))