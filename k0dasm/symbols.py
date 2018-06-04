
class SymbolTable(object):
    def __init__(self, initial_symbols=None):
        if initial_symbols is None:
            initial_symbols = {}
        self.symbols = initial_symbols.copy()

    def generate(self, memory, start_address):
        self.generate_code_symbols(memory, start_address)
        self.generate_data_symbols(memory, start_address)

    def generate_code_symbols(self, memory, start_address):
        for address in range(start_address, len(memory)):
            if memory.is_call_target(address):
                if memory.is_instruction_start(address):
                    self.symbols[address] = ('sub_%04x' % address, '')
            elif memory.is_jump_target(address) or memory.is_entry_point(address):
                if memory.is_instruction_start(address):
                    self.symbols[address] = ('lab_%04x' % address, '')
        # XXX do not overwrite

    def generate_data_symbols(self, memory, start_address):
        data_addresses = set()
        modes_always_data = ('saddrp', 'saddr', 'addrp16', 'sfr', 'sfrp',)
        modes_sometimes_data = ('addr16', )
        # never data: addr16
        # todo: imm16

        for _, inst in memory.iter_instructions():
            for mode in modes_always_data:
                address = getattr(inst, mode, None)
                if address is not None:
                    data_addresses.add(address)

            for mode in modes_sometimes_data:
                address = getattr(inst, mode, None)
                if address is not None:
                    jumped = memory.is_jump_target(address)
                    called = memory.is_call_target(address)
                    if (not jumped) and (not called):
                        data_addresses.add(address)

        for address in data_addresses:
            if address not in self.symbols:
                self.symbols[address] = ('mem_%04x' % address, '')


NEC78K0_COMMON_SYMBOLS = {}
for i, address in enumerate(range(0x40, 0x7f, 2)):
    NEC78K0_COMMON_SYMBOLS[address] = ("callt_%d_vect" % i, "CALLT #%d" % i)

D78F0831Y_SYMBOLS = NEC78K0_COMMON_SYMBOLS.copy()
D78F0831Y_SYMBOLS.update(
{
    # hardware vectors
    0x0000: ("rst_vect", "RST"),
    0x0002: ("unused0_vect", "(unused)"),
    0x0004: ("intwdt_vect", "INTWDT"),
    0x0006: ("intp0_vect", "INTP0"),
    0x0008: ("intp1_vect", "INTP1"),
    0x000a: ("intp2_vect", "INTP2"),
    0x000c: ("intp3_vect", "INTP3"),
    0x000e: ("intp4_vect", "INTP4"),
    0x0010: ("intp5_vect", "INTP5"),
    0x0012: ("intp6_vect", "INTP6"),
    0x0014: ("intp7_vect", "INTP7"),
    0x0016: ("intser0_vect", "INTSER0"),
    0x0018: ("intsr0_vect", "INTSR0"),
    0x001a: ("intst0_vect", "INTST0"),
    0x001c: ("intcsi30_vect", "INTCSI30"),
    0x001e: ("intcsi31_vect", "INTCSI31"),
    0x0020: ("intiic0_vect", "INTIIC0"),
    0x0022: ("intc2_vect", "INTC2"),
    0x0024: ("intwtni0_vect", "INTWTNI0"),
    0x0026: ("inttm000_vect", "INTTM000"),
    0x0028: ("inttm010_vect", "INTTM010"),
    0x002a: ("inttm001_vect", "INTTM001"),
    0x002c: ("inttm011_vect", "INTTM011"),
    0x002e: ("intad00_vect", "INTAD00"),
    0x0030: ("intad01_vect", "INTAD01"),
    0x0032: ("unused1_vect", "(unused)"),
    0x0034: ("intwtn0_vect", "INTWTN0"),
    0x0036: ("intkr_vect", "INTKR"),
    0x0038: ("unused2_vect", "(unused)"),
    0x003a: ("unused3_vect", "(unused)"),
    0x003c: ("unused4_vect", "(unused)"),
    0x003e: ("brk_i_vect", "BRK_I"),
    # special function registers
    0xff00: ('P0_', 'Port 0'),
    0xff02: ('P2_', 'Port 2'),
    0xff03: ('P3_', 'Port 3'),
    0xff04: ('P4_', 'Port 4'),
    0xff05: ('P5_', 'Port 5'),
    0xff06: ('P6_', 'Port 6'),
    0xff07: ('P7_', 'Port 7'),
    0xff08: ('P8_', 'Port 8'),
    0xff09: ('P9_', 'Port 9'),
    0xff0a: ('CR000_', '16-bit timer capture/compare register 000'),
    0xff0c: ('CR010_', '16-bit timer capture/compare register 010'),
    0xff0e: ('TM00_', '16-bit timer counter 00'),
    0xff10: ('CR001_', '16-bit timer capture/compare register 001'),
    0xff12: ('CR011_', '16-bit timer capture/compare register 011'),
    0xff14: ('TM01_', '16-bit timer counter 01'),
    0xff17: ('ADCR00_', 'A/D conversion result register 00'),
    0xff18: ('RXB0_TXS0_', 'Transmit shift register 0 / Receive buffer register 0'),
    0xff1a: ('SIO30_', 'Serial shift register 30'),
    0xff1b: ('SIO31_', 'Serial shift register 31'),
    0xff1f: ('IIC0_', 'IIC shift register 0'),
    0xff20: ('PM0_', 'Port mode register 0'),
    0xff22: ('PM2_', 'Port mode register 2'),
    0xff23: ('PM3_', 'Port mode register 3'),
    0xff24: ('PM4_', 'Port mode register 4'),
    0xff25: ('PM5_', 'Port mode register 5'),
    0xff26: ('PM6_', 'Port mode register 6'),
    0xff27: ('PM7_', 'Port mode register 7'),
    0xff28: ('PM8_', 'Port mode register 8'),
    0xff29: ('PM9_', 'Port mode register 9'),
    0xff30: ('PU0_', 'Pull-up resistor option register 0'),
    0xff32: ('PU2_', 'Pull-up resistor option register 2'),
    0xff33: ('PU3_', 'Pull-up resistor option register 3'),
    0xff34: ('PU4_', 'Pull-up resistor option register 4'),
    0xff35: ('PU5_', 'Pull-up resistor option register 5'),
    0xff36: ('PU6_', 'Pull-up resistor option register 6'),
    0xff37: ('PU7_', 'Pull-up resistor option register 7'),
    0xff40: ('CKS_', 'Clock output selection register'),
    0xff41: ('WTNM0_', 'Watch timer mode control register 0'),
    0xff42: ('WDCS_', 'Watchdog timer clock selection register'),
    0xff47: ('MEM_', 'Memory expansion mode register'),
    0xff48: ('EGP_', 'External interrupt rising edge enable register'),
    0xff49: ('EGN_', 'External interrupt falling edge enable register'),
    0xff4a: ('FLAPL_', 'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xff4b: ('FLAPH_', 'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xff4c: ('FLMC_',  'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xff4d: ('FLRB_',  'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xff4e: ('FLWB_',  'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xff4f: ('FLTSL_', 'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xff60: ('TMC00_', '16-bit timer mode control register 00'),
    0xff61: ('PRM00_', 'Prescaler mode register 00'),
    0xff62: ('CRC00_', 'Capture/compare control register 00'),
    0xff63: ('TOC00_', '16-bit timer output control register 00'),
    0xff68: ('TMC01_', '16-bit timer mode control register 01'),
    0xff69: ('PRM01_', 'Prescaler mode register 01'),
    0xff6a: ('CRC01_', 'Capture/compare control register 01'),
    0xff6b: ('TOC01_', '16-bit timer output control register 01'),
    0xff80: ('ADM00_', 'A/D converter mode register 00'),
    0xff81: ('ADS00_', 'Analog input channel specification register 00'),
    0xff88: ('ADM01_', 'A/D converter mode register 01'),
    0xff89: ('ADS01_', 'Analog input channel specification register 01'),
    0xff8b: ('ADCR01_', 'A/D conversion result register 01'),
    0xffa0: ('ASIM0_', 'Asynchronous serial interface mode register 0'),
    0xffa1: ('ASIS0_', 'Asynchronous serial interface status register 0'),
    0xffa2: ('BRGC0_', 'Baud rate generator control register 0'),
    0xffa8: ('IICC0_', 'IIC control register 0'),
    0xffa9: ('IICS0_', 'IIC status register 0'),
    0xffaa: ('IICCL0_', 'IIC transfer clock selection register 0'),
    0xffab: ('SVA0_', 'Slave address register 0'),
    0xffb0: ('CSIM30_', 'Serial operation mode register 30'),
    0xffb8: ('CSIM31_', 'Serial operation mode register 31'),
    0xffc0: ('C2CT1_', 'Class 2 control register 1'),
    0xffc1: ('C2CT2_', 'Class 2 control register 2'),
    0xffc2: ('C2ST1_', 'Class 2 status register 1'),
    0xffc3: ('C2ST2_', 'Class 2 status register 2'),
    0xffc4: ('C2TXFIFO_', 'Class 2 transmit FIFO register'),
    0xffc5: ('C2PDR_', 'Class 2 rise time propagation delay correction register'),
    0xffc6: ('C2PDF_', 'Class 2 fall time propagation delay correction register'),
    0xffc7: ('C2CLK_', 'Class 2 clock selection register'),
    0xffd0: ('FFD0_', 'FFD0 (External Access Area)'),
    0xffd1: ('FFD1_', 'FFD1 (External Access Area'),
    0xffd2: ('FFD2_', 'FFD2 (External Access Area'),
    0xffd3: ('FFD3_', 'FFD3 (External Access Area'),
    0xffd4: ('FFD4_', 'FFD4 (External Access Area'),
    0xffd5: ('FFD5_', 'FFD5 (External Access Area'),
    0xffd6: ('FFD6_', 'FFD6 (External Access Area'),
    0xffd7: ('FFD7_', 'FFD7 (External Access Area'),
    0xffd8: ('FFD8_', 'FFD8 (External Access Area'),
    0xffd9: ('FFD9_', 'FFD9 (External Access Area'),
    0xffda: ('FFDA_', 'FFDA (External Access Area'),
    0xffdb: ('FFDB_', 'FFDB (External Access Area'),
    0xffdc: ('FFDC_', 'FFDC (External Access Area'),
    0xffdd: ('FFDD_', 'FFDD (External Access Area'),
    0xffde: ('FFDE_', 'FFDE (External Access Area'),
    0xffdf: ('FFDF_', 'FFDF (External Access Area'),
    0xffe0: ('IF0L_', 'Interrupt request flag register 0L'),
    0xffe1: ('IF0H_', 'Interrupt request flag register 0H'),
    0xffe2: ('IF1L_', 'Interrupt request flag register 1L'),
    0xffe3: ('IF1H_', 'Interrupt request flag register 1H'),
    0xffe4: ('MK0L_', 'Interrupt mask flag register 0L'),
    0xffe5: ('MK0H_', 'Interrupt mask flag register 0H'),
    0xffe6: ('MK1L_', 'Interrupt mask flag register 1L'),
    0xffe7: ('MK1H_', 'Internal mask flag register 1H'),
    0xffe8: ('PR0L_', 'Priority level specification flag register 0L'),
    0xffe9: ('PR0H_', 'Priority level specification flag register 0H'),
    0xffea: ('PR1L_', 'Priority level specification flag register 1L'),
    0xffeb: ('PR1H_', 'Priority level specification flag register 1H'),
    0xfff0: ('IMS_', 'Memory size switching register'),
    0xfff2: ('CLKM_', 'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xfff4: ('IXS_', 'Internal expansion RAM size switching register'),
    0xfff8: ('MM_', 'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xfff9: ('WDTM_', 'Watchdog timer mode register'),
    0xfffa: ('OSTS_', 'Oscillation stabilization time selection register'),
    0xfffb: ('PCC_', 'Processor clock control register'),
})
