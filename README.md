# numpy-protobuf

Adds support for a Numpy array type, called `ndarray`, to Python protocol buffers.

Currently just includes the `ndarray` message type. Eventually the `npbuf` packages will also include code that will extend the Python implementation of protobuf such that `ndarray` will be treated like any other protobuf built-in type. In other words, you'll be able to 

    1. assign a Numpy array object directly to a protobuf field
    2. serialize and send that protobuf
    3. receive and deserialize that protobuf
    4. read a Numpy array object directly from that same field

in just the same way as you would be able to with an `int` or `string` field.

## Compiling the Numpy protobuf files

Assuming you have `protoc` (the protobuf compiler) installed, you can automatically recompile this packages `.proto` defintion files via the `setup.py` script. Either do a developer build:

```bash
cd numpy-protobuf
pip install -e .
```

or run the `ProtocCommand` directly via:

```bash
python setup.py protoc
```
