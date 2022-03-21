from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q

from .models import Topic, Room, Message, User, MessageRating
from .forms import UserUpdateForm, UserSignUpForm


# HOME TEMPLATE VIEW
class HomeView(TemplateView):
    template_name = 'forum/home.html'
    model = Room
    slug_field = 'False'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(topic__name__icontains=query) |
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        rooms_queried = self.get_queryset()
        context['rooms'] = rooms_queried
        context['topics'] = Topic.objects.all()
        context['room_messages'] = Message.objects.all()
        context['room_count'] = rooms_queried.count()
        context['room_total'] = Room.objects.all().count()
        return context


# ROOM CRUD VIEWS
class RoomDetailView(TemplateView):
    slug_field = 'pk'
    template_name = 'forum/room.html'

    def get_context_data(self, **kwargs):
        context = super(RoomDetailView, self).get_context_data()
        room = Room.objects.get(id=self.kwargs['pk'])
        context['room'] = room
        context['room_messages'] = room.message_set.all()
        context['participants'] = room.participants.all()
        return context


class RoomCreateView(CreateView):
    model = Room
    template_name = 'forum/room_add.html'
    fields = ['topic', 'name', 'description']

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super(RoomCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context

    def get_success_url(self):
        return reverse('home')


class RoomUpdateView(UpdateView):
    model = Room
    template_name = 'forum/room_add.html'
    fields = ['topic', 'name', 'description']
    slug_name = 'pk'

    def get_object(self, **kwargs):
        return Room.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('home')


class RoomDeleteView(DeleteView):
    model = Room
    slug_field = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.filter(id=self.kwargs['pk'])
        return context

    def get_object(self, queryset=None):
        return self.get_queryset().get(id=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('home')


# MESSAGE CRUD VIEWS
class MessageDeleteView(DeleteView):
    model = Message
    slug_field = 'pk'

    def get_object(self, queryset=None):
        return self.get_queryset().get(id=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('home')


class MessageCreateView(View):
    slug_field = 'pk'

    def post(self, request, *args, **kwargs):
        body = request.POST.get('body')
        user = request.user
        room = Room.objects.get(id=self.kwargs['pk'])
        room.participants.add(request.user)
        Message.objects.create(body=body, author=user, room=room)

        return HttpResponseRedirect(reverse('room_detail', kwargs={'pk': room.id}))


# TOPIC CRUD VIEWS
class TopicCreateView(CreateView):
    model = Topic
    template_name = 'forum/topic_add.html'
    fields = ['name']

    def get_success_url(self):
        return reverse('home')


class TopicSearchView(HomeView):

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(topic__name__icontains=query)
            )
        else:
            object_list = self.model.objects.all()
        return object_list


# PROFILE VIEW
class ProfileView(DetailView):
    model = User
    slug_field = 'pk'
    template_name = 'forum/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['pk'])
        context['user'] = user
        context['rooms'] = user.host.all()
        context['room_messages'] = user.message_set.all()
        context['room_total'] = Room.objects.all().count()
        context['topics'] = Topic.objects.all()
        return context


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    slug_field = 'pk'
    template_name = 'forum/update_user.html'

    def get_form(self, form_class=None):
        form = super(ProfileUpdateView, self).get_form(form_class)
        form.fields['bio'].required = False
        form.fields['avatar'].required = False
        return form

    def get_object(self, **kwargs):
        return User.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.kwargs['pk']})


# AUTHORIZATION VIEWS
class SignUpUserView(CreateView):
    model = User
    template_name = "forum/signup.html"
    form_class = UserSignUpForm

    def get_success_url(self):
        return reverse('home')


class SignInUserView(LoginView):
    template_name = "forum/login.html"
    next_page = 'home'


class SignOutUserView(TemplateView):
    template_name = "forum/logout.html"


class SignOut(LogoutView):
    next_page = 'home'


# CREATE MessageRating instance
class LikeOrDislikeMessage(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        message = Message.objects.get(id=self.kwargs['pk'])
        message_author = message.author
        room = message.room
        topic = room.topic
        user = request.user
        option = self.kwargs['option']
        if not MessageRating.objects.filter(user=user).filter(message=message).exists():
            MessageRating.objects.create(room=room, topic=topic, author=message_author, user=user, value=option,
                                         message=message)
        else:
            existing_message = MessageRating.objects.filter(user=user).get(message=message)
            if existing_message.value != option:
                existing_message.value = option
                existing_message.save()
            else:
                existing_message.delete()

        return HttpResponseRedirect(reverse('room_detail', kwargs={'pk': room.id}))
