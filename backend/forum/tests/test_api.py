from django.test import TestCase, Client
from django.urls import reverse

from forum.api.serializers import TopicSerializer, RoomSerializer, UserSerializer, MessageRatingSerializer
from rest_framework import status
from forum.models import Room, User, Topic, Message, MessageRating

client = Client()


# TOPIC API TEST

class GetTopicsListTest(TestCase):
    """ Test module for GET all Topics API """

    def setUp(self):
        Topic.objects.create(name='topic_1')
        Topic.objects.create(name='topic_2')

    def test_get_topics_list(self):
        response = client.get(reverse('topics-all'))
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetTopicRetrieveTest(TestCase):
    """ Test module for GET Topic retrieve API """

    def setUp(self):
        self.topic_1 = Topic.objects.create(name='topic_1')

    def test_get_topic_retrieve(self):
        response = client.get(reverse('topics-detail', kwargs={'pk': self.topic_1.id}))
        topic = Topic.objects.get(id=self.topic_1.id)
        serializer = TopicSerializer(topic)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_topic(self):
        response = client.get(reverse('topics-detail', kwargs={'pk': -1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetTopicRoomsTest(TestCase):
    """ Test module for GET Topic retrieve API """

    def setUp(self):
        self.topic_1 = Topic.objects.create(name='topic_1')
        user = User.objects.create(
            username='testuser',
            email='test@gmail.com',
            password='test',
        )
        room1 = Room.objects.create(
            name='test1',
            host=user,
            topic=self.topic_1,
            description='text'
        )
        room2 = Room.objects.create(
            name='test2',
            host=user,
            topic=self.topic_1,
            description='text'
        )

    def test_get_topic_rooms(self):
        response = client.get(reverse('topics-rooms', kwargs={'pk': self.topic_1.id}))
        rooms = Room.objects.filter(topic=self.topic_1)
        serializer = RoomSerializer(rooms, many=True)
        self.assertEqual(response.data, serializer.data)


# ROOMS API TEST

class GetRoomParticipantsTest(TestCase):

    def setUp(self):
        user1 = User.objects.create(
            username='testuser1',
            email='test1@gmail.com',
            password='test',
        )
        user2 = User.objects.create(
            username='testuser2',
            email='tes2t@gmail.com',
            password='test',
        )
        topic = Topic.objects.create(name='test')
        self.room = Room.objects.create(
            name='test',
            host=user1,
            topic=topic,
            description='text',
        )
        self.room.participants.set([user1, user2])

    def test_get_room_participants(self):
        response = client.get(reverse('rooms-participants', kwargs={'pk': self.room.id}))
        serializer = UserSerializer(self.room.participants, many=True)
        self.assertEqual(response.data, serializer.data)


class CreateDeleteUpdateMessageTest(TestCase):

    def setUp(self):
        topic = Topic.objects.create(
            name='test'
        )
        self.user = User.objects.create_user(
            username='test',
            email='test@gmail.com',
            password='test'
        )
        self.room = Room.objects.create(
            name='test',
            host=self.user,
            topic=topic,
            description='test',
        )
        self.message = Message.objects.create(
            body='test',
            author=self.user,
            room=self.room
        )

    def test_create_message(self):
        data = {
            'body': 'test',
            'room': self.room.id,
        }
        response = client.post(reverse('api-messages-create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        client.force_login(self.user)
        response = client.post(reverse('api-messages-create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_message(self):
        client.force_login(self.user)
        data = {
            'body': 'new_test'
        }
        client.patch(reverse('api-messages-update', kwargs={'pk': self.message.id}), data=data,
                     content_type='application/json')
        message = Message.objects.get(id=self.message.id)
        self.assertEqual(message.body, 'new_test')

    def test_wrong_user(self):
        user = User.objects.create_user(
            username='test1',
            email='test1@gmail.com',
            password='test1'
        )
        client.force_login(user)
        data = {
            'body': 'new_test'
        }
        response = client.patch(reverse('api-messages-update', kwargs={'pk': self.message.id}), data=data,
                                content_type='application/json')
        self.assertEqual(response.json(), {'detail': 'you are not author of this message'})

    def test_delete_message(self):
        client.force_login(self.user)
        response = client.delete(reverse('api-messages-delete', kwargs={'pk': self.message.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GetMessageRatingsFilteredTest(TestCase):

    def setUp(self):
        self.topic = Topic.objects.create(
            name='test'
        )
        self.user = User.objects.create_user(
            username='test',
            email='test@gmail.com',
            password='test'
        )
        self.room = Room.objects.create(
            name='test',
            host=self.user,
            topic=self.topic,
            description='test',
        )
        self.message = Message.objects.create(
            body='test',
            author=self.user,
            room=self.room
        )
        MessageRating1 = MessageRating.objects.create(
            room=self.room,
            topic=self.topic,
            author=self.user,
            user=self.user,
            message=self.message,
            value='Like',
        )
        MessageRating2 = MessageRating.objects.create(
            room=self.room,
            topic=self.topic,
            author=self.user,
            user=self.user,
            message=self.message,
            value='Dislike',
        )

    def test_get_message_rating_like_list(self):
        response = client.get(reverse('api-messagerating-likes'))
        likes = MessageRating.objects.filter(value='Like')
        serializer = MessageRatingSerializer(likes, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_message_rating_dislike_list(self):
        response = client.get(reverse('api-messagerating-dislikes'))
        dislikes = MessageRating.objects.filter(value='Dislike')
        serializer = MessageRatingSerializer(dislikes, many=True)
        self.assertEqual(response.data, serializer.data)
