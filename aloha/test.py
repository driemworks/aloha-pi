import base64
import os
from subscription_manager import subscribe


PHONE_STATUS_TOPIC = 'PHONE_STATUS'
VIZIO_STATUS_TOPIC = 'VIZIO_STATUS'


def bluetooth_connect(sub):
	decoded_message = base64.b64decode(sub['data']
		.encode('ascii')).decode('utf-8')
	if decoded_message == '1':
		print('Attempting bluetooth connection')
		os.system('~/scripts/autopair')
		print('Bluetooth connection established')
	else:
		print('You are not at home .')


subscribe('', PHONE_STATUS_TOPIC, bluetooth_connect)
