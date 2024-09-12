import appdaemon.plugins.hass.hassapi as hass # type: ignore
import globals
import time

class Alarm(hass.Hass):

    def initialize(self):
        self.run_daily(self.alarm_chuck, self.get_state(self.args["chuck"]["time"]))
        self.run_daily(self.alarm_ethan, self.get_state(self.args["ethan"]["time"]))

    def alarm_chuck(self, kwargs):
        if not globals.enabled(self.get_state(self.args["chuck"]["enabled"])):
            return
        for action in self.args["chuck"]["sequence"]:
            self.turn_on(action)
        self.call_service(
            self.args["chuck"]["media"]["volume_set"],
            entity_id=self.args["chuck"]["media"]["player"],
            volum_level=self.args["chuck"]["media"]["volume"]
        )
        self.call_service(
            self.args["chuck"]["media"]["play_media"],
            entity_id=self.args["chuck"]["media"]["player"],
            media_content_id=self.args["chuck"]["media"]["content_id"],
            media_content_type=self.args["chuck"]["media"]["content_type"]
        )
        volume_level = self.args["chuck"]["media"]["volume"] + 0.05
        for i in range(1, 10):
            time.sleep(10)
            self.log(volume_level)
            self.call_service(
                self.args["chuck"]["media"]["volume_set"],
                entity_id=self.args["chuck"]["media"]["player"],
                volume_level=volume_level
            )
            volume_level = volume_level + 0.05

    def alarm_ethan(self, kwargs):
        if not globals.enabled(self.get_state(self.args["ethan"]["enabled"])):
            return
        self.turn_on(entity for entity in self.args["ethan"]["on"])
