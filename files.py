import json

import os
def clear(): os.system('cls')


def extract_reev_actions_to_file(filename):
    clear()

    with open("C:\\Users\\quartzout\\Desktop\\ow ana paintball quartz\\generator\\Elements.json", 'r') as original_file:
        json_dict = json.load(original_file)
    
    json_actions = json_dict["actions"]

    with open("C:\\Users\\quartzout\\Desktop\\ow ana paintball quartz\\generator\\Results\\Actions.json", 'w') as actions_file:
        json.dump(json_actions, actions_file)

    def find_revs(item):
        params = dict(item).get("parameters", None)
        if params is None: return False

        reev = dict(params).get("Reevaluation", None)
        if reev is None: return False

        return True

    json_reev_actions = list(filter(find_revs, json_actions))

    #"C:\\Users\\quartzout\\Desktop\\ow ana paintball quartz\\generator\\Results\\Reev Actions.json"
    with open(filename, 'w') as reev_action_file:
        json.dump(json_reev_actions, reev_action_file)

    print(f"json file generated with {len(json_reev_actions)} actions")


def extract_reev_enums_to_file(filename):
    clear()
    
    with open("C:\\Users\\quartzout\\Desktop\\ow ana paintball quartz\\generator\\Elements.json") as original_file:
        json_dict = json.load(original_file)

    json_enums = json_dict["enumerators"]

    json_enums_filtered = {k: v for k, v in json_enums.items() if ('Rev' in k) or ("Eval" in k) or ('Reev' in k) }

    json_enums_filtered["Assist"] = ["Assisters And Targets", "None"]

    #C:\\Users\\quartzout\\Desktop\\ow ana paintball quartz\\generator\\Results\\enums.json
    with open(filename, "w") as enums_file:
        json.dump(json_enums_filtered, enums_file)

    print(f"json file generated with {len(json_enums_filtered)} actions")
