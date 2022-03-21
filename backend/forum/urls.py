from django.urls import path, include

from . import views
from .api import viewsets as api_views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('room/detail/<str:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('room/create/', views.RoomCreateView.as_view(), name='room_create'),
    path('room/update/<str:pk>', views.RoomUpdateView.as_view(), name='room_update'),
    path('room/delete/<str:pk>', views.RoomDeleteView.as_view(), name='room_delete'),

    path('topic/create', views.TopicCreateView.as_view(), name='topic_create'),
    path('topic/search', views.TopicSearchView.as_view(), name='topic_search'),

    path('message/delete/<str:pk>', views.MessageDeleteView.as_view(), name='message_delete'),
    path('message/create/<str:pk>', views.MessageCreateView.as_view(), name='message_create'),

    path('message/rate/<str:option>/<str:pk>', views.LikeOrDislikeMessage.as_view(), name='message_rate'),

    path('profile/<str:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/<str:pk>/', views.ProfileUpdateView.as_view(), name='profile_update'),

    path('signup/', views.SignUpUserView.as_view(), name='account_signup'),
    path('signin/', views.SignInUserView.as_view(), name='account_login'),
    path('signout/', views.SignOutUserView.as_view(), name='account_logout'),
    path('signout/c', views.SignOut.as_view(), name='account_logout_c'),
]

api_urls = [
    path('api/topics/', api_views.TopicListView.as_view(), name='topics-all'),
    path('api/topics/retrieve/<str:pk>/', api_views.TopicRetrieveView.as_view(), name='topics-detail'),
    path('api/topics/rooms/<str:pk>/', api_views.TopicRoomsView.as_view(),  name='topics-rooms'),

    path('api/rooms/', api_views.RoomListView.as_view()),
    path('api/rooms/retrieve/<str:pk>/', api_views.RoomRetrieveView.as_view()),
    path('api/rooms/messages/<str:pk>/', api_views.RoomMessagesView.as_view()),
    path('api/rooms/participants/<str:pk>/', api_views.RoomParticipantsView.as_view(), name='rooms-participants'),

    path('api/messages/', api_views.MessageListView.as_view()),
    path('api/messages/retrieve/<str:pk>/', api_views.MessageRetrieveView.as_view()),
    path('api/messages/create/', api_views.MessageCreateAPIView.as_view(), name='api-messages-create'),
    path('api/messages/update/<str:pk>/', api_views.MessageUpdateView.as_view(), name='api-messages-update'),
    path('api/messages/delete/<str:pk>/', api_views.MessageDestroyView.as_view(), name='api-messages-delete'),
    path('api/messages/ratings/<str:pk>/', api_views.GetMessageRatesView.as_view()),
    path('api/messages/best', api_views.GetBestMessagesList.as_view()),

    path('api/ratings/', api_views.MessageRatingListView.as_view()),
    path('api/ratings/retrieve/<str:pk>', api_views.MessageRatingRetrieveView.as_view()),
    path('api/ratings/likes', api_views.MessageRatingLikeList.as_view(), name='api-messagerating-likes'),
    path('api/ratings/dislikes', api_views.MessageRatingDislikeList.as_view(), name='api-messagerating-dislikes'),

    path('api/users/worst', api_views.GetWorstMessagesList.as_view()),
    path('api/users/scoring', api_views.GetUserScoringList.as_view()),

    path('api/', include('api.urls'))
]

urlpatterns += api_urls
