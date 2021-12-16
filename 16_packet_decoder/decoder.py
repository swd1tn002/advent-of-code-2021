import os
from typing import List, Dict, Set
from collections import namedtuple

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


class Packet:
    def __init__(self, bytes: str):
        # The first three bits encode the packet version.
        self.version = int(bytes[:3], 2)

        self.bytes = bytes

    def __repr__(self):
        return self.bytes[:10]

    def __eq__(self, __o: object) -> bool:
        return type(self) == type(__o) and self.sub_packets() == __o.sub_packets()

    def length(self) -> int:
        raise Exception('Must be implemented in subclass')

    def calculate(self) -> int:
        raise Exception('Must be implemented in subclass')

    def sub_packets(self) -> List['Packet']:
        raise Exception('Must be implemented in subclass')

    @staticmethod
    def parse(binary: str) -> 'Packet':
        types = [Sum, Product, Min, Max, Literal, Greater, Lower, Equal]
        type_id = int(binary[3:6], 2)
        return types[type_id](binary)


class Operator(Packet):
    def sub_values(self) -> List[int]:
        return [v.calculate() for v in self.sub_packets()]

    def sub_packets(self) -> List['Packet']:
        if self.length_type_id() == '0':
            """
            If the length type ID is 0, then the next 15 bits are a
            number that represents the total length in bits of the
            sub-packets contained by this packet.
            """
            payload_length = int(self.bytes[7: 7 + 15], 2)
            payload = self.bytes[7 + 15: 7 + 15 + payload_length]
            sub_count = 99999
        else:
            """
            If the length type ID is 1, then the next 11 bits are a
            number that represents the number of sub-packets immediately contained by this packet.
            """
            sub_count = int(self.bytes[7: 7 + 11], 2)
            payload = self.bytes[7 + 11:]

        packets = []
        while payload != '' and sub_count > 0:
            sub = Packet.parse(payload)
            packets.append(sub)
            payload = payload[sub.length():]
            sub_count -= 1

        return packets

    def length(self) -> int:
        return 7 + self.size_header_length() + sum(x.length() for x in self.sub_packets())

    def length_type_id(self):
        return self.bytes[6]

    def size_header_length(self):
        """
        If the length type ID is 0, then the next 15 bits are a number that represents the total length
        in bits of the sub-packets contained by this packet.
        If the length type ID is 1, then the next 11 bits are a number that represents the number of 
        sub-packets immediately contained by this packet.
        """
        return 11 if self.length_type_id() == '1' else 15

    def sub_packet_length(self):
        # operator packages only
        size_bits = self.size_header_length()
        return int(self.bytes[7: 7+size_bits], 2)


class Literal(Packet):
    """
    Literal value packets encode a single binary number.
    """

    def calculate(self) -> int:
        prefix_index = 6
        literal = ''
        while True:
            literal += self.bytes[prefix_index+1: prefix_index+5]
            # Each group is prefixed by a 1 bit except the last group,
            # which is prefixed by a 0 bit.
            if self.bytes[prefix_index] == '1':
                prefix_index += 5
            else:
                break
        return int(literal, 2)

    def length(self) -> int:
        prefix_index = 6
        while self.bytes[prefix_index] == '1':
            prefix_index += 5
        return prefix_index + 5

    def sub_packets(self) -> List['Packet']:
        return []


class Sum(Operator):
    def calculate(self) -> int:
        sub_values = [v.calculate() for v in self.sub_packets()]
        return sum(self.sub_values())


class Product(Operator):
    def calculate(self) -> int:
        sub_values = [v.calculate() for v in self.sub_packets()]
        product = 1
        for v in sub_values:
            product *= v
        return product


class Min(Operator):
    def calculate(self) -> int:
        sub_values = [v.calculate() for v in self.sub_packets()]
        return min(self.sub_values())


class Max(Operator):
    def calculate(self) -> int:
        sub_values = [v.calculate() for v in self.sub_packets()]
        return max(self.sub_values())


class Greater(Operator):
    def calculate(self) -> int:
        first, second, *_ = self.sub_values()
        return int(first > second)


class Lower(Operator):
    def calculate(self) -> int:
        first, second, *_ = self.sub_values()
        return int(first < second)


class Equal(Operator):
    def calculate(self) -> int:
        first, second, *_ = self.sub_values()
        return int(first == second)


def read_puzzle_input(filename=INPUT_FILE) -> str:
    """
    The transmission was sent using the Buoyancy Interchange Transmission System (BITS),
    a method of packing numeric expressions into a binary sequence. Your submarine's 
    computer has saved the transmission in hexadecimal (your puzzle input).
    """
    with open(filename) as file:
        return file.read()


def hex2bin(hex: str) -> str:
    """
    The first step of decoding the message is to convert the hexadecimal representation into
    binary. Each character of hexadecimal corresponds to four bits of binary data.
    """
    return format(int(hex, 16), 'b')


def sum_of_versions(packet: Packet) -> int:
    return packet.version + sum(sum_of_versions(sub) for sub in packet.sub_packets())


if __name__ == '__main__':
    bytes = hex2bin(read_puzzle_input())
    version_sum = 0

    root = Packet.parse(bytes)
    # print(sum_of_versions(root))
    print(root.calculate())
