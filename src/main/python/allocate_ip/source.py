"""
Copyright (c) 2020 VMware, Inc.

This product is licensed to you under the Apache License, Version 2.0 (the "License").
You may not use this product except in compliance with the License.

This product may include a number of subcomponents with separate copyright notices
and license terms. Your use of these subcomponents is subject to the terms and
conditions of the subcomponent's license, as noted in the LICENSE file.

Modifications for phpIPAM by John Bowdre (john@bowdre.net) 
"""

import requests
from vra_ipam_utils.ipam import IPAM
import logging
from datetime import datetime
import ipaddress

"""
Example payload

"inputs": {
    "resourceInfo": {
      "id": "11f912e71454a075574a728848458",
      "name": "external-ipam-it-mcm-323412",
      "description": "test",
      "type": "VM",
      "owner": "mdzhigarov@vmware.com",
      "orgId": "ce811934-ea1a-4f53-b6ec-465e6ca7d126",
      "properties": {
        "osType": "WINDOWS",
        "vcUuid": "ff257ed9-070b-45eb-b2e7-d63926d5bdd7",
        "__moref": "VirtualMachine:vm-288560",
        "memoryGB": "4",
        "datacenter": "Datacenter:datacenter-2",
        "provisionGB": "1",
        "__dcSelfLink": "/resources/groups/b28c7b8de065f07558b1612fce028",
        "softwareName": "Microsoft Windows XP Professional (32-bit)",
        "__computeType": "VirtualMachine",
        "__hasSnapshot": "false",
        "__placementLink": "/resources/compute/9bdc98681fb8b27557252188607b8",
        "__computeHostLink": "/resources/compute/9bdc98681fb8b27557252188607b8"
      }
    },
    "ipAllocations": [
      {
        "id": "111bb2f0-02fd-4983-94d2-8ac11768150f",
        "ipRangeIds": [
          "network/ZG5zLm5ldHdvcmskMTAuMjMuMTE3LjAvMjQvMA:10.23.117.0/24/default"
        ],
        "nicIndex": "0",
        "isPrimary": "true",
        "size": "1",
        "properties": {
          "__moref": "DistributedVirtualPortgroup:dvportgroup-307087",
          "__dvsUuid": "0c 8c 0b 50 46 b6 1c f2-e8 63 f4 24 24 d7 24 6c",
          "__dcSelfLink": "/resources/groups/abe46b8cfa663a7558b28a6ffe088",
          "__computeType": "DistributedVirtualPortgroup",
          "__portgroupKey": "dvportgroup-307087"
        }
      }
    ],
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
    IPAM.do_allocate_ip = do_allocate_ip

    return ipam.allocate_ip()

def auth_session(uri, auth, cert):
    auth_uri = f'{uri}/user/'
    req = requests.post(auth_uri, auth=auth, verify=cert)
    if req.status_code != 200:
        raise requests.exceptions.RequestException('Authentication Failure!')
    token = {"token": req.json()['data']['token']}
    return token

def do_allocate_ip(self, auth_credentials, cert):
    # Build variables
    username = auth_credentials["privateKeyId"]
    password = auth_credentials["privateKey"]
    hostname = self.inputs["endpoint"]["endpointProperties"]["hostName"]
    apiAppId = self.inputs["endpoint"]["endpointProperties"]["apiAppId"]
    uri = f'https://{hostname}/api/{apiAppId}/'
    auth = (username, password)

    # Auth to API
    token = auth_session(uri, auth, cert)
    bundle = {
      'uri': uri,
      'token': token,
      'cert': cert
    }
    
    allocation_result = []
    try:
        resource = self.inputs["resourceInfo"]
        for allocation in self.inputs["ipAllocations"]:
            allocation_result.append(allocate(resource, allocation, self.context, self.inputs["endpoint"], bundle))
    except Exception as e:
        try:
            rollback(allocation_result, bundle)
        except Exception as rollback_e:
            logging.error(f"Error during rollback of allocation result {str(allocation_result)}")
            logging.error(rollback_e)
        raise e

    assert len(allocation_result) > 0
    return {
        "ipAllocations": allocation_result
    }

def allocate(resource, allocation, context, endpoint, bundle):

    last_error = None
    for range_id in allocation["ipRangeIds"]:

        logging.info(f"Allocating from range {range_id}")
        try:
            return allocate_in_range(range_id, resource, allocation, context, endpoint, bundle)
        except Exception as e:
            last_error = e
            logging.error(f"Failed to allocate from range {range_id}: {str(e)}")

    logging.error("No more ranges. Raising last error")
    raise last_error


def allocate_in_range(range_id, resource, allocation, context, endpoint, bundle):
    if int(allocation['size']) ==1:
      vmName = resource['name']
      uri = bundle['uri']
      token = bundle['token']
      cert = bundle['cert']
      # Attempt to grab 'owner' to work around bug in vRA 8.6 (fixed in 8.6.1)
      try:
        owner_string = f" for {resource['owner']} "
      except:
        owner_string = " "
      payload = {
        'hostname': vmName,
        'description': f'Reserved by vRA{owner_string}at {datetime.now()}'
      }
      allocate_uri = f'{uri}/addresses/first_free/{str(range_id)}/'
      allocate_req = requests.post(allocate_uri, data=payload, headers=token, verify=cert)
      allocate_req = allocate_req.json()
      if allocate_req['success']:
        version = ipaddress.ip_address(allocate_req['data']).version
        result = {
          "ipAllocationId": allocation['id'],
          "ipRangeId": range_id,
          "ipVersion": "IPv" + str(version),
          "ipAddresses": [allocate_req['data']] 
        }
        logging.info(f"Successfully reserved {str(result['ipAddresses'])} for {vmName}.")
      else:
        raise Exception("Unable to allocate IP!")

      return result
    else:
      # TODO: implement allocation of continuous block of IPs
      pass
    raise Exception("Not implemented")

## Rollback any previously allocated addresses in case this allocation request contains multiple ones and failed in the middle
def rollback(allocation_result, bundle):
    uri = bundle['uri']
    token = bundle['token']
    cert = bundle['cert']
    for allocation in reversed(allocation_result):
        logging.info(f"Rolling back allocation {str(allocation)}")
        ipAddresses = allocation.get("ipAddresses", None)
        for ipAddress in ipAddresses:
          rollback_uri = f'{uri}/addresses/{allocation.get("id")}/'
          requests.delete(rollback_uri, headers=token, verify=cert)

    return
