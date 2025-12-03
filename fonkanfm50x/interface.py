import serial
import time

from .types import RFIDRegion, AvailableBaudRates

class FonkanUHF:
	"""
	Fonkan FM50x UHF RFID Reader class.
	ISO18000-64 / EPCglobal UHF Class 1 Gen 2 standard compliant..
	"""

	def __init__(self, serial_port: str = '/dev/ttyACM0'):
		# WARNING: The RFID Module MUST be connected through the non power USB port
		self.serial_port = serial_port
		self.ser: serial.Serial | None = None
		self.stall_time = 60
		self.last_tag = "initialise value"
		self.last_time = time.time() - self.stall_time

	def begin(self, 
		   	start_power: int = 25,
			baud_rate: AvailableBaudRates = AvailableBaudRates.BAUD_230400,
			region: RFIDRegion = RFIDRegion.EU
		):
		# baud parameter is ignored for now to match request
		self.ser = serial.Serial(
			port=self.serial_port,
			baudrate=38400,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=1,
		)

		# Configure reader
		self.set_power_level(start_power)
		self.set_region(region)
		self.change_baud_rate(baud_rate)

	def destroy(self):
		if self.ser and self.ser.is_open:
			try:
				self.ser.close()
			finally:
				self.ser = None

	####################################################################
	# Internal
	####################################################################

	def send_command(self, command: str):
		if not self.ser:
			raise RuntimeError("Serial port not initialized. Call begin() first.")
		self.ser.write(f"\n{command}\r".encode())
		# time.sleep(0.1)
	
	def send_command_and_get_response(self, command: str) -> str:
		self.send_command(command)
		time.sleep(0.1)
		response = self.ser.read(self.ser.in_waiting).decode('utf-8') #.replace(response_prefix, '').strip()
		return response

	####################################################################
	# Configuration
	####################################################################

	def set_region(self, region: RFIDRegion):
		# Set region
		self.send_command(f"N5,0{region.value}")
	
	def set_power_level(self, power_level: int):
		assert -2 <= power_level <= 25, "Power level must be between -2 and 25 dB"

		# Convert int to hex string
		power_level_hex = format(power_level, '02X')
		self.send_command(f"N1,{power_level_hex}")
	
	def change_baud_rate(self, baud_rate: AvailableBaudRates):
		# Change baud rate
		self.send_command(f"N2,{baud_rate.value}")
		time.sleep(0.2)
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
		return self.send_command_and_get_response("V")

	def get_reader_id(self) -> str:
		return self.send_command_and_get_response("N0")


	####################################################################
	# Configuration
	####################################################################
