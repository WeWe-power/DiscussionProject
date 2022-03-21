from forum.models import Topic, Room, Message, User, MessageRating
from rest_framework import serializers


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(RoomSerializer, self).to_representation(instance)
        representation['host'] = instance.host.username
        representation['topic'] = instance.topic.name
        representation['participants'] = [x.username for x in instance.participants.all()]

        return representation


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['user']

    def to_representation(self, instance):
        representation = super(MessageSerializer, self).to_representation(instance)
        representation['author'] = instance.author.name
        representation['room'] = instance.room.name

        return representation


class MessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating message
    """
    class Meta:
        model = Message
        fields = ['room', 'body']


class MessageUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating message
    """
    class Meta:
        model = Message
        fields = ['body']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'name', 'date_joined', 'bio', ]


class MessageRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageRating
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(MessageRatingSerializer, self).to_representation(instance)
        representation['room'] = instance.room.name
        representation['topic'] = instance.topic.name
        representation['author'] = instance.author.username
        representation['user'] = instance.user.username
        representation['message'] = instance.message.body

        return representation
