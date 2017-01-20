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
#   save_cx_stream_as_new_network
#   get_provenance
#   set_provenance
#   update_network_profile
#   get_network_summary
#   delete_network
#


class MyTestCase(unittest.TestCase):
    def test_provenance_and_profile(self):
        ndex = nc.Ndex(host=ndex_host, username=username_1, password=password_1)

        with open(example_network_1, 'r') as file_handler:
            network_in_cx = file_handler.read()


        # test save_cx_stream_as_new_network
        test_network_1_uri = ndex.save_cx_stream_as_new_network(network_in_cx)
        self.assertTrue(test_network_1_uri.startswith(ndex_host + ndex_network_resource))


        # test get_provenance
        network_UUID = str(test_network_1_uri.split("/")[-1])
        provenance = ndex.get_provenance(network_UUID)
        self.assertTrue(provenance)
        provenance_keys = provenance.keys()
        # check that fields creationEvent, properties and uri are fields in the provenance structure
        self.assertTrue('creationEvent' in provenance_keys)
        self.assertTrue('properties' in provenance_keys)
        self.assertTrue('uri' in provenance_keys)
        uri1 = str(provenance['uri']);
        uri2 = ndex_host + ndex_network_resource + network_UUID + "/summary"
        self.assertTrue(uri1 == uri2)


        # test update_network_profile
        new_version = "1.55"
        new_name = "New network name"
        new_description = "New network description"
        test_profile = {"version": new_version,
                        "name": new_name,
                        "description": new_description
                        }
        time.sleep(10)
        ndex.update_network_profile(network_UUID, test_profile)

        # test get_network_summary
        network_summary = ndex.get_network_summary(network_UUID)
        self.assertTrue(new_version == network_summary['version'])
        self.assertTrue(new_name == network_summary['name'])
        self.assertTrue(new_description == network_summary['description'])


        provenance_1 = ndex.get_provenance(network_UUID)

        # test set_provenance - change description of event
        provenance_1['creationEvent']['eventType'] = 'Modified Program Upload in CX'
        ndex.set_provenance(network_UUID, provenance_1)
        provenance_2 = ndex.get_provenance(network_UUID)
        self.assertTrue(provenance_2['creationEvent']['eventType'] == provenance_1['creationEvent']['eventType'])

        # set provenance back to the original one
        ndex.set_provenance(network_UUID, provenance)
        provenance_3 = ndex.get_provenance(network_UUID)
        self.assertTrue(provenance['creationEvent']['eventType'] == provenance_3['creationEvent']['eventType'])

        # test delete_network
        del_network_return = ndex.delete_network(network_UUID)
        self.assertTrue(del_network_return == '')

if __name__ == '__main__':
    unittest.main()

