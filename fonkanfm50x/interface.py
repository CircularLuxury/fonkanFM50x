import serial
import time
from fastcrc import crc16

from .types import RFIDRegion, AvailableBaudRates, EPCMemoryBank
from .exceptions import ReaderCommandNotSupportedException, UnexpectedReaderResponseException, raise_exception_from_code

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
            timeout=.3,
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
    
    def _write_command(self, command: str) -> str | None:
        if not self.ser:
            raise RuntimeError("Serial port not initialized. Call begin() first.")
        print(f">: {command.encode()}") if self.debug else None
        self.ser.write(f"\n{command}\r".encode())

    def _read_response(self) -> str | None:
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

        if decoded == '':
            return None
        else:
            return decoded

    def send_command_and_get_response(self, command: str, handle_error: callable = raise_exception_from_code) -> str:
        self._write_command(command)

        decoded = self._read_response()

        if decoded == 'X':
            raise ReaderCommandNotSupportedException(f"RFID Reader does not understand {command}")
        elif decoded and decoded[0] != command[0]:
            handle_error(decoded[0], f"response {decoded} while executing command {command}")
            raise UnexpectedReaderResponseException(f"RFID Reader returned unexpected response for {command}: {decoded}")

        return decoded[1:]
    
    def send_command_and_get_response_until(self, command: str, terminator: str) -> list[str]:
        # Call self.send_command_and_get_response repeatedly until terminator is found
        responses = []
        res = self.send_command_and_get_response(command)
        if res == terminator:
            # If not even the first response, return empty list
            return []
        while True:
            res = self._read_response()
            if res is None:
                break
            # remove command echo
            res = res[1:]

            responses.append(res)
            if res == terminator:
                break
        return responses

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
        # time.sleep(0.3)

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
    #     return self.send_command_and_get_response("N6,00")
    # def set_gpio_configuration(self, value: str):
    #     self.send_command(f"N7,{value}")
    # def read_gpio_pins(self) -> str:
    #     return self.send_command_and_get_response("N8,00")
    # def write_gpio_pins(self, value: str):
    #     self.send_command(f"N9,{value}")

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

    def _parse_tag_id_response(self, res: str) -> str:
        # res = PC+EPC+CRC16
        # Example read:
        # 3000E28068940000402C6FE0911EF6F4
        # 3000E28068940000402 C6FE0
        # 3000 E28068940000502 C6FE0

        pc_control_word = res[0:4]
        # if pc_control_word == "3000":
        #     # EPC length is 6 words, 12 bytes, 96 bits
        # elif pc_control_word == "4000":
        #     # EPC length is 8 words, 16 bytes, 128 bits
        # else:
        #     raise RuntimeWarning(f"Unsupported PC control word: {pc_control_word}")

        epc_tag_id = res[4:-4]
        read_crc16 = res[-4:]
        
        # check CRC, raise exception if invalid
        # Calculate CRC-16/GENIBUS
        # Found correct algo with https://crccalc.com/?crc=3000E28068940000402C6FE0A11E&method=CRC-16/GENIBUS&datatype=hex&outtype=hex
        expected_crc = crc16.genibus(bytes.fromhex(pc_control_word + epc_tag_id))
        #Convert to 4-digit hex
        expected_crc = format(expected_crc, '04X')

        if expected_crc != read_crc16:
            print(f'found {pc_control_word}, {epc_tag_id}, {read_crc16}, calculated {expected_crc}')
            raise RuntimeWarning(f"Invalid CRC16. Received: {read_crc16}, Calculated: {expected_crc}")
        return epc_tag_id

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
            return self._parse_tag_id_response(res)
    
    '''
    A: the RFID Tag memory (Tag) is divided into Reserved memory (retention), EPC (electronic product code), TID (Tag identification number) and the User (User) four independent storage block (Bank).

    Reserved area: store Kill Password (monkey) and Access Password (Access Password).

    EPC area: store the EPC number, etc.

    Every TID area: store tags identification number, number should be unique.

    The User area: storing User defined data.

    In addition to the Lock (Lock) status of each block and so on use and storage properties of units.
    '''

    def read_many_tag_id(self) -> list[str]:
        """
        Display tag EPC ID. Multiple at the same time if present.
        """
        # Find tags until we recieve 'U': no tags found.
        tags = self.send_command_and_get_response_until("U", terminator="")
        if tags is None:
            raise UnexpectedReaderResponseException("No response from read tag command")
        elif tags == []:
            return []
        else:
            tags_processed = []
            for res in tags:
                if res == "":
                    continue
                tags_processed.append(self._parse_tag_id_response(res))

            return tags_processed
    
    def read_tag_memory(self, bank: EPCMemoryBank, address: int, length: int) -> str | None:
        """
        Read tag memory
        bank: reserved/EPC/TID/User
        address: word address: 0-> 3FFF
        length: read word length: 1->1E (1->30 bytes)
        """
        res = self.send_command_and_get_response(f"R{bank.value},{address},{length}")
        if res == '':
            # No tag in RF field
            return None
        else:
            return res #bytes.fromhex(res).decode('utf-8')
    

    def read_tag_memory_multiband(self, bank: EPCMemoryBank, address: int, length: int, multiband:bool=False) -> tuple[str, str] | None:
        """
        Read tag memory, multiband. Returns EPC
        bank: reserved/EPC/TID/User
        address: word address: 0-> 3FFF
        length: read word length: 1->1E (1->30 bytes)
        """

        res = self.send_command_and_get_response(f"Q,R{bank.value},{address},{length}")
        if res == '':
            # No tag in RF field
            return None
        else:
            res = res.split(',')
            epc = res[0]
            data = ','.join(res[1:])
            # Raise error on communication with RFID error
            if data[0] != 'R':
                raise_exception_from_code(data[0])
            data = data[1:] # remove leading R, since command is Q,R and the R is echoed


            return self._parse_tag_id_response(epc), data #bytes.fromhex(res).decode('utf-8')
    