"""
Clangen in your terminal!
"""

from scripts.game_structure.load_cat import load_cats, version_convert
from scripts.game_structure.game_essentials import game
from scripts.cat.cats import Cat
from scripts.events import events_class
from scripts.clan import clan_class
from scripts.utility import quit as clangen_quit # pylint: disable=redefined-builtin

# Advance one moon:
#     events_class.one_moon()
#
# List of current events:
#     game.cur_events_list
#
# Patrol:
#     patrol_members: List[Cat] = []
#     patrol_obj = Patrol()
#     patrol_obj.setup_patrol(patrol_members, patrol_type)
#     patrol_obj.proceed_patrol("proceed")
#
# Cat Relationships
#     sorted(cat_obj.relationships.values(),
#              key=lambda x: sum(map(abs, [x.romantic_love, x.platonic_like, x.dislike,
#                                          x.admiration, x.comfortable, x.jealousy, x.trust])),
#            reverse=True)

class AmbiguousCatException(Exception):
    """Exception raised when lookup refers to multiple cats."""

class CatNotFoundException(Exception):
    """Exception raised when cat can't be found."""

def get_cat_by_name(name: str) -> Cat:
    """Retrieves Cat object from the cat's name. Looks across all cats.
    Raises AmbiguousCatException if multiple cats have the same name."""
    matched_cats = [cat for cat in Cat.all_cats_list if str(cat.name).lower() == name.lower()]
    if len(matched_cats) > 1:
        raise AmbiguousCatException(f"{len(matched_cats)} cats with name {name}")
    if len(matched_cats) == 0:
        raise CatNotFoundException()
    return matched_cats[0]

def get_cat_by_string(string: str) -> Cat:
    """
    Gets Cat object represented by a given string. The string can either be an ID or a name. 
    Tries to look up the ID before it looks up the name.
    """
    try:
        return Cat.all_cats[string]
    except KeyError: # couldn't find cat
        return get_cat_by_name(string)

if __name__ == "__main__":
    # initialize basic logging
    import logging
    logging.basicConfig()
    logger = logging.getLogger(__name__)

    # load clan
    clan_list = game.read_clans()
    if clan_list:
        game.switches['clan_list'] = clan_list
        try:
            load_cats()
            version_info = clan_class.load_clan()
            version_convert(version_info)
            game.load_events()
        except Exception as e:
            logger.exception("File failed to load")
            if not game.switches['error_message']:
                game.switches[
                    'error_message'] = 'There was an error loading the cats file!'
                game.switches['traceback'] = e

    while True:
        user_input = input(">>> ")
        user_input_split = user_input.split()
        if not user_input_split:
            continue
        command = user_input_split[0]
        args = user_input_split[1:]

        if command == "moonskip":
            moons_to_skip = 1
            if args:
                n = args[0]
                if not n.isdigit():
                    print(f"'{n}' is not a positive integer")
                else:
                    moons_to_skip = int(n)

            if moons_to_skip == 1:
                events_class.one_moon()
                print("The moon passes...")
            else:
                for i in range(moons_to_skip):
                    events_class.one_moon()
                print(f"Skipped {n} moons.")

        elif command == "events":
            for event in game.cur_events_list:
                if "interaction" not in event.types:
                    print(event.text)
        elif command == "cats":
            for cat in Cat.all_cats_list:
                print(f"{cat.name} - {cat.describe_cat()}")
        elif command == "quit":
            game.save_cats()
            game.clan.save_clan()
            game.clan.save_pregnancy(game.clan)
            game.save_events()
            clangen_quit()
        elif command == "kill":
            if args:
                try:
                    cat = get_cat_by_string(args[0])
                    if cat.is_alive():
                        cat.die()
                        print(f"{cat.name} was killed.")
                    else:
                        print(f"{cat.name} is already dead!")
                except AmbiguousCatException as e:
                    print(f"Multiple cats with the name `{args[0]}.`")
                except CatNotFoundException:
                    print(f"Could not find cat `{args[0]}`.")
            else:
                print("No cat specified to kill.")
        else:
            print(f"Command '{command}' not recognized.")
