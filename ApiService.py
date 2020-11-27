import requests


def get(url, headers):
    print(url)
    print(headers)
    try:
        return requests.get(url, headers=headers, verify=False)
    except Exception as e:
        print('an error occurred: {}'.format(e))


def put(url, headers, body):
    try:
        # TODO verify=False is very insecure..
        return requests.put(url, json=body, headers=headers, verify=False)
    except Exception as e:
        print('Something happened...{}'.format(e))