# Part of the ROBOID project - https://roboticsware.uz
# Copyright (C) 2022 RoboticsWare (neopia.uz@gmail.com)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

import time
import threading

from neobot.runner import Runner
from neobot.util import Util
from neobot.model import DeviceType
from neobot.model import DataType
from neobot.model import Neobot
from neobot.connector import Result
from neobot.neosoco import Neosoco
from neobot.serial_connector import SerialConnector
from neobot.linker import Linker


class NeosocoConnectionChecker(object):
    def __init__(self, neobot):
        self._roboid = neobot

    def check(self, info):
        if info[1] == "Neosoco" and info[2] == "04":
            self._roboid._set_model_code(0x04)
            return True
        elif info[2] == "0E":
            self._roboid._set_model_code(0x0E)
            return True
        else:
            return False


class NeosocoNeobot(Neobot):
    _COLOR_TO_RGB = {
        0: (0, 0, 0),
        1: (0, 0, 255),
        2: (0, 255, 0),
        3: (0, 255, 255),
        4: (255, 0, 0),
        5: (255, 0, 255),
        6: (255, 255, 0),
        7: (255, 255, 255)
    }
    _SPEED_TO_GAIN = {
        1: 6,
        2: 6,
        3: 5,
        4: 5,
        5: 4,
        6: 4,
        7: 3,
        8: 3,
        9: 2,
        10: 2
    }

    def __init__(self, index):
        super(NeosocoNeobot, self).__init__(Neosoco.ID, "Neosoco", 0x00400000)
        self._index = index
        self._connector = None
        self._ready = False
        self._thread = None
        self._thread_lock = threading.Lock()

        self._left_wheel = 0
        self._right_wheel = 0
        self._buzzer = 0
        self._output_a = 0
        self._output_b = 0
        self._topology = 0
        self._left_led = 0
        self._right_led = 0
        self._note = 0
        self._line_tracer_mode = 0
        self._line_tracer_speed = 5
        self._io_mode_a = 0
        self._io_mode_b = 0
        self._config_proximity = 2
        self._config_gravity = 0
        self._config_band_width = 3

        self._topology_written = False
        self._left_led_written = False
        self._right_led_written = False
        self._note_written = False
        self._line_tracer_mode_written = False
        self._line_tracer_speed_written = False
        self._io_mode_a_written = False
        self._io_mode_b_written = False
        self._config_proximity_written = False
        self._config_gravity_written = False
        self._config_band_width_written = False

        self._light = 0
        self._temperature = 0
        
        self._line_tracer_flag = 0
        self._line_tracer_event = 0
        self._line_tracer_state = 0
        self._line_tracer_count = 0
        
        self._event_tilt = -4
        self._event_battery_state = -1
        
        self._create_model()

    def _set_model_code(self, code):
        self._model_code = code

    def _create_model(self):
        from neobot.neosoco import Neosoco
        dict = self._device_dict = {}
        dict[Neosoco.LEFT_WHEEL] = self._left_wheel_device = self._add_device(Neosoco.LEFT_WHEEL, "LeftWheel", DeviceType.EFFECTOR, DataType.INTEGER, 1, -100, 100, 0)
        dict[Neosoco.RIGHT_WHEEL] = self._right_wheel_device = self._add_device(Neosoco.RIGHT_WHEEL, "RightWheel", DeviceType.EFFECTOR, DataType.INTEGER, 1, -100, 100, 0)
        dict[Neosoco.BUZZER] = self._buzzer_device = self._add_device(Neosoco.BUZZER, "Buzzer", DeviceType.EFFECTOR, DataType.FLOAT, 1, 0, 167772.15, 0.0)
        dict[Neosoco.OUTPUT_A] = self._output_a_device = self._add_device(Neosoco.OUTPUT_A, "OutputA", DeviceType.EFFECTOR, DataType.INTEGER, 1, 0, 255, 0)
        dict[Neosoco.OUTPUT_B] = self._output_b_device = self._add_device(Neosoco.OUTPUT_B, "OutputB", DeviceType.EFFECTOR, DataType.INTEGER, 1, 0, 255, 0)
        dict[Neosoco.TOPOLOGY] = self._topology_device = self._add_device(Neosoco.TOPOLOGY, "Topology", DeviceType.COMMAND, DataType.INTEGER, 1, 0, 15, 0)
        dict[Neosoco.LEFT_LED] = self._left_led_device = self._add_device(Neosoco.LEFT_LED, "LeftLed", DeviceType.COMMAND, DataType.INTEGER, 1, 0, 7, 0)
        dict[Neosoco.RIGHT_LED] = self._right_led_device = self._add_device(Neosoco.RIGHT_LED, "RightLed", DeviceType.COMMAND, DataType.INTEGER, 1, 0, 7, 0)
        dict[Neosoco.NOTE] = self._note_device = self._add_device(Neosoco.NOTE, "Note", DeviceType.COMMAND, DataType.INTEGER, 1, 0, 88, 0)
        dict[Neosoco.LINE_TRACER_MODE] = self._line_tracer_mode_device = self._add_device(Neosoco.LINE_TRACER_MODE, "LineTracerMode", DeviceType.COMMAND, DataType.INTEGER, 1, 0, 15, 0)
        dict[Neosoco.LINE_TRACER_SPEED] = self._line_tracer_speed_device = self._add_device(Neosoco.LINE_TRACER_SPEED, "LineTracerSpeed", DeviceType.COMMAND, DataType.INTEGER, 1, 1, 8, 5)
        dict[Neosoco.IO_MODE_A] = self._io_mode_a_device = self._add_device(Neosoco.IO_MODE_A, "IoModeA", DeviceType.COMMAND, DataType.INTEGER, 1, 0, 15, 0)
        dict[Neosoco.IO_MODE_B] = self._io_mode_b_device = self._add_device(Neosoco.IO_MODE_B, "IoModeB", DeviceType.COMMAND, DataType.INTEGER, 1, 0, 15, 0)
        dict[Neosoco.CONFIG_PROXIMITY] = self._config_proximity_device = self._add_device(Neosoco.CONFIG_PROXIMITY, "ConfigProximity", DeviceType.COMMAND, DataType.INTEGER, 1, 1, 7, 2)
        dict[Neosoco.CONFIG_GRAVITY] = self._config_gravity_device = self._add_device(Neosoco.CONFIG_GRAVITY, "ConfigGravity", DeviceType.COMMAND, DataType.INTEGER, 1, 0, 3, 0)
        dict[Neosoco.CONFIG_BAND_WIDTH] = self._config_band_width_device = self._add_device(Neosoco.CONFIG_BAND_WIDTH, "ConfigBandWidth", DeviceType.COMMAND, DataType.INTEGER, 1, 1, 8, 3)
        dict[Neosoco.SIGNAL_STRENGTH] = self._signal_strength_device = self._add_device(Neosoco.SIGNAL_STRENGTH, "SignalStrength", DeviceType.SENSOR, DataType.INTEGER, 1, -128, 0, 0)
        dict[Neosoco.LEFT_PROXIMITY] = self._left_proximity_device = self._add_device(Neosoco.LEFT_PROXIMITY, "LeftProximity", DeviceType.SENSOR, DataType.INTEGER, 1, 0, 255, 0)
        dict[Neosoco.RIGHT_PROXIMITY] = self._right_proximity_device = self._add_device(Neosoco.RIGHT_PROXIMITY, "RightProximity", DeviceType.SENSOR, DataType.INTEGER, 1, 0, 255, 0)
        dict[Neosoco.LEFT_FLOOR] = self._left_floor_device = self._add_device(Neosoco.LEFT_FLOOR, "LeftFloor", DeviceType.SENSOR, DataType.INTEGER, 1, 0, 255, 0)
        dict[Neosoco.RIGHT_FLOOR] = self._right_floor_device = self._add_device(Neosoco.RIGHT_FLOOR, "RightFloor", DeviceType.SENSOR, DataType.INTEGER, 1, 0, 255, 0)
        dict[Neosoco.ACCELERATION] = self._acceleration_device = self._add_device(Neosoco.ACCELERATION, "Acceleration", DeviceType.SENSOR, DataType.INTEGER, 3, -32768, 32767, 0)
        dict[Neosoco.LIGHT] = self._light_device = self._add_device(Neosoco.LIGHT, "Light", DeviceType.SENSOR, DataType.INTEGER, 1, 0, 65535, 0)
        dict[Neosoco.TEMPERATURE] = self._temperature_device = self._add_device(Neosoco.TEMPERATURE, "Temperature", DeviceType.SENSOR, DataType.INTEGER, 1, -40, 88, 0)
        dict[Neosoco.INPUT_A] = self._input_a_device = self._add_device(Neosoco.INPUT_A, "InputA", DeviceType.SENSOR, DataType.INTEGER, 1, 0, 255, 0)
        dict[Neosoco.INPUT_B] = self._input_b_device = self._add_device(Neosoco.INPUT_B, "InputB", DeviceType.SENSOR, DataType.INTEGER, 1, 0, 255, 0)
        dict[Neosoco.LINE_TRACER_STATE] = self._line_tracer_state_device = self._add_device(Neosoco.LINE_TRACER_STATE, "LineTracerState", DeviceType.EVENT, DataType.INTEGER, 1, 0, 255, 0)
        dict[Neosoco.TILT] = self._tilt_device = self._add_device(Neosoco.TILT, "Tilt", DeviceType.EVENT, DataType.INTEGER, 1, -3, 3, 0)
        dict[Neosoco.BATTERY_STATE] = self._battery_state_device = self._add_device(Neosoco.BATTERY_STATE, "BatteryState", DeviceType.EVENT, DataType.INTEGER, 1, 0, 2, 2)

    def find_device_by_id(self, device_id):
        return self._device_dict.get(device_id)

    def _run(self):
        try:
            while self._running or self._releasing:
                if self._receive(self._connector):
                    self._send(self._connector)
                    self._releasing = False
                time.sleep(0.01)
        except:
            pass

    def _init(self, port_name=None):
        Runner.register_required()
        self._running = True
        thread = threading.Thread(target=self._run)
        self._thread = thread
        thread.daemon = True
        thread.start()

        tag = "Neosoco[{}]".format(self._index)
        self._connector = SerialConnector(tag, NeosocoConnectionChecker(self))
        result = self._connector.open(port_name)
        if result == Result.FOUND:
            while self._ready == False and self._is_disposed() == False:
                time.sleep(0.01)
        elif result == Result.NOT_AVAILABLE:
            Runner.register_checked()

    def _release(self):
        self._releasing = True
        self._running = False
        thread = self._thread
        self._thread = None
        if thread:
            thread.join()

        connector = self._connector
        self._connector = None
        if connector:
            connector.close()

    def _dispose(self):
        if self._is_disposed() == False:
            super(NeosocoNeobot, self)._dispose()
            self._release()

    def _reset(self):
        super(NeosocoNeobot, self)._reset()

        self._left_wheel = 0
        self._right_wheel = 0
        self._buzzer = 0
        self._output_a = 0
        self._output_b = 0
        self._topology = 0
        self._left_led = 0
        self._right_led = 0
        self._note = 0
        self._line_tracer_mode = 0
        self._line_tracer_speed = 5
        self._io_mode_a = 0
        self._io_mode_b = 0
        self._config_proximity = 2
        self._config_gravity = 0
        self._config_band_width = 3

        self._topology_written = False
        self._left_led_written = False
        self._right_led_written = False
        self._note_written = False
        self._line_tracer_mode_written = False
        self._line_tracer_speed_written = False
        self._io_mode_a_written = False
        self._io_mode_b_written = False
        self._config_proximity_written = False
        self._config_gravity_written = False
        self._config_band_width_written = False

        self._light = 0
        self._temperature = 0
        
        self._line_tracer_event = 0
        self._line_tracer_state = 0
        self._line_tracer_count = 0
        
        self._event_tilt = -4
        self._event_battery_state = -1

    def _request_motoring_data(self):
        with self._thread_lock:
            self._left_wheel = self._left_wheel_device.read()
            self._right_wheel = self._right_wheel_device.read()
            self._buzzer = self._buzzer_device.read()
            self._output_a = self._output_a_device.read()
            self._output_b = self._output_b_device.read()
            if self._topology_device._is_written():
                self._topology = self._topology_device.read()
                self._topology_written = True
            if self._left_led_device._is_written():
                self._left_led = self._left_led_device.read()
                self._left_led_written = True
            if self._right_led_device._is_written():
                self._right_led = self._right_led_device.read()
                self._right_led_written = True
            if self._note_device._is_written():
                self._note = self._note_device.read()
                self._note_written = True
            if self._line_tracer_mode_device._is_written():
                self._line_tracer_mode = self._line_tracer_mode_device.read()
                self._line_tracer_mode_written = True
            if self._line_tracer_speed_device._is_written():
                self._line_tracer_speed = self._line_tracer_speed_device.read()
                self._line_tracer_speed_written = True
            if self._io_mode_a_device._is_written():
                self._io_mode_a = self._io_mode_a_device.read()
                self._io_mode_a_written = True
            if self._io_mode_b_device._is_written():
                self._io_mode_b = self._io_mode_b_device.read()
                self._io_mode_b_written = True
            if self._config_proximity_device._is_written():
                self._config_proximity = self._config_proximity_device.read()
                self._config_proximity_written = True
            if self._config_gravity_device._is_written():
                self._config_gravity = self._config_gravity_device.read()
                self._config_gravity_written = True
            if self._config_band_width_device._is_written():
                self._config_band_width = self._config_band_width_device.read()
                self._config_band_width_written = True
        self._clear_written()

    def _color_to_rgb(self, color):
        if isinstance(color, (int, float)):
            color = int(color)
            if color > 7: color = 7
            elif color < 0: color = 0
            return NeosocoNeobot._COLOR_TO_RGB[color]
        return NeosocoNeobot._COLOR_TO_RGB[0]

    def _speed_to_gain(self, speed):
        if isinstance(speed, (int, float)):
            speed = int(speed)
            if speed > 10: speed = 10
            elif speed < 1: speed = 1
            return NeosocoNeobot._SPEED_TO_GAIN[speed]
        return 2

    def _encode_motoring_packet(self, address):
        result = ""
        with self._thread_lock:
            if self._model_code == 0x0E:
                result += "10"
                result += self._to_hex(self._left_wheel)
                result += self._to_hex(self._right_wheel)
                rgb = self._color_to_rgb(self._left_led)
                result += self._to_hex(rgb[0])
                result += self._to_hex(rgb[1])
                result += self._to_hex(rgb[2])
                rgb = self._color_to_rgb(self._right_led)
                result += self._to_hex(rgb[0])
                result += self._to_hex(rgb[1])
                result += self._to_hex(rgb[2])
                result += "000000"
                temp = self._line_tracer_mode & 0x0f
                if temp > 7: temp += 1
                if self._line_tracer_mode_written:
                    self._line_tracer_count = 0
                    if temp > 0:
                        self._line_tracer_flag = (self._line_tracer_flag % 15) + 1
                        self._line_tracer_event = 1
                    else:
                        self._line_tracer_event = 0
                    self._line_tracer_mode_written = False
                temp |= (self._line_tracer_flag & 0x0f) << 4
                result += self._to_hex(temp)
                temp = (self._line_tracer_speed & 0x0f) << 4
                temp |= self._speed_to_gain(self._line_tracer_speed) & 0x0f
                result += self._to_hex(temp)
                temp = (self._config_proximity & 0x07) << 5
                temp |= (self._config_band_width & 0x07) << 2
                temp |= self._config_gravity & 0x03
                result += self._to_hex(temp)
                temp = (self._io_mode_a & 0x0f) << 4
                temp |= self._io_mode_b & 0x0f
                result += self._to_hex(temp)
                result += self._to_hex(self._output_a)
                result += self._to_hex(self._output_b)
                if self._note > 0:
                    result += "01"
                    result += self._to_hex(self._note)
                else:
                    temp = self._buzzer
                    if temp > 6500: temp = 6500
                    result += self._to_hex2(Util.round(temp * 10) + 512)
            else:
                result += self._to_hex(self._topology & 0x0f)
                result += "0010"
                result += self._to_hex(self._left_wheel)
                result += self._to_hex(self._right_wheel)
                result += self._to_hex(self._left_led)
                result += self._to_hex(self._right_led)
                result += self._to_hex3(Util.round(self._buzzer * 100))
                result += self._to_hex(self._note)
                if self._line_tracer_mode_written:
                    if self._line_tracer_mode > 0:
                        self._line_tracer_flag ^= 0x80
                        self._line_tracer_event = 1
                    self._line_tracer_mode_written = False
                temp = (self._line_tracer_mode & 0x0f) << 3
                temp |= (self._line_tracer_speed - 1) & 0x07
                temp |= self._line_tracer_flag & 0x80
                result += self._to_hex(temp)
                result += self._to_hex(self._config_proximity)
                temp = (self._config_gravity & 0x0f) << 4
                temp |= self._config_band_width & 0x0f
                result += self._to_hex(temp)
                temp = (self._io_mode_a & 0x0f) << 4
                temp |= self._io_mode_b & 0x0f
                result += self._to_hex(temp)
                result += self._to_hex(self._output_a)
                result += self._to_hex(self._output_b)
                result += "000000"
        result += "-"
        result += address
        result += "\r"
        return result

    def _decode_sensory_packet(self, packet):
        packet = str(packet)
        if self._model_code == 0x0E:
            value = int(packet[0:1], 16)
            if value != 1: return False
            value = int(packet[6:8], 16)
            self._left_proximity_device._put(value)
            value = int(packet[8:10], 16)
            self._right_proximity_device._put(value)
            value2 = int(packet[38:40], 16)
            if (value2 & 0x01) == 0:
                self._light = int(packet[10:14], 16)
            else:
                value = int(packet[10:12], 16)
                if value > 0x7f: value -= 0x100
                self._temperature = Util.round(value / 2.0 + 23)
            self._light_device._put(self._light)
            self._temperature_device._put(self._temperature)
            value = int(packet[14:16], 16)
            self._left_floor_device._put(value)
            value = int(packet[16:18], 16)
            self._right_floor_device._put(value)
            acc_x = int(packet[18:22], 16)
            if acc_x > 0x7fff: acc_x -= 0x10000
            self._acceleration_device._put_at(0, acc_x)
            acc_y = int(packet[22:26], 16)
            if acc_y > 0x7fff: acc_y -= 0x10000
            self._acceleration_device._put_at(1, acc_y)
            acc_z = int(packet[26:30], 16)
            if acc_z > 0x7fff: acc_z -= 0x10000
            self._acceleration_device._put_at(2, acc_z)
            if acc_z < 8192 and acc_x > 8192 and acc_y > -4096 and acc_y < 4096: value = 1
            elif acc_z < 8192 and acc_x < -8192 and acc_y > -4096 and acc_y < 4096: value = -1
            elif acc_z < 8192 and acc_y > 8192 and acc_x > -4096 and acc_x < 4096: value = 2
            elif acc_z < 8192 and acc_y < -8192 and acc_x > -4096 and acc_x < 4096: value = -2
            elif acc_z > 12288 and acc_x > -8192 and acc_x < 8192 and acc_y > -8192 and acc_y < 8192: value = 3
            elif acc_z < -12288 and acc_x > -4096 and acc_x < 4096 and acc_y > -4096 and acc_y < 4096: value = -3
            else: value = 0
            if value != self._event_tilt:
                self._tilt_device._put(value, self._event_tilt != -4)
                self._event_tilt = value
            value = int(packet[30:32], 16)
            self._input_a_device._put(value)
            value = int(packet[32:34], 16)
            self._input_b_device._put(value)
            value = int(packet[36:38], 16)
            value -= 0x100
            self._signal_strength_device._put(value)
            value = (value2 >> 6) & 0x03
            if (value & 0x02) != 0:
                if self._line_tracer_event == 1:
                    if value == 0x02:
                        self._line_tracer_count += 1
                        if self._line_tracer_count > 5: self._line_tracer_event = 2
                    else:
                        self._line_tracer_event = 2
                if self._line_tracer_event == 2:
                    if value != self._line_tracer_state or self._line_tracer_count > 5:
                        self._line_tracer_state = value
                        self._line_tracer_state_device._put(value << 5)
                        if value == 0x02:
                            self._line_tracer_event = 0
                            self._line_tracer_count = 0
            value = (value2 >> 1) & 0x03
            if value == 0: value = 2
            elif value >= 2: value = 0
            if value != self._event_battery_state:
                self._battery_state_device._put(value, self._event_battery_state != -1)
                self._event_battery_state = value
        else:
            value = int(packet[4:5], 16)
            if value != 1: return False
            value = int(packet[6:8], 16)
            value -= 0x100
            self._signal_strength_device._put(value)
            value = int(packet[8:10], 16)
            self._left_proximity_device._put(value)
            value = int(packet[10:12], 16)
            self._right_proximity_device._put(value)
            value = int(packet[12:14], 16)
            self._left_floor_device._put(value)
            value = int(packet[14:16], 16)
            self._right_floor_device._put(value)
            acc_x = int(packet[16:20], 16)
            if acc_x > 0x7fff: acc_x -= 0x10000
            self._acceleration_device._put_at(0, acc_x)
            acc_y = int(packet[20:24], 16)
            if acc_y > 0x7fff: acc_y -= 0x10000
            self._acceleration_device._put_at(1, acc_y)
            acc_z = int(packet[24:28], 16)
            if acc_z > 0x7fff: acc_z -= 0x10000
            self._acceleration_device._put_at(2, acc_z)
            if acc_z < 8192 and acc_x > 8192 and acc_y > -4096 and acc_y < 4096: value = 1
            elif acc_z < 8192 and acc_x < -8192 and acc_y > -4096 and acc_y < 4096: value = -1
            elif acc_z < 8192 and acc_y > 8192 and acc_x > -4096 and acc_x < 4096: value = 2
            elif acc_z < 8192 and acc_y < -8192 and acc_x > -4096 and acc_x < 4096: value = -2
            elif acc_z > 12288 and acc_x > -8192 and acc_x < 8192 and acc_y > -8192 and acc_y < 8192: value = 3
            elif acc_z < -12288 and acc_x > -4096 and acc_x < 4096 and acc_y > -4096 and acc_y < 4096: value = -3
            else: value = 0
            if value != self._event_tilt:
                self._tilt_device._put(value, self._event_tilt != -4)
                self._event_tilt = value
            value = int(packet[28:30], 16)
            if value == 0:
                self._light = int(packet[30:34], 16)
            else:
                value = int(packet[30:32], 16)
                if value > 0x7f: value -= 0x100
                self._temperature = Util.round(value / 2.0 + 24)
                value = (int(packet[32:34], 16) + 200) / 100.0
                if value < 3.6: value = 0
                elif value <= 3.7: value = 1
                else: value = 2
                if value != self._event_battery_state:
                    self._battery_state_device._put(value, self._event_battery_state != -1)
                    self._event_battery_state = value
            self._light_device._put(self._light)
            self._temperature_device._put(self._temperature)
            value = int(packet[34:36], 16)
            self._input_a_device._put(value)
            value = int(packet[36:38], 16)
            self._input_b_device._put(value)
            value = int(packet[38:40], 16)
            if (value & 0x40) != 0:
                if self._line_tracer_event == 1:
                    if value != 0x40:
                        self._line_tracer_event = 2
                if self._line_tracer_event == 2:
                    if value != self._line_tracer_state:
                        self._line_tracer_state = value
                        self._line_tracer_state_device._put(value)
                        if value == 0x40:
                            self._line_tracer_event = 0
        return True

    def _receive(self, connector):
        if connector:
            packet = connector.read()
            if packet:
                if self._decode_sensory_packet(packet):
                    if self._ready == False:
                        self._ready = True
                        Runner.register_checked()
                    self._notify_sensory_device_data_changed()
                return True
        return False

    def _send(self, connector):
        if connector:
            packet = self._encode_motoring_packet(connector.get_address())
            connector.write(packet)


class NeosocoLinkNeobot(NeosocoNeobot):
    def __init__(self, index):
        super(NeosocoLinkNeobot, self).__init__(index)
        self._is_hamster_s = False
        self._motoring = {
            'module': 'hamster',
            'index': index
        }
        self._clear_id_and_motoring()

    def _init(self, port_name=None):
        self._tag = "Neosoco[{}]".format(self._index)
        Linker.register_roboid('hamster', 'hamster', self._index, self._tag, self)
        while self._ready == False and self._is_disposed() == False:
            time.sleep(0.01)
        if self._is_hamster_s:
            self._config_band_width = 0
            self._motoring['configBandWidth'] = 0

    def _release(self):
        super(NeosocoLinkNeobot, self)._release()
        Linker.print_message(self._tag, 'Disposed')

    def _clear_id_and_motoring(self):
        self._topology_id = 0
        self._left_led_id = 0
        self._right_led_id = 0
        self._pulse_id = 0
        self._note_id = 0
        self._sound_id = 0
        self._line_tracer_mode_id = 0
        self._line_tracer_gain_id = 0
        self._line_tracer_speed_id = 0
        self._io_mode_a_id = 0
        self._io_mode_b_id = 0
        self._motion_id = 0
        self._motor_mode_id = 0
        self._config_proximity_id = 0
        self._config_gravity_id = 0
        self._config_band_width_id = 0
        self._line_tracer_state_id = -1
        self._tilt_id = -1
        self._battery_state_id = -1
        motoring = self._motoring
        motoring['leftWheel'] = self._left_wheel
        motoring['rightWheel'] = self._right_wheel
        motoring['buzzer'] = self._buzzer
        motoring['outputA'] = self._output_a
        motoring['outputB'] = self._output_b
        motoring['topologyId'] = 0
        motoring['topology'] = self._topology
        motoring['leftLedId'] = 0
        motoring['leftLed'] = self._left_led
        motoring['leftRed'] = 0
        motoring['leftGreen'] = 0
        motoring['leftBlue'] = 0
        motoring['rightLedId'] = 0
        motoring['rightLed'] = self._right_led
        motoring['rightRed'] = 0
        motoring['rightGreen'] = 0
        motoring['rightBlue'] = 0
        motoring['pulseId'] = 0
        motoring['pulse'] = 0
        motoring['noteId'] = 0
        motoring['note'] = self._note
        motoring['soundId'] = 0
        motoring['sound'] = 0
        motoring['lineTracerModeId'] = 0
        motoring['lineTracerMode'] = self._line_tracer_mode
        motoring['lineTracerGainId'] = 0
        motoring['lineTracerGain'] = 4
        motoring['lineTracerSpeedId'] = 0
        motoring['lineTracerSpeed'] = self._line_tracer_speed
        motoring['ioModeAId'] = 0
        motoring['ioModeA'] = self._io_mode_a
        motoring['ioModeBId'] = 0
        motoring['ioModeB'] = self._io_mode_b
        motoring['motorModeId'] = 0
        motoring['motorMode'] = 0
        motoring['configProximityId'] = 0
        motoring['configProximity'] = self._config_proximity
        motoring['configGravityId'] = 0
        motoring['configGravity'] = self._config_gravity
        motoring['configBandWidthId'] = 0
        motoring['configBandWidth'] = self._config_band_width

    def _reset(self):
        super(NeosocoLinkNeobot, self)._reset()
        self._clear_id_and_motoring()

    def get_motoring(self):
        return self._motoring

    def encode_motoring(self):
        with self._thread_lock:
            motoring = self._motoring
            motoring['leftWheel'] = self._left_wheel
            motoring['rightWheel'] = self._right_wheel
            motoring['buzzer'] = self._buzzer
            motoring['outputA'] = self._output_a
            motoring['outputB'] = self._output_b
            if self._note_written:
                self._note_written = False
                motoring['note'] = self._note
                self._note_id = (self._note_id % 255) + 1
                motoring['noteId'] = self._note_id
            if self._line_tracer_mode_written:
                self._line_tracer_mode_written = False
                motoring['lineTracerMode'] = self._line_tracer_mode
                self._line_tracer_mode_id = (self._line_tracer_mode_id % 255) + 1
                motoring['lineTracerModeId'] = self._line_tracer_mode_id
            if self._io_mode_a_written:
                self._io_mode_a_written = False
                motoring['ioModeA'] = self._io_mode_a
                self._io_mode_a_id = (self._io_mode_a_id % 255) + 1
                motoring['ioModeAId'] = self._io_mode_a_id
            if self._io_mode_b_written:
                self._io_mode_b_written = False
                motoring['ioModeB'] = self._io_mode_b
                self._io_mode_b_id = (self._io_mode_b_id % 255) + 1
                motoring['ioModeBId'] = self._io_mode_b_id
            if self._config_proximity_written:
                self._config_proximity_written = False
                motoring['configProximity'] = self._config_proximity
                self._config_proximity_id = (self._config_proximity_id % 255) + 1
                motoring['configProximityId'] = self._config_proximity_id
            if self._config_gravity_written:
                self._config_gravity_written = False
                motoring['configGravity'] = self._config_gravity
                self._config_gravity_id = (self._config_gravity_id % 255) + 1
                motoring['configGravityId'] = self._config_gravity_id
            if self._config_band_width_written:
                self._config_band_width_written = False
                motoring['configBandWidth'] = self._config_band_width
                self._config_band_width_id = (self._config_band_width_id % 255) + 1
                motoring['configBandWidthId'] = self._config_band_width_id
            if self._is_hamster_s:
                motoring['module'] = 'hamsterS'
                if self._left_led_written:
                    self._left_led_written = False
                    rgb = self._color_to_rgb(self._left_led)
                    motoring['leftRed'] = rgb[0]
                    motoring['leftGreen'] = rgb[1]
                    motoring['leftBlue'] = rgb[2]
                if self._right_led_written:
                    self._right_led_written = False
                    rgb = self._color_to_rgb(self._right_led)
                    motoring['rightRed'] = rgb[0]
                    motoring['rightGreen'] = rgb[1]
                    motoring['rightBlue'] = rgb[2]
                if self._line_tracer_speed_written:
                    self._line_tracer_speed_written = False
                    motoring['lineTracerSpeed'] = self._line_tracer_speed
                    self._line_tracer_speed_id = (self._line_tracer_speed_id % 255) + 1
                    motoring['lineTracerSpeedId'] = self._line_tracer_speed_id
                    motoring['lineTracerGain'] = self._speed_to_gain(self._line_tracer_speed)
                    self._line_tracer_gain_id = (self._line_tracer_gain_id % 255) + 1
                    motoring['lineTracerGainId'] = self._line_tracer_gain_id
                motoring['pulse'] = 0
                self._pulse_id = (self._pulse_id % 255) + 1
                motoring['pulseId'] = self._pulse_id
                motoring['sound'] = 0
                self._sound_id = (self._sound_id % 255) + 1
                motoring['soundId'] = self._sound_id
                motoring['motorMode'] = 0
                self._motor_mode_id = (self._motor_mode_id % 255) + 1
                motoring['motorModeId'] = self._motor_mode_id
            else:
                motoring['module'] = 'hamster'
                if self._topology_written:
                    self._topology_written = False
                    motoring['topology'] = self._topology
                    self._topology_id = (self._topology_id % 255) + 1
                    motoring['topologyId'] = self._topology_id
                if self._left_led_written:
                    self._left_led_written = False
                    motoring['leftLed'] = self._left_led
                    self._left_led_id = (self._left_led_id % 255) + 1
                    motoring['leftLedId'] = self._left_led_id
                if self._right_led_written:
                    self._right_led_written = False
                    motoring['rightLed'] = self._right_led
                    self._right_led_id = (self._right_led_id % 255) + 1
                    motoring['rightLedId'] = self._right_led_id
                if self._line_tracer_speed_written:
                    self._line_tracer_speed_written = False
                    motoring['lineTracerSpeed'] = self._line_tracer_speed
                    self._line_tracer_speed_id = (self._line_tracer_speed_id % 255) + 1
                    motoring['lineTracerSpeedId'] = self._line_tracer_speed_id

    def decode_sensory(self, received):
        self._is_hamster_s = received['module'] == 'hamsterS'
        self._ready = True
        self._signal_strength_device._put(received['signalStrength'])
        self._left_proximity_device._put(received['leftProximity'])
        self._right_proximity_device._put(received['rightProximity'])
        self._left_floor_device._put(received['leftFloor'])
        self._right_floor_device._put(received['rightFloor'])
        self._acceleration_device._put_at(0, received['accelerationX'])
        self._acceleration_device._put_at(1, received['accelerationY'])
        self._acceleration_device._put_at(2, received['accelerationZ'])
        self._light_device._put(received['light'])
        self._temperature_device._put(received['temperature'])
        self._input_a_device._put(received['inputA'])
        self._input_b_device._put(received['inputB'])
        t = received['lineTracerStateId']
        if t != self._line_tracer_state_id:
            if self._line_tracer_state_id != -1: self._line_tracer_state_device._put(received['lineTracerState'])
            self._line_tracer_state_id = t
        t = received['tiltId']
        if t != self._tilt_id:
            if self._tilt_id != -1: self._tilt_device._put(received['tilt'])
            self._tilt_id = t
        t = received['batteryStateId']
        if t != self._battery_state_id:
            if self._battery_state_id != -1: self._battery_state_device._put(received['batteryState'])
            self._battery_state_id = t