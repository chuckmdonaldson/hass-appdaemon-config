import appdaemon.plugins.hass.hassapi as hass # type: ignore

class LightEffect(hass.Hass):

    def initialize(self):
        self.listen_state(self.light_effect, "input_select.light_effect")

    def light_effect(self, entity, attribute, old, new, kwargs):
        self.log(f"Light Effect: {new}")
        match new:
            case "blink":
                self.turn_on("light.chuck_bedroom_group", effect="blink")
            case "breathe":
                self.turn_on("light.chuck_bedroom_group", effect="breathe")
            case "candle":
                self.turn_on("light.chuck_bedroom_group", effect="candle")
            case "colorloop":
                self.turn_on("light.chuck_bedroom_group", effect="colorloop")
            case "fireplace":
                self.turn_on("light.chuck_bedroom_group", effect="fireplace")
            case "okay":
                self.turn_on("light.chuck_bedroom_group", effect="okay")
            case "finish_effect" | "stop_effect" | "stop_hue_effect":
                self.turn_on("scene.chuck_bedroom_day") if self.sun_up() else self.turn_on("scene.chuck_bedroom_night")
