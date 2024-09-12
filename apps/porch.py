import appdaemon.plugins.hass.hassapi as hass # type: ignore

class Porch(hass.Hass):

    def initialize(self):
        self.run_at_sunrise(self.sunrise)
        self.run_at_sunset(self.sunset)

    def sunrise(self, kwargs):        
        self.turn_off("light.porch")
        
    def sunset(self, kwargs):
        self.turn_on("light.porch")
