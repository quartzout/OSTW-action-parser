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
    
