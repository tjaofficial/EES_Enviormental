from uuid import uuid4
from .models import tokens_model

def create_token(user):
    rand_token = uuid4()
    new_token = tokens_model(user=user, token=rand_token)
    new_token.save()
    return rand_token

def check_token(user, token):
    tokenModel = tokens_model.objects.all()
    try:
        realToken = tokenModel.get(user=user, token=token)
    except:
        realToken = False
    return realToken

def delete_token(user, token):
    tokenModel = tokens_model.objects.all()
    try:
        realToken = tokenModel.get(user=user, token=token)
        realToken.delete()
        print("token successfully removed")
    except:
        print("Not a valid token")
        
    