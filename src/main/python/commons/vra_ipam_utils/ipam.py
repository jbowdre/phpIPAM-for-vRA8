"""
Copyright (c) 2020 VMware, Inc.

This product is licensed to you under the Apache License, Version 2.0 (the "License").
You may not use this product except in compliance with the License.

This product may include a number of subcomponents with separate copyright notices
and license terms. Your use of these subcomponents is subject to the terms and
conditions of the subcomponent's license, as noted in the LICENSE file.
"""

import json
import tempfile
import os
import logging
from vra_ipam_utils.exceptions import InvalidCertificateException

class IPAM(object):
    """ IPAM holds util methods for interacting with vRA's IPAM service.

       Defines methods for the following ipam operations:
       1] Validate endpoint
       2] Get IP Ranges
       3] Allocate IP
       4] Deallocate IP
       5] Update record
    """

    def __init__(self, context, inputs):

        self.context = context
        self.inputs = inputs

        # Setup the logging globally
        self._setup_logger()

    def validate_endpoint(self):

        cert = None
        try:
            auth_credentials = self._get_auth_credentials()
            cert = self._get_cert()

            return self.do_validate_endpoint(auth_credentials, cert)
        except InvalidCertificateException as e:
            return {
                "certificateInfo": {
                    "certificate": self._fetch_server_certificate(e.host, e.port)
                },
                "error": self._build_error_response("3002", str(e))["error"] ## Return special status code "3002" on invalid certificate
            }
        finally:
            if cert is not None and type(cert) is str:
                os.unlink(cert)


    def get_ip_ranges(self):

        cert = None
        try:
            auth_credentials = self._get_auth_credentials()
            cert = self._get_cert()

            result = self.do_get_ip_ranges(auth_credentials, cert)

            # Validation of returned result
            err_msg = "{} is mandatory part of the response schema and must be present in the response"
            assert result.get("ipRanges") is not None, err_msg.format("ipRanges")
            assert isinstance(result["ipRanges"], list), "ipRanges must be a list type"
            for i in range(len(result["ipRanges"])):
                assert result["ipRanges"][i].get("id") is not None, err_msg.format(f"ipRanges[{i}]['id']")
                assert result["ipRanges"][i].get("name") is not None, err_msg.format(f"ipRanges[{i}]['name']")
                assert result["ipRanges"][i].get("startIPAddress") is not None, err_msg.format(f"ipRanges[{i}]['startIPAddress']")
                assert result["ipRanges"][i].get("endIPAddress") is not None, err_msg.format(f"ipRanges[{i}]['endIPAddress']")
                assert result["ipRanges"][i].get("ipVersion") is not None, err_msg.format(f"ipRanges[{i}]['ipVersion']")
                assert result["ipRanges"][i].get("subnetPrefixLength") is not None, err_msg.format(f"ipRanges[{i}]['subnetPrefixLength']")

            return result
        finally:
            if cert is not None and type(cert) is str:
                os.unlink(cert)


    def allocate_ip(self):

        cert = None
        try:
            auth_credentials = self._get_auth_credentials()
            cert = self._get_cert()

            result = self.do_allocate_ip(auth_credentials, cert)

             # Validation of returned result
            err_msg = "{} is mandatory part of the response schema and must be present in the response"
            assert result.get("ipAllocations") is not None, err_msg.format("ipAllocations")
            assert isinstance(result["ipAllocations"], list), "ipAllocations must be a list type"
            assert len(result["ipAllocations"]) == len(self.inputs["ipAllocations"]), "Size of ipAllocations in the inputs is different than the one in the outputs"
            for i in range(len(result["ipAllocations"])):
                assert result["ipAllocations"][i].get("ipAllocationId") is not None, err_msg.format(f"ipAllocations[{i}]['ipAllocationId']")
                assert result["ipAllocations"][i].get("ipRangeId") is not None, err_msg.format(f"ipAllocations[{i}]['ipRangeId']")
                assert result["ipAllocations"][i].get("ipVersion") is not None, err_msg.format(f"ipAllocations[{i}]['ipVersion']")
                assert result["ipAllocations"][i].get("ipAddresses") is not None, err_msg.format(f"ipAllocations[{i}]['ipAddresses']")
                assert isinstance(result["ipAllocations"][i]["ipAddresses"], list), f"ipAllocations[{i}]['ipAddresses'] must be a list type"
                assert len(result["ipAllocations"][i]["ipAddresses"]) > 0, f"ipAllocations[{i}]['ipAddresses'] must not be empty"

                for allocation in self.inputs["ipAllocations"]:
                    found = False
                    if allocation["id"] == result["ipAllocations"][i]["ipAllocationId"]:
                        found = True
                        break

                    assert found, f"Allocation result with id {result['ipAllocations'][i]['ipAllocationId']} not found"

            return result
        finally:
            if cert is not None and type(cert) is str:
                os.unlink(cert)

    def deallocate_ip(self):

        cert = None
        try:
            auth_credentials = self._get_auth_credentials()
            cert = self._get_cert()

            result = self.do_deallocate_ip(auth_credentials, cert)

            # Validation of returned result
            err_msg = "{} is mandatory part of the response schema and must be present in the response"
            assert result.get("ipDeallocations") is not None, err_msg.format("ipDeallocations")
            assert isinstance(result["ipDeallocations"], list), "ipDeallocations must be a list type"
            assert len(result["ipDeallocations"]) == len(self.inputs["ipDeallocations"]), "Size of ipDeallocations in the inputs is different than the one in the outputs"
            for i in range(len(result["ipDeallocations"])):
                assert result["ipDeallocations"][i].get("ipDeallocationId") is not None, err_msg.format(f"ipDeallocations[{i}]['ipDeallocationId']")

                for deallocation in self.inputs["ipDeallocations"]:
                    found = False
                    if deallocation["id"] == result["ipDeallocations"][i]["ipDeallocationId"]:
                        found = True
                        break

                    assert found, f"Deallocation result with id {result['ipDeallocations'][i]['ipDeallocationId']} not found"

            return result
        finally:
            if cert is not None and type(cert) is str:
                os.unlink(cert)

    def update_record(self):

        cert = None
        try:
            auth_credentials = self._get_auth_credentials();
            cert = self._get_cert()

            return self.do_update_record(auth_credentials, cert)
        finally:
            if cert is not None and type(cert) is str:
                os.unlink(cert)

    def get_ip_blocks(self):

        cert = None
        try:
            auth_credentials = self._get_auth_credentials()
            cert = self._get_cert()

            result = self.do_get_ip_blocks(auth_credentials, cert)

            # Validation of returned result
            err_msg = "{} is mandatory part of the response schema and must be present in the response"
            assert result.get("ipBlocks") is not None, err_msg.format("ipBlocks")
            assert isinstance(result["ipBlocks"], list), "ipRanges must be a list type"
            for i in range(len(result["ipBlocks"])):
                assert result["ipBlocks"][i].get("id") is not None, err_msg.format(f"ipBlocks[{i}]['id']")
                assert result["ipBlocks"][i].get("name") is not None, err_msg.format(f"ipBlocks[{i}]['name']")
                assert result["ipBlocks"][i].get("ipBlockCIDR") is not None, err_msg.format(f"ipBlocks[{i}]['ipBlockCIDR']")
                assert result["ipBlocks"][i].get("ipVersion") is not None, err_msg.format(f"ipBlocks[{i}]['ipVersion']")

            return result
        finally:
            if cert is not None and type(cert) is str:
                os.unlink(cert)

    def allocate_ip_range(self):

        cert = None
        try:
            auth_credentials = self._get_auth_credentials()
            cert = self._get_cert()

            result = self.do_allocate_ip_range(auth_credentials, cert)

             # Validation of returned result
            err_msg = "{} is mandatory part of the response schema and must be present in the response"
            assert result.get("ipRange") is not None, err_msg.format("ipRange")
            assert result["ipRange"].get("id") is not None, err_msg.format(f"ipRange['id']")
            assert result["ipRange"].get("name") is not None, err_msg.format(f"ipRange['name']")
            assert result["ipRange"].get("startIPAddress") is not None, err_msg.format(f"ipRange['startIPAddress']")
            assert result["ipRange"].get("endIPAddress") is not None, err_msg.format(f"ipRange['endIPAddress']")
            assert result["ipRange"].get("ipVersion") is not None, err_msg.format(f"ipRange['ipVersion']")
            assert result["ipRange"].get("subnetPrefixLength") is not None, err_msg.format(f"ipRange['subnetPrefixLength']")

            return result
        finally:
            if cert is not None and type(cert) is str:
                os.unlink(cert)

    def deallocate_ip_range(self):

        cert = None
        try:
            auth_credentials = self._get_auth_credentials()
            cert = self._get_cert()

            return self.do_deallocate_ip_range(auth_credentials, cert)
        finally:
            if cert is not None and type(cert) is str:
                os.unlink(cert)

    def do_validate_endpoint(self, auth_credentials, cert):
        raise Exception("Method do_validate_endpoint(self, auth_credentials, cert) not implemented")

    def do_get_ip_ranges(self, auth_credentials, cert):
        raise Exception("Method do_get_ip_ranges(self, auth_credentials, cert) not implemented")

    def do_allocate_ip(self, auth_credentials, cert):
        raise Exception("Method do_allocate_ip(self, auth_credentials, cert) not implemented")

    def do_deallocate_ip(self, auth_credentials, cert):
        raise Exception("Method do_deallocate_ip(self, auth_credentials, cert) not implemented")

    def do_update_record(self, auth_credentials, cert):
        raise Exception("Method do_update_record(self, auth_credentials, cert) not implemented")

    def do_get_ip_blocks(self, auth_credentials, cert):
        raise Exception("Method do_get_ip_blocks(self, auth_credentials, cert) not implemented")

    def do_allocate_ip_range(self, auth_credentials, cert):
        raise Exception("Method do_allocate_ip_range(self, auth_credentials, cert) not implemented")

    def do_deallocate_ip_range(self, auth_credentials, cert):
        raise Exception("Method do_deallocate_ip_range(self, auth_credentials, cert) not implemented")


    def _get_cert(self):
        inputs = self.inputs.get("endpoint", self.inputs)
        certificate = inputs["endpointProperties"].get("certificate", None)
        if certificate is not None:
            cert = tempfile.NamedTemporaryFile(mode='w', delete=False)
            cert.write(certificate)
            cert.close()
            return cert.name
        else:
            return True

    """ Fetches the server certificate of the host.
        Used in case the certificate is not automatically trusted
    """
    def _fetch_server_certificate(self, hostname, port):

        logging.info(f"Fetching certificate of {hostname}")
        import ssl
        import socket
        from OpenSSL import SSL
        from OpenSSL import crypto
        import os
        import idna

        hostname_idna = idna.encode(hostname)
        proxy = os.environ.get("http_proxy", None)
        if proxy is not None:
            from urllib.parse import urlparse
            o = urlparse(proxy)
            PROXY_ADDR = (o.hostname, o.port)
            CONNECT = "CONNECT %s:%s HTTP/1.0\r\nConnection: close\r\n\r\n" % (hostname, port)
            logging.info(f"HTTP Proxy is configured. Sending CONNECT command to {proxy}: {CONNECT}")
            CONNECT = bytes(CONNECT, "utf-8")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(PROXY_ADDR)
            sock.send(CONNECT)
            logging.info(sock.recv(4096))
        else:
            sock = socket.socket()
            sock.connect((hostname, port))

        ctx = SSL.Context(SSL.SSLv23_METHOD) # most compatible
        ctx.check_hostname = False
        ctx.verify_mode = SSL.VERIFY_NONE

        sock_ssl = SSL.Connection(ctx, sock)
        sock_ssl.set_connect_state()
        sock_ssl.set_tlsext_host_name(hostname_idna)
        sock_ssl.do_handshake()
        certs = sock_ssl.get_peer_cert_chain()
        sb = ""
        for cert in certs:
            cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
            cert = cert.decode()
            sb += cert

        sock_ssl.shutdown()
        sock_ssl.close()
        sock.close()

        return sb

    def _build_error_response(self, error_code, error_message):
        return {
            "error": {
                "errorCode": error_code,
                "errorMessage": error_message
            }
        }

    """ Fetches the auth credentials from vRA """
    def _get_auth_credentials(self):

        if self._is_mock_request(): # Used for testing purposes within VMware
            return {"privateKeyId": "admin", "privateKey":"VMware"}

        logging.info("Querying for auth credentials")
        inputs = self.inputs.get("endpoint", self.inputs)
        auth_credentials_link = inputs["authCredentialsLink"]
        auth_credentials_response = self.context.request(auth_credentials_link, 'GET', '') ## Integrators can use context.request() to call CAS/Prelude REST endpoints
        if auth_credentials_response["status"] == 200:
            logging.info("Credentials obtained successfully!")
            return json.loads(auth_credentials_response["content"])

        raise Exception('Failed to obtain auth credentials from {}: {}'.format(auth_credentials_link, str(auth_credentials_response)))


    def _setup_logger(self):
        logger = logging.getLogger()
        if logger.handlers:
            for handler in logger.handlers:
                logger.removeHandler(handler)

        logging.basicConfig(format="[%(asctime)s] [%(levelname)s] - %(message)s", level=logging.INFO)
        logging.StreamHandler.emit = lambda self, record: print(logging.StreamHandler.format(self, record))

    def _is_mock_request(self):
        endpoint = self.inputs.get("endpoint", self.inputs)
        return endpoint["endpointProperties"].get("isMockRequest", False)
