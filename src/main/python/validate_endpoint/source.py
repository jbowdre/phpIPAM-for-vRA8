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
from vra_ipam_utils.exceptions import InvalidCertificateException
import logging


'''
Example payload:

"inputs": {
    "authCredentialsLink": "/core/auth/credentials/13c9cbade08950755898c4b89c4a0",
    "endpointProperties": {
      "hostName": "sampleipam.sof-mbu.eng.vmware.com"
    }
  }
'''
def handler(context, inputs):

    ipam = IPAM(context, inputs)
    IPAM.do_validate_endpoint = do_validate_endpoint

    return ipam.validate_endpoint()

def auth_session(uri, auth, cert):
    auth_uri = f'{uri}/user/'
    req = requests.post(auth_uri, auth=auth, verify=cert)
    ## We don't need to handle errors or save the token here since we're just validating the endpoint
    # if req.status_code != 200:
    #     raise requests.exceptions.RequestException('Authentication Failed!')
    # logging.info('Authentication successful.')
    # token = {"token": req.json()['data']['token']}
    # return token
    return req

def do_validate_endpoint(self, auth_credentials, cert):
    # Build variables
    username = auth_credentials["privateKeyId"]
    password = auth_credentials["privateKey"]
    hostname = self.inputs["endpointProperties"]["hostName"]
    apiAppId = self.inputs["endpointProperties"]["apiAppId"]
    uri = f'https://{hostname}/api/{apiAppId}/'
    auth = (username, password)

    # Test auth connection
    try:
        response = auth_session(uri, auth, cert)

        if response.status_code == 200:
            return {
                "message": "Validated successfully",
                "statusCode": "200"
            }
        elif response.status_code == 500 and response.json()['message'] == 'Invalid username or password':
            logging.error(f"Invalid credentials error: {str(response.content)}")
            raise Exception(f"Invalid credentials error: {str(response.content)}")
        else:
            raise Exception(f"Failed to connect: {str(response.content)}")
    except Exception as e:
        """ In case of SSL validation error, a InvalidCertificateException is raised.
            So that the IPAM SDK can go ahead and fetch the server certificate
            and display it to the user for manual acceptance.
        """
        if "SSLCertVerificationError" in str(e) or "CERTIFICATE_VERIFY_FAILED" in str(e) or 'certificate verify failed' in str(e):
            raise InvalidCertificateException("certificate verify failed", self.inputs["endpointProperties"]["hostName"], 443) from e

        raise e
