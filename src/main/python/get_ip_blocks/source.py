"""
Copyright (c) 2020 VMware, Inc.

This product is licensed to you under the Apache License, Version 2.0 (the "License").
You may not use this product except in compliance with the License.

This product may include a number of subcomponents with separate copyright notices
and license terms. Your use of these subcomponents is subject to the terms and
conditions of the subcomponent's license, as noted in the LICENSE file.
"""

import requests
from vra_ipam_utils.ipam import IPAM
import logging

'''
Example payload:

"inputs": {
    "endpoint": {
      "id": "f097759d8736675585c4c5d272cd",
      "authCredentialsLink": "/core/auth/credentials/13c9cbade08950755898c4b89c4a0",
      "endpointProperties": {
        "hostName": "sampleipam.sof-mbu.eng.vmware.com",
        "certificate": "-----BEGIN CERTIFICATE-----\nMIID0jCCArqgAwIBAgIQQaJF55UCb58f9KgQLD/QgTANBgkqhkiG9w0BAQUFADCB\niTELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExEjAQBgNVBAcTCVN1\nbm55dmFsZTERMA8GA1UEChMISW5mb2Jsb3gxFDASBgNVBAsTC0VuZ2luZWVyaW5n\nMSgwJgYDVQQDEx9pbmZvYmxveC5zb2YtbWJ1LmVuZy52bXdhcmUuY29tMB4XDTE5\nMDEyOTEzMDExMloXDTIwMDEyOTEzMDExMlowgYkxCzAJBgNVBAYTAlVTMRMwEQYD\nVQQIEwpDYWxpZm9ybmlhMRIwEAYDVQQHEwlTdW5ueXZhbGUxETAPBgNVBAoTCElu\nZm9ibG94MRQwEgYDVQQLEwtFbmdpbmVlcmluZzEoMCYGA1UEAxMfaW5mb2Jsb3gu\nc29mLW1idS5lbmcudm13YXJlLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCC\nAQoCggEBAMMLNTqbAri6rt/H8iC4UgRdN0qj+wk0R2blmD9h1BiZJTeQk1r9i2rz\nzUOZHvE8Bld8m8xJ+nysWHaoFFGTX8bOd/p20oJBGbCLqXtoLMMBGAlP7nzWGBXH\nBYUS7kMv/CG+PSX0uuB0pRbhwOFq8Y69m4HRnn2X0WJGuu+v0FmRK/1m/kCacHga\nMBKaIgbwN72rW1t/MK0ijogmLR1ASY4FlMn7OBHIEUzO+dWFBh+gPDjoBECTTH8W\n5AK9TnYdxwAtJRYWmnVqtLoT3bImtSfI4YLUtpr9r13Kv5FkYVbXov1KBrQPbYyp\n72uT2ZgDJT4YUuWyKpMppgw1VcG3MosCAwEAAaM0MDIwMAYDVR0RBCkwJ4cEChda\nCoIfaW5mb2Jsb3guc29mLW1idS5lbmcudm13YXJlLmNvbTANBgkqhkiG9w0BAQUF\nAAOCAQEAXFPIh00VI55Sdfx+czbBb4rJz3c1xgN7pbV46K0nGI8S6ufAQPgLvZJ6\ng2T/mpo0FTuWCz1IE9PC28276vwv+xJZQwQyoUq4lhT6At84NWN+ZdLEe+aBAq+Y\nxUcIWzcKv8WdnlS5DRQxnw6pQCBdisnaFoEIzngQV8oYeIemW4Hcmb//yeykbZKJ\n0GTtK5Pud+kCkYmMHpmhH21q+3aRIcdzOYIoXhdzmIKG0Och97HthqpvRfOeWQ/A\nPDbxqQ2R/3D0gt9jWPCG7c0lB8Ynl24jLBB0RhY6mBrYpFbtXBQSEciUDRJVB2zL\nV8nJiMdhj+Q+ZmtSwhNRvi2qvWAUJQ==\n-----END CERTIFICATE-----\n"
      }
    },
    "pagingAndSorting": {
      "maxResults": 1000,
      "pageToken": "87811419dec2112cda2aa29685685d650ac1f61f"
    }
  }
'''
def handler(context, inputs):

    ipam = IPAM(context, inputs)
    IPAM.do_get_ip_blocks = do_get_ip_blocks

    return ipam.get_ip_blocks()

def do_get_ip_blocks(self, auth_credentials, cert):
    # Your implemention goes here
    username = auth_credentials["privateKeyId"]
    password = auth_credentials["privateKey"]

    ## If many IP blocks are expected on the IPAM server, it is considered a best practice
    ## to return them page by page instead of all at once.
    ## The vRA IPAM Service will propagate a pageToken string with each consecutive request
    ## until all pages are exhausted
    pageToken = self.inputs['pagingAndSorting'].get('pageToken', None) ## The first request that vRA sends is with 'None' pageToken

    ## Plug your implementation here to collect all the ip blocks from the external IPAM system
    result_ip_blocks, next_page_token = collect_ip_blocks(pageToken)

    result = {
        "ipBlocks": result_ip_blocks
    }

    ## Return the next page token so that vRA can process the first page and then fetch the second page or ip blocks with the next request
    if next_page_token is not None:
        result["nextPageToken"] = next_page_token

    return result

def collect_ip_blocks(pageToken):
    logging.info("Collecting ip blocks")

    ip_block1 = {
        "id": "block1",

        "name": "sample name 1",

        "ipBlockCIDR": "10.10.0.0/16",

        "description": "sampleDescription",

        "ipVersion": "IPv4",

        "addressSpaceId": "default",

        "gatewayAddress": "10.10.13.1",

        "domain": "test.local",

        "tags": [{
            "key": "Building",
            "value": "VMware main facility"
        }],

        "properties": {
        }
    }

    ip_block2 = {
        "id": "block2",

        "name": "sample name 2",

        "ipBlockCIDR": "10.10.40.0/24",

        "description": "sampleDescription",

        "ipVersion": "IPv4",

        "addressSpaceId": "default",

        "dnsServerAddresses": ["10.10.17.3", "10.10.22.1"],

        "dnsSearchDomains": ["com", "net", "test.local"],

        "domain": "test.local",

        "tags": [{
            "key": "Building",
            "value": "VMware main facility"
        }],

        "properties": {
        }
    }

    result = []
    next_page_token = None
    if pageToken is None:
        result = [ip_block1]
        next_page_token = "87811419dec2112cda2aa29685685d650ac1f61f"
    else:
        result = [ip_block2]

    return result, next_page_token
