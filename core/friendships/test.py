import json

from rest_framework.test import APITestCase

from t_helpers.profiles import set_up as profiles_set_up
from t_helpers.mixin401 import TMixin401
from .models import FriendshipInvitation
from .serializers import ReceivedFriendshipInvitationSerializer, CreatedFriendshipInvitationSerializer


class TestReceivedFriendshipInvitationsApi(APITestCase, TMixin401):
    URL = '/received_friend_invitations'
    CONTENT_TYPE = 'application/json'

    model_class = FriendshipInvitation
    serializer_class = ReceivedFriendshipInvitationSerializer

    @classmethod
    def instance_url(cls, instance: FriendshipInvitation):
        return f'{cls.URL}/{instance.id}'

    def setUp(self):
        profile_set_up = profiles_set_up()
        self.vasco, self.chi, self.joao = profile_set_up.profiles
        self.http_auth = profile_set_up.http_auth

        self.joao_vasco_inivitation = self.instance = self.model_class.objects.create(
            inviting=self.joao, invited=self.vasco
        )
        self.vasco_joao_invitation = self.model_class.objects.create(
            inviting=self.vasco, invited=self.joao
        )
        self.chi_vasco_invitation = self.model_class.objects.create(
            inviting=self.chi, invited=self.vasco
        )

    def test_options_200(self):
        response = self.client.options(self.URL, **self.http_auth)
        self.assertEqual(response.status_code, 200)

    def test_list_200(self):
        response = self.client.get(self.URL, **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()['next'])
        self.assertIsNone(response.json()['previous'])
        self.assertEqual(FriendshipInvitation.objects.count(), 3)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(
            response.json()['results'],
            [self.serializer_class(invitation).data
             for invitation in [self.vasco_joao_invitation]]
        )

    def test_list_200_search(self):
        pattern = 'vasco'
        response = self.client.get(f'{self.URL}?search={pattern}', **self.http_auth)
        self.assertEqual(response.status_code, 200)

        self.assertIsNone(response.json()['next'])
        self.assertIsNone(response.json()['previous'])
        self.assertEqual(response.json()['count'], 1)

        pattern = 'joao'
        response = self.client.get(f'{self.URL}?search={pattern}', **self.http_auth)
        self.assertEqual(response.status_code, 200)

        self.assertIsNone(response.json()['next'])
        self.assertIsNone(response.json()['previous'])
        self.assertEqual(response.json()['count'], 0)

    def test_list_200_ordering(self):
        chi_joao_inivitation = FriendshipInvitation.objects.create(
            inviting=self.chi, invited=self.joao
        )

        response = self.client.get(self.URL, **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()['next'])
        self.assertIsNone(response.json()['previous'])
        self.assertEqual(FriendshipInvitation.objects.count(), 4)
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(
            response.json()['results'],
            [self.serializer_class(invitation).data
             for invitation in [chi_joao_inivitation, self.vasco_joao_invitation]]
        )

    def test_retrieve_404(self):
        response = self.client.get(self.instance_url(self.chi_vasco_invitation), **self.http_auth)
        self.assertEqual(response.status_code, 404)

    def test_retrieve_404_inviting(self):
        response = self.client.get(self.instance_url(self.joao_vasco_inivitation), **self.http_auth)
        self.assertEqual(response.status_code, 404)

    def test_retrieve_200_invited(self):
        response = self.client.get(self.instance_url(self.vasco_joao_invitation), **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['friend']['uuid'], self.vasco.uuid)

    def test_create_405(self):
        response = self.client.post(
            self.URL, data=json.dumps({}), content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 405)

    def test_update_405(self):
        response = self.client.put(self.instance_url(self.vasco_joao_invitation),
                                   data=json.dumps({}), content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 405)

    def test_delete_404(self):
        response = self.client.delete(self.instance_url(self.chi_vasco_invitation), **self.http_auth)
        self.assertEqual(response.status_code, 404)

    def test_delete_404_inviting(self):
        response = self.client.delete(self.instance_url(self.joao_vasco_inivitation), **self.http_auth)
        self.assertEqual(response.status_code, 404)

    def test_delete_200_invited(self):
        self.assertEqual(FriendshipInvitation.objects.count(), 3)
        response = self.client.delete(self.instance_url(self.vasco_joao_invitation), **self.http_auth)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(FriendshipInvitation.objects.count(), 2)

    def test_accept(self):
        pass


class TestCreatedFriendshipInvitationsApi(APITestCase):
    URL = '/created_friend_invitations'
    CONTENT_TYPE = 'application/json'

    model_class = FriendshipInvitation
    serializer_class = CreatedFriendshipInvitationSerializer

    @classmethod
    def instance_url(cls, instance: FriendshipInvitation):
        return f'{cls.URL}/{instance.id}'

    def setUp(self):
        profile_set_up = profiles_set_up()
        self.vasco, self.chi, self.joao = profile_set_up.profiles
        self.http_auth = profile_set_up.http_auth

        self.joao_vasco_inivitation = self.model_class.objects.create(
            inviting=self.joao, invited=self.vasco
        )
        self.vasco_joao_invitation = self.instance = self.model_class.objects.create(
            inviting=self.vasco, invited=self.joao
        )
        self.chi_vasco_invitation = self.model_class.objects.create(
            inviting=self.chi, invited=self.vasco
        )

    def test_options_200(self):
        response = self.client.options(self.URL, **self.http_auth)
        self.assertEqual(response.status_code, 200)

    def test_list_200(self):
        response = self.client.get(self.URL, **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()['next'])
        self.assertIsNone(response.json()['previous'])
        self.assertEqual(FriendshipInvitation.objects.count(), 3)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(
            response.json()['results'],
            [self.serializer_class(invitation).data
             for invitation in [self.joao_vasco_inivitation]]
        )

    def test_list_200_ordering(self):
        joao_chi_invitation = FriendshipInvitation.objects.create(
            inviting=self.joao, invited=self.chi
        )

        response = self.client.get(self.URL, **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()['next'])
        self.assertIsNone(response.json()['previous'])
        self.assertEqual(FriendshipInvitation.objects.count(), 4)
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(
            response.json()['results'],
            [self.serializer_class(invitation).data
             for invitation in [joao_chi_invitation, self.joao_vasco_inivitation]]
        )

    def test_list_200_search(self):
        pattern = 'vasco'
        response = self.client.get(f'{self.URL}?search={pattern}', **self.http_auth)
        self.assertEqual(response.status_code, 200)

        self.assertIsNone(response.json()['next'])
        self.assertIsNone(response.json()['previous'])
        self.assertEqual(response.json()['count'], 1)

        pattern = 'joao'
        response = self.client.get(f'{self.URL}?search={pattern}', **self.http_auth)
        self.assertEqual(response.status_code, 200)

        self.assertIsNone(response.json()['next'])
        self.assertIsNone(response.json()['previous'])
        self.assertEqual(response.json()['count'], 0)

    def test_retrieve_404(self):
        response = self.client.get(self.instance_url(self.chi_vasco_invitation), **self.http_auth)
        self.assertEqual(response.status_code, 404)

    def test_retrieve_404_invited(self):
        response = self.client.get(self.instance_url(self.vasco_joao_invitation), **self.http_auth)
        self.assertEqual(response.status_code, 404)

    def test_retrieve_200_inviting(self):
        response = self.client.get(self.instance_url(self.joao_vasco_inivitation), **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['friend']['uuid'], self.vasco.uuid)

    def test_create_40_required(self):
        response = self.client.post(
            self.URL, data=json.dumps({}), content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 400)
        self.assertIn('friend_uuid', response.json())
        self.assertEqual(response.json()['friend_uuid'], ["This field is required."])

    def test_create_400_invalid(self):
        payload = {'friend_uuid': 'abc'}

        response = self.client.post(
            self.URL, data=json.dumps(payload), content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 400)
        self.assertIn('friend_uuid', response.json())
        self.assertEqual(response.json()['friend_uuid'], ["Must be a valid UUID."])

    def test_create_400_no_profile(self):
        payload = {'friend_uuid': self.chi.uuid}
        self.chi.delete()

        response = self.client.post(
            self.URL, data=json.dumps(payload), content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.json())
        self.assertEqual(response.json()['non_field_errors'], ["Unable to find Invited Profile."])

    def test_create_201(self):
        payload = {'friend_uuid': self.chi.uuid}

        from profiles.models import Profile
        Profile.objects.get(external_uuid=payload['friend_uuid'])

        self.assertEqual(FriendshipInvitation.objects.filter(inviting=self.joao).count(), 1)

        response = self.client.post(
            self.URL, data=json.dumps(payload), content_type=self.CONTENT_TYPE, **self.http_auth)
        print('\n\n\n~~~~~')
        import pprint
        pprint.pprint(response.json())
        print('~~~~~\n\n\n')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            FriendshipInvitation.objects.filter(inviting=self.joao).count(), 2)

        new_invitation = FriendshipInvitation.objects.get(id=response.json()['id'])
        self.assertEqual(new_invitation.inviting, self.joao)
        self.assertEqual(new_invitation.invited, self.chi)

    def test_update_405(self):
        response = self.client.put(self.instance_url(self.joao_vasco_inivitation),
                                   data=json.dumps({}), content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 405)

    def test_delete_404(self):
        response = self.client.delete(self.instance_url(self.chi_vasco_invitation), **self.http_auth)
        self.assertEqual(response.status_code, 404)

    def test_delete_404_invited(self):
        response = self.client.delete(self.instance_url(self.vasco_joao_invitation), **self.http_auth)
        self.assertEqual(response.status_code, 404)

    def test_delete_200_inviting(self):
        self.assertEqual(FriendshipInvitation.objects.count(), 3)
        response = self.client.delete(self.instance_url(self.joao_vasco_inivitation), **self.http_auth)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(FriendshipInvitation.objects.count(), 2)

    def test_accept(self):
        pass
