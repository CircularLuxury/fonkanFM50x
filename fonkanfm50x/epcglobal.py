from dataclasses import dataclass

@dataclass
class CardDetails:
    epc_tag_id: str
    comm_standard: str

    xtid_supported: bool
    security_bit_set: bool
    file_indicator_bit: bool

    designer: str
    model_name: str
    standard_header: str
    xtid_header: str

    def __str__(self):
        return f"CardDetails<{self.designer} | {self.model_name} | {self.comm_standard}>(S: {self.security_bit_set}, F:{self.file_indicator_bit}, X: {self.xtid_supported}, standard_header={self.standard_header}, xtid_header={self.xtid_header})"

class TagModelParser:
    # Source: https://www.gs1.org/docs/epc/mdid_list.json

    def __init__(self):
        import json
        import os
        
        # Get the directory where this module is located
        module_dir = os.path.dirname(os.path.abspath(__file__))
        mdid_absolute_source = os.path.join(module_dir, 'data', 'mdid_list.json')
        with open(mdid_absolute_source, 'r', encoding='utf-8') as f:
            self.mdid_data = json.load(f)
            self.designers_by_mdid = {
                designer['mdid']: designer
                for designer in self.mdid_data['registeredMaskDesigners']
            }
            
    def interpret_TID_data(self, tid_string:str) -> CardDetails:
        """
        Interpret the lower 48 bits of the TID data

        lower_48: segmented array with each segment (MSB in element 0) determined by the standard 48 bit TID Header
        """
        # Determine Standard
        #        '11100010': 'True', '11101101': 'Nonexistent'

        # extract memory segments based on GS1s TDS 2.0 document

        tid_bits = bin(int(tid_string, 16))[2:].zfill(len(tid_string)*4)

        # ISO / IEC 15963 Class Identifier 00h-07h
        class_identifier = tid_bits[0:8]
        standard = True if class_identifier == '11100010' else False

        xtid_bit = True if tid_bits[8] == '1' else False
        security_bit = True if tid_bits[9] == '1' else False
        file_indicator_bit = True if tid_bits[10] == '1' else False
        mdid = tid_bits[11:20] # Mask Designer Identifier
        tmn = tid_bits[20:32] # Tag Model Number
        tmn_hex = hex(int(tmn, 2))[2:].upper().zfill(3)

        # Get mask designer ID from json file
        model_name = ""
        try:
            designer = self.designers_by_mdid[mdid]
        except KeyError:
            designer = {"designerName": "Unknown", "chips": []}
            model_name = ""
        else:
            tag_model = None
            if 'chips' not in designer:
                designer['chips'] = []

            # Search for tag model in designer chips
            for _, chip in enumerate(designer['chips']):
                if chip['tmnBinary'] == tmn:
                    tag_model = chip
            model_name = ""
            if tag_model is None:
                model_name = "Unknown: 0x{}".format(tmn_hex)
            else:
                model_name = tag_model['modelName']

        # do nothing for now
        # EPC Tag Data Standard Header 20h-2Fh
        epc_TD_standard_header = int(tid_bits[32:48], 2)
        standard_header_hex = hex(epc_TD_standard_header)[2:].upper().zfill(2)

        if xtid_bit:
            xtid_header = int(tid_bits[48:], 2)
            xtid_header_hex = hex(xtid_header)[2:].upper().zfill(2)
        else:
            xtid_header_hex = None

        # serial number:
        # if interpreted_TID_data[4] == "Impinj":
        #     if interpreted_TID_data[5] == "Monza R6":
        #         # extract Monza R6 38-bit serial number
        #         return impinj_mr6.extract_38_Bit_serial_number(raw_bin_string)

        return CardDetails(
            epc_tag_id=tid_string,
            comm_standard="ISO/IEC 15963" if standard else "Unknown",
            xtid_supported=xtid_bit,
            security_bit_set=security_bit,
            file_indicator_bit=file_indicator_bit,
            designer=designer['manufacturer'].strip(),
            model_name=model_name,
            standard_header=standard_header_hex,
            xtid_header=xtid_header_hex
        )
