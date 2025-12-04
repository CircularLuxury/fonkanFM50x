# Fonkan FM-503 UHF RFID Module
> NOTE: FM-50x modules appear to be electrically identical, only differing in the provided antenna.

## Device

**Manufacturer:**
SHENZHEN FONKAN TECHNOLOGY CO., LTD
www.fonkan.com

Model No. FM-505
Interface: UART
RFID Protocol: ISO-18000-6C/ EPC class1 gen2
Operation range: Around 3m, dependent on tag

|  			Frequency 		                   |  			840-960MHZ 		                                                                                                                                             |  			Working 			Voltage 		         |  			DC 			3.5V – 5 V 		                                                           |
|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|---------------------------------------------------------------------------|
|  			   			  			  			Working 			area support 		 |  			US, 			Canada and other regions following U.S. FCC  			  			Europe 			and other regions following ETSI EN 302 208  			 Mainland 			China; Japan; Korea; Malaysia; Taiwan 		 |  			PCB 			size 		                |  			Pcb 			size:40*40mm , Ceramic antenna size:50*50mm 			 Overall height:8.5mm 		   |
|  			Protocol 		                    |  			EPC 			global UHF Class 1 Gen 2 / ISO 18000-6C 		                                                                                                            |  			Standby 			current 		         |  			<80mA 			(EN  pin high level) 		                                              |
|  			Output 			power 		                |  			0-25 			dBm 		                                                                                                                                               |  			Sleeping 			current 		        |  			<100uA 			(EN  pin low level) 		                                              |
|  			Read/write 		                  |  			Read: 			200-250cm;write: 10-50cm(adjusted) 		                                                                                                               |  			Operation 			current 		       |  			180mA 			@ 3.5V (26 dBm Output,25°C).  			 110mA 			@ 3.5V (18 dBm Output,25°C). 		 |
|  			Output 			power accuracy 		       |  			+/- 			1dB 		                                                                                                                                                |  			Operation 			temp. 		         |  			 - 			20 °C  -  + 70  °C 		                                                   |
|  			Output 			power flatness 		       |  			+/- 			0.2dB 		                                                                                                                                              |  			Storage 			temp. 		           |  			- 			20 °C  -  + 85  °C 		                                                    |
|  			Receive 			sensitivity 		         |  			< 			-70dBm 		                                                                                                                                               |  			Working 			humidity 		        |  			< 			95% ( + 25 °C) 		                                                        |
|  			Read 			tag peak speed 		         |  			> 			50pcs/sec 		                                                                                                                                            |  			Communication 			interface 		 |  			TTL 			Uart interface 		                                                      |
|  			Operating 			time 		              |  			<100mS. 		                                                                                                                                                |  			Heat-dissipating 			method 		 |  			Air 			cooling(no need for out install cooling fin) 		                        |
|  			Communication 			baud rate 		     |  			115200 			bps(default and recommend)  			 38400bps 		                                                                                                           |  			   			 		                     |  			   			 		                                                                     |
|  			   			 		                         |  			   			 		                                                                                                                                                    |  			   			 		                     |  			   			 		                                                                     |

> NOTE: in my particular case, the default baud rate was 38400bps, and the max baud rate is 230400bps. Datasheet seems to be outdated.

**Recommended operating conditions:**
|  			Frequency 		                   |  			840-960MHZ 		                                                                                                                                             |  			Working 			Voltage 		         |  			DC 			3.5V – 5 V 		                                                           |
|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|---------------------------------------------------------------------------|
|  			   			  			  			Working 			area support 		 |  			US, 			Canada and other regions following U.S. FCC  			  			Europe 			and other regions following ETSI EN 302 208  			 Mainland 			China; Japan; Korea; Malaysia; Taiwan 		 |  			PCB 			size 		                |  			Pcb 			size:40*40mm , Ceramic antenna size:50*50mm 			 Overall height:8.5mm 		   |
|  			Protocol 		                    |  			EPC 			global UHF Class 1 Gen 2 / ISO 18000-6C 		                                                                                                            |  			Standby 			current 		         |  			<80mA 			(EN  pin high level) 		                                              |
|  			Output 			power 		                |  			0-25 			dBm 		                                                                                                                                               |  			Sleeping 			current 		        |  			<100uA 			(EN  pin low level) 		                                              |
|  			Read/write 		                  |  			Read: 			200-250cm;write: 10-50cm(adjusted) 		                                                                                                               |  			Operation 			current 		       |  			180mA 			@ 3.5V (26 dBm Output,25°C).  			 110mA 			@ 3.5V (18 dBm Output,25°C). 		 |
|  			Output 			power accuracy 		       |  			+/- 			1dB 		                                                                                                                                                |  			Operation 			temp. 		         |  			 - 			20 °C  -  + 70  °C 		                                                   |
|  			Output 			power flatness 		       |  			+/- 			0.2dB 		                                                                                                                                              |  			Storage 			temp. 		           |  			- 			20 °C  -  + 85  °C 		                                                    |
|  			Receive 			sensitivity 		         |  			< 			-70dBm 		                                                                                                                                               |  			Working 			humidity 		        |  			< 			95% ( + 25 °C) 		                                                        |
|  			Read 			tag peak speed 		         |  			> 			50pcs/sec 		                                                                                                                                            |  			Communication 			interface 		 |  			TTL 			Uart interface 		                                                      |
|  			Operating 			time 		              |  			<100mS. 		                                                                                                                                                |  			Heat-dissipating 			method 		 |  			Air 			cooling(no need for out install cooling fin) 		                        |
|  			Communication 			baud rate 		     |  			115200 			bps(default and recommend)  			 38400bps 		                                                                                                           |  			   			 		                     |  			   			 		                                                                     |
|  			   			 		                         |  			   			 		                                                                                                                                                    |  			   			 		                     |  			   			 		                                                                     |

**DC characteristics (VIN =3.6V to 5V, VSS= 0V):**
|  			Parameter 		                 |  			Symbol 		 |  			Min. 		 |  			Typ. 		 |  			Max. 		 |  			Unit 		 |
|-----------------------------|----------|--------|--------|--------|--------|
|  			Average 			operating current 		 |  			IOC 		    |  			- 		    |  			280 		  |  			- 		    |  			mA 		   |
|  			Standby 			current 		           |  			ISB 		    |  			- 		    |  			- 		    |  			10 		   |  			mA 		   |
|  			Peak 			current 		              |  			Ipeak 		  |  			- 		    |  			300 		  |  			- 		    |  			mA 		   |

**DC Electrical Characteristics for Reader mode (VIN =5V, VSS= 0V):**
|  			Parameter 		                     |  			Symbol 		  |  			Min. 		 |  			Typ. 		 |  			Max. 		 |  			Unit 		 |
|---------------------------------|-----------|--------|--------|--------|--------|
|  			Enable 			  pin high (enabled) 		   |  			VEN(HI) 		 |  			0.9 		  |  			- 		    |  			VIN 		  |  			V 		    |
|  			Enable 			  pin low (disabled) 		   |  			VEN(LO) 		 |  			0 		    |  			- 		    |  			0.4 		  |  			V 		    |
|  			UART_RX 			  Input Low Voltage 		   |  			VIL 		     |  			-0.5 		 |  			- 		    |  			0.66 		 |  			V 		    |
|  			UART_RX 			  Input High Voltage 		  |  			VIH 		     |  			1.98 		 |  			- 		    |  			3.8 		  |  			V 		    |
|  			UART_TX 			  Output Low Voltage 		  |  			VOL 		     |  			- 		    |  			- 		    |  			0.5 		  |  			V 		    |
|  			UART_TX 			  Output High Voltage 		 |  			VOH 		     |  			2.2 		  |  			- 		    |  			- 		    |  			V 		    |


**AC characteristics (Ta =25℃, VIN =5V, VSS = 0V):**
|  			 Parameter 		                                                 |  			Symbol 		                               |     |  			Min. 		 |       |  			Typ. 		 |     |  			Max. 		 |  			Unit 		 |       |
|--------------------------------------------------------------|----------------------------------------|-----|--------|-------|--------|-----|--------|--------|-------|
|  			RF 			  Output Frequency 		                                      |  			Fc 		                                   |     |  			860 		  |       |  			- 		    |     |  			928 		  |  			Mhz 		  |       |
|  			RF 			  Output Power 		                                          |  			Pout 		                                 |     |  			  		    |       |  			25 		   |     |  			- 		    |  			dbm 		  |       |
|  			RF 			  Transmission setup time 		                               |  			TRF_OUT 		                              |     |  			- 		    |       |  			- 		    |     |  			0.5 		  |  			ms 		   |       |
|  			RF 			  Frequency error 		                                       |  			Ferror 		                               |     |  			- 		    |       |  			- 		    |     |  			1000 		 |  			ppm 		  |       |
|  			Interrogator 			  Transmit Spurious    Emissions, In-Band 		     |  			In 			accordance with local regulations 		 |     |        |       |        |     |        |  			- 		    |       |
|  			Interrogator 			  Transmit Spurious    Emissions, Out of-Band 		 |  			In 			accordance with local regulations 		 |     |        |       |        |     |        |  			- 		    |       |
|  			RF 			  Bandwidth 		                                             |  			In 			accordance with local regulations 		 |     |        |       |        |     |        |  			- 		    |       |
|  			Transmit 			  data rate 		                                       |  			DRate 		                                |     |  			- 		    |       |  			26K 		  |     |  			- 		    |  			bps 		  |       |
|  			Modulation 		                                                 |  			ASK 		                                  |     |        |       |        |     |        |        |       |
|  			Modulation 			  Type 		                                          |  			90% 			normally 		                         |     |        |       |        |     |        |        |       |
|  			Data Coding 		                                                |  			PIE 		                                  |     |        |       |        |     |        |        |       |
|  			Demodulation 		                                               |  			ASK 		                                  |     |        |       |        |     |        |        |       |
|  			Download 			  data rate 		                                       |  			DRate 		                                |  			- 		 |        |  			40K 		 |        |  			- 		 |        |        |  			bps 		 |
|  			Data 			  encoding 		                                            |  			FM0 		                                  |     |        |       |        |     |        |        |       |
