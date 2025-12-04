
from fonkanfm50x import FonkanUHF, AvailableBaudRates, RFIDRegion, EPCMemoryBank, TagGenericException
import time

if __name__ == '__main__':
    with FonkanUHF(start_power=25,#
                    baud_rate=AvailableBaudRates.BAUD_230400,
                    region=RFIDRegion.EU,
                    debug=False
                   ) as reader:
        print(f"Connected to reader id: {reader.get_reader_id()} | Firmware version: {reader.get_reader_firmware()} | Region: {reader.get_region()} | Power: {reader.get_power_level()} dBm")

        found_tag_ids = set()
        try:
            while True:
                # Read tag ids:
                # value = reader.read_tag_id()
                # if value is not None:
                #     print(value)

                # Read tag ids via memory multiband:
                # try:
                #     value = reader.read_tag_memory_multiband(bank=EPCMemoryBank.TID, address=0, length=6)
                #     if value is not None:
                #         print(value)
                # except TagGenericException as e:
                #     print(f"Error reading tag memory: {type(e)}: {e}")

                # Read multi tag ids:
                # try:
                #     tags = reader.read_many_tag_id()
                # except TagGenericException as e:
                #     print(f"Error reading tag: {e}")
                #     continue
                # else:
                #     if tags is not None and tags != []:
                #         for tag in tags:
                #             if tag not in found_tag_ids:
                #                 found_tag_ids.add(tag)
                #                 print(f"New tag found {tag} (total found: {len(found_tag_ids)})")

                # Read multi tag ids manually via memory multiband:
                try:
                    value = reader.read_multi_tag_memory_multiband(bank=EPCMemoryBank.TID, address=0, length=6, slot_q=3)
                    if value is not None and value != []:
                        print(value)
                except TagGenericException as e:
                    print(f"Error reading tag memory: {type(e)}: {e}")
        except KeyboardInterrupt:
            import sys
            sys.exit(0)
