from rest_framework import serializers
from core_app.models import Service,TerminalUser,QueLog,Terminal,User

class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'

class TerminalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Terminal
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)

class QlogSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name')
    terminal_name = serializers.CharField(source='terminal.name')
    user_name = serializers.CharField(source='user.username')


    class Meta:
        model = QueLog
        fields = ('num','service_name','terminal_name','user_name','date_join','date_call','date_end')

class DetailedSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    avg1 = serializers.FloatField(default=0)
    avg2 = serializers.FloatField(default=0)

class TerminalUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TerminalUser
        fields = '__all__'

