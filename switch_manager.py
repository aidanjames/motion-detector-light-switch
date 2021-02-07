from tplinkcloud import TPLinkDeviceManager
import os


class SwitchManager:

    def __init__(self):
        self.username = os.getenv("MY_EMAIL")
        self.password = os.getenv("PASSWORD")
        self.device_manager = TPLinkDeviceManager(self.username, self.password)

    def find_devices(self):
        return self.device_manager.get_devices()

    def toggle_switch(self, device_name):
        device = self.device_manager.find_device(device_name)
        if device:
            print(f'Found {device.model_type.name} device: {device.get_alias()}')
            device.toggle()
        else:
            print(f'Could not find {device_name}')

    def switch_on(self, device_name):
        device = self.device_manager.find_device(device_name)
        if device:
            if device.is_off():
                device.toggle()
            else:
                print(f"Device {device_name} is already on.")
        else:
            print(f'Could not find {device_name}')

    def switch_off(self, device_name):
        device = self.device_manager.find_device(device_name)
        if device:
            if device.is_on():
                device.toggle()
            else:
                print(f"Device {device_name} is already off.")
        else:
            print(f'Could not find {device_name}')