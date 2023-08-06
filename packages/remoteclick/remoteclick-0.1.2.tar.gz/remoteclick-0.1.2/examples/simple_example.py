import random

import time

from remoteclick import RemoteClickClient, DataNode
from remoteclick.value_type import ValueType

import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    client = RemoteClickClient()
    client.set_base_url('http://api.iotcloud.dev/api/')
    client.set_credentials("57b5e28d-8e8c-11e7-8cbc-000c295a122d", "fc333a2184a66d719b6deae26f3b184c")
    client.connect()

    for i in range(1, 12):
        temperature_node = client.save_data_node(
            DataNode(name="Temperatur", value_type=ValueType.NUMBER, unit="°C", keep_history=True,
                     path=str(i)+".OG/Klimaanlage", read_only=True)
        )

        # for index in range(1, 20):
        #     # create new value for data node
        #     value = temperature_node.new_value(random.randint(20, 30))
        #     # save the value
        #     client.save_data_node_value(value)
        #     time.sleep(1)
        #
        # # fetch 10 newest values of data node
        # temperature_values = client.get_data_node_values(temperature_node, limit=10)
        # for temperature_value in temperature_values:
        #     print(temperature_value)
        #
        # # save new data node which stores current status, does not store historic values and is read-only
        # status_node = client.save_data_node(
        #     DataNode(name="Betrieb", value_type=ValueType.BOOLEAN, unit="", keep_history=True, path=str(i)+".OG/Klimaanlage",
        #              read_only=False))
        # # store first value
        # status_value = client.save_data_node_value(status_node.new_value(value=True))

        # change the value and update it
        # status_value.value = "Alarm"
        # client.update_data_node_value(status_value)
