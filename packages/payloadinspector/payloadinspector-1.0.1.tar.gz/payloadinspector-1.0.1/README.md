# payloadinspector

Inspect byte strings as bit fields.

payloadinspector takes a bit field (an ordered list of name-bitlength tuples) and a payload (a string of bytes) as arguments. It maps the data contents of the payload to the bit field and outputs one, several or all of the values.

## Install

Install payloadinspector with pip

```bash
$ pip install payloadinspector
```

payloadinspector can also be installed from a local copy with

```bash
# Clone the repo one of:
#   - git@gitlab.com:fredrikh/payloadinspector.git
#   - https://gitlab.com/fredrikh/payloadinspector.git
$ git clone <repo-url>
$ cd payloadinspector

# Set up virtual environment, for example with
$ python3 -m venv .venv

# Install PayloadInspector
$ pip install $(pwd)
```

## Usage

After installation payloadinspector can be called from the command line.
Try running it with the `-h` flag to see the help text with formatting rules.

### Reading bitfield format from argument

As an example, let's say we have a bitfield that looks like this:

```
             -------------------------------------------------------
element name | address | padding | priority | padding | data | CRC |
             -------------------------------------------------------
# of bits    |   16    |    8    |     4    |    4    |  64  |  16 |
             -------------------------------------------------------
```

Note that there are two sections with the name 'padding'.
They must be given unique names in the bitfield specification.

The data we have from our debugger or similar is:

```0x00 0x03 0x00 0x50 0x43 0xc1 0xac 0x6f 0x90 0xaa 0x43 0xdf 0x43 0xd6```

To inspect the value of each bitfield element, we would run

```bash
$ payloadinspector --bitfield "(address, 16), (padding1, 8), (priority, 4), (padding2, 4), (data, 64), (crc, 16)" --payload "0x00 0x03 0x00 0x50 0x43 0xc1 0xac 0x6f 0x90 0xaa 0x43 0xdf 0x43 0xd6"
```
Which would output:

```
address: 3, padding1: 0, priority: 5, padding2: 0, data: 4882373066214753247, crc: 17366
```

The output format can be configured using the `-f, --format` argument. It can either be used to specify the encoding as `dec` (default) `bin` or `hex`:

```bash
$ payloadinspector --bitfield "(address, 16), (padding1, 8), (priority, 4), (padding2, 4), (data, 64), (crc, 16)" --payload "0x00 0x03 0x00 0x50 0x43 0xc1 0xac 0x6f 0x90 0xaa 0x43 0xdf 0x43 0xd6" --format hex
```
Which gives:
```
address: 0x3, padding1: 0x0, priority: 0x5, padding2: 0x0, data: 0x43c1ac6f90aa43df, crc: 0x43d6
```
It can also be used to specify a subset of the bitfield elements:
```bash
$ payloadinspector --bitfield "(address, 16), (padding1, 8), (priority, 4), (padding2, 4), (data, 64), (crc, 16)" --payload "0x00 0x03 0x00 0x50 0x43 0xc1 0xac 0x6f 0x90 0xaa 0x43 0xdf 0x43 0xd6" --format "address, priority"
```
Which gives the output:
```
address: 3, priority: 5
```

Finally, the format string can be used to specify individual encodings for each element:
```bash
$ payloadinspector --bitfield "(address, 16), (padding1, 8), (priority, 4), (padding2, 4), (data, 64), (crc, 16)" --payload "0x00 0x03 0x00 0x50 0x43 0xc1 0xac 0x6f 0x90 0xaa 0x43 0xdf 0x43 0xd6" --format "address,  data:hex, priority:bin"
```
Which gives the output:
```
address: 3, data: 0x43c1ac6f90aa43df, priority: 0b101
```
The example above also shows that the order of the elements can be rearranged with the format string.

### Reading bitfield format from C file
The bitfield structure can also be read by parsing a C bitfiled.
If you have a C header file `header.h` which contains the struct

```C
/* ... */

struct bitfield1
{
    uint8_t element1 : 3;
    uint8_t element2 : 5;
    uint16_t element3 : 14;
    uint8_t padding : 2
};

typedef struct
{
    uint8_t element4 : 4;
    uint8_t element5 : 4;
    uint16_t element6 : 10;
    uint8_t padding 6
} bitfield2;

/* ... */
```

You can load each struct directly from the file by giving the `--source-struct`argument like this:

```bash
$ payloadinspector --source-struct "header.h:bitfield1" --payload "0xdf 0x43 0xd6"
```
Which would give the output:
```
element1: 6, element2: 31, element3: 4341, padding: 2
```

It is also possible to only print the format of the bitfield by omitting the `--payload` argument:

```bash
$ payloadinspector --source-struct "header.h:bitfield1"
```
gives the output:
```
element1: 3
element2: 5
element3: 14
padding: 2
```

Several formats of struct definitions are supported, both typedefed and non-typedefed, as well as with attributes like "packed".

However, **all** elements must be given a name and a bit size as an integer. `#define`-d constants are not supported. The following structs will not work

```C
struct incompatible_bitfield1
{
    uint8_t element1 : 3;
    uint8_t element2; // ERROR: Cannot parse bit size
    uint16_t element3 : 14;
};

struct incompatible_bitfield2
{
    uint8_t element1 : 4;
    uint8_t : 4; // ERROR: No element name
    uint16_t element2 : 16;
};

#define N_BITS_ELEMENT1 3
#define N_BITS_ELEMENT2 5

struct incompatible_bitfield3
{
    uint8_t element1 : N_BITS_ELEMENT1; // ERROR: Cannot parse bit size
    uint8_t element2 : N_BITS_ELEMENT2;
}
```
