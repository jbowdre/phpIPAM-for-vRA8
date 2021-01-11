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

"""
Example payload

"inputs": {
    "resourceInfo": {
      "id": "/resources/sub-networks/255ac10c-0198-4a92-9414-b8e0c23c0204",
      "name": "net1-mcm223-126361015194",
      "type": "SUBNET",
      "orgId": "e0d6ea3a-519a-4308-afba-c973a8903250",
      "owner": "jason@csp.local",
      "properties": {
        "networkType": "PRIVATE",
        "datacenterId": "Datacenter:datacenter-21",
        "__networkCidr": "192.168.197.0/28",
        "__deploymentLink": "/resources/deployments/f77fbe4d-9e78-4b1b-93b0-024d342d0872",
        "__infrastructureUse": "true",
        "__composition_context_id": "f77fbe4d-9e78-4b1b-93b0-024d342d0872",
        "__isInfrastructureShareable": "true"
      }
    },
    "ipRangeAllocation": {
      "name": "net1-mcm223-126361015194",
      "ipBlockIds": [
        "block1",
        "block2"
      ],
      "properties": {
        "networkType": "PRIVATE",
        "datacenterId": "Datacenter:datacenter-21",
        "__networkCidr": "192.168.197.0/28",
        "__deploymentLink": "/resources/deployments/f77fbe4d-9e78-4b1b-93b0-024d342d0872",
        "__infrastructureUse": "true",
        "__composition_context_id": "f77fbe4d-9e78-4b1b-93b0-024d342d0872",
        "__isInfrastructureShareable": "true"
      },
      "subnetCidr": "192.168.197.0/28",
      "addressSpaceId": "default"
    },
    "endpoint": {
      "id": "f097759d8736675585c4c5d272cd",
      "endpointProperties": {
        "hostName": "sampleipam.sof-mbu.eng.vmware.com",
        "projectId": "111bb2f0-02fd-4983-94d2-8ac11768150f",
        "providerId": "d8a5e3f2-d839-4365-af5b-f48de588fdc1",
        "certificate": "-----BEGIN CERTIFICATE-----\nMIID0jCCArqgAwIBAgIQQaJF55UCb58f9KgQLD/QgTANBgkqhkiG9w0BAQUFADCB\niTELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExEjAQBgNVBAcTCVN1\nbm55dmFsZTERMA8GA1UEChMISW5mb2Jsb3gxFDASBgNVBAsTC0VuZ2luZWVyaW5n\nMSgwJgYDVQQDEx9pbmZvYmxveC5zb2YtbWJ1LmVuZy52bXdhcmUuY29tMB4XDTE5\nMDEyOTEzMDExMloXDTIwMDEyOTEzMDExMlowgYkxCzAJBgNVBAYTAlVTMRMwEQYD\nVQQIEwpDYWxpZm9ybmlhMRIwEAYDVQQHEwlTdW5ueXZhbGUxETAPBgNVBAoTCElu\nZm9ibG94MRQwEgYDVQQLEwtFbmdpbmVlcmluZzEoMCYGA1UEAxMfaW5mb2Jsb3gu\nc29mLW1idS5lbmcudm13YXJlLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCC\nAQoCggEBAMMLNTqbAri6rt/H8iC4UgRdN0qj+wk0R2blmD9h1BiZJTeQk1r9i2rz\nzUOZHvE8Bld8m8xJ+nysWHaoFFGTX8bOd/p20oJBGbCLqXtoLMMBGAlP7nzWGBXH\nBYUS7kMv/CG+PSX0uuB0pRbhwOFq8Y69m4HRnn2X0WJGuu+v0FmRK/1m/kCacHga\nMBKaIgbwN72rW1t/MK0ijogmLR1ASY4FlMn7OBHIEUzO+dWFBh+gPDjoBECTTH8W\n5AK9TnYdxwAtJRYWmnVqtLoT3bImtSfI4YLUtpr9r13Kv5FkYVbXov1KBrQPbYyp\n72uT2ZgDJT4YUuWyKpMppgw1VcG3MosCAwEAAaM0MDIwMAYDVR0RBCkwJ4cEChda\nCoIfaW5mb2Jsb3guc29mLW1idS5lbmcudm13YXJlLmNvbTANBgkqhkiG9w0BAQUF\nAAOCAQEAXFPIh00VI55Sdfx+czbBb4rJz3c1xgN7pbV46K0nGI8S6ufAQPgLvZJ6\ng2T/mpo0FTuWCz1IE9PC28276vwv+xJZQwQyoUq4lhT6At84NWN+ZdLEe+aBAq+Y\nxUcIWzcKv8WdnlS5DRQxnw6pQCBdisnaFoEIzngQV8oYeIemW4Hcmb//yeykbZKJ\n0GTtK5Pud+kCkYmMHpmhH21q+3aRIcdzOYIoXhdzmIKG0Och97HthqpvRfOeWQ/A\nPDbxqQ2R/3D0gt9jWPCG7c0lB8Ynl24jLBB0RhY6mBrYpFbtXBQSEciUDRJVB2zL\nV8nJiMdhj+Q+ZmtSwhNRvi2qvWAUJQ==\n-----END CERTIFICATE-----\n"
      },
      "authCredentialsLink": "/core/auth/credentials/13c9cbade08950755898c4b89c4a0"
    }
  }
"""
def handler(context, inputs):

    ipam = IPAM(context, inputs)
    IPAM.do_allocate_ip_range = do_allocate_ip_range

    return ipam.allocate_ip_range()

def do_allocate_ip_range(self, auth_credentials, cert):
    # Your implemention goes here

    username = auth_credentials["privateKeyId"]
    password = auth_credentials["privateKey"]

    resource = self.inputs["resourceInfo"]
    allocation = self.inputs["ipRangeAllocation"]
    ipRange = allocate(resource, allocation, self.context, self.inputs["endpoint"])

    return {
        "ipRange": ipRange
    }

def allocate(resource, allocation, context, endpoint):

    last_error = None
    for ip_block_id in allocation["ipBlockIds"]:

        logging.info(f"Allocating from ip block {ip_block_id}")
        try:
            return allocate_in_ip_block(ip_block_id, resource, allocation, context, endpoint)
        except Exception as e:
            last_error = e
            logging.error(f"Failed to allocate from ip block {ip_block_id}: {str(e)}")

    logging.error("No more ip blocks. Raising last error")
    raise last_error


def allocate_in_ip_block(ip_block_id, resource, allocation, context, endpoint):

    ## Plug your implementation here to allocate an ip range
    ## ...
    ## Allocation successful

    result = {
        "id": "range-new",

        "name": "sample range new",

        "startIPAddress": "10.10.40.1",

        "endIPAddress": "10.10.40.10",

        "description": "sampleDescription",

        "ipVersion": "IPv4",

        "addressSpaceId": "default",

        "subnetPrefixLength": "24",

        "gatewayAddress": "10.10.13.1",

        "domain": "test.local",

        "tags": [{
            "key": "Building",
            "value": "VMware main facility"
        }],

        "properties": {
        }
    }

    return result
