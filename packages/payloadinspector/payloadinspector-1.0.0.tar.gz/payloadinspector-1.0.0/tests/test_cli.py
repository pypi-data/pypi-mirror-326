import subprocess


def run_cli_command(cmd_and_args: list[str]):
    result = subprocess.run(cmd_and_args, capture_output=True, text=True)
    return result.returncode, result.stdout


def test_version():
    retcode, output = run_cli_command(['payloadinspector', '--version'])
    assert retcode == 0
    assert output == 'payloadinspector 1.0.0\n'

def test_standard_arguments():
    retcode, output = run_cli_command(['payloadinspector',
                              '-b', "('field1', 4), ('field2', 4), ('field3', 8)",
                              '-p', "0xac 0x11"])
    assert retcode == 0
    assert output == 'field1: 10, field2: 12, field3: 17\n'

def test_standard_arguments_with_comma():
    retcode, output = run_cli_command(['payloadinspector',
                              '-b', "('field1', 4), ('field2', 4), ('field3', 8)",
                              '-p', "0xac, 0x11"])
    assert retcode == 0
    assert output == 'field1: 10, field2: 12, field3: 17\n'

def test_too_many_payload_bytes():
    retcode, output = run_cli_command(['payloadinspector',
                              '-b', "('field1', 4), ('field2', 4), ('field3', 8)",
                              '-p', "0xac 0x11 0x32"])
    assert retcode == 0
    assert output == '''WARNING: Bitfield is 16 bits, and payload is 24 bits. Extra payload data is discarded.
field1: 10, field2: 12, field3: 17\n'''

def test_too_few_payload_bytes():
    retcode, output = run_cli_command(['payloadinspector',
                              '-b', "('field1', 4), ('field2', 4), ('field3', 8)",
                              '-p', "0xac"])
    assert retcode == 1
    assert output == 'ERROR: Bitfield is 16 bits, but payload is only 8 bits.\n'

def test_standard_arguments_binary():
    retcode, output = run_cli_command(['payloadinspector',
                              '-b', "('field1', 4), ('field2', 4), ('field3', 8)",
                              '-p', "0xac, 0x11",
                              '-f', 'bin'])
    assert retcode == 0
    assert output == 'field1: 0b1010, field2: 0b1100, field3: 0b10001\n'

def test_standard_arguments_single_element():
    retcode, output = run_cli_command(['payloadinspector',
                              '-b', "('field1', 4), ('field2', 4), ('field3', 8)",
                              '-p', "0xac, 0x11",
                              '-f', 'field2'])
    assert retcode == 0
    assert output == 'field2: 12\n'

def test_standard_arguments_format_and_element_selection():
    retcode, output = run_cli_command(['payloadinspector',
                              '-b', "('field1', 4), ('field2', 4), ('field3', 8)",
                              '-p', "0xac, 0x11",
                              '-f', 'field1:bin, field3'])
    assert retcode == 0
    assert output == 'field1: 0b1010, field3: 17\n'

def test_bitfield_from_struct():
    retcode, output = run_cli_command(['payloadinspector',
                              '-s', 'tests/header.h:message'])
    assert retcode == 0
    assert output == '''field1: 1
field2: 2
big_value: 32
field3: 3\n'''
