from data import get_list_of_actions_from_file, ReevAction
from overloads_from_action import get_overloads_from_action
from useful_methods import chop, clear_console
import os
import glob
from strings import VISIBLE_TO_PARAM_STRINGS

ENUMS_FILENAME = "C:\\Users\\quartzout\\Desktop\\ow ana paintball quartz\\generator\\Inputs\\enums.json"
REEV_ACTIONS_MODIFIED_FILENAME = "C:\\Users\\quartzout\\Desktop\\ow ana paintball quartz\\generator\\Inputs\\Reev Actions Modified.json"
RESULTS_DIRECTORY = "C:\\Users\\quartzout\\Desktop\\ow ana paintball quartz\\generator\\Results\\"
RESULT_FILENAME = "result"

BETWEEN_METHODS = "\n\n"

TEST = \
"""
import "result 0.ostw";

rule: "test" {
	Any testvar = 4;

	_CreateBeamEffect(
		visibleTo: AllPlayers(Team.All),
		beamType: BeamType.BadBeam,
		startPosition_reev_for: p => Vector(0,0,0),
		endPosition: Vector(1,1,1),
		color: Color.White
	);

}
"""

OVERLOADS_IN_FILE = 500
ONLY_WITH_NAME = "Create Beam Effect"

def save_overloads_to_file(result_directory: str, overloads: list[str]):

    

    files = glob.glob(result_directory + "*")
    for f in files:
        os.remove(f)

    for chunk_index, overload_chunk in enumerate(chop(overloads, OVERLOADS_IN_FILE)):
        
        fullname = result_directory + RESULT_FILENAME + f" {chunk_index}" + ".ostw"
        
        with open(fullname, "w") as file:
            content = ("\n" + BETWEEN_METHODS).join(overload_chunk) + "\n"
            file.write(content)
            
    test_file_fullname = result_directory + "test.ostw"        
    with open(test_file_fullname, "w") as file:
        file.write(TEST)


def get_overloads(actions: list[ReevAction]) -> list[str]:
    return [
        overload
        for action in actions
        if ONLY_WITH_NAME in action.info.name_spaced
        for overload in get_overloads_from_action(action) 
    ]


def main():
    
    clear_console()
    
    actions = get_list_of_actions_from_file(REEV_ACTIONS_MODIFIED_FILENAME, ENUMS_FILENAME)
    overloads = get_overloads(actions)
    save_overloads_to_file(RESULTS_DIRECTORY, overloads)
    
    print(f"\n\nGenerated {len(overloads)} overloads")
    
  


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))


if __name__ == "__main__":
    main()
