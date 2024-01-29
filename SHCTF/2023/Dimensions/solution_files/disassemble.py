class VMParser:
    """
    A virtual machine (VM) parser for executing and decoding the `Dimensions` custom instruction sets.
    """
    def __init__(self):
        self.vm_rodata = {}
        self.registers = {
            "reg_30": 0x0,
            "reg_38": 0x0,
            "reg_90": 0x0,
            "reg_98": 0x0,
        }
        self.opcodes = self._initialize_opcodes()
    
    @staticmethod
    def reverse_qword_order(num):
        hex_str = format(num, '016x')
        return ''.join(reversed([hex_str[i:i+2] for i in range(0, len(hex_str), 2)]))

    def _initialize_opcodes(self):
        return {
            0x00: ("mov: reg_30, 8", self.parse_ops),
            0x01: ("mov: reg_38, 8", self.parse_ops),
            0x02: ("xor: reg_30, reg_38, 8", self.parse_ops),
            0x03: ("add: reg_30, reg_38, 8", self.parse_ops),
            0x04: ("load: reg_90, reg_30, 8", self.parse_ops),
            0x05: ("load: reg_98, reg_30, 8", self.parse_ops), 
            0x06: ("mov: reg_38, reg_90, 8", self.parse_ops),
            0x07: ("mov: reg_38, reg_98, 8", self.parse_ops),
            0x08: ("cmp: reg_30, reg_38, 8", self.parse_ops),
            0x09: ("print(Correct key!)", None),
            0x0a: ("exit()", None),
        }
    
    def get_addr_value(self, instructions, idx):
        value = 0
        addr = int(instructions[idx+2: idx+4], 16)
        try:
            round_addr = addr & 0xf0
            offset = addr - round_addr
            offset = 16 if offset > 0 else 0
            value = self.vm_rodata[round_addr][offset: offset+16]
            value = int(value, 16)
        except:
            value = addr
        return hex(addr), value, 2

    def parse_ops(self, instructions, idx, descr):
        steps = 0
        ops_params = descr.split(': ')
        ops = ops_params[0]
        params = ops_params[1].split(', ')

        reg_1 = params[0]
        reg_2 = params[1] if len(params) == 3 else None
        size = int(params[-1])
        if ops == "xor":
            self.registers[reg_1] = self.registers[reg_1] ^ self.registers[reg_2]
        elif ops == "add":
            self.registers[reg_1] = self.registers[reg_1] + self.registers[reg_2]
        elif ops == "load":
            self.registers[reg_1] = self.registers[reg_2]
        elif ops == "mov":
            if len(params) == 2:
            # get value from address 
                addr, value, steps = self.get_addr_value(instructions, idx)
            else:
                value = self.registers[reg_2]
            self.registers[reg_1] = value
            
        descr = f"{ops}({reg_1}, {addr if reg_2 is None else reg_2}, {size})\n {reg_1} = {hex(self.registers[reg_1])}\n"

        if ops == "cmp":
            # int to ascii
            reg_1 = format(self.registers[reg_1], 'x')
            reg_1 = bytes.fromhex(reg_1).decode("ascii")

            reg_2 = format(self.registers[reg_2], 'x')
            reg_2 = bytes.fromhex(reg_2).decode("ascii")

            descr += f"cmp({reg_1}, {reg_2})\n"

        return descr, steps

    def execute(self, instructions):
        i = 0
        while i < len(instructions):
            descr = ""
            inst = int(instructions[i: i+2], 16)
            if inst in self.opcodes:
                descr += self.opcodes[inst][0]
                if self.opcodes[inst][1]:
                    descr, skips = self.opcodes[inst][1](instructions, i, descr)
                    i += skips
            else:
                descr += f"Unknown instruction: {hex(inst)}"
            print(descr)
            i = i+ 2

    def load_instructions(self, vm_instructions):
        rev_instr = ''.join([self.reverse_qword_order(x) for x in vm_instructions])
        self.vm_rodata[0x70] = rev_instr

    def load_obfuscated_strings(self, obfuscated_string, address, key=0x5454545454545454):
        processed_string = [self.reverse_qword_order(x ^ key) for x in obfuscated_string]
        self.vm_rodata[address] = ''.join(processed_string)

# Example usage
parser = VMParser()
parser.load_instructions([0x1800040240011000, 0x0806600005034801, 0x0a09080768000806])
parser.load_obfuscated_strings([0x655F1115751E6EA9, 0x4141414141414241], 0x10)
parser.load_obfuscated_strings([0x17686A53215D26FA, 0x3C7E094F1E021948], 0x40)
parser.execute(parser.vm_rodata[0x70])