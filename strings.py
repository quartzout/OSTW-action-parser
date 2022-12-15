from overload_classes import ParamReevState
from enum import Enum, auto

NAME_PREFIX = "_"
REEV_POSTFIX = "_reev"
REEV_FOR_POSTFIX = "_reev_for"

PH = "#" #placeholder identifier
#placeholder variable names
class ph(Enum): 
    PARAM_NAME = auto()
    ARG_NAME = auto()
    TYPE_NAME = auto()
    DEFAULT_VALUE = auto()
    METHOD_NAME = auto()
    METHOD_PARAMETERS = auto()
    METHOD_ARGUMENTS = auto()
    REEV_TYPE_NAME = auto()
    REEV_NAME = auto()
    

VISIBLE_TO_PARAM_STRINGS = {

    #visible_to reev state
    ParamReevState.static: {
        
        #visible_if reev state
        ParamReevState.reev: [
            f"\tin Player | Player[] visibleTo = AllPlayers(Team.All)",
            f"\tconst () => Boolean visibleIf{REEV_POSTFIX}"
        ],
        ParamReevState.reev_for: [
            f"\tin Player | Player[] visibleTo = AllPlayers(Team.All)",
            f"\tconst Player => Boolean visibleIf{REEV_FOR_POSTFIX}"
        ]
    },

    ParamReevState.reev: {
        
        #visible_if reev state
        ParamReevState.static: [
            f"\tconst () => Player | Player[] visibleTo{REEV_POSTFIX}",
            f"\tin Boolean visibleIf = true"
        ],
        ParamReevState.reev: [
            f"\tconst () => Player | Player[] visibleTo{REEV_POSTFIX}",
            f"\tconst () => Boolean visibleIf{REEV_POSTFIX}"
        ],
        ParamReevState.reev_for: [
            f"\tconst () => Player | Player[] visibleTo{REEV_POSTFIX}", 
            f"\tconst Player => Boolean visibleIf{REEV_FOR_POSTFIX}"
        ]
    }
}

VISIBLE_TO_ARG_STRINGS = {

    #visible_to reev state
    ParamReevState.static: {
        
        #visible_if reev state
        ParamReevState.reev:        f"\t\t{PH}{ph.ARG_NAME}: visibleIf{REEV_POSTFIX}() && EvaluateOnce(visibleTo.Contains(LocalPlayer())) ? AllPlayers(Team.All) : null",
        ParamReevState.reev_for:    f"\t\t{PH}{ph.ARG_NAME}: visibleIf{REEV_FOR_POSTFIX}(LocalPlayer()) && EvaluateOnce(visibleTo.Contains(LocalPlayer())) ? AllPlayers(Team.All) : null"
    },

    ParamReevState.reev: {
        
        #visible_if reev state
        ParamReevState.static:      f"\t\t{PH}{ph.ARG_NAME}: EvaluateOnce(visibleIf) && visibleTo{REEV_POSTFIX}().Contains(LocalPlayer()) ? AllPlayers(Team.All) : null",
        ParamReevState.reev:        f"\t\t{PH}{ph.ARG_NAME}: visibleIf{REEV_POSTFIX}() && visibleTo{REEV_POSTFIX}().Contains(LocalPlayer()) ? AllPlayers(Team.All) : null",
        ParamReevState.reev_for:    f"\t\t{PH}{ph.ARG_NAME}: visibleIf{REEV_FOR_POSTFIX}(LocalPlayer()) && visibleTo{REEV_POSTFIX}().Contains(LocalPlayer()) ? AllPlayers(Team.All) : null"
    }
}


PARAM_STRINGS = {

    #Is variable
    True: f"\tref Any {PH}{ph.PARAM_NAME}",

    False: {
        
        #Param reev state
        ParamReevState.static: {
            
            #Has default
            True: {
                
                #Is prebuilt type
                True:               f"\tin {PH}{ph.PARAM_NAME} {PH}{ph.PARAM_NAME} = {PH}{ph.DEFAULT_VALUE}",
                False:              f"\t{PH}{ph.TYPE_NAME} {PH}{ph.PARAM_NAME} = {PH}{ph.DEFAULT_VALUE}"
            },
            
            False: {
                
                #Is prebuilt type
                True:               f"\tin {PH}{ph.TYPE_NAME} {PH}{ph.PARAM_NAME}",
                False:              f"\t{PH}{ph.TYPE_NAME} {PH}{ph.PARAM_NAME}"
            }
            
        },
        ParamReevState.reev:        f"\tconst () => {PH}{ph.TYPE_NAME} {PH}{ph.PARAM_NAME}{REEV_POSTFIX}",
        ParamReevState.reev_for:    f"\tconst Player => {PH}{ph.TYPE_NAME} {PH}{ph.PARAM_NAME}{REEV_FOR_POSTFIX}"
    }
    
}

ARG_STRINGS = {
    
    #Is variable
    True:                           f"\t\t {PH}{ph.ARG_NAME}: {PH}{ph.PARAM_NAME}",

    False: {
        
        #Arg reev state
        ParamReevState.static:  {
            
            #is evaluate once
            True:                   f"\t\t{PH}{ph.ARG_NAME}: EvaluateOnce({PH}{ph.PARAM_NAME})",
            False:                  f"\t\t{PH}{ph.ARG_NAME}: {PH}{ph.PARAM_NAME}"
        },
        ParamReevState.reev:        f"\t\t{PH}{ph.ARG_NAME}: {PH}{ph.PARAM_NAME}{REEV_POSTFIX}()",
        ParamReevState.reev_for:    f"\t\t{PH}{ph.ARG_NAME}: {PH}{ph.PARAM_NAME}{REEV_FOR_POSTFIX}(LocalPlayer())"
    }
}

REEVALUATION_ARGUMENT = f"\t\t{PH}{ph.ARG_NAME}: {PH}{ph.REEV_TYPE_NAME}.{PH}{ph.REEV_NAME}"

METHOD_TEMPLATE = \
f"""
void {NAME_PREFIX}{PH}{ph.METHOD_NAME}(
{PH}{ph.METHOD_PARAMETERS}    
) {{
    {PH}{ph.METHOD_NAME}(
{PH}{ph.METHOD_ARGUMENTS}
    );
}}
"""

