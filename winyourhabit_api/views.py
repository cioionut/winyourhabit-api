from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route


from winyourhabit_api.models import User, Proof, HabitGroup, Objective, Vote
from winyourhabit_api.serializers import UserSerializer, ProofSerializer
from winyourhabit_api.serializers import HabitGroupSerializer, ObjectiveSerializer
from winyourhabit_api.serializers import VoteSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    # remove permissions just for development purposes
    # permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @detail_route(methods=['get'], url_path='groups')
    def list_related_groups(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            user_groups = user.habit_groups.all()
            hg_serialized = HabitGroupSerializer(user_groups, many=True)
            return Response(hg_serialized.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProofViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    # remove permissions just for development purposes
    # permission_classes = (permissions.IsAuthenticated, )
    queryset = Proof.objects.all()
    serializer_class = ProofSerializer


class HabitGroupViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    # remove permissions just for development purposes
    # permission_classes = (permissions.IsAuthenticated, )
    queryset = HabitGroup.objects.all()
    serializer_class = HabitGroupSerializer

    @detail_route(methods=['post'], url_path='join')
    def join(self, request, *args, **kwargs):
        try:
            user_id = int(request.data.get('user_id'))
            hg = self.get_object()
            user = User.objects.get(id=user_id)
            hg.users.add(user)
            hg_serialized = HabitGroupSerializer(hg)
            return Response(hg_serialized.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ObjectiveViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    # remove permissions just for development purposes
    # permission_classes = (permissions.IsAuthenticated, )
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer


class VoteViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    # remove permissions just for development purposes
    # permission_classes = (permissions.IsAuthenticated, )
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


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
