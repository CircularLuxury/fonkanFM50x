# FM50x UHF RFID Reader Library

Unofficial python library for Fonkan FM50x series UHF RFID readers (ISO18000-6C/EPC Class 1 Gen 2).

## Project Status
+ [x] connection management & interface class
+ [x] device configuration: power, region, baudrate...
+ [x] tag id reading methods
+ [x] multiple tag reading (with CRC check)
+ [ ] multiband tag reading
+ [ ] advanced tag operations (read/write memory, lock, kill...)

## Hardware
For more details, read [FM50x_specs.md](./FM50x_specs.md)

- **Model**: FM-50x family (FM-503/FM-505/...)
- **Interface**: UART (i.e. over USB with the provided USB adapter)

## Quick Usage

```bash
uv run python3 -m fonkanfm50x
```

## Library usage

```python

from fonkanfm50x import FonkanUHF
import time

if __name__ == '__main__':
    with FonkanUHF() as reader:
        version = reader.get_reader_firmware()
        serial = reader.get_reader_id()
        print(f"Connected to reader id: {serial} | Firmware version: {version}")

        # Find more commands in fonkanfm50x/__main__.py
```

## Configuration
For more details, read [FM50x_protocol.md](./FM50x_protocol.md)

### Regions
+ `RFIDRegion.US` (902-928 MHz)
+ `RFIDRegion.EU` (865-868 MHz)
+ `RFIDRegion.CN` (920-925 MHz) 
+ `RFIDRegion.JP` (916-921 MHz)
+ `RFIDRegion.KR` (917-921 MHz)
+ Others: TW, CN2, VN...

### Baud Rates
4800 | 9600 | 14400 | 19200 | 38400 | 57600 | 115200 | 230400

### Power
-2 to 25 dBm (default: 25)
