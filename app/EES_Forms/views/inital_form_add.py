import datetime
from ..models import Forms, braintreePlans
from django.contrib.auth.models import Group # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.models import Permission # type: ignore
from django.contrib.contenttypes.models import ContentType # type: ignore
from ..utils.main_utils import create_starting_forms

def add_forms_to_database():
    if Group.objects.count() < 3:
        today = datetime.date.today()
        GROUP_LIST = ['supervisor', 'client', 'observer']
        MODEL_LIST = ContentType.objects.all()
        PERMISSION_LIST = ['view', 'add', 'change', 'delete']
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
    
    if not braintreePlans.objects.all().exists():
        newPlan1 = braintreePlans(
            planID='prod_SLIRV6ib2zYLW1',
            priceID='price_1RQbqHG3aFwevvRDxuhnKPA5',
            name='MethodPro+',
            price=250.00,
            description='Registration for one (1) supervisor and one (1) observer.'
        )
        newPlan2 = braintreePlans(
            planID='prod_SLIR4o0rd3VEtv',
            priceID='price_1RQbqLG3aFwevvRDtUeQs9Dj',
            name='MethodPremium+',
            price=300.00,
            description='Registration for one (1) supervisor and one (1) observer.'
        )
        newPlan3 = braintreePlans(
            planID='prod_SLIRRYnXCQlyXn',
            priceID='price_1RQbq8G3aFwevvRDy7Lyh9Ds',
            name='MethodPlus+',
            price=199.00,
            description='Registration for one (1) supervisor and one (1) observer.'
        )
        newPlan1.save()
        newPlan2.save()
        newPlan3.save()
