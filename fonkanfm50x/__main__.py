from fonkanfm50x import FonkanUHF
import time

if __name__ == '__main__':
    reader = FonkanUHF()
    reader.begin(start_power=25, start_baud_ignored_for_now=None)

    version = reader.get_reader_firmware()
    serial = reader.get_reader_id()
    print(f"Connected to reader id: {serial} | Firmware version: {version}")

    try:
        while True:
            reader.send_command()
            RFID_Tag, RFID_Time = reader.read_buffer()
            time.sleep(0.1)
            if len(RFID_Tag) > 15:
                if RFID_Tag != reader.last_tag:
                    print(f"New tag found {RFID_Tag.split('\n')[1]} after {time.time() - reader.last_time} seconds")
                    reader.last_tag = RFID_Tag
                    reader.last_time = time.time()
                elif time.time() - reader.last_time > reader.stall_time:
                    print(f"\t\tFound tag again after {reader.stall_time} seconds")
                    reader.last_tag = RFID_Tag
                    reader.last_time = time.time()
    except KeyboardInterrupt:
        pass
    finally:
        reader.destroy()