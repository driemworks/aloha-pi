import ipfshttpclient

TOPIC = 'a'

def start(ipfs_addr, topic, callback):
    with ipfshttpclient.connect() as client:
        while True:
            with client.pubsub.subscribe(topic) as sub:
                callback(sub)

def test(sub):
    print(sub)


start('', TOPIC,  test)
