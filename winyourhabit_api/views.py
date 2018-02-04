from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework import permissions


from django.contrib.auth.models import User

from winyourhabit_api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `detail`, `create` and `delete`
    """

    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class UserCreate(APIView):
#     """
#     Creates the user.
#     """
#
#     def post(self, request, format='json'):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             if user:
#                 token = Token.objects.create(user=user)
#                 json = serializer.data
#                 json['token'] = token.key
#                 return Response(json, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
