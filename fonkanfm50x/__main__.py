
from fonkanfm50x import FonkanUHF, AvailableBaudRates, RFIDRegion, TagReadException

if __name__ == '__main__':
    with FonkanUHF(start_power=25,#
                    baud_rate=AvailableBaudRates.BAUD_230400,
                    region=RFIDRegion.EU,
                    debug=False
                   ) as reader:
        version = reader.get_reader_firmware()
        serial = reader.get_reader_id()
        print(f"Connected to reader id: {serial} | Firmware version: {version} | Region: {reader.get_region()} | Power: {reader.get_power_level()} dBm")

        found_tag_ids = set()
        try:
            while True:
                try:
                    tags = reader.read_many_tag_id()
                except TagReadException as e:
                    print(f"Error reading tag: {e}")
                    continue
                if tags is not None and tags != []:
                    for tag in tags:
                        if tag not in found_tag_ids:
                            found_tag_ids.add(tag)
                            print(f"New tag found {tag} (total found: {len(found_tag_ids)})")
                    # print(f"New tag found {tag}")
        except KeyboardInterrupt:
            import sys
            sys.exit(0)
