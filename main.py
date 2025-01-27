import logging
from ncclient import manager
from rich import print
from lxml import etree

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    device = {
        "host": "10.1.100.1",
        "port": 830,
        "username": "admin",
        "password": "BvsTv3965!",
        "hostkey_verify": False,
    }

    # try:
    #     with manager.connect(**device) as nconf:
    #         print("[green]Connected successfully![/green]")
    #         print("[cyan]Server Capabilities:[/cyan]")
    #         print(list(nconf.server_capabilities))
    # except Exception as e:
    #     print(f"[red]Error: {e}[/red]")

    # try:
    #     with manager.connect(**device) as nconf:
    #         print("[green]Connected successfully![/green]")
    #         print("[cyan]Server Capabilities:[/cyan]")
    #         nc_reply = nconf.get_config(source="running")
    #         xml_data = etree.tostring(
    #             nc_reply.data_ele,
    #             pretty_print=True,
    #         ).decode()
    #         print(xml_data)
    # except Exception as e:
    #     print(f"[red]Error: {e}[/red]")

    try:
        nconf = manager.connect(**device, timeout=60)
        if nconf:
            print("[green]Connected successfully![/green]")
            print("[cyan]Server Capabilities:[/cyan]")
            nc_reply = nconf.get_config(source="running")
            xml_data = etree.tostring(
                nc_reply.data_ele, pretty_print=True).decode()
            with open("running.xml", "wt") as f:
                f.write(xml_data)
        else:
            print("[red]Failed to connect to the device.[/red]")
    except Exception as e:
        print(f"[red]Error: {e}[/red]")
