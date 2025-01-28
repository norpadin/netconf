import logging
from ncclient import manager
from rich import print
import xml.dom.minidom

# Suppress ncclient debug logs
logging.getLogger("ncclient").setLevel(logging.WARNING)


def iosxe_connect(host, port, user, password):
    """Establish a NETCONF connection to the Cisco IOS-XE device."""
    return manager.connect(
        host=host,
        port=port,
        username=user,
        password=password,
        device_params={'name': "iosxe"},
        timeout=60,
        hostkey_verify=False,
        look_for_keys=False
    )


def get_filtered_config(session):
    """Retrieve a filtered running-config from the device."""
    filter = """
    <filter>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface/>
        </native>
    </filter>
    """
    return session.get_config("running", filter)


if __name__ == "__main__":
    # Configure application-level logging
    logging.basicConfig(level=logging.INFO)

    nconf = None
    try:
        logging.info("Connecting to the NETCONF server...")
        nconf = iosxe_connect("10.1.100.1", 830, "netconf", "netconf")
        print("[green]Connected successfully![/green]")

        print("[cyan]Server Capabilities:[/cyan]")
        print(list(nconf.server_capabilities))

        # Get filtered configuration
        print("[cyan]Filtered running-config:[/cyan]")
        netconf_reply = get_filtered_config(nconf)
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

    except Exception as e:
        logging.error(f"Error: {e}")

    finally:
        # Ensure session is closed
        if nconf:
            logging.info("Closing the NETCONF session...")
            nconf.close_session()
            print("[green]Session closed.[/green]")
