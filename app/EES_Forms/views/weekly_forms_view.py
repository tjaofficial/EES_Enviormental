from django.shortcuts import render
from ..forms import Forms
import datetime

today = datetime.date.today()


def weekly_forms(request):
    pull = Forms.objects.filter(submitted__exact=False).order_by('form')
    pullNot = Forms.objects.filter(submitted__exact=True).order_by('form')

    form_incomplete = []
    for x in pull:
        if x.form in {"D", "G-1", "H"}:
            form_incomplete.append(x)

    form_complete = []
    for s in pullNot:
        if s.form in {"D", "G-1", "H"}:
            form_complete.append(s)

    return render(request, "ees_forms/dashboard.html", {
        "pull": pull, "pullNot": pullNot, "today": today, 'form_incomplete': form_incomplete, 'form_complete': form_complete
    })
