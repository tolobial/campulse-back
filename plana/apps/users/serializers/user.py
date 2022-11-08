import string, random

from rest_framework import serializers

from allauth.account.adapter import get_adapter

from django.contrib.auth.models import Group

from plana.apps.users.models import User, AssociationUsers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        if type(data) == str:
            return User.objects.get(username=data)
        elif type(data) == int:
            return User.objects.get(pk=data)


class AssociationUsersSerializer(serializers.ModelSerializer):
    user = UserRelatedField(queryset=User.objects.all(), many=False)

    class Meta:
        model = AssociationUsers
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)


class CustomRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')

    def get_validation_exclusions(self):
        exclusions = super(CustomRegisterSerializer, self).get_validation_exclusions()
        return exclusions + ['phone']

    # TODO: Add check if user exists before save
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = request.data
        adapter.save_user(request, user, self)

        user.username = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']

        user.save()
        return user

