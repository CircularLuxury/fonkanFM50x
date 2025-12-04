
from fonkanfm50x import FonkanUHF, AvailableBaudRates, RFIDRegion, TagReadException

if __name__ == '__main__':
    with FonkanUHF(start_power=25,#
                    baud_rate=AvailableBaudRates.BAUD_230400,
                    region=RFIDRegion.EU
                   ) as reader:
        version = reader.get_reader_firmware()
        serial = reader.get_reader_id()
        print(f"Connected to reader id: {serial} | Firmware version: {version}")

        try:
            while True:
                try:
                    tag = reader.read_tag_id()
                except TagReadException as e:
                    print(f"Error reading tag: {e}")
                    continue
                if tag is not None:
                    print(f"New tag found {tag}")
        except KeyboardInterrupt:
            import sys
            sys.exit(0)
