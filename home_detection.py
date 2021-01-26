import ipfshttpclient
import nmap3

nmap = nmap3.NmapScanTechniques()


def is_connected(ip):
	results = nmap.nmap_ping_scan(ip)
	return results != [] and results is not None


status = is_connected('192.168.1.220')
with ipfshttpclient.connect() as client:
	client.pubsub.publish('tony_mobile', status)
