import ipfshttpclient


def start(ipfs_addr, topic, callback):
    # client = ipfshttpclient.connect(ipfs_addr)
    with ipfshttpclient.connect() as client:
        print('hello ipfs')
        # subscribe to topic
        while True:
            print('creating subscription to ' + topic)
            with client.pubsub.subscribe(topic) as sub:
                print(sub)


start('', 'tony_mobile', None)
