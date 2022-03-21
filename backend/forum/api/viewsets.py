import redis
import json
from rest_framework import mixins, generics, permissions, authentication, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TopicSerializer, RoomSerializer, MessageSerializer, UserSerializer, MessageRatingSerializer, \
    MessageCreateSerializer, MessageUpdateSerializer
from forum.models import Topic, Message, Room, MessageRating

client = redis.Redis(host='redis', port=6379, db=0)


class DefaultAuth(generics.GenericAPIView):
    """
    Default view that auths with django
    """
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


# TOPIC CRUD----------------------------------------------------------------------------------------------------------
class TopicCRUDBase(generics.GenericAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    lookup_field = 'pk'


class TopicListView(TopicCRUDBase, mixins.ListModelMixin):
    """
    Shows all topics
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TopicRetrieveView(TopicCRUDBase, mixins.RetrieveModelMixin):
    """
    Detail look of topic
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class TopicRoomsView(TopicCRUDBase, generics.RetrieveAPIView):
    """
    Show all rooms connected with selected topic
    """

    def get(self, request, *args, **kwargs):
        topics = Topic.objects.get(id=kwargs['pk'])
        rooms = topics.room_set
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


# ROOM CRUD----------------------------------------------------------------------------------------------------------

class RoomCRUDBase(generics.GenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'pk'


class RoomListView(RoomCRUDBase, mixins.ListModelMixin):
    """
    Shows all rooms
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RoomRetrieveView(RoomCRUDBase, mixins.RetrieveModelMixin):
    """
    Detail look of room
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RoomMessagesView(RoomCRUDBase, generics.RetrieveAPIView):
    """
    Show all messages in selected room
    """

    def get(self, request, *args, **kwargs):
        room = Room.objects.get(id=kwargs['pk'])
        room_messages = room.message_set
        serializer = MessageSerializer(room_messages, many=True)
        return Response(serializer.data)


class RoomParticipantsView(RoomCRUDBase, generics.RetrieveAPIView):
    """
    Show all participants in selected room
    """

    def get(self, request, *args, **kwargs):
        room = Room.objects.get(id=kwargs['pk'])
        serializer = UserSerializer(room.participants, many=True)
        return Response(serializer.data)


# MESSAGE CRUD----------------------------------------------------------------------------------------------------------

class MessageCRUDBase(generics.GenericAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookup_field = 'pk'


class MessageListView(MessageCRUDBase, mixins.ListModelMixin):
    """
    Shows all messages
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MessageCreateAPIView(MessageCRUDBase, DefaultAuth, mixins.CreateModelMixin):
    """
    Create a message
    """
    serializer_class = MessageCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MessageRetrieveView(MessageCRUDBase, mixins.RetrieveModelMixin):
    """
    Detail look of message
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class GetMessageRatesView(MessageCRUDBase, mixins.RetrieveModelMixin):
    """
    Detail look of message
    """

    def get(self, request, *args, **kwargs):
        message = Message.objects.get(id=kwargs['pk'])
        rates = message.messagerating_set
        serializer = MessageRatingSerializer(rates, many=True)

        return Response(serializer.data)


class MessageUpdateView(MessageCRUDBase, DefaultAuth, mixins.UpdateModelMixin):
    """
    Update a message info
    """
    serializer_class = MessageUpdateSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.author == request.user:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        return Response({'detail': 'you are not author of this message'})


class MessageDestroyView(MessageCRUDBase, mixins.DestroyModelMixin):
    """
    Delete message instance
    """

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == request.user:
            self.perform_destroy(instance)
        else:
            return Response({'detail': 'you are not author of this message'})
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


# MESSAGE RATING CRUD----------------------------------------------------------------------------------------------------------

class MessageRatingCRUDBase(generics.GenericAPIView):
    queryset = MessageRating.objects.all()
    serializer_class = MessageRatingSerializer
    lookup_field = 'pk'


class MessageRatingListView(MessageRatingCRUDBase, mixins.ListModelMixin):
    """
    Shows all likes and dislikes
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MessageRatingRetrieveView(MessageRatingCRUDBase, mixins.RetrieveModelMixin):
    """
    Detail look of likes and dislikes
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class MessageRatingLikeList(MessageRatingCRUDBase, generics.ListAPIView):
    """
    Show all dislikes
    """

    def get(self, request, *args, **kwargs):
        rates = MessageRating.objects.filter(value='Like')
        serializer = MessageRatingSerializer(rates, many=True)
        return Response(serializer.data)


class MessageRatingDislikeList(MessageRatingCRUDBase, generics.ListAPIView):
    """
    Show all likes
    """

    def get(self, request, *args, **kwargs):
        rates = MessageRating.objects.filter(value='Dislike')
        serializer = MessageRatingSerializer(rates, many=True)
        return Response(serializer.data)


# OTHERS --------------------------------------------------------------------------------------------------------------

class GetUserScoringList(APIView):
    """
    Get user rankings
    """

    def get(self, request, *args, **kwargs):
        return Response(json.loads(client.get('users_scoring').decode('utf8')))


class GetBestMessagesList(APIView):
    """
    Get best messages
    """

    def get(self, request, *args, **kwargs):
        return Response(json.loads(client.get('best_messages').decode('utf8')))


class GetWorstMessagesList(APIView):
    """
    Get worst messages
    """

    def get(self, request, *args, **kwargs):
        return Response(json.loads(client.get('worst_messages').decode('utf8')))
