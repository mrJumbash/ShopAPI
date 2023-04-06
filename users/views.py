from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserLoginValidateSerializer, UserCreateValidateSerializer, ConfirmCodeValidateSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .models import ConfirmUserCode
from random import choices


class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserLoginValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={'error': 'Username or password wrong!'})


@api_view(['POST'])
def registration_api_views(request):
    serializer = UserCreateValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')
    activate_code = ''.join(choices('0123456789', k=6))
    user = User.objects.create_user(username=username, password=password, is_active=False)
    code = ConfirmUserCode.objects.create(user_id=user.id, code=activate_code)
    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id,
                          'code': code.code})


@api_view(["POST"])
def confirm_user_views(request):
    serializer = ConfirmCodeValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        if ConfirmUserCode.objects.filter(code=request.data['code']):
            User.objects.update(is_active=True)
            return Response(status=status.HTTP_202_ACCEPTED,
                            data={'success': 'confirmed'})

        return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                        data={'error': 'wrong id or code!'})

    except ValueError:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                        data={'error': 'write code number!'})

