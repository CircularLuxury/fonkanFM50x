
from fonkanfm50x import FonkanUHF, AvailableBaudRates, RFIDRegion, EPCMemoryBank, TagGenericException
from fonkanfm50x.epcglobal import TagModelParser

if __name__ == '__main__':
    tag_parser = TagModelParser()

    with FonkanUHF(start_power=25,#
                    baud_rate=AvailableBaudRates.BAUD_38400,
                    region=RFIDRegion.EU,
                    debug=False
                   ) as reader:
        print(f"Connected to reader id: {reader.get_reader_id()} | Firmware version: {reader.get_reader_firmware()} | Region: {reader.get_region()} | Power: {reader.get_power_level()} dBm")
        found_tag_ids = set()
        try:
            while True:
                # Read tag ids one by one:
                # value = reader.read_tag_id()
                # if value is not None:
                #     print(value)

                # Read tag ids one by one via memory multiband:
                # try:
                #     value = reader.read_tag_memory_multiband(bank=EPCMemoryBank.TID, address=0, length=6)
                #     if value is not None:
                #         print(value)
                # except TagGenericException as e:
                #     print(f"Error reading tag memory: {type(e)}: {e}")

                # Read multiple tag ids:
                try:
                    for tag in reader.read_many_tag_id():
                        if tag not in found_tag_ids:
                            found_tag_ids.add(tag)
                            print(f"{len(found_tag_ids)}: Found new tag {tag_parser.interpret_TID_data(tag)}")
                except TagGenericException as e:
                    print(f"Error reading tag: {e}")
                    continue

                # Read multiple tag ids manually via memory multiband:
                # try:
                #     for tag, mem in reader.read_multi_tag_memory_multiband(bank=EPCMemoryBank.TID, address=0, length=6, slot_q=3):
                #         if tag not in found_tag_ids:
                #             found_tag_ids.add(tag)
                #             print(f"{len(found_tag_ids)}: Found new tag {tag_parser.interpret_TID_data(tag)}")
                #             # print(f"New tag found {tag} (total found: {len(found_tag_ids)}) with data {mem}")
                # except TagGenericException as e:
                #     print(f"Error reading tag memory: {type(e)}: {e}")
        except KeyboardInterrupt:
            import sys
            sys.exit(0)
