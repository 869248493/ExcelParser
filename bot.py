from io_flow import IOFlow
from Excel_Parser import ExcelParser
from datetime import    timedelta
from utilities import load_file, get_files_to_dict, load_ws, print_end
import config
import json
from io_interface import IOInterface


class Bot:
    def __init__(self):
        # io output
        self.excel_files_dict = None
        self.ws = None
        self.quote_file_content = None
        # io flow
        self.io_flow = IOFlow()
        self.parser = None

        # TODO: ADD YOUR NEW FUNCTION TO DICTIONARY
        self.io_name_function_dictionary = {
            "select_excel": self.select_excel_func,
            "select_mode": self.select_mode_func,
            "select_date": self.select_date_func,
            "select_number": self.select_number_func,
            "select_return": self.select_return_func
        }

    def main(self):
        self.initialise()
        while True:
            current_io = self.io_flow.current()
            if current_io.tail:
                self.parser.main()
                print_end()
            usr_choice = current_io.main()
            process_func = self.io_name_function_dictionary[current_io.name]
            process_func(usr_choice)

    def initialise(self):
        self.set_quote_file()
        self.set_excel_file_dict()
        self.reg_IOs()

    def set_quote_file(self):
        quote_file = load_file(config.QUOTE_DIRECTORY)
        self.quote_file_content = quote_file.readlines()

    def set_excel_file_dict(self):
        self.excel_files_dict = get_files_to_dict()

    def reg_IOs(self):
        io_list = load_IOs()
        for io in io_list:
            if io.display_dict == None:
                if io.name == "select_excel":
                    io.display_dict = self.excel_files_dict
            self.io_flow.reg(io)

    # TODO: ADD YOUR NEW FUNCTIONALITY BELOW
    def select_excel_func(self, usr_choice):
        self.ws = load_ws(self.excel_files_dict[usr_choice])
        self.io_flow.set_next()

    # TODO: ADD YOUR NEW MODE HERE
    def select_mode_func(self, usr_choice):
        go_return_set = {1}
        go_next_set = {2, 3, 4}

        if usr_choice == 0:
            self.io_flow.set_previous()
        else:
            self.parser = ExcelParser(usr_choice, self.ws, self.quote_file_content)

            if usr_choice in go_next_set:
                self.io_flow.set_next()

            if usr_choice in go_return_set:
                self.io_flow.go_to('select_return')

    def select_date_func(self, usr_choice):
        if usr_choice == 0:
            self.io_flow.set_previous()
        else:
            if usr_choice == 1:
                self.parser.time_delta = timedelta(days=-1)
            else:
                self.parser.time_delta = timedelta(days=0)

            self.io_flow.set_next()

    def select_number_func(self, usr_choice):
        if usr_choice == 0:
            self.io_flow.set_previous()
        else:
            if usr_choice != 3:
                self.parser.max_rank_number = int(usr_choice) * 5
            else:
                self.parser.max_rank_number = float('inf')
            self.io_flow.set_next()

    def select_return_func(self, usr_choice):
        if usr_choice == 0:
            self.io_flow.set_previous()
        else:
            if usr_choice == 1:
                print("going mode")
                self.io_flow.go_to("select_mode")
            else:
                print("going excel")
                self.io_flow.go_to("select_excel")


# Helper functions
def load_IOs():
    io_list = []
    f = load_file(config.JSON_DIRECTORY)
    data = json.load(f)
    sequence = 1

    for io in data:
        io_inst = IOInterface(io["io_name"], sequence, io["display_dict"], io["input_display"])
        if sequence == 1:
            io_inst.head = True
        elif sequence == len(data):
            io_inst.tail = True
        io_list.append(io_inst)
        sequence += 1

    return io_list

