from datetime import datetime
import appdaemon.plugins.hass.hassapi as hass # type: ignore
import globals

class Motion(hass.Hass):

    def initialize(self):
        self.listen_state(self.last_movement_detected, self.args["sensors"], new="on", old="off")
        self.listen_state(self.enable_motion, "input_boolean.enable_motion_detection", new="on", old="off", duration=900)
        self.listen_state(self.motion_detected, self.args["sensors"])

    def last_movement_detected(self, entity, attribute, old, new, kwargs):
        match entity:
            case "binary_sensor.chuck_bathroom_motion_occupancy":
                self.set_state("input_datetime.chuck_vanity_last_movement", state=datetime.strftime(datetime.now(), "%H:%M:%S"))
            case "binary_sensor.chuck_closet_motion_occupancy":
                self.set_state("input_datetime.chuck_closet_last_movement", state=datetime.strftime(datetime.now(), "%H:%M:%S"))
            case "binary_sensor.chuck_shower_motion_occupancy":
                self.set_state("input_datetime.chuck_shower_last_movement", state=datetime.strftime(datetime.now(), "%H:%M:%S"))

    def enable_motion(self, entity, attribute, old, new, kwargs):
        self.turn_on(entity)

    def motion_detected(self, entity, attribute, old, new, kwargs):
        if not globals.enabled(self.get_state("input_boolean.enable_motion_detection")):
            return
        try:
            light, scene_day, scene_night = globals.get_motion_sensor(entity)
        except ValueError as e:
            self.log(e)
            return        
        match new:
            case "on":
                self.turn_on(scene_day) if self.sun_up() else self.turn_on(scene_night)
            case "off":
                self.turn_off(light)
