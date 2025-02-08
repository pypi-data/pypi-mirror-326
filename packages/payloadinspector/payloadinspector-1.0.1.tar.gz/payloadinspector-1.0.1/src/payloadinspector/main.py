import argparse
from payloadinspector import get_field_values, BitField, Payload, format_output

def main():
    desc = 'Map a data payload to a specified bitfield'

    argparser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
    input_group = argparser.add_mutually_exclusive_group()
    input_group.add_argument('-b', '--bitfield', help='Bitfield format as a list of tuples with a name-string and number of bits. Allowed formats:\n'+
                                                      '"(field1, 1), (field2, 2), (field3, 3), (field4, 4)"\n'+
                                                      '"(\'field1\', 1), (\'field2\', 2), (\'field3\', 3), (\'field4\', 4)"\n'+
                                                      '\'("field1", 1), ("field2", 2), ("field3", 3), ("field4", 4)\'\n'+
                                                      '"(\'field1\', 1),(\'field2\', 2),(\'field3\', 3),(\'field4\', 4)"\n'+
                                                      '"[(\'field1\', 1), (\'field2\', 2), (\'field3\', 3), (\'field4\', 4)]"')
    input_group.add_argument('-s', '--source-struct', help='Bitfield read as a struct from a C source file (or header).'+
                                                           'The format is "<file-path>:<structname>"')
    argparser.add_argument('-p', '--payload', help='The data to be put into the bitfield. Allowed formats:\n'+
                                                    '"0x0a 0x80 0xff"\n'+
                                                    '"0a 80 ff"\n'+
                                                    '"0x0a, 0x80, 0xff"\n'+
                                                    '"0a, 80, ff"\n'+
                                                    '"[0x0a, 0x80, 0xff]"\n'+
                                                    '"[0a, 80, ff]"\n'+
                                                    '"0x0a0x800xff"\n'+
                                                    '"0a80ff"'+
                                                    'If this argument is omitted, the bitfield format is printed.')
    argparser.add_argument('-f', '--format', help='Output format specifier. By default all bitfield elements are printed as decimal values.\n'+
                                                  'The format string can specify \'bin\', \'hex\' or \'dec\' to force a different format for all values.\n'+
                                                  'Alternatively, to only show some elements, a list of element names can be given, ex: \'field1, field3\'.\n'+
                                                  'It is also possible to specify different encoding formats for different elements, ex: \'field1:bin, field3:hex\'',
                                             default='dec')
    argparser.add_argument('--version', action='version', version='%(prog)s 1.0.1')
    args = argparser.parse_args()
    if args.bitfield:
        try:
            bf = BitField.from_string(args.bitfield)
        except Exception as err:
            print(f'ERROR: {err}.')
            exit(1)
    elif args.source_struct:
        try:
            file_name, struct_name = args.source_struct.split(':')
            bf = BitField.from_c_source(file_name, struct_name)
        except Exception as err:
            print(f'ERROR: {err}.')
            exit(1)
    else:
        print("ERROR: Either -b or -s argument must be given")
        exit(1)

    if args.payload:
        try:
            payload = Payload.from_string(args.payload)
        except Exception as err:
            print(f'ERROR: {err}.')
            exit(1)
    else:
        print(bf)
        exit(0)

    if bf.total_bits > payload.total_bits:
        print(f'ERROR: Bitfield is {bf.total_bits} bits, but payload is only {payload.total_bits} bits.')
        exit(1)
    if bf.total_bits < payload.total_bits:
        print(f'WARNING: Bitfield is {bf.total_bits} bits, and payload is {payload.total_bits} bits. Extra payload data is discarded.')
    try:
        output_string = format_output(get_field_values(bf, payload), args.format)
    except Exception as err:
        print(f'ERROR: {err}.')
        exit(1)
    print(output_string)

if __name__ == '__main__':
    main()
