import appdaemon.plugins.hass.hassapi as hass # type: ignore
import globals

class Dimmer(hass.Hass):

    def initialize(self):
        self.listen_state(self.dimmer_action, self.args["dimmers"])

    def dimmer_action(self, entity, attribute, old, new, kwargs):        
        light, scene_day, scene_night = globals.get_dimmer(entity)
        lights = [ light, "light.chuck_closet", "light.chuck_shower" ] if light == "light.chuck_bathroom" else [ light ]
        scenes_day = [ scene_day, "scene.chuck_closet_day", "scene.chuck_shower_day" ] if light == "light.chuck_bathroom" else [ scene_day ] 
        scenes_night = [ scene_night, "scene.chuck_closet_night", "scene.chuck_shower_night" ] if light == "light.chuck_bathroom" else [ scene_night ] 

        if entity == "sensor.ethan_dimmer_action":
            match new:
                case "on_press" | "on-press":
                    self.turn_on("light.ethan_fan")
                case "up_press" | "up-press":
                    self.turn_on("light.ethan_fan", brightness_step_pct=10)
                case "down_press" | "down-press":
                    self.turn_on("light.ethan_fan", brightness_step_pct=-10)
                case "off_press" | "off-press":
                    for light in lights:
                        self.turn_off("light.ethan_fan")
        else:
            match new:
                case "on_press" | "on-press":
                    if self.sun_up():
                        for scene in scenes_day:
                            self.turn_on(scene)
                    else:
                        for scene in scenes_night:
                            self.turn_on(scene)
                case "up_press" | "up-press":
                    self.turn_on(light, brightness_step_pct=10)
                case "down_press" | "down-press":
                    self.turn_on(light, brightness_step_pct=-10)
                case "off_press" | "off-press":
                    for light in lights:
                        self.turn_off(light)
                case "on_hold" | "on-hold":
                    for scene in scenes_day:
                        self.turn_on(scene)
                case "up_hold" | "up-hold":
                    pass
                case "down_hold" | "down-hold":
                    pass
                case "off_hold" | "off-hold":
                    pass
