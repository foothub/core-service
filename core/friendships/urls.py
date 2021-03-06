from rest_framework import routers
from .views import (
    ReceivedFriendshipInvitationViewSet,
    CreatedFriendshipInvitationViewSet,
    FriendshipViewSet
)


router = routers.SimpleRouter(trailing_slash=False)
router.register(
    r'received_friend_invitations', ReceivedFriendshipInvitationViewSet, 'received_friend_invitations')

router.register(
    r'created_friend_invitations', CreatedFriendshipInvitationViewSet, 'created_friend_invitations')

router.register(r'friends', FriendshipViewSet, 'friends')

urlpatterns = router.urls
