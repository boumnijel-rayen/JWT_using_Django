from django.http import JsonResponse
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentification import decode_auth_token
from .models import *
from .serializers import employeeSerializer, AdminSerializer
import jwt, datetime


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = Admin.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('login failed')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload,'secret', algorithm='HS256').encode('utf-8')

        if user.check_password(password):
            return Response({'JWT': token})
        else:
            raise AuthenticationFailed('login failed')


class emplyeeApiView(APIView):
    def get(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_auth_token(token)
            data = employee.objects.all()
            serializer = employeeSerializer(data, many=True)
            return Response(serializer.data)
        raise AuthenticationFailed('unauthorized')

    def post(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_auth_token(token)
            serializer = employeeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        raise AuthenticationFailed('unauthorized')

class emplyeeParamsApiView(APIView):
    def put(self, request, pk):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_auth_token(token)
            employee1 = employee.objects.get(id=pk)
            serializer = employeeSerializer(instance=employee1, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        raise AuthenticationFailed('unauthorized')

    def delete(self, request, pk):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_auth_token(token)
            employee1 = employee.objects.get(id=pk)
            employee1.delete()
            return Response('Item successfully deleted!')
        raise AuthenticationFailed('unauthorized')

    def get(self, request, pk):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_auth_token(token)
            employee1 = employee.objects.get(id=pk)
            serializer = employeeSerializer(employee1, many=False)
            return JsonResponse(serializer.data, safe=False)
        raise AuthenticationFailed('unauthorized')