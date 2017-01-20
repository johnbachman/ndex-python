from __future__ import absolute_import

import unittest
from os import path
import ndex.client as nc
import uuid
import time
import json


TESTSERVER= "http://dev.ndexbio.org"
HERE = path.abspath(path.dirname(__file__))

class NdexClientTestCase1(unittest.TestCase):

    def testConstructorException(self):
        with self.assertRaises(Exception):
            print "testing ndex client constructor."
            ndex = nc.Ndex(host="www.google.com", username="foo", password="bar")


class NdexClientTestCase2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._ndex = nc.Ndex(host=TESTSERVER, username="pytest", password="pyunittest")
        with open(path.join(HERE, 'tiny_network.cx'),'r') as cx_file:
            cls._nrc = cls._ndex.save_cx_stream_as_new_network(cx_file)
            networkId = uuid.UUID('{'+cls._nrc[-36:] + '}')
            cls._networkId = str(networkId)

    @classmethod
    def tearDownClass(cls):
        cls._ndex.delete_network(cls._networkId)
        print "Network " + cls._networkId + " deleted from " + cls._ndex.username +" account " + cls._ndex.host

    #def setup(self):
    #    self.ndex = nc.Ndex(host="http://public.ndexbio.org", username="drh", passwor="drh")


    def testGetNetwork(self):
        summary = self._ndex.get_network_summary(self._networkId)
        self.assertEqual(summary.get(u'externalId'), self._networkId)
        print "get_network_summary() passed."

    def testGrantGroupPermission(self):
        ndex2 = nc.Ndex(TESTSERVER, username='pytest2' , password = 'pyunittest')
        with self.assertRaises(Exception) as context:
            ndex2.get_network_summary(self._networkId)
#        print context.exception
        count = 0
        while count < 30 :
            try :
                self._ndex.update_network_group_permission('d7ef9957-de81-11e6-8835-06832d634f41', self._networkId, 'READ')
                count = 60
            except Exception as inst :
                d = json.loads(inst.response.content)
                if d.get('message').startswith("Can't modify locked network.") :
                    print "retry in 5 seconds(" + str(count) + ")"
                    count += 1
                    time.sleep(5)
                else :
                    raise inst

        summary = ndex2.get_network_summary(self._networkId)
        self.assertEqual(summary.get(u'externalId'), self._networkId)
        print "update_network_group_permission() passed."



class NdexClientTestCase3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._ndex = nc.Ndex(host=TESTSERVER, username="pytest", password="pyunittest")
        with open(path.join(HERE, 'tiny_network.cx'),'r') as cx_file:
            cls._nrc = cls._ndex.save_cx_stream_as_new_network(cx_file)
            networkId = uuid.UUID('{'+cls._nrc[-36:] + '}')
            cls._networkId = str(networkId)

    @classmethod
    def tearDownClass(cls):
        cls._ndex.delete_network(cls._networkId)
        print "Network " + cls._networkId + " deleted from " + cls._ndex.username +" account " + cls._ndex.host

    #def setup(self):
    #    self.ndex = nc.Ndex(host="http://public.ndexbio.org", username="drh", passwor="drh")

    def testGrantUserPermission(self):
        ndex2 = nc.Ndex(TESTSERVER, username='pytest2' , password = 'pyunittest')
        with self.assertRaises(Exception) as context:
            ndex2.get_network_summary(self._networkId)
#        print context.exception
        count = 0
        while count < 30 :
            try :
                self._ndex.update_network_user_permission('0a9d3b58-de82-11e6-8835-06832d634f41', self._networkId, 'READ')
                count = 60
            except Exception as inst :
                d = json.loads(inst.response.content)
                if d.get('message').startswith("Can't modify locked network.") :
                    print "retry in 5 seconds(" + str(count) + ")"
                    count += 1
                    time.sleep(5)
                else :
                    raise inst

        summary = ndex2.get_network_summary(self._networkId)
        self.assertEqual(summary.get(u'externalId'), self._networkId)
        print "update_network_user_permission() passed."


class NdexClientTestCase3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._ndex = nc.Ndex(host=TESTSERVER, username="pytest", password="pyunittest")
        with open(path.join(HERE, 'tiny_network.cx'),'r') as cx_file:
            cls._nrc = cls._ndex.save_cx_stream_as_new_network(cx_file)
            networkId = uuid.UUID('{'+cls._nrc[-36:] + '}')
            cls._networkId = str(networkId)

    @classmethod
    def tearDownClass(cls):
        cls._ndex.delete_network(cls._networkId)
        print "Network " + cls._networkId + " deleted from " + cls._ndex.username +" account " + cls._ndex.host

    #def setup(self):
    #    self.ndex = nc.Ndex(host="http://public.ndexbio.org", username="drh", passwor="drh")

    def testUpdateNetwork(self):
        time.sleep(5)
        summary1 = self._ndex.get_network_summary(self._networkId)
        self.assertEqual(summary1['name'], 'rudi')
        time.sleep(5)
        count = 0
        while count < 30 :
            try :
                with open(path.join(HERE, 'A549-SL-network.cx'), 'r') as cx_file:
                    self._ndex.update_cx_network(cx_file, self._networkId)
                break
            except Exception as inst :
                if inst.response and inst.response.get('content') :
                    d = json.loads(inst.response.content)
                    if d and d.get('message') and d.get('message').startswith("Can't modify locked network.") :
                        print "retry in 5 seconds(" + str(count) + ")"
                        count += 1
                        time.sleep(5)
                    else:
                        raise inst
                else :
                    raise inst

      #  time.sleep(1)

        count = 0
        while count < 30:
            try:
                summary1 = self._ndex.get_network_summary(self._networkId)
                if ( summary1.get('isValid') ):
                    break
                else:
                     count+=1
            except Exception as inst:
                if (not inst.response) or (not inst.response.get('content')):
                    raise inst
                d = json.loads(inst.response.content)
                if d and d.get('message') and d.get('message').startswith("Can't modify locked network."):
                    print "retry in 5 seconds(" + str(count) + ")"
                    count += 1
                    time.sleep(5)
                else:
                    raise inst

        self.assertEqual(summary1.get(u'name'), "A549-SL-network")
        print "update_cx_network() passed."
