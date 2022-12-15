from data import ActionInfo
from overload_classes import OverloadParam, VisibleToInfo
from overload_string_extraction import (
    get_arg_string, 
    get_param_string, 
    get_method, 
    get_visible_to_arg_string, 
    get_visible_to_param_strings, 
    get_reev_argument)
from useful_methods import remove_spaces


def generate_overload(
    action: ActionInfo, 
    parameters: list[OverloadParam], 
    visible_to_info: VisibleToInfo, 
    reev_name_code: str, 
    overload_number: int
) -> str:

    # print(action.name_spaced, list(map(lambda param: param.name_spaced, parameters)))

    parameter_lines = (
        get_visible_to_param_strings(visible_to_info)
        if visible_to_info.is_present_and_not_static
        else []
    )
    
    # if overload_number < 100:
    #     print(action.name_spaced, parameter_lines)
    
    argument_lines = (
        [get_visible_to_arg_string(visible_to_info, action.are_argument_names_capitalized)] 
        if visible_to_info.is_present_and_not_static
        else []
    )
    
    

    parameter_lines += [
        get_param_string(param)
        for param in parameters
    ]
    
    # if overload_number < 100:
    #     print(overload_number, action.name_spaced, parameter_lines, "\n\n")

    argument_lines += [
        get_arg_string(param, action.are_argument_names_capitalized)
        for param in parameters
    ]
        
    argument_lines.append(get_reev_argument(action.reev_type_name, reev_name_code, action.are_argument_names_capitalized))
    
    

    method_name = remove_spaces(action.name_spaced)

    return f"//{overload_number}\n" + get_method(method_name, parameter_lines, argument_lines)
