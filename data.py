from json import load
from useful_methods import remove_spaces

class Parameter:
    '''Reev parameter pulled from json, without any additional info'''
    name_spaced: str
    name_reev: str
    default = None
    is_variable: bool
    is_prebuilt_type: bool
    type_name_code: str


class ReevVariant:
    name_code: str
    parameters: list[Parameter]

    def __init__(self): #This is used for None variant generation
        self.name_code = "None"
        self.parameters = []


class ActionInfo: 
    has_local_player_access: bool
    has_visible_to: bool
    name_spaced: str
    reev_type_name: str
    are_argument_names_capitalized: bool


class ReevAction:
    '''Actions that support reevaluation (excluding Boolean ones). 
    Parameters in "parameters" property and inside reev_variants list are pointing to the same objects, 
    thus enabling using "is" for conditions'''
    info: ActionInfo
    reev_variants: list[ReevVariant]
    parameters: list[Parameter]
    reev_parameters: list[Parameter]
    


def get_list_of_parameters_from_raw_params_dict(params_dict: dict) -> list[Parameter]:

    result = []
    for name, param_dict in params_dict.items():

        #Getting name as it would be spelled inside reev_variant 
        reev_name = param_dict.get("reev")
        if reev_name is None:
            reev_name = name

        parameter = Parameter()
        parameter.name_spaced = name
        parameter.name_reev = reev_name
        parameter.default = param_dict.get("default")

        raw_type_name = param_dict.get("type")
        if not raw_type_name is None:
            parameter.is_prebuilt_type = isPrebuildType = _is_prebuilt_type(raw_type_name)
            parameter.type_name_code = _get_param_type_name_code_from_raw_name(raw_type_name, isPrebuildType)
        else:
            parameter.is_prebuilt_type = None
            parameter.type_name_code = None

        parameter.is_variable = not param_dict.get("var-ref-global") is None
        result.append(parameter)

    return result


def _is_prebuilt_type(raw_type_name):
    #in actions json file, prebuilt types (Number, String) spelled
    #fully lowercase, and enum types (BeamType) are spelled with CamelCase
    return raw_type_name.islower()


import string
def _get_param_type_name_code_from_raw_name(raw_type_name: str, is_prebuilt_type: bool) -> str:

    #All types in code start with capitals and use CamelCase

    if (is_prebuilt_type):
        #Because in the file there are pipe types like "player | vector", for prebuild types we need to capitalize first letters of every word
        #for them to become code-formatted, like "Player | Vector"
        return string.capwords(raw_type_name)
    else:
        #Enum types are already spelled like in code
        return raw_type_name


def _get_reev_variants_for_action_from_reev_variants_raw_list(raw_variant_list: list, action_params: list[ReevAction]) -> list[ReevVariant]:
    '''Extracts list of reev variants from file for action'''

    variants = [ _get_reev_variant_from_raw_list(raw_variant, action_params) for raw_variant in raw_variant_list ]
    return variants


def _get_reev_variant_from_raw_list(raw_variant: dict | str, action_params: list[Parameter]) -> ReevVariant:
   

    variant = ReevVariant()

    #if its a dict, use "name" value for extracting Reevparameter names for list that would be passed in CreateVariant and "alias" value for 
    #actual in-code variant name that would also be passed in CreateVariant for setting Reevaluation attribute on called method
    
    is_dict = type(raw_variant) is dict
    
    reev_variant_for_splitting: str = raw_variant["name"] if is_dict else raw_variant
    variant.name_code = raw_variant["alias"] if is_dict else remove_spaces(raw_variant.replace(" and ", " And "))

    #If variant is "None", return "None" variant
    if variant.name_code == "None":
        return ReevVariant()

    #otherwise, extract parameter names for list from reev variant name
    parameter_names_spaced = [
        item 
        for item in map(
            lambda item: item.replace("_", " "), 
            (reev_variant_for_splitting
                .replace("Visible To", "Visible_To")
                .replace("Sort Order", "Sort_Order")
                .split(" ")
            )
        ) 
        if item != 'And' and item != "and"
    ]
    
    # map parameter names to parameters in action object
    variant.parameters = [ 
        parameter
        #list with all action parameters that have reev_name as in current parameter from parameter_names_spaced
        for parameter_name_spaced in parameter_names_spaced
        for parameter in [
            parameter
            for parameter in action_params 
            if parameter.name_reev == parameter_name_spaced
        ]
        
    ]
        

    return variant


def _get_list_of_reev_params_for_action(action_params: list[Parameter], variants: list[ReevVariant]) -> list[Parameter]:
    '''Returns list of all parameters of action that can be reevaluated'''

    all_params_from_variants = []
    for variant in variants:
        all_params_from_variants.extend(variant.parameters)

    reev_params = [ 
        param 
        for param in action_params 
        if param in all_params_from_variants 
    ] 
    
    return reev_params


def _does_action_have_has_local_player_access(action_name: str) -> bool:
    '''Determining if action has access to LocalPlayer() value by checking its name'''

    isHudAction = "Text" in action_name and "Chat" not in action_name
    isEffectAction = "Effect" in action_name
    isObjectiveDescription = "Description" in action_name

    result = isHudAction or isEffectAction or isObjectiveDescription

    return result





def get_list_of_actions_from_file(actions_filename: str, reev_enums_filename: str) -> list[ReevAction]:
    '''Extracts list from file with ReevActions'''

    with open(actions_filename) as reev_actions_modified_file:
        raw_actions_list = load(reev_actions_modified_file)

    with open(reev_enums_filename) as enums_file:
        reev_enums_raw_dict = load(enums_file)

    result = []
    for raw_action in raw_actions_list:

        action = ReevAction()
        action.info = ActionInfo()
        
        action.info.reev_type_name = raw_action["parameters"]["Reevaluation"]["type"]
        if action.info.reev_type_name == "boolean":
            continue
        action.info.are_argument_names_capitalized = raw_action.get("hidden") is None

        action.parameters = get_list_of_parameters_from_raw_params_dict(raw_action["parameters"])
        action.reev_variants = _get_reev_variants_for_action_from_reev_variants_raw_list(reev_enums_raw_dict[action.info.reev_type_name], action.parameters)
        action.reev_parameters = _get_list_of_reev_params_for_action(action.parameters, action.reev_variants)


        action.info.name_spaced = raw_action["name"]
        action.info.has_local_player_access = _does_action_have_has_local_player_access(action.info.name_spaced)
        action.info.has_visible_to = len([param for param in action.parameters if param.name_spaced == "Visible To"]) == 1

        result.append(action)

    return result