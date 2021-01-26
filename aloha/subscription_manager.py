import ipfshttpclient


def subscribe(ipfs_addr, topic, callback):
    with ipfshttpclient.connect() as client:
        while True:
            with client.pubsub.subscribe(topic) as sub:
                callback(sub.read_message())
