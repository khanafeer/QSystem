from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^call/$', consumers.CallConsumer),
    url(r'^sounds/$', consumers.SoundConsumer),
]