import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.template import Context, Template
from .models import notifications_model

class NotifConsumer(AsyncWebsocketConsumer): 
    async def connect(self):
        self.facilityName = self.scope['url_route']['kwargs']['facility']
        self.groupName = 'notifications_%s' % self.facilityName
        await self.accept()
        await self.channel_layer.group_add(self.groupName, self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.groupName, self.channel_name)
    
    async def receive(self, text_data):
        data_from_form_json = json.loads(text_data)
        print('Message', data_from_form_json['notifID'])
        if 'notifID' in data_from_form_json.keys():
            notifID = data_from_form_json['notifID']
            selector = data_from_form_json['selector']
            notifUpdate = await database_sync_to_async(self.get_name)(notifID, selector)
        else:
            count = data_from_form_json['count']
            facility = data_from_form_json['facility']
        
            await self.channel_layer.group_send(
                self.groupName,
                {
                    'type': 'notification',
                    'count': count,
                    'facility': facility
                }
            )
    
    async def notification(self, event):
        count = event['count']
        facility = event['facility']
        
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'count': count,
            'facility': facility
        }))
        
    def get_name(self, notifID, selector):
        notifSelect = notifications_model.objects.get(id=notifID)
        if selector == 'click':
            notifSelect.clicked = True
        notifSelect.hovered = True
        notifSelect.save()
        return 'database Updated'