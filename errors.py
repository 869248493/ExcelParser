import sys


############################## User Input Error ##############################
def invalid_number():
    print("输入包含非数字，请重新输入")


def invalid_choice():
    print("无效序列，请重新选择：")


def invalid_format():
    print("输入格式有误，请重新输入")


############################## Coding Error ##############################
def io_not_found():
    print("ERROR: IO NOT FOUND")
    sys.exit(1)


############################## Program Error ##############################
def empty_folder_error(folder_path):
    print(f"错误0： 文件夹 '{folder_path}' 为空，请添加文件或确认config路径，程序终止")
    sys.exit(1)


def file_not_found_error(file_path):
    print(f"错误1： 无法找到目标文件：{file_path}，程序终止")
    sys.exit(1)


def ws_number_error():
    print(f"错误2： 当前excel文件worksheet不等于1， 程序终止")
    sys.exit(1)


def kw_error(kw):
    print(f"错误3：在指定文档无法找到keyword '{kw}' ，请修改excel文件或更新程序逻辑，程序终止")
    sys.exit(1)


def boundary_error(valid_type):
    print(f"错误4： 规律错误，无法找到type: '{valid_type}' 的边界 ，请修改excel文件或更新程序逻辑，程序终止")


def pattern_error_1():
    print("错误5：规律错误，在指定栏下方无法找到数字，请修改excel文件或更新程序逻辑，程序终止")
    sys.exit(1)


def pattern_error_2():
    print("错误6：规律错误，所有老师数字目前都是0")
    sys.exit(1)