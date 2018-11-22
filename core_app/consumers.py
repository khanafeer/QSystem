from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class SoundConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'sounds',
            self.channel_name
        )
        await self.accept()
        print("accepted SSS000")

    async def disconnect(self,close_code):
        print("disconnect ")

    async def receive_json(self, content, **kwargs):
        print("recieved",content)
        # Receive message from room group

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class CallConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            'terminals',
            self.channel_name
        )
        print("accepted")
        await self.accept()

    async def disconnect(self,close_code):
        print("disconnect ")

    async def receive_json(self, content, **kwargs):
        await self.channel_layer.group_send(
            'sounds',
            {
                'type': 'chat_message',
                'message': content
            }
        )
        print("text sent",content)
        # Receive message from room group

    async def chat_message(self, event):
        message = event['message']
        print("gggg",message)

        # Send message to WebSocket
        await self.send_json(json.dumps({
            'type':'websocket.send',
            'message': message
        }))
