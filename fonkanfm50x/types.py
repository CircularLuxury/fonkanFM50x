from enum import Enum

class RFIDRegion(Enum):
	# 01: US 902~928 MHz
	# 02: TW 922~928 MHz
	# 03: CN 920~925 MHz
	# 04: CN2 840~845 MHz
	# 05: EU 865~868 MHz
	# 06: JP 916~921 MHz
	# 07: KR 917~921 MHz
	# 08: VN 918~923 MHz
	US = 1
	TW = 2
	CN = 3
	CN2 = 4
	EU = 5
	JP = 6
	KR = 7
	VN = 8

class AvailableBaudRates(Enum):
	'''
	0: 4800  1: 9600  2: 14400  3: 19200  4: 38400  5: 57600  6: 115200  7: 230400     
	'''
	BAUD_4800 = 0
	BAUD_9600 = 1
	BAUD_14400 = 2
	BAUD_19200 = 3
	BAUD_38400 = 4
	BAUD_57600 = 5
	BAUD_115200 = 6
	BAUD_230400 = 7

	def to_int(self) -> int:
		return {
			AvailableBaudRates.BAUD_4800: 4800,
			AvailableBaudRates.BAUD_9600: 9600,
			AvailableBaudRates.BAUD_14400: 14400,
			AvailableBaudRates.BAUD_19200: 19200,
			AvailableBaudRates.BAUD_38400: 38400,
			AvailableBaudRates.BAUD_57600: 57600,
			AvailableBaudRates.BAUD_115200: 115200,
			AvailableBaudRates.BAUD_230400: 230400,
		}[self]