from utilities import dict_to_display, print_divider
import errors


class IOInterface:
    def __init__(self, name, sequence, display_dict, input_display):
        self.head = False
        self.tail = False
        self.name = name
        self.sequence = sequence
        self.display_dict = display_dict
        self.input_display = input_display

    def main(self):
        print(dict_to_display(self.display_dict))
        print_divider()
        index = None
        index_valid = False
        while not index_valid:
            index = input(self.input_display)
            # check if input is number
            try:
                index = int(index)
            except ValueError:
                errors.invalid_number()
                continue
            # check for invalid choice
            min_choice = 0
            if self.head or self.tail:
                min_choice = 1
            if len(self.display_dict) >= index >= min_choice:
                index_valid = True
            else:
                errors.invalid_choice()
        print_divider()
        return index






