from payloadinspector import get_field_values, BitField, Payload

class Case:
    def __init__(self, bitfield: BitField, payload: Payload, correct_result: dict[str, int]):
        self.bitfield = bitfield
        self.payload = payload
        self.correct_result = correct_result


def test_case_1():
    # 0001 0010 1010 1100
    # 000 10010 101011 00
    #   0    18     43  0
    run_test_case(Case(BitField([('field1', 3), ('field2', 5), ('field3', 6), ('field4', 2)]),
                       Payload([0x12, 0xac]),
                       {'field1': 0, 'field2': 18, 'field3': 43, 'field4': 0}))

def test_case_2():
    # 0001 0010 1010 1100
    # 000100101 0101 100
    #        37     5   4
    run_test_case(Case(BitField([('field1', 9), ('field2', 4), ('field3', 3)]),
                       Payload([0x12, 0xac]),
                       {'field1': 37, 'field2': 5, 'field3': 4}))

def test_case_3():
    # 0001 0010 1010 1100
    # 000 10010101011 00
    #   0        1195  0
    run_test_case(Case(BitField([('field1', 3), ('field2', 11), ('field3', 2)]),
                       Payload([0x12, 0xac]),
                       {'field1': 0, 'field2': 1195, 'field3': 0}))


def run_test_case(test: Case):
    assert get_field_values(test.bitfield, test.payload) == test.correct_result
