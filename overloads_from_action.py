from data import ReevAction, ReevVariant, Parameter
from overload_classes import OverloadParam, VisibleToInfo, ParamReevState
from overload import generate_overload
from useful_methods import binary_combinations, first_or, first


class _OverloadParameters:
    overload_parameters: list[OverloadParam]
    visible_to_info: VisibleToInfo
    reev_type_name: str

    def __init__(self, parameters: list[OverloadParam], visible_to_info: VisibleToInfo, reev_type_name: str):
        self.overload_parameters = parameters
        self.visible_to_info = visible_to_info
        self.reev_type_name = reev_type_name


def _get_smallest_variant_from_list_that_has_all_parameters(combination: list[Parameter],  variants :list[ReevVariant]) -> ReevVariant:
    
    # Take variant with the biggest amount of parameters
    smallest_variant = max(variants, key = lambda variant: len(variant.parameters))
         
    # Getting smallest reev variant that has all parameters from current combination inside
    for variant in variants:

        # Checking if combination is insede variant.parameter_name_list 
        # (we can use sets because parameter names are unique and in this case their order doesnt matter)
        variant_param_names_set =  set(list(map(lambda param: param.name_spaced, variant.parameters)))
        combination_param_names_set = set(list(map(lambda param: param.name_spaced, combination)))

        is_subset = combination_param_names_set.issubset(variant_param_names_set)
        is_smallest = len(variant.parameters) < len(smallest_variant.parameters)

        if is_subset and is_smallest:
            smallest_variant = variant

    return smallest_variant


def _add_static_parameters_from_variant(variant: ReevVariant, combination: list[OverloadParam], has_visible_to: bool) -> list[OverloadParam]: 

    result_combination = combination.copy()
    static_params = [ 
        OverloadParam(parameter, ParamReevState.static, True) 
        for parameter in variant.parameters 
        if not parameter in combination 
        and not (has_visible_to and "Visible To" in parameter.name_spaced)
    ]
    result_combination.extend(static_params)
    return result_combination


def _generate_visible_to_infos(combination_has_visible_to: bool) -> list[VisibleToInfo]:
    
    #If combination has Visible To, create five combinations with ReevParameterLpVt parameters, one overload for possible combination of visibleTo properties values
    if combination_has_visible_to:
        return [
            VisibleToInfo.CreateWithVisibleTo(visible_to_state = ParamReevState.static, visible_if_state = ParamReevState.reev),
            VisibleToInfo.CreateWithVisibleTo(visible_to_state = ParamReevState.static, visible_if_state = ParamReevState.reev_for),
            VisibleToInfo.CreateWithVisibleTo(visible_to_state = ParamReevState.reev, visible_if_state = ParamReevState.static),
            VisibleToInfo.CreateWithVisibleTo(visible_to_state = ParamReevState.reev, visible_if_state = ParamReevState.reev),
            VisibleToInfo.CreateWithVisibleTo(visible_to_state = ParamReevState.reev, visible_if_state = ParamReevState.reev_for)
        ]
        
    # If it has not, create just one overload with ReevParameterLp params
    else:
        return [VisibleToInfo.CreateWithoutVisibleTo()]


def _get_overload_params_from_combination_for_action(action: ReevAction, combination: list[OverloadParam], has_visible_to: bool)  -> list[OverloadParam]:
    
    overload_params: list[OverloadParam] = [
        first_or(
            iterable = [
                overload_param 
                for overload_param in combination 
                if overload_param.name_spaced == parameter.name_spaced
            ], 
            if_empty = OverloadParam(parameter, ParamReevState.static, False)
        ) 
        for parameter in action.parameters
        if not "Reevaluation" in parameter.name_spaced
        and not (has_visible_to and "Visible To" in parameter.name_spaced)
    ]

    return overload_params






def get_overloads_from_action(action: ReevAction) -> list[str]:   

    overloads: list[str] = []

    overload_number = 0

    for state_combination in binary_combinations(len(action.reev_parameters)):

        combination = [
            param
            for param, state in zip(action.reev_parameters, state_combination)
            if state
        ]
        
        # Find variant of action that fits combination
        smallest_variant = _get_smallest_variant_from_list_that_has_all_parameters(combination, action.reev_variants)
        
        # print(overload_number)
        # print("current smallest_variant name:", smallest_variant.name_code)
        # print("current param combination:", list(map(lambda param: param.name_spaced, combination))) 
        # print("all actions variant names:", list(map(lambda variant: variant.name_code, action.reev_variants)))
        # print("all actions variant parameters:", list(map(lambda variant: list(map(lambda param: param.name_spaced, variant.parameters)), action.reev_variants)))
        # print("\n\n")
        
        combination_without_visible_to =  [param for param in combination if not "Visible To" in param.name_spaced]
        has_visible_to = len(combination_without_visible_to) != len(combination)


        if action.info.has_local_player_access:
            bool_reev_state_combinations = binary_combinations(len(combination))
        else:
            bool_reev_state_combinations = [[False] * len(combination)]
        
            
        for bool_reev_state_combination in bool_reev_state_combinations:
            
            overload_params_combination = [ 
                OverloadParam(param, ParamReevState.reev_for if bool_reev_state else ParamReevState.reev, False) 
                for bool_reev_state, param in zip(bool_reev_state_combination, combination_without_visible_to) 
            ]

            visibleToInfos = _generate_visible_to_infos(has_visible_to)

            for info in visibleToInfos:

                extended_overload_params_combination = _add_static_parameters_from_variant(smallest_variant, overload_params_combination, has_visible_to)

                parameters = _get_overload_params_from_combination_for_action(action, extended_overload_params_combination, has_visible_to)

                overload_number += 1
                
                overload = generate_overload(
                    action = action.info, 
                    parameters = parameters, 
                    visible_to_info = info, 
                    reev_name_code = smallest_variant.name_code, 
                    overload_number = overload_number
                )
                
                overloads.append(overload)
            
    return overloads


