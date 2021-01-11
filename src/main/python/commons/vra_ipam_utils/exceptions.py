class InvalidCertificateException(Exception):
    def __init__(self, message, host, port):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        
        self.host = host
        self.port = port