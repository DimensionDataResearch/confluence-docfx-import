#!/usr/bin/python

"""
Extract topic mappings from Confluence.
"""

import argparse
import os
import requests
import yaml

OFFSET_STEP = 50


def main():
    """
    The main program entry-point.
    """

    parser = argparse.ArgumentParser(__file__, __doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--confluence-address",
        default=os.getenv("CONFLUENCE_ADDR"),
        help="The base address of the Confluence server."
    )
    parser.add_argument("--confluence-user",
        default=os.getenv("CONFLUENCE_USER"),
        help="The user name for authentication to Confluence."
    )
    parser.add_argument("--confluence-password",
        default=os.getenv("CONFLUENCE_PASSWORD"),
        help="The password for authentication to Confluence."
    )
    parser.add_argument("--confluence-space",
        required=True,
        help="The key (short name) of the target space in Confluence."
    )
    args = parser.parse_args()

    if not args.confluence_address:
        parser.exit(status=1, message="Must specify address of Confluence server using --confluence-address argument or CONFLUENCE_ADDR environment variable.")

    if not args.confluence_user:
        parser.exit(status=1, message="Must specify user name for authentication to Confluence server using --confluence-user argument or CONFLUENCE_USER environment variable.")

    if not args.confluence_password:
        parser.exit(status=1, message="Must specify password for authentication to Confluence server using --confluence-password argument or CONFLUENCE_PASSWORD environment variable.")


    print("# Page mappings from {}".format(args.confluence_address))
    page_mappings = load_page_mappings(args.confluence_address, args.confluence_user, args.confluence_password)
    print(
        yaml.dump(page_mappings, default_flow_style=False)
    )

    parser.exit(status=0)

def load_page_mappings(confluence_address, confluence_user, confluence_password):
    """
    Load page-mappings from Confluence.

    :param confluence_address: The base address for the Confluence server.
    :param confluence_user: The user name for authentication to Confluence.
    :param confluence_password: The password for authentication to Confluence.
    :returns: A list of Confluence page mappings: {confluence_id, docfx_uid, docfx_href}.
    :rtype: list
    """

    page_mappings = []

    uri_template = confluence_address
    if not uri_template.endswith('/'):
        uri_template += '/'
    uri_template += 'rest/api/content?type=page&expand=metadata.properties.docfx&start={start}&limit={limit}'

    confluence_credentials = (confluence_user, confluence_password)

    offset = 0
    while True:
        uri = uri_template.format(
            start=offset,
            limit=OFFSET_STEP
        )
        result = requests.get(uri, auth=confluence_credentials).json()
        if result["size"] == 0:
            break # No more records.

        for result in result["results"]:
            properties = result["metadata"]["properties"]
            if "docfx" not in properties:
                continue # Page does not have DocFX properties.

            docfx_properties = properties["docfx"]["value"]["content"]

            page_mappings.append({
                "confluence_id": result["id"],
                "docfx_uid": docfx_properties["docfx_uid"],
                "docfx_href": docfx_properties["docfx_href"]
            })

        offset += OFFSET_STEP

    return page_mappings

if __name__ == "__main__":
    main()
