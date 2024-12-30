import os
import time

import ximu3

# Open connection
connection = ximu3.Connection(ximu3.NetworkAnnouncement().get_messages_after_short_delay()[0].to_udp_connection_info())

if connection.open() != ximu3.RESULT_OK:
    raise Exception("Unable to open connection")

connection.send_commands(['{"ahrs_message_type":0}'], 2, 500)
connection.send_commands(['{"apply":null}'], 2, 500)
connection.send_commands(['{"serial_mode":2}'], 2, 500)

# Log data
destination = os.path.dirname(os.path.abspath(__file__))
name = "Logged Data"

data_logger = ximu3.DataLogger(destination, name, [connection])

if data_logger.get_result() != ximu3.RESULT_OK:
    raise Exception("Data logger failed")

time.sleep(1)

connection.send_commands(['{"initialise":null}'], 2, 500)

for value in [0, 1, 2, 3, 3, 4]:
    connection.send_commands([f'{{"ahrs_message_type":{value}}}'], 2, 500)
    connection.send_commands(['{"apply":null}'], 2, 500)
    connection.send_commands([f'{{"note":"Example notification {value}"}}'], 2, 500)
    time.sleep(1)

del data_logger

time.sleep(2)
