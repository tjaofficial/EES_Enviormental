# Make a function with new formID in the format: "formXXsettings"

# Each form will have different settings to help customize the experience
# The "mainLabel" is the label that comes after the packetID which is the
# name of the input that is being set to be customized. Make secondary labels
# and other layers for the dict to go deeper into customized settings (see 
# examples below).
#
# End the function with "return json.loads(json.dumps(settings))"

import json
withoutSettings = [2,4,6,9,21,23]
def formSettingsFunc(keysList, requestPost, formID):
    settings = {}
    print(keysList)
    newLabel = requestPost['newLabel'] if "newLabel" in requestPost else False
    print(newLabel)
    for key, value in requestPost.items():
        defaultDictUpdate = False
        if key not in ['csrfmiddlewaretoken', 'update', 'newLabel'] and key in keysList:
            print(key.split("-"))
            mainLabel = key.split("-")[1]
            print(mainLabel)
            if formID in withoutSettings:
                if mainLabel == 'custom_name':
                    defaultDictUpdate = True
            elif formID == 31:
                pairLen = len(key.split("-"))
                pairFormID = key.split("-")[0]
                if mainLabel == 'custom_name':
                    defaultDictUpdate = True
                elif mainLabel[:4] == 'tank':
                    if mainLabel not in settings.keys():
                        settings[mainLabel] = {
                            "id": requestPost[f"{pairFormID}-{mainLabel}-id"],
                            "name": requestPost[f"{pairFormID}-{mainLabel}-name"],
                            "class": requestPost[f"{pairFormID}-{mainLabel}-class"],
                            "contents": requestPost[f"{pairFormID}-{mainLabel}-contents"],
                        }
            elif formID == 30:
                pairLen = len(key.split("-"))
                pairFormID = key.split("-")[0]
                if mainLabel == 'custom_name':
                    defaultDictUpdate = True
                elif mainLabel == 'num_of_areas':
                    settings[mainLabel] = int(requestPost[key])
                elif mainLabel == 'num_of_waste_cat':
                    settings[mainLabel] = int(requestPost[key])
                elif mainLabel[:4] == 'area':
                    if mainLabel not in settings.keys():
                        settings[mainLabel] = requestPost[key]
                elif mainLabel[:3] == 'cat':
                    if mainLabel not in settings.keys():
                        settings[mainLabel] = requestPost[key]
            elif formID == 20:
                if mainLabel == 'custom_name':
                    defaultDictUpdate = True
                elif mainLabel == 'days_weekly':
                    settings[mainLabel] = int(requestPost[key])
            elif formID == 19:
                if mainLabel in ['custom_name', 'height_above_ground_level', 'describe_emissions_point_start', 'describe_emissions_point_stop', 'process_equip1', 'operating_mode1', 'process_equip2']:
                    defaultDictUpdate = True
            elif formID == 18:
                if mainLabel in ['custom_name', 'height_above_ground_level', 'describe_emissions_point_start', 'describe_emissions_point_stop', 'process_equip1', 'operating_mode1', 'process_equip2']:
                    defaultDictUpdate = True
            elif formID == 17:
                if mainLabel in ['custom_name', 'height_above_ground_level', 'describe_emissions_point_start', 'describe_emissions_point_stop', 'process_equip1', 'operating_mode1', 'process_equip2']:
                    defaultDictUpdate = True
            elif formID == 8:
                if mainLabel == 'custom_name':
                    defaultDictUpdate = True
                elif mainLabel == 'number_of_options':
                    settings[mainLabel] = int(requestPost[key])
                elif mainLabel[:6] == 'option':
                    if mainLabel not in settings['options'].keys():
                        settings['options'][str(mainLabel[6:])] = requestPost[key]
            elif formID == 7:
                pairLen = len(key.split("-"))
                pairFormID = key.split("-")[0]
                secondaryLabel = False
                if pairLen == 3:
                    secondaryLabel = key.split("-")[2]
                if mainLabel == 'custom_name':
                    defaultDictUpdate = True
                elif mainLabel == 'number_of_areas':
                    settings[mainLabel] = int(requestPost[key])
                elif mainLabel[:-1] == 'area':
                    if mainLabel not in settings.keys():
                        settings[mainLabel] = {}
                        settings[mainLabel]['options'] = {}
                        if not secondaryLabel:
                            settings[mainLabel]['name'] = requestPost[key]
                    if pairLen == 3:
                        if secondaryLabel == 'optionsQty':
                            settings[mainLabel]['number_of_options'] = int(requestPost[key])
                        else:
                            if requestPost[key]:
                                settings[mainLabel]['options'][str(secondaryLabel[6:])] = str(requestPost[key])
            elif formID == 5:
                if mainLabel in ['custom_name', 'larry_car_quantity']:
                    defaultDictUpdate = True
            elif formID == 3:
                if mainLabel in ['custom_name','one_pass']:
                    defaultDictUpdate = True
            elif formID == 1:
                if mainLabel in ['custom_name','larry_car_quantity', 'organize_larry_car', 'organize_ovens']:
                    defaultDictUpdate = True
            
            if defaultDictUpdate:
                settings[mainLabel] = False if not requestPost[key] else requestPost[key]
                print(settings[mainLabel])
    settingsDict = json.loads(json.dumps(settings))
    return newLabel, settingsDict

# def form23settings(keysList, requestPost):
#     settings = {}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             mainLabel = key.split("-")[1]
#             if mainLabel == 'custom_name':
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#     return json.loads(json.dumps(settings))

# def form21settings(keysList, requestPost):
#     settings = {}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             mainLabel = key.split("-")[1]
#             if mainLabel == 'custom_name':
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#     return json.loads(json.dumps(settings))

# def form20settings(keysList, requestPost):
#     settings = {}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             mainLabel = key.split("-")[1]
#             if mainLabel == 'custom_name':
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#             elif mainLabel == 'days_weekly':
#                 settings[mainLabel] = int(requestPost[key])
#     return json.loads(json.dumps(settings))

# def form19settings(keysList, requestPost):
#     settings = {}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             mainLabel = key.split("-")[1]
#             if mainLabel in ['custom_name', 'height_above_ground_level', 'describe_emissions_point_start', 'describe_emissions_point_stop', 'process_equip1', 'operating_mode1', 'process_equip2']:
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#     return json.loads(json.dumps(settings))

# def form18settings(keysList, requestPost):
#     settings = {}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             mainLabel = key.split("-")[1]
#             if mainLabel in ['custom_name', 'height_above_ground_level', 'describe_emissions_point_start', 'describe_emissions_point_stop', 'process_equip1', 'operating_mode1', 'process_equip2']:
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#     return json.loads(json.dumps(settings))

# def form17settings(keysList, requestPost):
#     settings = {}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             mainLabel = key.split("-")[1]
#             if mainLabel in ['custom_name', 'height_above_ground_level', 'describe_emissions_point_start', 'describe_emissions_point_stop', 'process_equip1', 'operating_mode1', 'process_equip2']:
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#     return json.loads(json.dumps(settings))

# def form9settings(keysList, requestPost):
#     settings = {}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             mainLabel = key.split("-")[1]
#             if mainLabel == 'custom_name':
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#     return json.loads(json.dumps(settings))

# def form8settings(keysList, requestPost):
#     settings = {'options':{}}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             # pairLen = len(key.split("-"))
#             # pairFormID = key.split("-")[0]
#             mainLabel = key.split("-")[1]
#             if mainLabel == 'custom_name':
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#             elif mainLabel == 'number_of_options':
#                 settings[mainLabel] = int(requestPost[key])
#             elif mainLabel[:6] == 'option':
#                 if mainLabel not in settings['options'].keys():
#                     settings['options'][str(mainLabel[6:])] = requestPost[key]
#     return json.loads(json.dumps(settings))

# def form7settings(keysList, requestPost):
#     settings = {}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             pairLen = len(key.split("-"))
#             pairFormID = key.split("-")[0]
#             mainLabel = key.split("-")[1]
#             secondaryLabel = False
#             if pairLen == 3:
#                 secondaryLabel = key.split("-")[2]
            
#             if mainLabel == 'custom_name':
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#             elif mainLabel == 'number_of_areas':
#                 settings[mainLabel] = int(requestPost[key])
#             elif mainLabel[:-1] == 'area':
#                 if mainLabel not in settings.keys():
#                     settings[mainLabel] = {}
#                     settings[mainLabel]['options'] = {}
#                     if not secondaryLabel:
#                         settings[mainLabel]['name'] = requestPost[key]
#                 if pairLen == 3:
#                     if secondaryLabel == 'optionsQty':
#                         settings[mainLabel]['number_of_options'] = int(requestPost[key])
#                     else:
#                         if requestPost[key]:
#                             settings[mainLabel]['options'][str(secondaryLabel[6:])] = str(requestPost[key])
#     return json.loads(json.dumps(settings))
                





#     # custom_name
#     # number_of_areas
#     # areaX
#     # areaX-optionsQty
#     # areaX-choiceX

#     # cSettings = {
#     #     "custom_name": "Coal Field Inspections", 
#     #     "number_of_areas": "4", 
#     #     "area1": {
#     #         "name": "Trucks",
#     #         "number_of_options": 7,
#     #         "options": {
#     #             "1": {"Contractor": "Contractor"},
#     #             "2": {"#5": "meat"},
#     #             "3": {"#6": "meat"},
#     #             "4": {"#7": "meat"},
#     #             "5": {"#9": "meat"},
#     #             "6": {"Dozer": "meat"},
#     #             "7": {"Water Truck": "meat"}
#     #         }
#     #     }, 
#     #     "area2": {
#     #         "name": "Coal Storage Areas",
#     #         "number_of_options": 5,
#     #         "options": {
#     #             "Panther Eagle": "meat",
#     #             "Kepler": "meat",
#     #             "Rock Lick": "meat",
#     #             "McClure": "meat",
#     #             "Elk Valley": "meat"
#     #         }
#     #     }, 
#     #     "area3": {
#     #         "name": "Area B Coke Storage",
#     #         "number_of_options": 0,
#     #         "options": {}
#     #     }, 
#     #     "area4": {
#     #         "name": "Salt Pile",
#     #         "number_of_options": 0,
#     #         "options": {}
#     #     }
#     # }





#     # {
#     #     'custom_name': 'sdfdfsdfsfdf', 
#     #     'number_of_areas': '2', 
#     #     'area1': {
#     #         'options': {
#     #             '': 'gas'
#     #         }, 
#     #         'name': 'truck', 
#     #         'number_of_options': '3'
#     #     }, 
#     #     'area2': {
#     #         'options': {'': 'fudge'}, 'name': 'Poptarts', 'number_of_options': '3'}}

# def form6settings(keysList, requestPost):
#     settings = {}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             mainLabel = key.split("-")[1]
#             if mainLabel == 'custom_name':
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#     return json.loads(json.dumps(settings))

# def form5settings(keysList, requestPost):
#     settings = {}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             mainLabel = key.split("-")[1]
#             if mainLabel in ['custom_name', 'larry_car_quantity']:
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#     return json.loads(json.dumps(settings))

# def form4settings(keysList, requestPost):
#     settings = {}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             mainLabel = key.split("-")[1]
#             if mainLabel == 'custom_name':
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#     return json.loads(json.dumps(settings))

# def form3settings(keysList, requestPost):
#     settings = {}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             mainLabel = key.split("-")[1]
#             if mainLabel in ['custom_name','one_pass']:
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#     return json.loads(json.dumps(settings))

# def form2settings(keysList, requestPost):
#     settings = {}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             mainLabel = key.split("-")[1]
#             if mainLabel == 'custom_name':
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#     return json.loads(json.dumps(settings))

# def form1settings(keysList, requestPost):
#     settings = {}
#     print(keysList)
#     for key in keysList:
#         if key not in ['csrfmiddlewaretoken', 'update']:
#             mainLabel = key.split("-")[1]
#             if mainLabel in ['custom_name','larry_car_quantity', 'organize_larry_car', 'organize_ovens']:
#                 settings[mainLabel] = False if not requestPost[key] else requestPost[key]
#     return json.loads(json.dumps(settings))
