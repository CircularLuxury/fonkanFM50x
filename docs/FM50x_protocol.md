# FM50x RFID Reader Protocol Documentation
Tested with FM-505 reader. Will work with FM-503 and others in the same family.

## Connection
UART (QinHeng Electronics USB Single Serial USB) on /dev/ttyACM0

Default: `38400 8N1`, parity: `none`


## Command Format
Command and return message is transmitted as ASCII format. All commands start with a character that describes commands: + arguments (if any, in hexadecimal units) and stop with a `<CR>` (0x0D hex).

Response message starts with a `<LF>` (0x0A hex), command first character and stop with a `<CR><LF>`. There shall always be a response to acknowledge the command. Usually, the response message will start with the same command character, except in case of an error (see below).

If the command is not found, the return message will be `<LF>X<CR><LF>`.

> **Note:**
> + queries are encapsulated in `<LF>________<CR>`
> + responses are encapsulated in `<LF>_______<CR><LF>`

### Examples:
1. Get reader firmware version
```
>: <LF>S<CR>
<: <LF>S01234567<CR><LF>
```
2. Read TID memory bank, start address at 0, read 4 words length, TID data is `0x1234567890`
```
>: <LF>R2,0,4<CR>
<: <LF>R123456789ABCDEF0<CR><LF>
```
3. Write USER memory bank, start address at 12, write 2 word length, write data is `0xAAAABBBB`
```
>: <LF>W3,C,2,AAAABBBB<CR>
<: <LF>W<OK><CR><LF>
```


## Command table
**`<error code>` (distilled from fields):**`
+ `0` : other error
+ `3` : memory overrun
+ `4` : memory locked
+ `B` : Insufficient power
+ `F` : Non-specific error
> NOTE: There appears to be another error code when reading: 'E', which seems to be a sort of low RSSI/connection interruption/collision error.

### Device commands:
| Command*                                                                                                                                                                                                          | Return Message**                                                                                                                                                                                                                                                 | Description                     |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| `V`                                                                                                                                                                                                                 | `Vxxyy,<message>`<br> xx: major version number <br>yy: minor version number<br>`<message>`: other info.                                                                                                                                                                         | display reader firmware version |
| `S`                                                                                                                                                                                                                 | `S01234567` <br>where 01234567 is reader ID                                                                                                                                                                                                                                  | display reader ID               |

### Read Tag operations:
| Command*                                                                                                                                                                                                          | Return Message**                                                                                                                                                                                                                                                 | Description                     |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| `Q`                                                                                                                                                                                                                 | `Q<none or EPC>`<br> none: no tag in RF field <br>EPC: PC+EPC+CRC16                                                                                                                                                                                          | display tag EPC ID                                                                               |
| `U`                                                                                                                                                                                                                 | `U<none or EPC>`<br> none: no tag in RF field <br>EPC: PC+EPC+CRC16                                                                                                                                                                                          | Multi-TAG read EPC                                                                               |
| `R<bank>,<address>,<length>`. <br>`<bank>` memory bank <br>`<address>` start address 0 ~ 3FFF <br>`<length>` read word length 1 ~ 1E                                                                 | `R<none or read data>` or `<error code>` <br> none: no tag in RF field                                                                      | read tag memory data                                                                             |
| `QR: Q , R<band>,<address>,<length>` <br>`<bank>` memory bank <br>`<address>` start word address 0 ~ 3FFF <br>`<length>` read word length 1 ~ 1E                                                    | `Q<EPC>,R<DATA>` or `<error code>`<br> EPC= PC+EPC+CRC16<br>DATA= read data                                                                                    | Multi-Band data read with EPC for single-Tag read                                                |
| `UR: U<slot Q>, R<band>,<address>, <length>` <br>`<slot Q>`: 0~10 <br>`<bank>` memory bank <br>`<address>` start word address 0 ~ 3FFF <br>`<length>` read word length 1 ~ 1E                              | `U<EPC>,R<DATA>` or `<error code>` <br>EPC= PC+EPC+CRC16 <br>DATA= read data                                                                                     | Multi-Band data read with EPC for multi-Tag read                                                 |


### Write tag operations:
**memory `<bank>` values:**
+ `0` : reserved
+ `1` : EPC
+ `2` : TID
+ `3` : USER

| Command*                                                                                                                                                                                                          | Return Message**                                                                                                                                                                                                                                                 | Description                     |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| `T<bank>,<bit address>,<bit length >,<bit data >` <br>`<bank>` memory bank <br>`<bit address>` start bit address 0~3FFF <br>`<bit length >` select bit length 1~60 <br>`<bit data >` select bit mask data | T                                                                                                                                                                                                                                                                | Select matching tag                                                                              |
| `W<bank>,<address>, <length>,<data>` <br>`<bank>` memory bank <br>`<address>` start address 0 ~ 3FFF <br>`<length>` write words length 1 ~ 1E                                                       | `W<none or <OK>>` or `<error code>` <br>`<none or <OK>>`: none: no tag in RF field \| `<OK>`: written ok <br>| Z00~Z1F: words write 3Z00~3Z1F: error code and words write | write data to tag memory                                                                         |
| `K<password>,<recom>` <br>`<password>` kill password 00000000~FFFFFFFF <br>`<recom>` recommissioning 0~7                                                                                                                        | `K<none or <OK>>` or `<error code>` <br>`<none or <OK>>` none: no tag in RF field \| `<OK>`: kill ok                                                                | kill tag                                                                                         |
| `L<mask>,<action>` <br>`<mask>` lock mask 000~3FF <br>`<action>` lock action 000~3FF                                                                                                                                            | `L<none or <OK>>` or `<error code>` <br>`<none or <OK>>` none: no tag in RF field \| `<OK>`: lock ok                                                                 | lock memory                                                                                      |

### Security operations:
| Command*                                                                                                                                                                                                          | Return Message**                                                                                                                                                                                                                                                 | Description                     |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| `P<password>` <br>`<password>` access password   00000000~FFFFFFFF                                                                                                                                                        | `P`                                                                                                                                                                                                                                                                | set access password for R W L command, one time use                                              |

### Reader configuration commands:

**Regulation values:**
+ 01: US 902~928
+ 02: TW 922~928
+ 03: CN 920~925
+ 04: CN2 840~845   05: EU 865~868   06: JP 916~921   07: KR 917~921     08: VN 918~923
+ 05: EU 865~868
+ 06: JP 916~921
+ 07: KR 917~921
+ 08: VN 918~923

**UART Baud Rate values:**
+ 0: 4800
+ 1: 9600
+ 2: 14400
+ 3: 19200
+ 4: 38400
+ 5: 57600
+ 6: 115200
+ 7: 230400

| Command*                                                                                                                                                                                                          | Return Message**                                                                                                                                                                                                                                                 | Description                     |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| `G1` `G0` `G2`                                                                                                                                                                                                          | `G1` `G0` `G2`                                                                                                                                                                                                                                                         | Start command logging <br>End command logging <br>Run logging commands <br>For external TACT switch function |
| `N0,00` read RFID Reader power <br>`N1, <value>` set RFID Reader power (-2~25dBm) <br>`<value>` 00~1B                                                                                                                           | `N<value>` or `<NULL>`                                                                                                                                                                                                                                                 | Read/Set RFID Reader power level                                                                 |
| `N4,00` read Regulation <br>`N5, <value>` set Regulation <br>`<value>` regulation value 01~08 | `N<value>` <br>`<value>` regulation value                                                                                                            | Read/Set Frequency Range                                                                         |
| `NA,<value>` setting UART Baud Rate <br>`<value>` baud rate value                                                                                       | `N<value>` <br>`<value>` baud rate value                                                                                                                                                                | Setting UART Baud Rate. After getting the reply,Baud Rate will be changed                        |
| `N6,00` get GPIO configuration <br>`N7,<value>` set GPIO configuration <br>`<value>`first digit: mask \| second digit: OUT(1)/IN(0)        | `N<value>`<br> `<value>` 3bitpins OUT=1 IN=0                                                                                                                                                                                                    | get/set GPIO input/output configuration                                                          |
| `N8,00` read GPIO pins <br>`N9,<value>` write GPIO pins <br>`<value>`: first digit: 3bit mask \| second digit: HIGH=1 LOW=0                    | `N<value>` <br>`<value>` 3bitpins  level HIGH=1 LOW=0                                                                                                                                                                              | read/write GPIO pins                                                                             |

**GPIO 3bit Pin/Mask Selection:**
```
1 1 1
| | +-- pin14 (decimal value 1)
| +---- pin11 (decimal value 2)
+------ pin10 (decimal value 4)
```
