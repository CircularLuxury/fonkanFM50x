# FM50x UHF RFID Reader Library

Unofficial python library for Fonkan FM50x series UHF RFID readers (ISO18000-6C/EPC Class 1 Gen 2).

This is a reverse-engineered library, since Fonkan did not provide me with any SDK or protocol documentation when I bought the reader, even though I asked for it.

## Hardware
For more details, read [FM50x_specs.md](./docs/FM50x_specs.md)

- **Model**: FM-50x family (FM-503/FM-505/FM-507...)
- **Interface**: UART (i.e. over USB with the provided USB adapter)

## Quick Usage
A small tag searching tool is provided in `fonkanfm50x/__main__.py`, which can be run with:
```bash
uv run python3 -m fonkanfm50x
```

## Library usage
Pretty much self-described in the type signatures and docstrings. For specific implementation details, read [FM50x_protocol.md](./docs/FM50x_protocol.md)

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

## Project Status
+ [x] reliable reader/counter
    + [x] connection management & interface class
    + [x] device configuration: power, region, baudrate...
    + [x] tag id reading methods
    + [x] multiple tag reading (with CRC check)
    + [x] multiband tag reading
    + [x] GPIO control (untested)
    + [x] generator multi-tag reading (not just a for loop return)
    + [x] simple EPC tag ID manufacturer identification

- [ ] writer/password-protected operations
    + [ ] password usage (simplified, as argument?)
    + [ ] tag write operations (read/write memory, lock, kill...)
    + [ ] advanced G1 G2 settings (what's that?)