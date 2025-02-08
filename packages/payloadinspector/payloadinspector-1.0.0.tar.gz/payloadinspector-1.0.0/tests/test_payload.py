import pytest
from payloadinspector import Payload

def test_init_with_ints():
    data = [10, 128, 255]
    payload = Payload(data)
    assert all(payload[i] == data[i] for i in range(3))

def test_init_with_hex():
    data = [0x0a, 0x80, 0xff]
    payload = Payload(data)
    assert all(payload[i] == data[i] for i in range(3))

def test_init_with_string():
    data = [0x0a, 'value', 0xff]
    with pytest.raises(TypeError):
        payload = Payload(data)

def test_init_out_of_range():
    data = [0x0a, 300, 0xff]
    with pytest.raises(ValueError):
        payload = Payload(data)

def test_iteration():
    data = [0x0a, 0x80, 0xff]
    payload = Payload(data)
    assert [val for val in payload] == data

def test_equal():
    data1 = [10, 128, 255]
    payload1 = Payload(data1)
    data2 = [0x0a, 0x80, 0xff]
    payload2 = Payload(data2)
    assert payload1 == payload2

def test_unequal_size():
    data1 = [10, 128, 255]
    payload1 = Payload(data1)
    data2 = [0x0a, 0x80]
    payload2 = Payload(data2)
    assert payload1 != payload2

def test_unequal_value():
    data1 = [10, 128, 255]
    payload1 = Payload(data1)
    data2 = [0x0a, 0x80, 0x00]
    payload2 = Payload(data2)
    assert payload1 != payload2

def test_len():
    data = [0x0a, 0x80, 0xff]
    payload = Payload(data)
    assert len(payload) == 3

def test_total_bits():
    data = [0x0a, 0x80, 0xff]
    payload = Payload(data)
    assert payload.total_bits == 24

def string_initializer_test(string):
    data = [0x0a, 0x80, 0xff]
    payload_from_list = Payload(data)
    payload_from_string = Payload.from_string(string)

    assert payload_from_list == payload_from_string

def test_string_initialization_0x():
    string = "0x0a 0x80 0xff"
    string_initializer_test(string)

def test_string_initialization_no_0x():
    string = "0a 80 ff"
    string_initializer_test(string)

def test_string_initialization_0x_with_comma():
    string = "0x0a, 0x80, 0xff"
    string_initializer_test(string)

def test_string_initialization_with_comma():
    string = "0a, 80, ff"
    string_initializer_test(string)

def test_string_initialization_0x_with_comma_and_square_brackets():
    string = "[0x0a, 0x80, 0xff]"
    string_initializer_test(string)

def test_string_initialization_with_comma_and_square_brackets():
    string = "[0a, 80, ff]"
    string_initializer_test(string)

def test_string_initialization_0x_no_whitespace():
    string = "0x0a0x800xff"
    string_initializer_test(string)

def test_string_initialization_no_0x_no_whitespace():
    string = "0a80ff"
    string_initializer_test(string)
