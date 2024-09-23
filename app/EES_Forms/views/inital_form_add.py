import datetime
from ..models import Forms, braintreePlans
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from ..utils import braintreeGateway, create_starting_forms

def add_forms_to_database():
    if Group.objects.count() < 3:
        today = datetime.date.today()
        GROUP_LIST = ['supervisor', 'client', 'observer']
        MODEL_LIST = ContentType.objects.all()
        PERMISSION_LIST = ['view','add', 'change', 'delete']
        DONT_CHANGE = ['log entry', 'permission', 'group', 'user', 'content type', 'session', 'fa q_model']

        for group in GROUP_LIST:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODEL_LIST:
                if model.name not in DONT_CHANGE:
                    print(model.name)
                    for perm in PERMISSION_LIST:
                        codename_build = perm + '_' + model.name
                        name_build = 'Can '+ perm + ' ' + model.name 
                        print(codename_build)  
                        print(name_build) 
                        permission = Permission.objects.get(
                            #codename=codename_build,
                            name=name_build,
                            content_type=model
                        )
                        new_group.permissions.add(permission)
            print("added " + group)

    if Forms.objects.count() <= 5:
        create_starting_forms()
        
    if braintreePlans.objects.count() == 0:
        gateway = braintreeGateway()
        plans = gateway.plan.all()
        print(plans)
        for plan in plans:
            add_plan = braintreePlans(
                planID = plan.id,
                name = plan.name,
                price = plan.price,
                description = plan.description
            )
            add_plan.save()
