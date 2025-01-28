import requests
import urllib3
import sys

# disable warnings from SSL/TLS certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# use the IP address or hostname of your Cat9300
HOST = '172.26.198.63'

# use your user credentials to access the Cat9300
USER = 'cisco'
PASS = 'cisco'


# create a main() method
def main():
    """Main method that configures the Ip address for a interface via RESTCONF."""

    # url string to issue GET request
    url = "https://172.26.198.63/restconf/data/Cisco-IOS-XE-native:native/interface/TenGigabitEthernet=1%2F0%2F10/ip/address/primary"

    # RESTCONF media types for REST API headers
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}
    # this statement performs a GET on the specified url
    response = requests.request("DELETE", url, auth=(USER, PASS),
                                headers=headers, verify=False)
    # print the json that is returned
    print(response.text)


if __name__ == '__main__':
    sys.exit(main())
