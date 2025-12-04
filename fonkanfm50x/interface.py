import serial
import time

from .types import RFIDRegion, AvailableBaudRates

AFTER_SETTING_COMMAND_DELAY = 0.3 # Tested with default 38400 baud rate

class FonkanUHF:
	"""
	Fonkan FM50x UHF RFID Reader class.
	ISO18000-64 / EPCglobal UHF Class 1 Gen 2 standard compliant..
	"""

	def __init__(self, 
			  serial_port: str = '/dev/ttyACM0',
			  start_power: int = 25,
			  baud_rate: AvailableBaudRates = AvailableBaudRates.BAUD_38400,
			  region: RFIDRegion = RFIDRegion.EU):
		# WARNING: The RFID Module MUST be connected through the non power USB port
		self.serial_port = serial_port
		self.start_power = start_power
		self.baud_rate = baud_rate
		self.region = region
		self.ser: serial.Serial | None = None
		self.stall_time = 60
		self.last_tag = "initialise value"
		self.last_time = time.time() - self.stall_time

	def __enter__(self):
		# baud parameter is ignored for now to match request
		self.ser = serial.Serial(
			port=self.serial_port,
			baudrate=38400,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=1,
		)

		self.set_power_level(self.start_power)
		self.set_region(self.region)
		self.change_baud_rate(self.baud_rate)

		return self
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.ser and self.ser.is_open:
			try:
				self.ser.close()
			finally:
				self.ser = None
		return False

	####################################################################
	# Internal
	####################################################################

	def send_command(self, command: str):
		res = self.send_command_and_get_response(command)
		assert res is not None, f"No ACK for command {command}"
	
	def send_command_and_get_response(self, command: str) -> str | None:
		if not self.ser:
			raise RuntimeError("Serial port not initialized. Call begin() first.")
		print(f">: {command.encode()}")
		self.ser.write(f"\n{command}\r".encode())

		response = b''
		# Read until first LF
		while True:
			byte = self.ser.read(1)
			if not byte:
				break
			if byte == b'\n':  # LF
				break
		# Read until CR LF
		while True:
			byte = self.ser.read(1)
			if not byte:
				break
			response += byte
			if response.endswith(b'\r\n'):  # CR LF
				response = response[:-2]  # Strip the CR LF
				break

		decoded = response.decode('utf-8', errors='ignore')
		print(f"<: {decoded}")

		if decoded == 'X':
			raise RuntimeError(f"RFID Reader does not understand {command}")
		elif decoded == '':
			return None
		elif decoded[0] != command[0]:
			raise RuntimeError(f"RFID Reader returned unexpected response for {command}: {decoded}")

		return decoded[1:]

	####################################################################
	# Configuration
	####################################################################
    
	def get_region(self) -> RFIDRegion:
		res = self.send_command_and_get_response("N4,00")
		region_value = int(res)
		for region in RFIDRegion:
			if region.value == region_value:
				return region
		raise ValueError(f"Unknown region value: {region_value}")

	def set_region(self, region: RFIDRegion):
		# Set region
		self.send_command(f"N5,0{region.value}")
		
		# This command requires a rate-limit after running to prevent the device from locking
		time.sleep(AFTER_SETTING_COMMAND_DELAY)
	
	def get_power_level(self) -> int:
		res = self.send_command_and_get_response("N0,00")
		assert res is not None, "No response from get power level command"
		return int(res, 16)

	def set_power_level(self, power_level: int):
		assert -2 <= power_level <= 25, "Power level must be between -2 and 25 dB"

		# Convert int to hex string
		power_level_hex = format(power_level, '02X')
		self.send_command(f"N1,{power_level_hex}")
		
		# This command requires a rate-limit after running to prevent the device from locking
		time.sleep(AFTER_SETTING_COMMAND_DELAY)

	def change_baud_rate(self, baud_rate: AvailableBaudRates):
		# Change baud rate
		res = self.send_command_and_get_response(f"NA,0{baud_rate.value}")
		assert res[0:2] == f"0{baud_rate.value}"
		time.sleep(AFTER_SETTING_COMMAND_DELAY)

		# Close current serial connection
		self.ser.close()
		# Reopen with new baud rate
		new_baud = {
			AvailableBaudRates.BAUD_4800: 4800,
			AvailableBaudRates.BAUD_9600: 9600,
			AvailableBaudRates.BAUD_14400: 14400,
			AvailableBaudRates.BAUD_19200: 19200,
			AvailableBaudRates.BAUD_38400: 38400,
			AvailableBaudRates.BAUD_57600: 57600,
			AvailableBaudRates.BAUD_115200: 115200,
			AvailableBaudRates.BAUD_230400: 230400,
		}[baud_rate]
		self.ser.baudrate = new_baud
		self.ser.open()
		time.sleep(0.3)

	# GPIO
	# | N6,00 get GPIO configuration N7,<value> set GPIO configuration <value>mask and setting mask: first digi 4+2+1 4: pin10 2: pin11 1: pin14 setting: second digi 4+2+1 4: pin10 out 2: pin11 out 1: pin14 out        | N<value> <value> 4+2+1 4: pin10 out 2: pin11 out 1: pin14 out                                                                                                                                                                                                    |                                 | get/set GPIO input/output configuration                                                          |
	# | N8,00 read GPIO pins N9,<value> write GPIO pins <value>mask and setting mask: first digi 4+2+1 4: pin10 2: pin11 1: pin14 setting: second digi 4+2+1 4: pin10 high 2: pin11 high 1: pin14 high                    | N<value> <value> 4+2+1 4: pin10 high level 2: pin11 high level 1: pin14 high level                                                                                                                                                                               |                                 | read/write GPIO pins                                                                             |

	# def get_gpio_configuration(self) -> str:
	# 	return self.send_command_and_get_response("N6,00")
	# def set_gpio_configuration(self, value: str):
	# 	self.send_command(f"N7,{value}")
	# def read_gpio_pins(self) -> str:
	# 	return self.send_command_and_get_response("N8,00")
	# def write_gpio_pins(self, value: str):
	# 	self.send_command(f"N9,{value}")

	####################################################################
	# Status commands
	####################################################################

	def get_reader_firmware(self) -> str:
		res = self.send_command_and_get_response("V")
		assert res is not None, "No response from reader firmware command"
		res = res.split(',')
		
		major = res[0][0:2]
		minor = res[0][2:4]
		comment = ','.join(res[1:])
	
		# parse major from hex to int
		major_int = int(major, 16)
		minor_int = int(minor, 16)

		return f"v{major_int}.{minor_int} ({major}{minor}, comment: {comment})"

	def get_reader_id(self) -> str:
		return self.send_command_and_get_response("S")


	####################################################################
	# Configuration
	####################################################################
