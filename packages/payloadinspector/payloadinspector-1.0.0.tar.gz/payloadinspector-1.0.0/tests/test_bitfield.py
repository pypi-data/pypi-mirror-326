import pytest
from payloadinspector import BitField, BitFieldElement

def test_init_with_bitfieldelements():
    elements = [BitFieldElement('field1', 1),
                BitFieldElement('field2', 2),
                BitFieldElement('field3', 3),
                BitFieldElement('field4', 4)]
    bitfield = BitField(elements)

def test_init_with_tuples():
    elements = [('field1', 1),
                ('field2', 2),
                ('field3', 3),
                ('field4', 4)]
    bitfield = BitField(elements)
    for i in range(len(elements)):
        assert isinstance(bitfield[i], BitFieldElement)

def test_init_with_mixed_args():
    elements = [('field1', 1),
                BitFieldElement('field2', 2),
                ('field3', 3),
                BitFieldElement('field4', 4)]
    bitfield = BitField(elements)
    for i in range(len(elements)):
        assert isinstance(bitfield[i], BitFieldElement)

def test_init_with_string_n_bits():
    elements = [('field1', 'string')]
    with pytest.raises(TypeError):
        bitfield = BitField(elements)

def test_init_with_float_n_bits():
    elements = [('field1', 1.2)]
    with pytest.raises(TypeError):
        bitfield = BitField(elements)

def test_init_with_int_name():
    elements = [(1, 1)]
    with pytest.raises(TypeError):
        bitfield = BitField(elements)

def test_init_with_duplicate_names():
    elements = [('field1', 1), ('field1', 1)]
    with pytest.raises(ValueError):
        bitfield = BitField(elements)

def test_iteration():
    elements = [('field1', 1),
                ('field2', 2),
                ('field3', 3),
                ('field4', 4)]
    bitfield = BitField(elements)
    assert [n.name for n in bitfield] == ['field1', 'field2', 'field3', 'field4']
    assert [n.n_bits for n in bitfield] == [1, 2, 3, 4]

def test_subscripting():
    elements = [('field1', 1),
                ('field2', 2),
                ('field3', 3),
                ('field4', 4)]
    bitfield = BitField(elements)
    for i in range(4):
        assert bitfield[i] == BitFieldElement(f'field{i+1}', i+1)

def test_equal():
    elements1 = [('field1', 1),
                 ('field2', 2),
                 ('field3', 3),
                 ('field4', 4)]
    elements2 = [BitFieldElement('field1', 1),
                 BitFieldElement('field2', 2),
                 BitFieldElement('field3', 3),
                 BitFieldElement('field4', 4)]
    bf1 = BitField(elements1)
    bf2 = BitField(elements2)
    assert bf1 == bf2

def test_unequal_sizes():
    elements1 = [('field1', 1),
                 ('field2', 2),
                 ('field3', 3),
                 ('field4', 4)]
    elements2 = [BitFieldElement('field1', 1),
                 BitFieldElement('field2', 2),
                 BitFieldElement('field3', 3)]
    bf1 = BitField(elements1)
    bf2 = BitField(elements2)
    assert bf1 != bf2

def test_unequal_bits():
    elements1 = [('field1', 1),
                 ('field2', 2),
                 ('field3', 3),
                 ('field4', 4)]
    elements2 = [BitFieldElement('field1', 100),
                 BitFieldElement('field2', 2),
                 BitFieldElement('field3', 3),
                 BitFieldElement('field4', 4)]
    bf1 = BitField(elements1)
    bf2 = BitField(elements2)
    assert bf1 != bf2

def test_unequal_names():
    elements1 = [('field1', 1),
                 ('field2', 2),
                 ('field3', 3),
                 ('field4', 4)]
    elements2 = [BitFieldElement('field_one', 1),
                 BitFieldElement('field2', 2),
                 BitFieldElement('field3', 3),
                 BitFieldElement('field4', 4)]
    bf1 = BitField(elements1)
    bf2 = BitField(elements2)
    assert bf1 != bf2

def test_len():
    elements = [('field1', 1),
                ('field2', 2),
                ('field3', 3),
                ('field4', 4)]
    bitfield = BitField(elements)
    assert len(bitfield) == 4

def test_total_bits():
    elements = [('field1', 1),
                ('field2', 2),
                ('field3', 3),
                ('field4', 4)]
    bitfield = BitField(elements)
    assert bitfield.total_bits == 10

def string_initializer_test(string: str):
    elements = [('field1', 1),
                ('field2', 2),
                ('field3', 3),
                ('field4', 4)]
    bitfield_from_list = BitField(elements)
    bitfield_from_string = BitField.from_string(string)

    assert bitfield_from_list == bitfield_from_string

def test_string_initialization_single_quotes():
    string = "('field1', 1), ('field2', 2), ('field3', 3), ('field4', 4)"
    string_initializer_test(string)

def test_string_initialization_double_quotes():
    string = '("field1", 1), ("field2", 2), ("field3", 3), ("field4", 4)'
    string_initializer_test(string)

def test_string_initialization_no_quotes():
    string = '(field1, 1), (field2, 2), (field3, 3), (field4, 4)'
    string_initializer_test(string)

def test_string_initialization_without_whitespace():
    string = "('field1', 1),('field2', 2),('field3', 3),('field4', 4)"
    string_initializer_test(string)

def test_string_initialization_with_square_brackets():
    string = "[('field1', 1), ('field2', 2), ('field3', 3), ('field4', 4)]"
    string_initializer_test(string)

def test_string_initialization_with_newlines():
    string = "[('field1', 1),\n('field2', 2), \n('field3', 3),\n ('field4', 4)]"
    string_initializer_test(string)

def assert_equal_bitfields(bf1: BitField, bf2: BitField):
    '''Helper function to find which elements if any dont match'''
    assert len(bf1) == len(bf2)
    for i in range(len(bf1)):
        assert bf1[i].name == bf2[i].name
        assert bf1[i].n_bits == bf2[i].n_bits

def test_header_file_message():
    bitfield_from_file = BitField.from_c_source('tests/header.h', 'message')
    true_bitfield = BitField([('field1', 1), ('field2', 2), ('big_value', 32), ('field3', 3)])
    assert_equal_bitfields(bitfield_from_file, true_bitfield)

def test_header_file_message2():
    bitfield_from_file = BitField.from_c_source('tests/header.h', 'message2')
    true_bitfield = BitField([('field4', 4), ('field5', 5)])
    assert_equal_bitfields(bitfield_from_file, true_bitfield)

def test_header_file_message3():
    bitfield_from_file = BitField.from_c_source('tests/header.h', 'message3')
    true_bitfield = BitField([('field6', 6), ('field7', 7)])
    assert_equal_bitfields(bitfield_from_file, true_bitfield)

def test_header_file_message4():
    bitfield_from_file = BitField.from_c_source('tests/header.h', 'message4')
    true_bitfield = BitField([('field8', 8), ('field9', 9)])
    assert_equal_bitfields(bitfield_from_file, true_bitfield)

def test_header_file_message5():
    bitfield_from_file = BitField.from_c_source('tests/header.h', 'message5')
    true_bitfield = BitField([('field1', 1), ('field2', 2)])
    assert_equal_bitfields(bitfield_from_file, true_bitfield)

def test_header_file_message6():
    bitfield_from_file = BitField.from_c_source('tests/header.h', 'message6')
    true_bitfield = BitField([('field1', 1), ('field2', 2)])
    assert_equal_bitfields(bitfield_from_file, true_bitfield)

def test_missing_struct():
    with pytest.raises(ValueError):
        BitField.from_c_source('tests/header.h', 'message_does_not_exist')

def test_header_file_packed_struct():
    bitfield_from_file = BitField.from_c_source('tests/header.h', 'packed_struct')
    true_bitfield = BitField([('field1', 1), ('field2', 2)])
    assert_equal_bitfields(bitfield_from_file, true_bitfield)

def test_header_file_packed_struct_wo_whitespace():
    bitfield_from_file = BitField.from_c_source('tests/header.h', 'packed_struct_wo_whitespace')
    true_bitfield = BitField([('field1', 1), ('field2', 2)])
    assert_equal_bitfields(bitfield_from_file, true_bitfield)

def test_header_file_missing_bit_number():
    with pytest.raises(ValueError):
        BitField.from_c_source('tests/header.h', 'struct_with_missing_bit_number')

def test_header_file_missing_bit_number2():
    with pytest.raises(ValueError, match='Some elements are missing bit size'):
        BitField.from_c_source('tests/header.h', 'struct_with_missing_bit_number2')

def test_header_file_defined_bit_number():
    with pytest.raises(ValueError, match='Could not parse bit size.*'):
        BitField.from_c_source('tests/header.h', 'struct_with_defined_bit_number')
