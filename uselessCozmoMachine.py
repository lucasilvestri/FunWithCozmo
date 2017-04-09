'''
This is a mini game for Cozmo. Start Cozmo with a view of the 3 cubes. When it says 'My favourite color is green' you
can tap a cube and see it goes to revert it to green. Like an useless machine.
'''

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps

import time, random

id_cube = 0


def tap_handler(evt, obj=None, tap_count=None, **kwargs):
    cube_tapped = evt.obj
    cube_tapped.set_lights(cozmo.lights.Light(on_color=cozmo.lights.Color(
        rgb=(round(random.random() * 255), round(random.random() * 100), round(random.random() * 255)))))
    # print(cube, tap_count)
    print("Tapped: ", cube_tapped.object_id)
    global id_cube
    id_cube = cube_tapped.object_id


def cozmo_program(robot: cozmo.robot.Robot):
    print("--------------------------")
    print("Battery (below 3.5V is low)")
    print(robot.world.robot.battery_voltage)
    print("--------------------------")
    new_color = cozmo.lights.Color(rgb=(0, 255, 0))
    green = cozmo.lights.Light(on_color=new_color)

    cubes = [robot.world.light_cubes.get(cozmo.objects.LightCube1Id),
             robot.world.light_cubes.get(cozmo.objects.LightCube2Id),
             robot.world.light_cubes.get(cozmo.objects.LightCube3Id)]
    for cube in cubes:
        cube.set_lights(green)
    time.sleep(1)
    robot.world.add_event_handler(cozmo.objects.EvtObjectTapped, tap_handler)

    if robot.is_on_charger:
        robot.drive_off_charger_contacts().wait_for_completed()
        robot.drive_straight(distance_mm(100), speed_mmps(50)).wait_for_completed()
    robot.say_text("Where are my cubes?").wait_for_completed()
    look = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    cube_vision = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=30,
                                                             include_existing=True)
    look.stop()
    print("Cubes found")
    robot.say_text("My favourite color is green!").wait_for_completed()
    global id_cube
    while True:
        time.sleep(1)
        if id_cube:
            robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseSession).wait_for_completed()
            print("Going to cube ", id_cube)
            for mycube in cube_vision:
                if mycube.object_id == id_cube:
                    robot.go_to_object(mycube, distance_mm(60)).wait_for_completed()
                    robot.play_anim(name="ID_pokedB").wait_for_completed()
                    mycube.set_lights(green)
            id_cube = None


cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
