from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from accounts.models import User
from hrmis.utils import Blocker, Unblocker,UnBlock
from .serializers import  loginSerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    Blocker()
    try:
        qs = User.objects.get(pk=token.user_id)
    except User.DoesNotExist:
        return Response({'error': 'user id does not exist'}, status=HTTP_404_NOT_FOUND)
    return Response({'token': token.key, 'user_id': token.user_id,'role':qs.designation}, status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
def logout(request):
    print(request.user.auth_token)
    if not request.user.auth_token:
        return Response({'error': 'something went wrong'}, status=HTTP_404_NOT_FOUND)
    request.user.auth_token.delete()
    UnBlock()
    return Response({'success': 'successfully logout'}, status=HTTP_200_OK)
    