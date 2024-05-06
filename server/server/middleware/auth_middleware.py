
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import status
from django.http import HttpResponse

class TokenExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        
        if request.path_info in ['/api/customers/login', '/api/customers/']:
            return self.get_response(request)
        
        authorization_header = request.headers.get('Authorization')

        if not authorization_header or not authorization_header.startswith('Bearer '):
            return HttpResponse({'Authorization header missing or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
       
        token = authorization_header.split()[1]

        try:
            JWTAuthentication().get_validated_token(token)

        except InvalidToken:
            return HttpResponse({'Token invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
            # raise AuthenticationFailed('Invalid or expired token')
        
        # except AuthenticationFailed as e:
        #     return None, Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED) # This will return a 401 Unauthorized

        response = self.get_response(request)
        return response
