# bin: int --> binary
# ord: char --> int
from PIL import Image

default_stega_img_path = './images/stega_image.png'

# Indices
RED = 0
GREEN = 1
BLUE = 2


class LsbStega():
    def __init__(self):
        super().__init__()

    def to_binary(self, char):
        decimal = ord(char)
        binary = bin(decimal)
        return binary

    def text_to_bits(self, text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
        return self.fill_bits(bits, 8)

    def text_from_bits(self, bits, encoding='utf-8', errors='surrogatepass'):
        n = int(bits, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

    def fill_bits(self, value, bitcount):
        return value.zfill(bitcount * ((len(value) + (bitcount-1)) // bitcount))

    def encode_text(self, img_path, text):
        print("Hiding text in picture")
        text_length_binary = bin(len(text))[2:]
        text_length_bits = self.fill_bits(text_length_binary, 16)
        text_as_bits = self.text_to_bits(text)
        data_to_hide = text_length_bits + text_as_bits

        img = Image.open(img_path)
        src_img_pixels = img.load()
        img_x_size = img.size[0]
        img_y_size = img.size[1]

        result_img = Image.new("RGB", (img_x_size, img_y_size))
        result_img_pixels = result_img.load()

        current_position = 0
        for y in range(img_y_size):
            for x in range(img_x_size):
                if current_position >= len(data_to_hide) or (bin(src_img_pixels[x, y][BLUE])[-1]) == data_to_hide[current_position]:
                    result_img_pixels[x, y] = src_img_pixels[x, y]

                else:
                    pixel = src_img_pixels[x, y]
                    blue_binary = self.fill_bits(bin(pixel[BLUE])[2:], 8)
                    blue_binary = blue_binary[:-1] + \
                        data_to_hide[current_position]
                    result_img_pixels[x, y] = (
                        src_img_pixels[x, y][RED], src_img_pixels[x, y][GREEN], int(blue_binary, 2))
                    # print(
                    #     "src pixel:", src_img_pixels[x, y], "--> result pixel:", result_img_pixels[x, y])

                current_position += 1
        result_img.save(default_stega_img_path)
        print("Your text was hidden in the picture saved at", default_stega_img_path)

    def decode_text(self, img_path=default_stega_img_path):
        print("Extracting text from picture")
        img = Image.open(img_path)
        img_x_size = img.size[0]
        img_y_size = img.size[1]
        blue_values = img.split()[BLUE]

        length_binary = ''
        for x in range(16):
            length_binary += bin(blue_values.getpixel((x, 0)))[-1]
            length_decimal = int(length_binary, 2)

        bits_to_read = length_decimal * 8
        current_position = -15
        extracted_data = ''
        for y in range(img_y_size):
            for x in range(img_x_size):
                if current_position <= bits_to_read:
                    extracted_data += bin(blue_values.getpixel((x, 0)))[-1]
                    current_position += 1
                else:
                    break
        extracted_data = extracted_data[16:]

        text = self.text_from_bits(extracted_data)
        print("Extracted text from picture")
        return text


def main():
    action = input(
        "(e) Encode image (hide message) or (d) Decode image (extract message): ")
    stega = LsbStega()
    if action == 'e':
        img_path = input("Enter the path to the image: ")
        text = input("Enter your hidden message: ")
        stega.encode_text(img_path, text)
    elif action == 'd':
        img_path = input("Enter the path to the image (leave empty for default): ")
        if img_path:
           text = stega.decode_text(img_path=img_path)
        else:
            text = stega.decode_text()
        print("Extracted text:", text)


if __name__ == "__main__":
    main()
