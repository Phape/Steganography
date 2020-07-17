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
        # return bits.zfill(8 * ((len(bits) + 7) // 8))
        return self.fill_bits(bits, 8)

    def text_from_bits(self, bits, encoding='utf-8', errors='surrogatepass'):
        n = int(bits, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

    def fill_bits(self, value, bitcount):
        return value.zfill(bitcount * ((len(value) + (bitcount-1)) // bitcount))

    def encode_text(self, img_location, text):
        text_length_binary = bin(len(text))[2:]

        text_length_bits = self.fill_bits(text_length_binary, 16)
        print("text lenth bits:", text_length_bits)
        text_as_bits = self.text_to_bits(text)
        data_to_hide = text_length_bits + text_as_bits
        print("data to hide:", data_to_hide)

        img = Image.open(img_location)
        src_img_pixels = img.load()
        RED = 0
        GREEN = 1
        BLUE = 2
        img_x_size = img.size[0]
        img_y_size = img.size[1]

        result_img = Image.new("RGB", (img_x_size, img_y_size))
        result_img_pixels = result_img.load()

        current_position = 0
        for y in range(img_y_size):
            for x in range(img_x_size):
                if current_position >= len(data_to_hide) or (bin(src_img_pixels[x, y][BLUE])[-1]) == data_to_hide[current_position]:
                    # print("pixel is correct")
                    result_img_pixels[x, y] = src_img_pixels[x, y]

                else:
                    pixel = src_img_pixels[x, y]
                    blue_binary = self.fill_bits(bin(pixel[BLUE])[2:], 8)
                    blue_binary = blue_binary[:-1] + \
                        data_to_hide[current_position]
                    result_img_pixels[x, y] = (
                        src_img_pixels[x, y][RED], src_img_pixels[x, y][GREEN], int(blue_binary, 2))
                    print(
                        "src pixel:", src_img_pixels[x, y], "--> result pixel:", result_img_pixels[x, y])

                current_position += 1
        result_img.save('./images/stega_image.png')


def main():
    stega = LsbStega()
    stega.encode_text('./sample_picture.png', "A")


if __name__ == "__main__":
    main()
