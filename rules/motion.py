from idiotic.rule import bind, Command, Change, Schedule, augment, Delay, DeDup
from idiotic.declare import Rule, StateIsCondition, StateBetweenCondition, ItemLambdaCondition, CommandReceivedCondition, CommandAction, SceneAction, SceneCondition, StateAction
from idiotic.scene import Scene
from idiotic.timer import Timer
from idiotic.modutils import require_rules
from idiotic import instance as c
import functools

require_rules('weather')

Scene("Entertainment Room Sleep")
Scene("Living Room Sleep")
Scene("Music Room Sleep")
Scene("Bedroom Sleep")
Scene("Office Sleep")

Scene("Living Room Media")

Scene("Kitchen Occupied")
Scene("Living Room Occupied")
Scene("Entertainment Room Occupied")
Scene("Laundry Room Occupied")
Scene("Bathroom Occupied")
Scene("Music Room Occupied")
Scene("Bedroom Occupied")
Scene("Office Occupied")

# When any of:
#   - Kitchen door was opened within one minute
#   - Kitchen motion sensor was activated within 1 minute
# Do:
#   Enter scene KitchenOccupied
Rule(CommandReceivedCondition(c.items.kitchen_motion, 600, 'on') |
     CommandReceivedCondition(c.items.kitchen_door, 60, 'on'),
     SceneAction(c.scenes.kitchen_occupied))

# When the living room motion sensor was activated within 15 minutes:
# Enter scene LivingRoomOccupied
Rule(CommandReceivedCondition(c.items.living_room_motion, 900, 'on'),
     SceneAction(c.scenes.living_room_occupied))

# When any of:
#   - Entertainment room / laundry room door was opened within 10 seconds
#   - Entertainment room motion sensor was activated within 3 minutes
# Do:
#   Enter scene EntertainmentRoomOcupied
Rule(CommandReceivedCondition(c.items.living_room_motion, 180, 'on'),
# NYI
#     StateIsCondition(c.items.entertainment_room_laundry_room_door, False, since=180),
     SceneAction(c.scenes.entertainment_room_occupied))

# Enter LaundryRoomOccupied on motion or door change
Rule(CommandReceivedCondition(c.items.laundry_room_motion, 180, 'on'),
# NYI
#     StateIsCondition(c.items.entertainment_room_laundry_room_door, False, since=180) |
#     StateIsCondition(c.items.laundry_room_door, False, since=180),
     SceneAction(c.scenes.laundry_room_occupied))

# Enter BathroomOccupied when the door is closed
Rule(StateIsCondition(c.items.bathroom_door, True, since=6),
     SceneAction(c.scenes.bathroom_occupied))

# Enter LivingRoomMedia when the projector is on
Rule(StateIsCondition(c.items.living_room_projector, True),
     SceneAction(c.scenes.living_room_media))

# Turn on the kitchen light when it's occupied and not daylight
Rule(SceneCondition(c.scenes.kitchen_occupied) &
     ~SceneCondition(c.scenes.daylight),
     [StateAction(c.items.kitchen_light, True, False),
      StateAction(c.items.kitchen_counter_light, True, False)])

# When:
#  - The living room or kitchen is occuped
#  - It is not daylight
#  - We are not watching a movie
#  - We are not sleeping
# Do:
#   Turn on the kitchen table light
Rule(
    (
        SceneCondition(c.scenes.kitchen_occupied) |
        SceneCondition(c.scenes.living_room_occupied)
    ) &
     ~SceneCondition(c.scenes.daylight) &
     ~SceneCondition(c.scenes.living_room_media) &
     ~SceneCondition(c.scenes.living_room_sleep),
     StateAction(c.items.kitchen_table_light, True, False))

# When:
#  - The living romo is occupied
#  - It is not daylight
#  - We are not sleeping
#  - We are not watching a movie
# Do:
#   Turn on the living room lamp
Rule(SceneCondition(c.scenes.living_room_occupied) &
     ~SceneCondition(c.scenes.daylight) &
     ~SceneCondition(c.scenes.living_room_sleep) &
     ~SceneCondition(c.scenes.living_room_media),
     StateAction(c.items.living_room_lamp, True, False))

# Turn on bathroom light when bathroom occupied is active
Rule(SceneCondition(c.scenes.bathroom_occupied),
     StateAction(c.items.bathroom_light, True, False))

# When:
#  - The entertainment room is occupied
#  - We are not sleeping
#  - It is not daylight
Rule(SceneCondition(c.scenes.entertainment_room_occupied) &
     ~SceneCondition(c.scenes.entertainment_room_sleep) &
     ~SceneCondition(c.scenes.daylight),
     StateAction(c.items.entertainment_room_light))

# When the laundry room is occupied,
# turn on the light
Rule(SceneCondition(c.scenes.laundry_room_occupied),
     StateAction(c.items.laundry_room_light))
