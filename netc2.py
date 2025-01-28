import sys
from argparse import ArgumentParser
from ncclient import manager
from rich import print
import xml.dom.minidom

if __name__ == '__main__':
    host = "10.1.100.1"
    port = 830
    user = "restconf"
    password = "restconf"

    m = manager.connect(
        host=host,
        port=port,
        username=user,
        password=password,
        hostkey_verify=False,
        device_params={'name': "iosxe"},
        timeout=60,
        look_for_keys=False)

    hostname_filter = '''
                      <filter>
                          <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                          </native>
                      </filter>
                      '''

    # Pretty print the XML reply
    xmlDom = xml.dom.minidom.parseString(
        str(m.get_config('running', hostname_filter)))
    print(xmlDom.toprettyxml(indent="  "))
