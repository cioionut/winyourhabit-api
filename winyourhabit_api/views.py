from datetime import datetime, timedelta
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route


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

    @detail_route(methods=['get'], url_path='active-objectives')
    def active_objectives(self, request, *args, **kwargs):
        try:
            user_id = int(self.request.query_params.get('user_id', None))
            hg = self.get_object()
            objectives = list()
            for hg_user in hg.users.all():
                if hg_user.id == user_id:
                    objectives += (
                            hg_user.objectives.filter(
                            Q(start_date__gte=datetime.now().date()) |
                            Q(start_date__gte=datetime.now().date() - timedelta(days=hg.time_frame)),
                            habit_group=hg.id,
                            proof__isnull=True,
                        ).order_by('start_date').all())
                else:
                    objs = (
                        hg_user.objectives.filter(
                            start_date__lte=datetime.now().date(),
                            start_date__gte=datetime.now().date() - timedelta(days=hg.time_frame),
                            habit_group=hg.id,
                            proof__isnull=True,
                        ).order_by('start_date'))
                    if len(objs) > 0:
                        objectives.append(objs[0])
            sobjectives = ObjectiveSerializer(objectives, many=True)
            return Response(sobjectives.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get'], url_path='inactive-objectives')
    def inactive_objectives(self, request, *args, **kwargs):
        try:
            user_id = int(self.request.query_params.get('user_id', None))
            hg = self.get_object()
            objectives = list()

            for hg_user in hg.users.all():

                if hg_user.id != user_id:
                    objectives += (
                        hg_user.objectives.filter(
                            # start_date__lte=datetime.now().date() - timedelta(days=hg.time_frame),
                            valid=True,
                            proof__isnull=False,
                            habit_group=hg.id,
                        ).order_by('start_date').all())
            new_objectives = list()
            for objective in objectives:
                voters_id = [vote.user.id for vote in Vote.objects.filter(objective=objective.id).all()]
                if user_id not in voters_id:
                    new_objectives.append(objective)

            sobjectives = ObjectiveSerializer(new_objectives, many=True)
            return Response(sobjectives.data, status=status.HTTP_201_CREATED)

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
