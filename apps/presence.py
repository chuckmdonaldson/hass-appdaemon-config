import appdaemon.plugins.hass.hassapi as hass # type: ignore
import globals

class Presence(hass.Hass):

    def initialize(self):
        self.listen_event(self.record_event, globals.EVENTS)
        self.listen_state(self.presence_change, self.args["people"], new = "home", old = "not_home")
        self.listen_state(self.presence_change, self.args["people"], new = "not_home", old = "home")

    def record_event(self, event_name, data, cb_args):
        if data["mac_address"] in globals.UNKNOWN:
            msg = f"{event_name}, {data['hostname']}, {data['ip_address']}, {data['mac_address']}, {data['connection']}, {data['band']}"
            self.log(msg)
            self.notify(msg, name="mobile_app_chuck_iphone")

    def presence_change(self, entity, attribute, old, new, kwargs):
        match entity:
            case "person.chuck":
                self.notify(f"Chuck is {new}", name="mobile_app_chuck_iphone")
            case "person.ethan":    
                self.notify(f"Ethan is {new}", name="mobile_app_chuck_iphone")
            case "person.maddie":
                self.notify(f"Maddie is {new}", name="mobile_app_chuck_iphone")
            case "person.morgan":
                self.notify(f"Morgan is {new}", name="mobile_app_chuck_iphone")
            case "person.taylor":
                self.notify(f"Taylor is {new}", name="mobile_app_chuck_iphone")
