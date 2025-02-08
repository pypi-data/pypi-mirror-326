from dataclasses import dataclass
from typing import Iterator
import re

@dataclass
class BitFieldElement:
    name: str
    n_bits: int

    def __str__(self) -> str:
        return f'{self.name}: {self.n_bits}'

class BitField:
    def __init__(self, bitfield_elements: list) -> None:
        self._data = []
        for element in bitfield_elements:
            if isinstance(element, BitFieldElement):
                self._data.append(element)
            elif isinstance(element, tuple) and list(map(type, element)) == [str, int]:
                self._data.append(BitFieldElement(*element))
            else:
                raise TypeError(f'Unparsable bitfield element: {element}. Format is (\'name\', n_bits)')
            if self._data[-1].name in [e.name for e in self._data[:-1]]:
                raise ValueError(f'Bitfield element name occurs several times: {element[0]}')

    def __str__(self) -> str:
        return '\n'.join([str(e) for e in self._data])

    def __iter__(self) -> Iterator[BitFieldElement]:
        return self._data.__iter__()

    def __getitem__(self, key) -> BitFieldElement:
        return self._data.__getitem__(key)

    def __eq__(self, other):
        return len(self) == len(other) and \
               all([self[i] == other[i] for i in range(len(self))])

    def __len__(self) -> int:
        """Returns the number of elements in the BitField"""
        return self._data.__len__()

    @property
    def total_bits(self) -> int:
        """Total number of bits in BitField"""
        return sum([e.n_bits for e in self._data])

    @classmethod
    def from_string(cls, string: str):
        """
        Create a BitField object from a string.

        Args:
            string: String describing the format of the BitField as a list of tuples.
        """
        result = []
        current_tuple = []
        string = string.replace(' ', '').replace('\n', '').replace('[', '').replace(']', '')
        for token in string.split(','):
            if '(' in token:
                field_name = token.replace('(', '').replace(')', '').replace('\'', '').replace('"', '')
                current_tuple.append(field_name)
            else:
                n_bits = token.replace('(', '').replace(')', '')
                current_tuple.append(int(n_bits))
            if ')' in token:
                result.append(tuple(current_tuple))
                current_tuple = []
        return cls(result)

    @classmethod
    def from_c_source(cls, file_name: str, struct_name: str):
        """
        Create a BitField object based on a C struct bitfield.

        The struct must have a bit size for all elements.
        The data type and its size are ignored.

            Args:
                file_name: Filename of a C source file.
                struct_name: Name of the struct in the file to load.

            Returns:
                BitField: BitField object modeled after the C struct.
        """
        struct_text = cls._get_struct_text(file_name, struct_name)
        struct_elements = struct_text.split(':')
        elements = []
        for i in range(len(struct_elements) - 1):
            name = struct_elements[i].split()[-1]
            n_bits_string = struct_elements[i+1].split()[0].replace(';', '')
            try:
                n_bits = int(n_bits_string)
            except ValueError:
                raise ValueError(f'Could not parse bit size {n_bits_string}')
            elements.append((name, n_bits))
        if len(elements) < struct_text.count(';') - 1:
            raise ValueError('Some elements are missing bit size')
        return cls(elements)

    @classmethod
    def _get_struct_text(cls, file_name: str, struct_name: str) -> str:
        """
        Extract a given C struct from a source/header file.

            Args:
                file_name: Filename of a C source file.
                struct_name: Name of the struct in the file to load.

            Returns:
                str: The struct definition as a string.
        """
        with open(file_name, 'r') as file:
            content = file.read()
        # Try to find the struct defined in the format
        # struct <struct_name>
        # {
        #   ...
        # };
        struct_text = re.search(f'struct\\s*{struct_name}\\s*'+'{[^{]*}[^;]*;', content)
        if not struct_text:
            # Try to find the struct defined in the format
            # typedef struct
            # {
            #   ...
            # } <struct_name>;
            struct_text = re.search('{[^{]*}[^;]*'+f'{struct_name};', content)
        if not struct_text:
            raise ValueError(f'Could not find struct {struct_name}')
        struct_text = struct_text.group()
        return struct_text

class Payload:
    def __init__(self, data: list[int]) -> None:
        for i, value in enumerate(data):
            if not isinstance(value, int):
                raise TypeError(f'Payload value {i}: {value} is not an integer')
            if value < 0 or value > 255:
                raise ValueError(f'Fayload value {i}: {value} outside legal range [0, 255]')
        self._data = data

    def __iter__(self) -> Iterator[int]:
        return self._data.__iter__()

    def __getitem__(self, key: int) -> int:
        return self._data.__getitem__(key)

    def __eq__(self, other):
        return self._data == other._data

    def __len__(self) -> int:
        return self._data.__len__()

    @property
    def total_bits(self) -> int:
        return self.__len__() * 8

    @classmethod
    def from_string(cls, string: str):
        # Remove [',', '[', ']', ' ']
        string = string.replace(',', '').replace('[', '').replace(']', '').replace(' ', '')

        # Insert whitespaces at the correct position
        if string.startswith('0x'):
            string = ' '.join((string[i:i+4] for i in range(0, len(string), 4)))
        else:
            string = ' '.join((string[i:i+2] for i in range(0, len(string), 2)))

        return cls([int(i, 16) for i in string.split()])

def get_bits_from_byte(byte, start_bit: int, n_bits: int) -> int:
    """
    Extract a series of bits from a byte
    """
    return (byte >> (8-start_bit-n_bits)) & ((1 << n_bits) - 1)

def format_output(result: dict[str, int], format=''):
    output_string = ''
    # Create list of (name, encoding) tuples
    if format == '' or format == 'dec':
        elements = [(name, 'dec') for name in result.keys()]
    elif format == 'hex' or format == 'bin':
        elements = [(name, format) for name in result.keys()]
    else:
        elements = []
        element_formats = format.split(',')
        for e in element_formats:
            components = e.split(':')
            name = components[0].replace(' ', '')
            encoding = 'dec' if len(components) == 1 else components[1].replace(' ', '')
            elements.append((name, encoding))

    # Add each element with correct encoding
    for e in elements:
        element_name = e[0]
        encoding = e[1]
        if element_name not in result.keys():
            raise ValueError(f'Element name in format string does not exist in bitfield: {element_name}')
        if encoding == 'dec':
            output_string += f'{element_name}: {result[element_name]}, '
        elif encoding == 'hex':
            output_string += f'{element_name}: {hex(result[element_name])}, '
        elif encoding == 'bin':
            output_string += f'{element_name}: {bin(result[element_name])}, '
    return output_string.rstrip(', ')


def get_field_values(bit_field: BitField, payload: Payload) -> dict[str, int]:
    """
    Find the value of each element in a BitField.
    """
    values = {}
    current_byte = 0
    bits_left_in_current_byte = 8
    for field in bit_field:
        current_field_value = 0
        unread_bits_in_current_field = field.n_bits
        while unread_bits_in_current_field > 0:
            bits_to_read = min(bits_left_in_current_byte, unread_bits_in_current_field)
            temp_field_value = get_bits_from_byte(payload[current_byte], 8-bits_left_in_current_byte, bits_to_read)
            unread_bits_in_current_field -= bits_to_read
            bits_left_in_current_byte -= bits_to_read
            current_field_value += temp_field_value << unread_bits_in_current_field
            if bits_left_in_current_byte == 0:
                current_byte += 1
                bits_left_in_current_byte = 8
        values[field.name] = current_field_value
    return values
