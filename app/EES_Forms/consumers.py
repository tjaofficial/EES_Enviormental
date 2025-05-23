import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer # type: ignore
from channels.db import database_sync_to_async # type: ignore
from django.template import Context, Template # type: ignore
from django.template.loader import render_to_string # type: ignore

class NotifConsumer(AsyncWebsocketConsumer): 
    async def connect(self):
        user = self.scope['user']

        if user.is_anonymous:
            await self.close()
            return

        self.company_name = await self.get_company_name(user)
        clean_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', self.company_name)[:90]
        self.groupName = f"notifications_{clean_name}"
        await self.accept()
        await self.channel_layer.group_add(
            self.groupName, 
            self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.groupName, self.channel_name)
    
    async def receive(self, text_data):
        print("🔥 RECEIVE TRIGGERED")
        print(f"WHAT THE ACTRUAL FUCK IS HAPPEND")
        data_from_form_json = json.loads(text_data)
        print('Message', data_from_form_json['notifID'])

        if 'notifID' in data_from_form_json.keys():
            notifID = data_from_form_json['notifID']
            selector = data_from_form_json['selector']
            await database_sync_to_async(self.get_name)(notifID, selector)
        else:
            count = data_from_form_json['count']
            facility = data_from_form_json['facility']
            notif_id = data_from_form_json['notif_id']

            notif_html = await build_notification_html(notif_id, facility)
            print(f'HHHHHHHHHHHHHHHHHHHHH{notif_html}')
            await self.channel_layer.group_send(
                self.groupName,
                {
                    'type': 'notification',
                    'count': count,
                    'facility': facility,
                    'html': notif_html
                }
            )

    async def notification(self, event):
        print(f"Let me see the event: {event}")
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notif_type': event['notif_type'],
            #'count': event['count'],
            'facility': event['facility'],
            'facID': event['facID'],
            'html': event['html']
        }))
        
    def get_name(self, notifID, selector):
        from .models import notifications_model
        notifSelect = notifications_model.objects.get(id=notifID)
        if selector == 'click':
            notifSelect.clicked = True
        notifSelect.hovered = True
        notifSelect.save()
        return 'database Updated'
    
    @database_sync_to_async
    def get_company_name(self, user):
        from .models import user_profile_model
        profile = user_profile_model.objects.get(user=user)
        return profile.company.company_name

@database_sync_to_async
def build_notification_html(notif_id, facility):
    from .models import notifications_model, form_settings_model

    notif_obj = notifications_model.objects.get(id=notif_id)
    form_settings = form_settings_model.objects.get(id=notif_obj.form_id)
    form_type = notif_obj.form_type
    print("NOTIF HTML", render_to_string("shared/components/notification_item.html", {...}))

    return render_to_string("shared/components/notification_item.html", {
        "notif": (form_settings, notif_obj, form_type),
        "facility": facility,
    })