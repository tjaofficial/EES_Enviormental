

#include on views within forms to say hello to the person logged in
def greet(request,name):
    return HttpResponse(f"Hello, {name.capitalize()}!")

path(<str;name>, views.greet, name="greet")