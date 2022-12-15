from strings import *
from overload_classes import OverloadParam, VisibleToInfo
from useful_methods import spaced_to_lower_camel_case, capitalize_word
from copy import deepcopy

def _sub_vars(str: str, vars: dict[str, str]) -> str:
    result = str[:]
    for var_name, var_value in vars.items():
        placeholder = f"{PH}{var_name}"
        if placeholder in result:
            result = result.replace(placeholder, var_value)

    if PH in result:
        raise Exception("Unfilled vars are in string: ", result)
    return result
   
   
def _get_recursively(source: dict, keys: list[str]):
    result = deepcopy(source.get(keys[0]))
    if type(result) is dict:
        new_keys = keys[1:]
        if len(new_keys) == 0:
            raise Exception("Not enough keys given")
        return _get_recursively(result, new_keys)
    else:
        #print(source, keys)
        return result


def _prepare_to_insertion(lines: list[str]):
    '''convert list of lines to single string with commas and \\n at the end of every line except the last'''
    return "\n".join(list(map(lambda str: f"{str},", lines[:-1])) + lines[-1:])

def get_method(name: str, parameters: list[str], arguments: list[str]):

    return _sub_vars(METHOD_TEMPLATE, { 
        ph.METHOD_NAME: name,
        ph.METHOD_PARAMETERS: _prepare_to_insertion(parameters),
        ph.METHOD_ARGUMENTS: _prepare_to_insertion(arguments)
    })

    


def get_param_name_code(param: OverloadParam):
    return spaced_to_lower_camel_case(param.name_spaced)

def get_argument_name_code(param: OverloadParam, are_argument_names_capitalised: bool):
    if are_argument_names_capitalised:
        return capitalize_word(get_param_name_code(param))
    else:
        return get_param_name_code(param)

def get_param_string(parameter: OverloadParam) -> str:
   
    string = _get_recursively(PARAM_STRINGS, [
        parameter.is_variable, 
        parameter.reev_state, 
        not parameter.default is None, 
        parameter.is_prebuilt_type
    ])
    
    param_name_code = get_param_name_code(parameter)
    return _sub_vars(string, {
        ph.PARAM_NAME: param_name_code,
        ph.TYPE_NAME: parameter.type_name_code,
        ph.DEFAULT_VALUE: parameter.default
    })

def get_arg_string(parameter: OverloadParam, are_argument_names_capitalised: bool) -> str:

    string = _get_recursively(ARG_STRINGS, [
        parameter.is_variable, 
        parameter.reev_state,
        parameter.evaluate_once
    ])

    param_name_code = get_param_name_code(parameter)
    arg_name_code = get_argument_name_code(parameter, are_argument_names_capitalised)
    return _sub_vars(string, {
        ph.ARG_NAME: arg_name_code,
        ph.PARAM_NAME: param_name_code,
        ph.TYPE_NAME: parameter.type_name_code,
        ph.DEFAULT_VALUE: parameter.default
    })

def get_visible_to_arg_string(info: VisibleToInfo, are_argument_names_capitalised: bool) -> str:
    
    string = _get_recursively(VISIBLE_TO_ARG_STRINGS, [info.visible_to_state, info.visible_if_state]) 

    arg_name = "VisibleTo" if are_argument_names_capitalised else "visibleTo"
    return _sub_vars(string, {
        ph.ARG_NAME: arg_name
    })

def get_reev_argument(reev_type_name: str, reev_name: str, are_argument_names_capitalized: bool) -> str:
    arg_name = "Reevaluation" if are_argument_names_capitalized else "reevaluation"
    return _sub_vars(REEVALUATION_ARGUMENT, { 
        ph.ARG_NAME: arg_name,
        ph.REEV_TYPE_NAME: reev_type_name,
        ph.REEV_NAME: reev_name 
    })


def get_visible_to_param_strings(info: VisibleToInfo) -> list[str]:
   return  _get_recursively(VISIBLE_TO_PARAM_STRINGS, [info.visible_to_state, info.visible_if_state]) 

