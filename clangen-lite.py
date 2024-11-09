"""
Clangen in your terminal!
"""

from scripts.game_structure.load_cat import load_cats, version_convert
from scripts.game_structure.game_essentials import game
from scripts.clan import clan_class
from scripts.utility import quit  # pylint: disable=redefined-builtin

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
