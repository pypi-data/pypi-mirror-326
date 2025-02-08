import pytest
from payloadinspector import format_output

def test_no_format():
    result = {'field1': 1, 'field2': 128, 'field3': 215}
    output = format_output(result)
    assert output == 'field1: 1, field2: 128, field3: 215'

def test_dec_format():
    result = {'field1': 1, 'field2': 128, 'field3': 215}
    output = format_output(result, 'dec')
    assert output == 'field1: 1, field2: 128, field3: 215'

def test_hex_format():
    result = {'field1': 1, 'field2': 128, 'field3': 215}
    output = format_output(result, 'hex')
    assert output == 'field1: 0x1, field2: 0x80, field3: 0xd7'

def test_bin_format():
    result = {'field1': 1, 'field2': 128, 'field3': 215}
    output = format_output(result, 'bin')
    assert output == 'field1: 0b1, field2: 0b10000000, field3: 0b11010111'

def test_one_element():
    result = {'field1': 1, 'field2': 128, 'field3': 215}
    output = format_output(result, 'field2')
    assert output == 'field2: 128'

def test_two_elements():
    result = {'field1': 1, 'field2': 128, 'field3': 215}
    output = format_output(result, 'field2, field3')
    assert output == 'field2: 128, field3: 215'

def test_different_formatting():
    result = {'field1': 1, 'field2': 128, 'field3': 215}
    output = format_output(result, 'field1: dec, field2:bin, field3:hex')
    assert output == 'field1: 1, field2: 0b10000000, field3: 0xd7'

def test_one_element_with_formatting():
    result = {'field1': 1, 'field2': 128, 'field3': 215}
    output = format_output(result, 'field2:bin')
    assert output == 'field2: 0b10000000'

def test_two_elements_with_formatting():
    result = {'field1': 1, 'field2': 128, 'field3': 215}
    output = format_output(result, 'field2:bin, field3:hex')
    assert output == 'field2: 0b10000000, field3: 0xd7'

def test_nonexisting_element():
    result = {'field1': 1, 'field2': 128, 'field3': 215}
    with pytest.raises(ValueError):
        format_output(result, 'field4')
