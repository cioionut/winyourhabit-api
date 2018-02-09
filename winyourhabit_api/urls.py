from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from winyourhabit_api import views
from django.urls import path



# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'proofs', views.ProofViewSet)
router.register(r'habit-groups', views.HabitGroupViewSet)
router.register(r'objectives', views.ObjectiveViewSet)
router.register(r'votes', views.VoteViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls))
]


# from django.conf.urls import url
# from django.urls import path
#
# from winyourhabit_api.views import UserCreate
#
# urlpatterns = [
#     # url(r'api/users^$', UserCreate.as_view(), name='account-create'),
#     path('api/users/', UserCreate.as_view(), name='account-create')
# ]
