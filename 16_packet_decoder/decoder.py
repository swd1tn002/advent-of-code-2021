import os
from typing import List, Dict, Set, Tuple
from collections import namedtuple

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


class Packet:
    def __init__(self, bytes: str):
        # The first three bits encode the packet version.
        self.version = int(bytes[:3], 2)

        self.bytes = bytes
        self.sub_packets = self._sub_packets()

    def __repr__(self):
        return self.bytes[:10]

    def __eq__(self, __o: object) -> bool:
        return type(self) == type(__o) and self.sub_packets == __o._sub_packets

    def calculate(self) -> int:
        raise Exception('Must be implemented in subclass')

    def _sub_packets(self) -> List['Packet']:
        raise Exception('Must be implemented in subclass')

    @staticmethod
    def parse(binary: str) -> 'Packet':
        types = [Sum, Product, Min, Max, Literal, Greater, Lower, Equal]
        type_id = int(binary[3:6], 2)
        return types[type_id](binary)


class Operator(Packet):
    """
    An operator performs some calculation on one or more sub-packets
    contained within.

    An operator packet contains one or more packets. To indicate which subsequent
    binary data represents its sub-packets, an operator packet can use one of two
    modes indicated by the bit immediately after the packet header; this is 
    called the length type ID:

    * If the length type ID is 0, then the next 15 bits are a number that represents
      the total length in bits of the sub-packets contained by this packet. 
    * If the length type ID is 1, then the next 11 bits are a number that represents
      the number of sub-packets immediately contained by this packet.
    """

    def _sub_packets(self) -> List['Packet']:
        payload = self._payload()
        packets = []
        if self._length_type() == 'bits':
            while payload != '':
                sub = Packet.parse(payload)
                packets.append(sub)
                payload = payload[len(sub):]
        else:
            for i in range(self._subpacket_size()):
                sub = Packet.parse(payload)
                packets.append(sub)
                payload = payload[len(sub):]

        return packets

    def sub_values(self) -> List[int]:
        return [v.calculate() for v in self.sub_packets]

    def __len__(self) -> int:
        """
        The length of this binary sequence in bits.
        """
        return 7 + self._size_header_length() + sum(len(x) for x in self.sub_packets)

    def _subpacket_size(self) -> str:
        start = 7
        end = start + self._size_header_length()
        return int(self.bytes[start: end], 2)

    def _payload(self) -> str:
        start = 7 + self._size_header_length()
        if self._length_type() == 'bits':
            size_binary = self.bytes[7:7+15]
            size = int(size_binary, 2)
            return self.bytes[start: start + size]
        else:
            return self.bytes[start:]

    def _size_header_length(self):
        return 15 if self._length_type() == 'bits' else 11

    def _length_type(self) -> str:
        """
        Returns either 'bits' or 'packets' depending on the value
        """
        return 'bits' if self.bytes[6] == '0' else 'packets'


class Literal(Packet):
    """
    Literal value packets encode a single binary number.
    """

    def calculate(self) -> int:
        return int(''.join(self.groups()), 2)

    def payload(self):
        """
        Returns the payload content after 6 header bits.
        """
        return self.bytes[6:]

    def __len__(self) -> int:
        """
        The length of this binary sequence in bits.
        """
        headers = 6
        return headers + sum(1 + len(c) for c in self.groups())

    def groups(self):
        """
        Each group is prefixed by a 1 bit except the last group,
        which is prefixed by a 0 bit.
        """
        payload = self.payload()
        for i in range(0, len(payload), 5):
            prefix = payload[i]
            group = payload[i + 1: i + 5]
            yield group
            if prefix == '0':
                return

    def _sub_packets(self) -> List['Packet']:
        return []

    def __eq__(self, __o: object) -> bool:
        return type(self) == type(__o) and self.calculate() == __o.calculate()


class Sum(Operator):
    def calculate(self) -> int:
        return sum(self.sub_values())


class Product(Operator):
    def calculate(self) -> int:
        product = 1
        for v in self.sub_values():
            product *= v
        return product


class Min(Operator):
    def calculate(self) -> int:
        return min(self.sub_values())


class Max(Operator):
    def calculate(self) -> int:
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
    return packet.version + sum(sum_of_versions(sub) for sub in packet.sub_packets)


if __name__ == '__main__':
    bytes = hex2bin(read_puzzle_input())

    # Part 1
    version_sum = 0
    root = Packet.parse(bytes)
    print(f'Part 1: sum of versions is {sum_of_versions(root)}')

    # Part 2
    print(f'Part 2: calculated value is {root.calculate()}')
