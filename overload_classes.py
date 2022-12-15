from enum import Enum, auto
from data import Parameter

class ParamReevState(Enum):
    static = 1
    reev = 2
    reev_for = 3


class OverloadParam():
    name_spaced: str
    name_reev: str
    default = None
    is_variable: bool
    is_prebuilt_type: bool
    type_name_code: str

    reev_state: ParamReevState
    evaluate_once: bool

    def __init__(self, param: Parameter, reev_state: ParamReevState, evaluate_once: bool):
        self.name_spaced = param.name_spaced
        self.name_reev = param.name_reev
        self.default = param.default
        self.is_variable = param.is_variable
        self.is_prebuilt_type = param.is_prebuilt_type
        self.type_name_code = param.type_name_code

        self.reev_state = reev_state
        self.evaluate_once = evaluate_once


class VisibleToInfo: 
    is_present_and_not_static: bool
    visible_to_state: ParamReevState
    visible_if_state: ParamReevState

    @staticmethod
    def CreateWithVisibleTo(visible_to_state: bool, visible_if_state: bool):
        
        result = VisibleToInfo()
        result.is_present_and_not_static = True

        result.visible_if_state = visible_if_state
        result.visible_to_state = visible_to_state

        return result

    @staticmethod
    def CreateWithoutVisibleTo():
        
        result = VisibleToInfo()
        result.is_present_and_not_static = False

        return result

