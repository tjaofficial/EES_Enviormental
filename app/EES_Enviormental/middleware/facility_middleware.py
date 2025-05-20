# middleware/facility_middleware.py

from django.shortcuts import redirect # type: ignore
from EES_Forms.models import facility_model

class FacilityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        facility_id = request.session.get("selected_facility")
        
        if facility_id:
            try:
                facility_id = int(facility_id)
                try:
                    request.facility = facility_model.objects.get(id=facility_id)
                except facility_model.DoesNotExist:
                    request.facility = None
                    #print("IF no facililty then revert back to Default check 2")
            except:
                request.facility = None
                #print("IF no facililty then revert back to Default check 3")
        else:
            request.facility = None
            #print("IF no facililty then revert back to Default check 1")

        return self.get_response(request)
