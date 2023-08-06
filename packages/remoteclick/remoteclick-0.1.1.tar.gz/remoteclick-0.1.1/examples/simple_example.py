import random

import time

from remoteclick import RemoteClickClient, DataNode
from remoteclick.value_type import ValueType

import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    client = RemoteClickClient()
    client.set_credentials("95856bd5-8b66-11e7-a9bc-38eaa7353b44", "0f980bd37b56bfc2e5ecd60d6e25e728")
    client.connect()

    for i in range(1, 4):
        temperature_node = client.save_data_node(
            DataNode(name="Temperatur", value_type=ValueType.NUMBER, unit="°C", keep_history=True,
                     path="Zone"+str(i), read_only=True)
        )

        for index in range(1, 20):
            # create new value for data node
            value = temperature_node.new_value(random.randint(20, 30))
            # save the value
            client.save_data_node_value(value)
            time.sleep(1)

        # fetch 10 newest values of data node
        temperature_values = client.get_data_node_values(temperature_node, limit=10)
        for temperature_value in temperature_values:
            print(temperature_value)

        # save new data node which stores current status, does not store historic values and is read-only
        status_node = client.save_data_node(
            DataNode(name="Status", value_type=ValueType.STRING, unit="", keep_history=False, path="Zone"+str(i),
                     read_only=True))
        # store first value
        status_value = client.save_data_node_value(status_node.new_value(value="Ok"))

        # change the value and update it
        status_value.value = "Alarm"
        client.update_data_node_value(status_value)
