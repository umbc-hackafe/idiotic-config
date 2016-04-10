from idiotic.declare import Rule, StateIsCondition, StateBetweenCondition, ItemLambdaCondition, CommandReceivedCondition, CommandAction, SceneAction, SceneCondition, StateAction
from idiotic.scene import Scene
from idiotic.timer import Timer
from idiotic.modutils import require_rules, require_items
from idiotic import instance as c
import functools

require_rules("climate")
require_rules("daytime")

Scene("Sleep")

Scene("Theater")

Scene("Kitchen Occupied")
Scene("Living Room Occupied")
Scene("Bedroom Occupied")
Scene("Office Occupied")

# When any of:
#   - Kitchen door was opened within 1 minute
#   - Kitchen motion sensor was activated within 1 minute
# Do:
#   Enter scene KitchenOccupied
Rule(CommandReceivedCondition(c.items.kitchen_motion, 60, 'trigger') |
     CommandReceivedCondition(c.items.kitchen_door, 60, 'on'),
     SceneAction(c.scenes.kitchen_occupied))

# When the living room motion sensor was activated within 1 minute:
# Enter scene LivingRoomOccupied
Rule(CommandReceivedCondition(c.items.living_room_motion, 60, 'trigger'),
     SceneAction(c.scenes.living_room_occupied))

# When the bedroom motion sensor was activated within 1 minute:
# Enter scene BedroomOccupied
Rule(CommandReceivedCondition(c.items.bedroom_motion, 60, 'trigger'),
     SceneAction(c.scenes.bedroom_occupied))

# When the office motion sensor was activated within 1 minute:
# Enter scene OfficeOccupied
Rule(CommandReceivedCondition(c.items.office_motion, 60, 'trigger'),
     SceneAction(c.scenes.office_occupied))

# Turn on the kitchen light when it's occupied and not daytime
Rule(SceneCondition(c.scenes.kitchen_occupied) &
     ~SceneCondition(c.scenes.daytime),
     StateAction(c.items.kitchen_light, True, False))

# When:
#  - The living room is occuped
#  - It is not daytime
#  - We are not watching a movie
# Do:
#   Turn on the living room light
Rule(
    SceneCondition(c.scenes.living_room_occupied) &
     ~SceneCondition(c.scenes.daytime) &
     ~SceneCondition(c.scenes.theater),
     StateAction(c.items.living_room_light, True, False))

# When:
#  - The kitchen is occupied
#  - It is not daytime
# Do:
#   Turn on the kitchen light
Rule(SceneCondition(c.scenes.kitchen_occupied) &
     ~SceneCondition(c.scenes.daytime),
     StateAction(c.items.kitchen_light, True, False))

# When:
#  - The bedroom room is occupied
#  - We are not sleeping
#  - It is not daytime
Rule(SceneCondition(c.scenes.bedroom_occupied) &
     ~SceneCondition(c.scenes.sleep) &
     ~SceneCondition(c.scenes.daytime),
     StateAction(c.items.bedroom_light, True, False))

# When:
#  - The office is occupied
#  - It is not daytime
# When the laundry room is occupied,
# turn on the light
Rule(SceneCondition(c.scenes.office_occupied) &
     ~SceneCondition(c.scenes.daytime),
     StateAction(c.items.office_light, True, False))
