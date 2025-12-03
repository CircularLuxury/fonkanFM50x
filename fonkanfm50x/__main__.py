
from fonkanfm50x import FonkanUHF, AvailableBaudRates, RFIDRegion
import time

if __name__ == '__main__':
    with FonkanUHF(start_power=25,#
                    baud_rate=AvailableBaudRates.BAUD_115200,
                    region=RFIDRegion.EU
                   ) as reader:
        version = reader.get_reader_firmware()
        serial = reader.get_reader_id()
        print(f"Connected to reader id: {serial} | Firmware version: {version}")

        try:
            while True:
                tag = reader.search_tags()
                print(f"New tag found {tag.split('\n')[1]} after {time.time() - reader.last_time} seconds")
        except KeyboardInterrupt:
            import sys
            sys.exit(0)
