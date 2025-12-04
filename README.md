# FM50x UHF RFID Reader Library

Unofficial python library for Fonkan FM50x series UHF RFID readers (ISO18000-6C/EPC Class 1 Gen 2).

## Hardware
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
    with FonkanUHF(start_power=25) as reader:
        version = reader.get_reader_firmware()
        serial = reader.get_reader_id()
        print(f"Connected to reader id: {serial} | Firmware version: {version}")

        # Find more commands in fonkanfm50x/__main__.py
```

## Configuration

### Regions
+ `RFIDRegion.US` (902-928 MHz)
+ `RFIDRegion.EU` (865-868 MHz)
+ `RFIDRegion.CN` (920-925 MHz) 
+ `RFIDRegion.JP` (916-921 MHz)
+ `RFIDRegion.KR` (917-921 MHz)
+ Others: TW, CN2, VN

### Baud Rates
4800 | 9600 | 14400 | 19200 | 38400 | 57600 | 115200 | 230400

### Power
-2 to 25 dBm (default: 25)
