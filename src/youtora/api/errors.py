

class InvalidRequestError(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.status_code = 400
        self.message = message
        if status_code:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = self.status_code
        return rv
