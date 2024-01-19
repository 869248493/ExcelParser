from utilities import copy_to_clipboard, convert_num_to_emoji, count_chinese_char, EMOJI_DICTIONARY
import random
from datetime import datetime
import errors


class ExcelParser:
    def __init__(self, mode, ws, quote_file_content):
        self.mode = mode
        self.EMOJI_NO_LIST = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]
        self.max_rank_number = None
        self.quote_content = quote_file_content
        self.ws = ws
        self.time_delta = None
        # TODO: ADD YOUR NEW MODE HERE
        self.mode_to_function_dictionary = {
            1: self.total_records,
            2: self.today_group_opened_ranking,
            3: self.today_group_formed_ranking,
            4: self.accumulate_group_formed_ranking
        }

    def main(self):
        self.mode_to_function_dictionary[self.mode]()

    ########################################
    #       Functionality Functions        #
    ########################################
    # TODO: ADD YOUR NEW MODE FUNCTIONALITY HERE
    def total_records(self):
        valid_input = False
        output_l = []
        while not valid_input:
            input_str = input("请输入 (支付订单 浏览量 开团数量 成团单量 分享次数) 并以空格分开: ")
            input_l = input_str.split()
            if len(input_l) != 5:
                errors.invalid_format()
                continue

            valid_number = True
            for i in range(len(input_l)):
                try:
                    output_l.append(int(input_l[i]))
                except ValueError:
                    errors.invalid_number()
                    valid_number = False
                    continue
            if not valid_number:
                continue
            else:
                valid_input = True

        time_now = datetime.now().strftime("%H")
        quote = self.gen_quote()
        sun = EMOJI_DICTIONARY["sun"]
        circle = EMOJI_DICTIONARY["circle"]
        celebrate = EMOJI_DICTIONARY["celebrate"]
        res = (
            f'各位小伙伴们{sun}{circle}\n截止{time_now}:00时段总数据播报{celebrate}\n\n支付订单 {output_l[0]}单\n成团订单'
            f'{output_l[3]}单\n\n浏览量 {output_l[1]}次 开团数量 {output_l[2]}个 分享次数 {output_l[4]}次\n\n{quote}'
        )

        print(res)

        copy_to_clipboard(res)

    def today_group_opened_ranking(self):
        date_type = "今日"
        keyword = "开团"
        self.general_ranking_output_generator(date_type, keyword)

    def today_group_formed_ranking(self):
        date_type = "今日"
        keyword = "成团"
        self.general_ranking_output_generator(date_type, keyword)

    def accumulate_group_formed_ranking(self):
        date_type = "累计"
        keyword = "成团"
        self.general_ranking_output_generator(date_type, keyword)

    def general_ranking_output_generator(self, date_type, keyword):
        res = ""
        title = self.gen_title(date_type, keyword)
        ranking = self.gen_ranking(keyword)
        quote = self.gen_quote()

        res += title
        res += ranking
        res += "\n"
        res += quote

        print(res)
        copy_to_clipboard(res)

    #################################
    #       Helper Functions        #
    #################################

    def gen_title(self, date_type, ranking_type):
        bell = EMOJI_DICTIONARY["bell"]
        return f"{bell}截止目前{date_type}个人{ranking_type}排名{bell}\n如下⬇\n\n排序       名字       {ranking_type}数量\n"

    def gen_ranking(self, kw, accumulate=False):
        # Locate kw
        kw_row, kw_col = self.locate_str(kw, (1, self.ws.max_row+1), (1, self.ws.max_column+1))

        # Date row definition:
        date_row = kw_row + 1

        # Locate date | at (date_row), from (kw_col to max) |
        date_row_range = (date_row, date_row + 1)
        date_col_range = (kw_col, self.ws.max_column + 1)
        # Locate date | at (kw_row + 1), from (kw_col to max) |
        # TODO: DELETE DAY
        date_searching = (datetime.now().replace(microsecond=0, second=0, minute=0, hour=0)) + self.time_delta
        date_row, date_col = self.locate_str(date_searching, date_row_range, date_col_range)

        # Accumulate row definition
        accumulate_row = date_row

        # Locate accumulate col | at (date_row), from (kw_col to max)
        _, accumulate_col = self.locate_str(f"累计{kw}", date_row_range, date_col_range)


        # Candidate start row definition:
        candidate_start_row = date_row + 1

        # Locate candidate name column as boundary of non-int | at (candidate_row), from (date_row to 1) |
        candidate_row_range = (candidate_start_row, candidate_start_row+1)
        candidate_col_range = (date_col, 1)
        _, candidate_col = self.locate_boundary(int, candidate_row_range, candidate_col_range, reverse_col=True)

        # Total col definition:
        total_col = candidate_col

        # Locate total row as "合计" | from (candidate_start_row to max), at (total col) |
        total_row_range = (candidate_start_row, self.ws.max_row+1)
        total_col_range = (total_col, total_col+1)
        total_row, _ = self.locate_str("合计", total_row_range, total_col_range)

        '''
        POS FOUND:
        kw_row, kw_pos
        date_row, date_col
        candidate_start_row, candidate_col
        total_row, total_col
        '''

        if accumulate:
            rank_dict = self.build_rank_dict(candidate_col, (candidate_start_row, total_row), accumulate_col)
        else:
            rank_dict = self.build_rank_dict(candidate_col, (candidate_start_row, total_row), date_col)
        rank_name_list, rank_number_list, value_list = self.build_rank_list(rank_dict)
        if value_list[0] == 0:
            errors.pattern_error_2()
        rank_string = self.build_rank_string(rank_name_list, rank_number_list, value_list)

        rank_string += "\n"

        unit = "单" if kw == "成团" else "个"
        date_total_value = self.ws.cell(row=total_row, column=date_col).value
        accumulate_value = self.ws.cell(row=total_row, column=accumulate_col).value
        rank_string += f"今日{kw}：{date_total_value}{unit}\n"
        rank_string += f"累计{kw}：{accumulate_value}{unit}\n"

        return rank_string

    def gen_quote(self):
        random_line = random.randint(0, len(self.quote_content) - 1)
        return self.quote_content[random_line]

    def locate_str(self, kw, row_range, col_range):
        """
        :param kw: keyword
        :param row_range: tuple (from, to)
        :param col_range: tuple (from, to)
        :return: tuple (row, col)
        """
        for i in range(row_range[0], row_range[1]):
            for j in range(col_range[0], col_range[1]):
                if self.ws.cell(row=i, column=j).value == kw:
                    kw_pos = (i, j)
                    return kw_pos
        errors.kw_error(kw)

    def locate_boundary(self, valid_type, row_range, col_range, reverse_row=False, reverse_col=False):
        row_order = 1
        col_order = 1
        if reverse_row:
            row_order = -1
        elif reverse_col:
            col_order = -1

        for i in range(row_range[0], row_range[1], row_order):
            for j in range(col_range[0], col_range[1], col_order):
                if type(self.ws.cell(row=i, column=j).value) != valid_type:
                    # found boundary
                    # if j == 0:
                    #     i -= row_order
                    #     j = col_range[1] - col_order
                    # else:
                    #     j -= col_order
                    return i, j

        errors.boundary_error(valid_type)

    def build_rank_dict(self, candidate_col, row_range, ranking_col):
        rank_dict = dict()

        for cur_row in range(row_range[0], row_range[1]):
            cur_cell_value = self.ws.cell(row=cur_row, column=ranking_col).value

            # check if cell below date is a number
            if type(cur_cell_value) is not int:
                errors.pattern_error_1()

            # find col of name
            candidate_name = self.ws.cell(row=cur_row, column=candidate_col).value
            rank_dict[candidate_name] = cur_cell_value

        rank_dict = dict(sorted(rank_dict.items(), key=lambda item: item[1], reverse=True))

        return rank_dict

    def build_rank_list(self, rank_dict):
        rank_number_list = []
        rank_name_list = []
        value_list = []
        prev_value = - float('inf')
        max_rank_number_counter = self.max_rank_number
        cur_rank = 0

        for key, value in rank_dict.items():
            if max_rank_number_counter == 0:
                break
            if value == prev_value:
                rank_number_list.append(cur_rank)
            else:
                cur_rank += 1
                rank_number_list.append(cur_rank)
            value_list.append(value)
            rank_name_list.append(key)
            prev_value = value
            max_rank_number_counter -= 1

        return rank_name_list, rank_number_list, value_list

    def build_rank_string(self, rank_name_list, rank_number_list, value_list):
        padding_num_to_name = 7
        padding_name_to_value = 26
        res = ""

        for i in range(len(rank_name_list)):
            rank_number_emoji = convert_num_to_emoji(rank_number_list[i])
            candidate_name = rank_name_list[i]
            candidate_value = value_list[i]

            # add ranking number emoji
            res += rank_number_emoji
            # add padding from ranking number to name
            for _ in range(padding_num_to_name):
                res += " "
            # add ranking name
            res += candidate_name
            # add padding from name to value
            ch_letters = count_chinese_char(candidate_name)
            eng_letters = len(candidate_name) - ch_letters
            padding = padding_name_to_value - ((ch_letters * 4) + (eng_letters*2))
            padding = 7 if padding < 7 else padding
            for _ in range(padding):
                res += " "
            # add value
            res += str(candidate_value)
            res += "\n"

        return res
