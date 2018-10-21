import zlib, struct
import numpy as np

MAGIC_NUMBER = b'\x89PNG\x0d\x0a\x1a\x0a'
PACK_FORMAT = "!2I5B"
DEPTH_TO_COLOR_TYPES = {
    1:0, # Grayscale
    2:4, # Grayscale with alpha
    3:2, # RGB
    4:6  # RGBA
}
COLOR_TYPES_TO_DEPTH = {
    0:1, # Grayscale
    4:2, # Grayscale with alpha
    2:3, # RGB
    6:4  # RGBA
}

# http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html
def read_png(filename):
    # Open binary file
    f = open(filename, 'rb')
    bytes = f.read()

    # Check type
    if bytes[:len(MAGIC_NUMBER)] != MAGIC_NUMBER:
        raise RuntimeError("%s is not a PNG file." % filename)

    # Get locations
    hdr_loc = bytes.find(b'IHDR') + 4
    dat_loc = bytes.find(b'IDAT') + 4
    end_loc = bytes.find(b'IEND') + 4

    # Read and unpack header
    header = bytes[hdr_loc:hdr_loc+13]
    width, height, bit_depth, color_type, a, b, c = struct.unpack(PACK_FORMAT,
                                                                  header)
    if bit_depth != 8:
        raise RuntimeError("Only 8-bit images in lab.")

    # Get structure depth from color type
    if color_type in COLOR_TYPES_TO_DEPTH.keys():
        depth = COLOR_TYPES_TO_DEPTH[color_type]
    else:
        raise(RuntimeError("Only grayscale, alpha grayscale, RGB and RGBA images allowed in labs. Chcek out"))

    # Read data
    compressed_data = bytes[dat_loc:end_loc]
    raw_data = zlib.decompress(compressed_data)

    # Convert to numpy and remove leading zeros
    width_byte = width * depth
    image = np.frombuffer(raw_data, dtype=np.uint8)
    image = np.delete(image, np.arange(0, len(image), width_byte + 1))

    image = image.reshape(height,width,depth)

    return(image)

def write_png(image, filename):
    # Check correct type
    if image.dtype != np.uint8:
        raise(RuntimeError("We use only 8-bit images in labs."))

    # First convert image to byte array and get its size
    buf = bytearray(np.flipud(image))
    dimensions = image.shape

    # Determine color type
    if len(dimensions) == 2:
        # Grayscale image
        color_type = 0
        height, width = dimensions
        depth = 1

    elif len(dimensions) == 3:
        height, width, depth = dimensions
        if depth in DEPTH_TO_COLOR_TYPES.keys():
            color_type = DEPTH_TO_COLOR_TYPES[depth]
        else:
            raise(RuntimeError("Only grayscale, alpha grayscale, RGB and RGBA images allowed in labs. Chcek out."))
    else:
        raise(RuntimeError("Image should be 2D or 3D array."))

    # Prepare raw data
    width_byte = width * depth
    raw_data = b''.join(
        b'\x00' + buf[span:span + width_byte]
        for span in range((height - 1) * width_byte, -1, - width_byte)
    )

    def png_pack(png_tag, data):
        chunk_head = png_tag + data
        return (struct.pack("!I", len(data)) +
                chunk_head +
                struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head)))
    # Header
    bit_depth = 8
    header = struct.pack(PACK_FORMAT, width, height,
                         bit_depth, color_type,
                         0, 0, 0)

    h_pack = struct.unpack(PACK_FORMAT, header)

    # Compress data
    compressed_data = zlib.compress(raw_data, 9)

    # Prepare data
    data = b''.join([
        MAGIC_NUMBER,
        png_pack(b'IHDR', header),
        png_pack(b'IDAT', compressed_data),
        png_pack(b'IEND', b'')])

    # Write data
    f = open(filename, 'wb')
    f.write(data)
    f.close()
