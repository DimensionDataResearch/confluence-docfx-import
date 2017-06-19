#!/usr/bin/python

"""
Script for publishing content from a generated DocFX web site to Confluence.
"""

import argparse
import json
import os
import requests
import yaml

from os import path
from urllib.parse import urljoin

def main():
    """
    The main program entry-point.
    """

    args = parse_args()

    manifest = load_docfx_manifest(args.docfx_manifest)
    base_directory = path.dirname(args.docfx_manifest)
    docfx_mappings = load_docfx_xref_map(
        filename=path.join(base_directory, manifest["xrefmap"])
    )

    confluence_client = ConfluenceClient(args.confluence_address, args.confluence_user, args.confluence_password)
    confluence_mappings = get_confluence_mappings(confluence_client)

    docfx_uid_to_confluence_id = {
        (entry["docfx_uid"], entry["confluence_id"]) for entry in confluence_mappings
    }

    new_mappings = [
        docfx_mapping for docfx_mapping in docfx_mappings
        if docfx_mapping["uid"] not in docfx_uid_to_confluence_id
    ]
    if new_mappings:
        print("Need to create {} new pages in confluence:".format(
            len(new_mappings)
        ))

        for mapping in new_mappings:
            print("\t{href} (UID='{uid}')".format(**mapping))

def get_confluence_mappings(confluence_client):
    """
    Retrieve existing page mappings from Confluence.abs

    :param confluence_client: The Confluence REST API client.
    :returns: A list of mappings (confluence_id, docfx_uid, docfx_href).
    :type confluence_client: ConfluenceClient
    :rtype: list
    """

    mappings = []

    step = 50
    uri_template="content?type=page&expand=metadata.properties.docfx&start={start}&limit={limit}"

    offset = 0
    while True:
        results = confluence_client.get_json(
            uri_template.format(start=offset, limit=step)
        )
        if results["size"] == 0:
            break # No more records.

        for result in results["results"]:
            properties = result["metadata"]["properties"]
            if "docfx" not in properties:
                continue # Page does not have DocFX properties.

            docfx_properties = properties["docfx"]["value"]["content"]

            mappings.append({
                "confluence_id": result["id"],
                "docfx_uid": docfx_properties["docfx_uid"],
                "docfx_href": docfx_properties["docfx_href"]
            })

        offset += step

    return mappings

def load_docfx_manifest(filename):
    """
    Load and parse a DocFX site manifest from the specified file.

    :param filename: The local file-system path of the file containing the DocFX site manifest.
    :returns: A dictionary containing the manifest.
    :rtype: dict
    """

    with open(filename) as docfx_manifest_file:
        return json.load(docfx_manifest_file)

def load_docfx_xref_map(filename):
    """
    Load and parse a DocFX cross-reference map from the specified file.

    :param filename: The local file-system path of the file containing the DocFX cross-reference map.
    :returns: A list containing the map entries.
    :rtype: list
    """

    with open(filename) as xref_map_file:
        return yaml.load(xref_map_file)["references"]

def parse_args():
    """
    Parse command-line arguments.

    :returns: The parsed arguments.
    """

    parser = argparse.ArgumentParser(__file__,
        description="Publish content from a generated DocFX web site to Confluence.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--docfx-manifest",
        required=True,
        help="The local file-system path of manifest.json in the generated DocFX web site."
    )
    parser.add_argument("--confluence-space",
        required=True,
        help="The key (short name) of the target space in Confluence."
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
    args = parser.parse_args()

    if not args.confluence_address:
        parser.exit(status=1, message="Must specify address of Confluence server using --confluence-address argument or CONFLUENCE_ADDR environment variable.")

    if not args.confluence_user:
        parser.exit(status=1, message="Must specify user name for authentication to Confluence server using --confluence-user argument or CONFLUENCE_USER environment variable.")

    if not args.confluence_password:
        parser.exit(status=1, message="Must specify password for authentication to Confluence server using --confluence-password argument or CONFLUENCE_PASSWORD environment variable.")

    return args


class ConfluenceClient(object):
    """
    Simple client for the Confluence REST API.
    """

    def __init__(self, base_address, username, password):
        """
        Create a new ConfluenceClient.

        :param base_address: The base address of the Confluence REST API end-point.
        :param user: The user name for authenticating to Confluence.
        :param password: The password for authenticating to Confluence.
        :type base_address: str
        :type user: str
        :type password: str
        """

        self.base_address = base_address
        if not self.base_address.endswith("/rest/api/"):
            self.base_address = urljoin(base_address, "rest/api/")

        self.session = requests.Session()
        self.session.auth = (username, password)

    def get_json(self, relative_url, **kwargs):
        """
        Perform an HTTP GET, and return the result as JSON.

        :param relative_url: The target URL (relative to the base address).
        """

        target_url = urljoin(self.base_address, relative_url)
        response = self.session.get(target_url, *kwargs)

        return response.json()

    def post_json(self, relative_url, data, **kwargs):
        """
        Perform an HTTP POST, and return the result as JSON.

        :param relative_url: The target URL (relative to the base address).
        :param data: The request body.
        """

        target_url = urljoin(self.base_address, relative_url)
        response = self.session.post(target_url, data, *kwargs).json()

        return response.json()

    def put_json(self, relative_url, data, **kwargs):
        """
        Perform an HTTP PUT, and return the result as JSON.

        :param relative_url: The target URL (relative to the base address).
        :param data: The request body.
        """

        target_url = urljoin(self.base_address, relative_url)
        response = self.session.put(target_url, data, *kwargs).json()

        return response.json()

    def delete_json(self, relative_url, **kwargs):
        """
        Perform an HTTP POST, and return the result as JSON.

        :param relative_url: The target URL (relative to the base address).
        """

        target_url = urljoin(self.base_address, relative_url)
        response = self.session.delete(target_url, *kwargs).json()

        return response.json()

if __name__ == "__main__":
    main()
