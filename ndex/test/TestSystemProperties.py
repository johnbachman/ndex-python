import unittest

import ndex.client as nc
import time


ndex_host = "http://dev.ndexbio.org"
ndex_network_resource = "/v2/network/"
username_1 = "ttt"
password_1 = "ttt"

example_network_1 = './A549-SL-network.cx'

# Python Client APIs tested:
#
#   set_network_system_properties
#


class MyTestCase(unittest.TestCase):

    def test_network_system_properties(self):
        ndex = nc.Ndex(host=ndex_host, username=username_1, password=password_1)

        with open(example_network_1, 'r') as file_handler:
            network_in_cx = file_handler.read()

        # test save_cx_stream_as_new_network
        test_network_1_uri = ndex.save_cx_stream_as_new_network(network_in_cx)
        self.assertTrue(test_network_1_uri.startswith(ndex_host + ndex_network_resource))

        network_UUID = str(test_network_1_uri.split("/")[-1])

        # get network summary
        network_summary = ndex.get_network_summary(network_UUID)
        network_visibility = str(network_summary['visibility'])
        network_read_only  =  network_summary['isReadOnly']
        self.assertTrue(network_visibility.upper() == 'PRIVATE')
        self.assertTrue(network_read_only == False)


        # test set_network_system_properties
        time.sleep(10)


        # make network ReadOnly and PUBLIC
        ndex.set_network_system_properties(network_UUID, {'readOnly': True})
        ndex.set_network_system_properties(network_UUID, {'visibility': 'PUBLIC'})

        # check if we succeeded in making the netwrk ReadOnly and PUBLIC
        network_summary = ndex.get_network_summary(network_UUID)
        self.assertTrue(str(network_summary['visibility']).upper() == 'PUBLIC')
        self.assertTrue(network_summary['isReadOnly'] == True)

        # make network Read-Write and PRIVATE
        ndex.set_network_system_properties(network_UUID, {'readOnly': False})
        ndex.set_network_system_properties(network_UUID, {'visibility': 'PRIVATE'})
        network_summary = ndex.get_network_summary(network_UUID)
        self.assertTrue(str(network_summary['visibility']).upper() == 'PRIVATE')
        self.assertTrue(network_summary['isReadOnly'] == False)



        # make network ReadOnly and PUBLIC in one call
        ndex.set_network_system_properties(network_UUID, {'readOnly': True, 'visibility': 'PUBLIC'})
        network_summary = ndex.get_network_summary(network_UUID)
        self.assertTrue(str(network_summary['visibility']).upper() == 'PUBLIC')
        self.assertTrue(network_summary['isReadOnly'] == True)

        # make network ReadWrite and PRIVATE in one call
        ndex.set_network_system_properties(network_UUID, {'readOnly': False, 'visibility': 'PRIVATE'})
        network_summary = ndex.get_network_summary(network_UUID)
        self.assertTrue(str(network_summary['visibility']).upper() == 'PRIVATE')
        self.assertTrue(network_summary['isReadOnly'] == False)

        # make network ReadOnly and PRIVATE in one call
        ndex.set_network_system_properties(network_UUID, {'readOnly': True, 'visibility': 'PRIVATE'})
        network_summary = ndex.get_network_summary(network_UUID)
        self.assertTrue(str(network_summary['visibility']).upper() == 'PRIVATE')
        self.assertTrue(network_summary['isReadOnly'] == True)

        # make network ReadWrite and PUBLIC in one call
        ndex.set_network_system_properties(network_UUID, {'readOnly': False, 'visibility': 'PUBLIC'})
        network_summary = ndex.get_network_summary(network_UUID)
        self.assertTrue(str(network_summary['visibility']).upper() == 'PUBLIC')
        self.assertTrue(network_summary['isReadOnly'] == False)



        # test delete_network
        del_network_return = ndex.delete_network(network_UUID)
        self.assertTrue(del_network_return == '')

if __name__ == '__main__':
    unittest.main()

