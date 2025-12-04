import serial
import time

from .types import RFIDRegion, AvailableBaudRates
from .exceptions import UnexpectedReaderResponseException, TagReadException

AFTER_SETTING_COMMAND_DELAY = 0.3 # Tested with default 38400 baud rate up to 230400 baud rate, so not dependent on connection speed

class FonkanUHF:
	"""
	Fonkan FM50x UHF RFID Reader class.
	ISO18000-64 / EPCglobal UHF Class 1 Gen 2 standard compliant..
	"""

	def __init__(self, 
			  serial_port: str = '/dev/ttyACM0',
			  start_power: int = 25,
			  baud_rate: AvailableBaudRates = AvailableBaudRates.BAUD_38400,
			  region: RFIDRegion = RFIDRegion.EU,
			  debug: bool = False):
		# WARNING: The RFID Module MUST be connected through the non power USB port
		self.serial_port = serial_port
		self.start_power = start_power
		self.baud_rate = baud_rate
		self.region = region
		self.debug = debug
		self.ser: serial.Serial | None = None
		self.stall_time = 60
		self.last_tag = "initialise value"
		self.last_time = time.time() - self.stall_time

	def __enter__(self):
		# baud parameter is ignored for now to match request
		self.ser = serial.Serial(
			port=self.serial_port,
			baudrate=self.baud_rate.to_int(),
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=1,
		)

		# Try command to check if connection baud rate is correct.
        # If not, try changing it until we find the right one, finally setting the chosen baud rate
		# We require this because the reader remembers the last baud rate even after power cycling
		connected_to_id:str|None = None
		try:
			connected_to_id = self.get_reader_id()
		except UnexpectedReaderResponseException:
			print(f"Could not connect at initial baud rate {self.baud_rate.to_int()}, searching for correct rate...")
			for rate in AvailableBaudRates:
				try:
					self._change_serial_connection_baud_rate(rate)

					connected_to_id = self.get_reader_id()
					if connected_to_id:
						break
				except Exception:
					continue

			if not connected_to_id:
				raise RuntimeError("Could not establish connection with the RFID reader on any baud rate")
			else:
				print(f"Successfully connected to reader id: {connected_to_id} at baud rate {rate.to_int()}. Changing reader baud rate to desired {self.baud_rate.to_int()}.")
				# Now set to desired baud rate
				self.change_baud_rate(self.baud_rate)

		# print(f"current power level: {self.get_power_level()}")
		current_power = self.get_power_level()
		if current_power != self.start_power:
			self.set_power_level(self.start_power)
		current_region = self.get_region()
		if current_region != self.region:
			self.set_region(self.region)

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
		if res is None:
			raise UnexpectedReaderResponseException(f"No ACK for command {command}")
	
	def send_command_and_get_response(self, command: str) -> str | None:
		if not self.ser:
			raise RuntimeError("Serial port not initialized. Call begin() first.")
		print(f">: {command.encode()}") if self.debug else None
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
		print(f"<: {decoded}") if self.debug else None

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
		if res is None:
			raise UnexpectedReaderResponseException("No response from get power level command")
		return int(res, 16)

	def set_power_level(self, power_level: int):
		assert -2 <= power_level <= 25, "Power level must be between -2 and 25 dB"

		# Convert int to hex string
		power_level_hex = format(power_level, '02X')
		self.send_command(f"N1,{power_level_hex}")
		
		# This command requires a rate-limit after running to prevent the device from locking
		time.sleep(AFTER_SETTING_COMMAND_DELAY)

	def _change_serial_connection_baud_rate(self, baud_rate: AvailableBaudRates):
		if not self.ser:
			raise RuntimeError("Serial port not initialized. Call begin() first.")

		# Close current serial connection
		self.ser.close()
		# Reopen with new baud rate
		self.ser.baudrate = baud_rate.to_int()
		self.ser.open()
		time.sleep(0.3)

	def change_baud_rate(self, baud_rate: AvailableBaudRates):
		# Change baud rate
		res = self.send_command_and_get_response(f"NA,0{baud_rate.value}")
		assert res[0:2] == f"0{baud_rate.value}"
		time.sleep(AFTER_SETTING_COMMAND_DELAY)

        # Change serial connection baud rate
		self._change_serial_connection_baud_rate(baud_rate)

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
		if res is None:
			raise UnexpectedReaderResponseException("No response from get firmware command")
		res = res.split(',')
		
		major = res[0][0:2]
		minor = res[0][2:4]
		comment = ','.join(res[1:])
	
		# parse major from hex to int
		major_int = int(major, 16)
		minor_int = int(minor, 16)

		return f"v{major_int}.{minor_int} ({major}{minor}, comment: {comment})"

	def get_reader_id(self) -> str:
		res = self.send_command_and_get_response("S")
		if res is None:
			raise UnexpectedReaderResponseException("No response from get reader ID command")
		return res


	####################################################################
	# Tag Operations
	####################################################################

	def _calculate_crc16(self, data: bytes) -> str:
		'''
		Calculate CRC16-CCITT (0xFFFF initial value, polynomial 0x1021)
		Returns hex string in uppercase
		'''
		crc = 0xFFFF
		for byte in data:
			crc ^= (byte << 8)
			for _ in range(8):
				if (crc & 0x8000) != 0:
					crc = (crc << 1) ^ 0x1021
				else:
					crc <<= 1
				crc &= 0xFFFF  # Keep crc to 16 bits
		return format(crc, '04X')

	def read_tag_id(self) -> str | None:
		"""
		Display tag EPC ID
		"""
		res = self.send_command_and_get_response("Q")
		if res is None:
			raise UnexpectedReaderResponseException("No response from read tag command")
		elif res == '':
			return None
		else:			
			# res = PC+EPC+CRC16
			# Example read:
			# 3000E28068940000402C6FE0911EF6F4
			# 3000E28068940000402 C6FE0
			# 3000 E28068940000502 C6FE0

			# pc_control_word = res[0:4]
			# if pc_control_word == "3000":
			# 	# EPC length is 6 words, 12 bytes, 96 bits
			# elif pc_control_word == "4000":
			# 	# EPC length is 8 words, 16 bytes, 128 bits
			# else:
			# 	raise TagReadException(f"Unsupported PC control word: {pc_control_word}")

			epc_tag_id = res[4:-4]
			# crc16 = res[-4:]
			# epc_tag_id = res[4:]
			
			# check CRC, raise exception if invalid
			# calculated_crc16 = self._calculate_crc16(bytes.fromhex(pc + epc))
			# if calculated_crc16 != crc16:
			# 	print(f'found {pc}, {epc}, {crc16}, calculated {calculated_crc16}')
			# 	raise TagReadException(f"Invalid CRC16. Received: {crc16}, Calculated: {calculated_crc16}")
			
			return epc_tag_id
	
	'''
	A: the RFID Tag memory (Tag) is divided into Reserved memory (retention), EPC (electronic product code), TID (Tag identification number) and the User (User) four independent storage block (Bank).

	Reserved area: store Kill Password (monkey) and Access Password (Access Password).

	EPC area: store the EPC number, etc.

	Every TID area: store tags identification number, number should be unique.

	The User area: storing User defined data.

	In addition to the Lock (Lock) status of each block and so on use and storage properties of units.
	'''

	# def read_many_tag_ids(self) -> list[str]:
	# 	"""
	# 	Read multiple tag EPC IDs
	# 	"""

	# 	res = self.send_command_and_get_response("Q")
	# 	if res is None:
	# 		raise UnexpectedReaderResponseException("No response from read tag command")
	# 	elif res == '':
	# 		return None
	# 	else:
	# 		# res = PC+EPC+CRC16
	# 		# example: 3000E28068940000402C6FE0911EF6F4
	# 		pc = res[0:4]
	# 		epc = res[4:-4]
	# 		crc16 = res[-4:]
	
	# 		# check CRC, raise exception if invalid
	# 		calculated_crc16 = self._calculate_crc16(bytes.fromhex(pc + epc))
	# 		if calculated_crc16 != crc16:
	# 			print(f'found {pc}, {epc}, {crc16}, calculated {calculated_crc16}')
	# 			raise TagReadException(f"Invalid CRC16. Received: {crc16}, Calculated: {calculated_crc16}")
			
	# 		return res

