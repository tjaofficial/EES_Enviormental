import json

def form7settings(keysList, requestPost):
    settings = {}
    print(keysList)
    for key in keysList:
        pairLen = len(key.split("-"))
        pairFormID = key.split("-")[0]
        mainLabel = key.split("-")[1]
        secondaryLabel = False
        print(pairFormID)
        print(mainLabel)
        if pairLen == 3:
            secondaryLabel = key.split("-")[2]
            print(secondaryLabel)
        
        if mainLabel == 'custom_name' or mainLabel == 'number_of_areas':
            settings[mainLabel] = requestPost[key]
        elif mainLabel[:-1] == 'area':
            if mainLabel not in settings.keys():
                settings[mainLabel] = {}
                settings[mainLabel]['options'] = {}
                if not secondaryLabel:
                    settings[mainLabel]['name'] = requestPost[key]
            if pairLen == 3:
                if secondaryLabel == 'optionsQty':
                    settings[mainLabel]['number_of_options'] = requestPost[key]
                else:
                    settings[mainLabel]['options'][str(secondaryLabel[6:])] = str(requestPost[key])
    return json.loads(json.dumps(settings))
                





    # custom_name
    # number_of_areas
    # areaX
    # areaX-optionsQty
    # areaX-choiceX

    # cSettings = {
    #     "custom_name": "Coal Field Inspections", 
    #     "number_of_areas": "4", 
    #     "area1": {
    #         "name": "Trucks",
    #         "number_of_options": 7,
    #         "options": {
    #             "1": {"Contractor": "Contractor"},
    #             "2": {"#5": "meat"},
    #             "3": {"#6": "meat"},
    #             "4": {"#7": "meat"},
    #             "5": {"#9": "meat"},
    #             "6": {"Dozer": "meat"},
    #             "7": {"Water Truck": "meat"}
    #         }
    #     }, 
    #     "area2": {
    #         "name": "Coal Storage Areas",
    #         "number_of_options": 5,
    #         "options": {
    #             "Panther Eagle": "meat",
    #             "Kepler": "meat",
    #             "Rock Lick": "meat",
    #             "McClure": "meat",
    #             "Elk Valley": "meat"
    #         }
    #     }, 
    #     "area3": {
    #         "name": "Area B Coke Storage",
    #         "number_of_options": 0,
    #         "options": {}
    #     }, 
    #     "area4": {
    #         "name": "Salt Pile",
    #         "number_of_options": 0,
    #         "options": {}
    #     }
    # }





    # {
    #     'custom_name': 'sdfdfsdfsfdf', 
    #     'number_of_areas': '2', 
    #     'area1': {
    #         'options': {
    #             '': 'gas'
    #         }, 
    #         'name': 'truck', 
    #         'number_of_options': '3'
    #     }, 
    #     'area2': {
    #         'options': {'': 'fudge'}, 'name': 'Poptarts', 'number_of_options': '3'}}
    
# class form7_model(models.Model):
#     facilityChoice = models.ForeignKey(bat_info_model, on_delete=models.CASCADE, blank=True, null=True)
#     date = models.DateField(auto_now_add=False, auto_now=False)
#     area_json_1 = models.JSONField(
#         default=dict,
#         null=True,
#         blank=True
#     )
#     area_json_1 = {
#         "selection": "Truck #5",
#         "start_time": "time",
#         "stop_time": "time",
#         "readings": {
#             "1": 0,
#             "2": 0,
#             "3": 0,
#             "4": 0,
#             "5": 0,
#             "6": 0,
#             "7": 0,
#             "8": 0,
#             "9": 0,
#             "10": 0,
#             "11": 0,
#             "12": 0,
#         },
#         "average": 0
#     }

#     area_json_2 =models.JSONField(
#         default=dict,
#         null=True,
#         blank=True
#     )
#     area_json_3 =models.JSONField(
#         default=dict,
#         null=True,
#         blank=True
#     )
#     area_json_4 =models.JSONField(
#         default=dict,
#         null=True,
#         blank=True
#     )
#     observer = models.CharField(
#         max_length=30
#     )
#     cert_date = models.DateField(
#         auto_now_add=False,
#         auto_now=False
#     )
#     comments = models.CharField(
#         max_length=600
#     )


#     truck_sel = models.CharField(max_length=30, choices=truck_choices)
#     area_sel = models.CharField(max_length=30, choices=area_choices)
#     truck_start_time = models.TimeField()
#     truck_stop_time = models.TimeField()
#     area_start_time = models.TimeField()
#     area_stop_time = models.TimeField()
#     sto_start_time = models.TimeField(
#         blank = True, null=True
#     )
#     sto_stop_time = models.TimeField(blank = True, null=True)
#     salt_start_time = models.TimeField(blank = True, null=True)
#     salt_stop_time = models.TimeField(blank = True, null=True)
#     average_t = models.FloatField(blank=True)
#     average_p = models.FloatField(blank=True)
#     average_storage = models.FloatField(blank=True, null=True)
#     average_salt = models.FloatField(blank=True, null=True)