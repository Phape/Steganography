# bin: int --> binary
# ord: char --> int
from PIL import Image


class LsbStega():
    def __init__(self):
        super().__init__()

    def to_binary(self, char):
        decimal = ord(char)
        binary = bin(decimal)
        return binary

    def text_to_bits(self, text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))

    def text_from_bits(self, bits, encoding='utf-8', errors='surrogatepass'):
        n = int(bits, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

    def encode_text(self, img_location, text):
        text_length_binary = bin(len(text))[2:]
        text_length_bits = text_length_binary.zfill(16 * ((len(text_length_binary) + 15) // 16)) # 16 bits --> text length can be 2^16 = 65 536 chars
        print("text lenth bits:", text_length_bits)

        img = Image.open(img_location)
        img_pixels = img.load()
        img_x_size = img.size[0]
        img_y_size = img.size[1]
        red_pixels = img.split()[0]
        green_pixels = img.split()[1]
        blue_pixels = img.split()[2]
        # print(img_x_size)
        # print(img_y_size)

        result_img = Image.new("RGB", (img_x_size, img_y_size))
        for y in range(img_y_size):
            for x in range(img_x_size):
                print("x:", x, "y:", y, "rgb:", img_pixels[x, y], "bin:", bin(blue_pixels.getpixel((x, y)))[-1])
                pass
        pass


def main():
    stega = LsbStega()
    # print(stega.to_binary('A'))
    print("text-to-bits:", stega.text_to_bits('AB'))
    stega.encode_text('./sample_picture.png', "hello my name is Philipp jasklfjweiojgonboanvadnvynjgojregoijaojvoyjvoijaagjioarjgoiajdivjdooiaiogjegaiondivnjkdjgnjgöarjojavonöafdnbklkdfjglfdkjgaoöerigjeikvfjmevfjefjöajfcöa")


if __name__ == "__main__":
    main()
