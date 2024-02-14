import binascii
from typing import Tuple

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
    
    @staticmethod
    def reverse_little_endian(input_str):
        return ''.join(input_str[i - 2:i] for i in range(len(input_str), 0, -2))
   
    @staticmethod
    def hex_to_binary(hex_string: str, base: int) -> str:
        value = bin(int(hex_string, base))[2:]
        binary = format(int(value, 2), '012b')
        return binary
    
    @staticmethod
    def string_reverse_binary(input_str):
        reversed_str = input_str[::-1]
        return reversed_str

    @staticmethod
    def pad_right(s, size, pad):
        builder = list(s)
        while len(builder) < size:
            builder.append(pad)
        return ''.join(builder)

    @staticmethod
    def extract_substrings(load_data):
        # Define start and end patterns
        start_pattern = "4801"
        end_pattern = "0a00"

        # Initialize start_index
        start_index = 0

        # Initialize list to store substrings
        substrings = []

        # Find occurrences of start_pattern after each end_pattern
        while True:
            # Find start_index of the next occurrence of start_pattern
            start_index = load_data.find(start_pattern, start_index)

            # Break if start_pattern is not found
            if start_index == -1:
                break

            # Find end_index of the next occurrence of end_pattern
            end_index = load_data.find(end_pattern, start_index)

            # Extract the first substring starting with start_pattern and ending with end_pattern
            substring1 = load_data[start_index:end_index + len(end_pattern)]

            # Append the first substring to the list
            substrings.append(substring1)

            # Extract the second substring starting from end_pattern to the end of the string
            substring2 = load_data[end_index + len(end_pattern):]

            # Append the second substring to the list
            substrings.append(substring2)

            # Move start_index forward to the character after the current end_index
            start_index = end_index + len(end_pattern)
        return substrings
 
   

# Example usage
if __name__ == "__main__":
    hex_converter = HexConverter()

    input_str = "Hello, World!"
    hex_result = hex_converter.convert_ascii_to_hex(input_str)
    print(f"ASCII to HEX: {hex_result}")

    data = "1051"
    reversed_result = hex_converter.string_reverse(data)
    print(f"Reversed HEX: {reversed_result}")

    ascii_result = hex_converter.convert_hex_to_ascii(reversed_result)
    print(f"HEX to ASCII: {ascii_result}")


    # Pass values from another code
    hex_data = "48015110d90000000100730000007b22646574223a7b226e756d223a22736432222c227374223a2234227d2c22647475223a22323032332d31312d30312031323a35393a3133222c226563223a223136222c226574223a22323032332d31312d30312031323a35393a3133222c227374223a22222c2275756964223a22227d0a00170b010d00152f070000170b010c3b0d5707000032000b008ba5df060023e6f5050007f6ffffff0000b5010a00010000001f0003010301000000000000000f00000000000000000000003f0000000000000000000000010050f104003e0d0000"    

    # Call the function to extract substrings
    sub_str = hex_converter.extract_substrings(hex_data)
    print(sub_str)

    content = "EF03"
    content = content[2:4]+content[0:2]
    binary_content = hex_converter.hex_to_binary(content, 16)
    print(binary_content)

    input_string = "10000001"
    result = hex_converter.string_reverse_binary(input_string)
    print(result)

    
    input_string = "example"
    padded_string = hex_converter.pad_right(input_string, 10, ' ')
    print(padded_string)