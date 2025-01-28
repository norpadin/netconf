import requests
import urllib3
from rich import print
import json

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def restconf_connect(host, port, user, password):
    """Base configuration for RESTCONF requests."""
    return {
        "base_url": f"https://{host}:{port}/restconf/data",
        "headers": {
            "Accept": "application/yang-data+json",
            "Content-Type": "application/yang-data+json"
        },
        "auth": (user, password),
        "verify": False  # Disable SSL certificate verification
    }


def get_filtered_config(connection, filter_path):
    """Retrieve filtered configuration using RESTCONF."""
    url = f"{connection['base_url']}{filter_path}"
    response = requests.get(
        url, headers=connection["headers"],
        auth=connection["auth"],
        verify=connection["verify"])

    # Check for errors
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


if __name__ == "__main__":
    host = "10.1.100.1"
    port = 443
    user = "restconf"
    password = "restconf"

    try:
        print("[cyan]Connecting to the device using RESTCONF...[/cyan]")
        connection = restconf_connect(host, port, user, password)

        # Define the YANG model path for filtering
        filter_path = "/Cisco-IOS-XE-native:native/interface"

        print("[green]Retrieving filtered configuration...[/green]")
        config = get_filtered_config(connection, filter_path)

        # Pretty-print the JSON result
        print("[cyan]Filtered Configuration:[/cyan]")
        print(json.dumps(config, indent=4))

    except requests.exceptions.HTTPError as http_err:
        print(f"[red]HTTP error occurred: {http_err}[/red]")
    except Exception as err:
        print(f"[red]An error occurred: {err}[/red]")
