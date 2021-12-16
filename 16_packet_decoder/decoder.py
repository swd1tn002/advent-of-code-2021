
import os
from typing import List, Dict, Set
from collections import namedtuple

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


class Packet:
    def __init__(self, bytes: str):
        self.bytes = bytes

    def version(self) -> int:
        """
        The first three bits encode the packet version.
        """
        return int(self.bytes[:3], 2)

    def type_id(self) -> int:
        """
        The next three bits after version encode the packet type ID.
        """
        return int(self.bytes[3:6], 2)

    def literal_value(self) -> int:
        """
        Packets with type ID 4 represent a literal value. Literal value
        packets encode a single binary number.
        """
        if self.type_id() != 4:
            raise f'Incorrect type {self.type_id()} for literal value!'

        prefix_index = 6
        literal = ''
        while True:
            literal += self.bytes[prefix_index+1: prefix_index+5]
            if self.bytes[prefix_index] == '1':
                # Each group is prefixed by a 1 bit except the last group,
                # which is prefixed by a 0 bit.
                prefix_index += 5
            else:
                break
        return int(literal, 2)

    def get_operator(self) -> None:
        if self.type_id() == 4:
            raise f'Incorrect type {self.type_id()} for operator!'
        return None

    def sub_packets(self) -> List['Packet']:
        if self.type_id() == 4:
            return []

        length_type_id = self.bytes[6]

        if length_type_id == '0':
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
        while len(payload) > 3 and sub_count > 0:
            sub = Packet(payload)
            packets.append(sub)
            payload = payload[sub.length():]
            sub_count -= 1

        return packets

    def size_header_length(self):
        # operator packages only
        return 11 if self.bytes[6] == '1' else 15

    def sub_packet_length(self):
        # operator packages only
        size_bits = self.size_header_length()
        return int(self.bytes[7: 7+size_bits], 2)

    def __repr__(self):
        return str(self.type_id())

    def __eq__(self, __o: object) -> bool:
        return self.type_id() == __o.type_id() and self.sub_packets() == __o.sub_packets()

    def length(self) -> int:
        if self.type_id() == 4:
            # literal packages
            prefix_index = 6
            while self.bytes[prefix_index] == '1':
                prefix_index += 5
            return prefix_index + 5
        else:
            # operator packages
            return 7 + self.size_header_length() + sum(x.length() for x in self.sub_packets())

    def calculate(self) -> int:
        sub_values = [v.calculate() for v in self.sub_packets()]
        if self.type_id() == 0:
            return sum(sub_values)
        if self.type_id() == 1:
            product = 1
            for v in sub_values:
                product *= v
            return product
        elif self.type_id() == 2:
            return min(sub_values)
        elif self.type_id() == 3:
            return max(sub_values)
        elif self.type_id() == 4:
            return self.literal_value()
        elif self.type_id() == 5:
            return 1 if sub_values[0] > sub_values[1] else 0
        elif self.type_id() == 6:
            return 1 if sub_values[0] < sub_values[1] else 0
        elif self.type_id() == 7:
            return 1 if sub_values[0] == sub_values[1] else 0


def read_puzzle_input(filename=INPUT_FILE) -> str:
    """
    The transmission was sent using the Buoyancy Interchange Transmission System (BITS), a method of packing numeric expressions into a binary sequence. Your submarine's computer has saved the transmission in hexadecimal (your puzzle input).
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
    return packet.version() + sum(sum_of_versions(sub) for sub in packet.sub_packets())


if __name__ == '__main__':
    bytes = hex2bin(read_puzzle_input())
    version_sum = 0

    root = Packet(bytes)
    # print(sum_of_versions(root))
    print(root.calculate())
