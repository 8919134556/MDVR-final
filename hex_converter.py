import binascii

class HexConverter:

    @staticmethod
    def convert_ascii_to_hex(input_str):
        return ''.join([format(ord(c), '02X') for c in input_str])

    @staticmethod
    def string_reverse(s):
        result = ''.join(s[i:i+2][::-1] for i in range(0, len(s)-1, 2))
        return result[::-1]

    @staticmethod
    def convert_hex_to_ascii(hex_str):
        try:
            ascii_str = binascii.unhexlify(hex_str).decode('utf-8')
            return ascii_str
        except binascii.Error as e:
            print(f"Error converting hex to ASCII: {e}")
            return None

# Example usage
if __name__ == "__main__":
    hex_converter = HexConverter()

    input_str = "Hello, World!"
    hex_result = hex_converter.convert_ascii_to_hex(input_str)
    print(f"ASCII to HEX: {hex_result}")

    reversed_result = hex_converter.string_reverse(hex_result)
    print(f"Reversed HEX: {reversed_result}")

    ascii_result = hex_converter.convert_hex_to_ascii(reversed_result)
    print(f"HEX to ASCII: {ascii_result}")

