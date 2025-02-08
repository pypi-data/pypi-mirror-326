from payloadinspector import get_bits_from_byte

def test_1():
    byte = 0b01010101
    bits = get_bits_from_byte(byte, 1, 3)
    assert bits == 0b101

def test_2():
    byte = 0b00110000
    bits = get_bits_from_byte(byte, 1, 3)
    assert bits == 0b011

def test_3():
    byte = 0b00110000
    bits = get_bits_from_byte(byte, 1, 4)
    assert bits == 0b0110

def test_4():
    byte = 0b00110011
    bits = get_bits_from_byte(byte, 0, 8)
    assert bits == 0b00110011

def test_5():
    byte = 0b00110011
    bits = get_bits_from_byte(byte, 4, 4)
    assert bits == 0b0011

def test_6():
    byte = 0b11111111
    bits = get_bits_from_byte(byte, 0, 8)
    assert bits == 0b11111111

def test_7():
    byte = 0b11111111
    bits = get_bits_from_byte(byte, 0, 0)
    assert bits == 0b0

def test_8():
    byte = 0b11111111
    bits = get_bits_from_byte(byte, 0, 1)
    assert bits == 0b1
