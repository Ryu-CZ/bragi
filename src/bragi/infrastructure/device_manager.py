# infrastructure/device_manager.py

import pulsectl


class VirtualMicrophone:
    """
    Usage example:
    ```
    with VirtualMicrophone("VirtualMic") as virtual_mic:
        print(virtual_mic.sink_name)
    ```
    """
    def __init__(self, sink_name="VirtualMic"):
        self.sink_name = sink_name
        self.module_index = None
        self.pulse = pulsectl.Pulse("virtual-mic-manager")
        self.create_virtual_mic()

    def create_virtual_mic(self):
        module_args = f"sink_name={self.sink_name} sink_properties=device.description={self.sink_name}"
        self.module_index = self.pulse.module_load("module-null-sink", module_args)
        print(
            f'Created virtual sink "{self.sink_name}" with module index {self.module_index}'
        )

    def unload_virtual_mic(self):
        if self.module_index is not None:
            self.pulse.module_unload(self.module_index)
            print(f"Unloaded virtual sink with module index {self.module_index}")
            self.module_index = None

    def __del__(self):
        self.unload_virtual_mic()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.unload_virtual_mic()

    def __str__(self):
        return f"VirtualMicrophone({self.sink_name})"

    def __repr__(self):
        return str(self)