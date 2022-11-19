import jwt
from rest_framework.exceptions import AuthenticationFailed


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token,'secret', algorithms=['HS256'])
        return payload['id']
    except:
        raise AuthenticationFailed('unauthorized')