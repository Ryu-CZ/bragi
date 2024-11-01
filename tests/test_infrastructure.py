# tests/test_device_manager.py
import time
import unittest
from src.bragi.infrastructure.device_manager import VirtualMicrophone
import pulsectl


class TestVirtualMicrophone(unittest.TestCase):
    def setUp(self):
        self.sink_name = "TestVirtualMic"
        self.pulse = pulsectl.Pulse("virtual-mic-manager")

    def test_create_and_unload_virtual_mic(self):
        with VirtualMicrophone(self.sink_name) as virtual_mic:
            self.assertEqual(virtual_mic.sink_name, self.sink_name)
            self.assertIsNotNone(virtual_mic.module_index)
            # Check if the virtual sink is created
            sinks = self.pulse.sink_list()
            sink_names = [sink.name for sink in sinks]
            self.assertIn(self.sink_name, sink_names)

        # Check if the virtual sink is unloaded
        sinks = self.pulse.sink_list()
        sink_names = [sink.name for sink in sinks]
        self.assertNotIn(self.sink_name, sink_names)


if __name__ == "__main__":
    unittest.main()