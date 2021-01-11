input = {
  "resourceInfo": {
    "id": "5613490d-e64d-4797-ad70-3062d648b332",
    "name": "external-ipam-it-mcm-3234139",
    "description": "test",
    "type": "VM",
    "owner": "vraikov@vmware.com",
    "hostname": "bond-006",
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
  "addressInfos": [{
    "nicIndex": 0,
    "address": "10.23.117.1",
    "macAddress": "00:30:26:a7:23:26"
  }],
  "endpoint": {
      "endpointProperties": {
        "hostName": "infoblox.sof-mbu.eng.vmware.com",
        "projectId": "111bb2f0-02fd-4983-94d2-8ac11768150f",
        "providerId": "d8a5e3f2-d839-4365-af5b-f48de588fdc1",
        "isLocalEnv":"true",
        "certificate": """-----BEGIN CERTIFICATE-----\nMIID0jCCArqgAwIBAgIQQaJF55UCb58f9KgQLD/QgTANBgkqhkiG9w0BAQUFADCB\niTELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExEjAQBgNVBAcTCVN1\nbm55dmFsZTERMA8GA1UEChMISW5mb2Jsb3gxFDASBgNVBAsTC0VuZ2luZWVyaW5n\nMSgwJgYDVQQDEx9pbmZvYmxveC5zb2YtbWJ1LmVuZy52bXdhcmUuY29tMB4XDTE5\nMDEyOTEzMDExMloXDTIwMDEyOTEzMDExMlowgYkxCzAJBgNVBAYTAlVTMRMwEQYD\nVQQIEwpDYWxpZm9ybmlhMRIwEAYDVQQHEwlTdW5ueXZhbGUxETAPBgNVBAoTCElu\nZm9ibG94MRQwEgYDVQQLEwtFbmdpbmVlcmluZzEoMCYGA1UEAxMfaW5mb2Jsb3gu\nc29mLW1idS5lbmcudm13YXJlLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCC\nAQoCggEBAMMLNTqbAri6rt/H8iC4UgRdN0qj+wk0R2blmD9h1BiZJTeQk1r9i2rz\nzUOZHvE8Bld8m8xJ+nysWHaoFFGTX8bOd/p20oJBGbCLqXtoLMMBGAlP7nzWGBXH\nBYUS7kMv/CG+PSX0uuB0pRbhwOFq8Y69m4HRnn2X0WJGuu+v0FmRK/1m/kCacHga\nMBKaIgbwN72rW1t/MK0ijogmLR1ASY4FlMn7OBHIEUzO+dWFBh+gPDjoBECTTH8W\n5AK9TnYdxwAtJRYWmnVqtLoT3bImtSfI4YLUtpr9r13Kv5FkYVbXov1KBrQPbYyp\n72uT2ZgDJT4YUuWyKpMppgw1VcG3MosCAwEAAaM0MDIwMAYDVR0RBCkwJ4cEChda\nCoIfaW5mb2Jsb3guc29mLW1idS5lbmcudm13YXJlLmNvbTANBgkqhkiG9w0BAQUF\nAAOCAQEAXFPIh00VI55Sdfx+czbBb4rJz3c1xgN7pbV46K0nGI8S6ufAQPgLvZJ6\ng2T/mpo0FTuWCz1IE9PC28276vwv+xJZQwQyoUq4lhT6At84NWN+ZdLEe+aBAq+Y\nxUcIWzcKv8WdnlS5DRQxnw6pQCBdisnaFoEIzngQV8oYeIemW4Hcmb//yeykbZKJ\n0GTtK5Pud+kCkYmMHpmhH21q+3aRIcdzOYIoXhdzmIKG0Och97HthqpvRfOeWQ/A\nPDbxqQ2R/3D0gt9jWPCG7c0lB8Ynl24jLBB0RhY6mBrYpFbtXBQSEciUDRJVB2zL\nV8nJiMdhj+Q+ZmtSwhNRvi2qvWAUJQ==\n-----END CERTIFICATE-----\n"""
      },
      "authCredentialsLink": "/core/auth/credentials/13c9cbade08950755898c4b89c4a0"
  }
}

import unittest
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

context = MagicMock()
auth_credentials = {"status": 200, "content": "{\"privateKeyId\": \"admin\", \"privateKey\": \"VMware1!\"}"}
subnet_ranges = {"status": 200, "content": "{\"totalCount\": 1, \"documents\": {\"/resources/subnet-ranges/c19bd2921af950755777fd33fe060\": {\"domain\": \"test.local\"}}}"}
context.request.side_effect = [auth_credentials, auth_credentials, subnet_ranges, subnet_ranges]

print(handler(context, input))