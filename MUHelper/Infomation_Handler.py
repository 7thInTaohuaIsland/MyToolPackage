import xlrd, xlwt
from typing import List


class ToolBox:
    def __init__(self):
        pass

    def __str2hex(self, s):
        '''
        把十六进制表示的字符转换成数值（'AA'->170）
        :param s: 单个数字（str格式）
        :return:单个数字（数值）
        '''
        odata = 0
        su = s.upper()
        for c in su:
            tmp = ord(c)
            if tmp <= ord('9'):
                odata = odata << 4
                odata += tmp - ord('0')
            elif ord('A') <= tmp <= ord('F'):
                odata = odata << 4
                odata += tmp - ord('A') + 10
        return odata

    def CheckSum(self, string: str) -> str:
        '''
        计算字符串的校验和，返回字符。从第3位到最后一位
        :param string:
        :return:
        '''
        num_list = self.strlist2numlist(string)
        sum = 0
        for i in range(2, len(num_list)):
            sum += num_list[i]
        return hex(sum & 0xFF)

    def CheckSum_num(self, num_list: List[int]) -> int:
        '''
        计算数值列表的校验和，返回数值。从第3位到最后一位
        :param num_list:
        :return:
        '''
        sum = 0
        for i in range(2, len(num_list)):
            sum += num_list[i]
        return sum & 0xFF

    def strlist2numlist(self, string: str):
        '''
        把一串接收的字符数据转译成数值形式
        :param string:接收的数据，十六进制，空格分隔，不包含0x标识符
        :return:字符数据 转译成的 数值列表
        '''
        str_list = str.split(string)
        num_list = []
        for i in range(len(str_list)):
            num_list.append(self.__str2hex(str_list[i]))
        return num_list

    def buma_interpreter(self, data):
        '''
        把补码解析成数值
        :param data:有符号数的补码形式(也是一个数值）
        :return:有符号的数值形式
        '''
        n = int(data)
        if n & 0x8000 == 0:
            return data
        else:
            b = bin(n)[3:]
            list_b = [1] * (16 - len(b))
            list_b = list_b + list(map(lambda x: (int(x) + 1) % 2, b))
            str_b = "".join('%d' % i for i in list_b)
            int_b = int(str_b, base=2) + 1
            ans = bin(int_b)[2:]
            res = 0
            for i in range(15):
                ans_s = int(ans[i + 1])
                res += ans_s * 2 ** (14 - i)
            return -res

    def num2code(self, num, length) -> List[str]:
        '''
        把有符号数数值编码成有符号数补码，兼容无符号数编码
        多个字节会以字节为单位按从低位到高位排序
        :param num:数值
        :param length:编码数据长度，单位4bit（字节数*2)
        :return:有符号数-》补码编码；无符号数-》编码
        '''
        if num >= 0:
            hex_str = '0' * length
            temp_str = hex(num)[2:]
            hex_str = hex_str[0:length - len(temp_str)] + temp_str
        else:
            hex_str = '0' * (length)
            temp_str = hex((2 ** (length * 4) + num))[2:]
            hex_str = hex_str[0:length - len(temp_str)] + temp_str
        code_i = ['0'] * (length // 2)
        for j in range(length // 2):
            code_i[j] = hex_str[length - (j + 1) * 2:length - (j) * 2]
        return code_i

    def read_log(self, fname):
        '''
        :param fname: 由串口助手记录下来的log文件
        :return:把log文件中的字符串解析成的List[List[]]
        '''
        line_list = []
        with open(fname, "r") as f:
            for line in f.readlines():
                line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                line = self.strlist2numlist(line)
                line_list.append(line)
        line_list.pop(0)
        return line_list


class Data2Cmd:
    def __init__(self, PATH_XLSX):
        data = xlrd.open_workbook(PATH_XLSX)
        self.table = data.sheets()[0]

    def code(self):
        '''
        编码数据成十六位指令格式
        :return: 十六位指令字符串格式
        '''
        nrows = self.table.nrows
        ncols = self.table.ncols
        code_str = ''
        title_dict = {}
        for i in range(ncols):
            title_dict[self.table.cell_value(0, i)] = 0
        for i in range(1, nrows):
            code_i = []  # [AA] or [0D,32]
            for j in range(ncols):
                title_dict[self.table.cell_value(0, j)] = self.table.cell_value(i, j)
            try:
                value = float(title_dict['值']) / float(title_dict['当量'])
                code_i = ToolBox().num2code(int(value), int(title_dict['长度']) * 2)
            except:
                value = title_dict['值'][2:4]
                code_i.append(value)
            for code in code_i:
                code_str = code_str + ' ' + code
        checksum = ToolBox().CheckSum(code_str)
        if len(checksum) == 4:
            code_str = code_str + ' ' + checksum[2:]
        else:
            code_str = code_str + ' 0' + checksum[2:]
        code_str = code_str.upper()
        return code_str


class Cmd2Data:
    def __init__(self, PATH_LOG, PATH_XLSX, PATH_SAVE):
        self.PATH_LOG = PATH_LOG
        self.PATH_XLSX = PATH_XLSX
        self.PATH_SAVE = PATH_SAVE

    def xlsx_cmd_concate(self, cmd: List[int]) -> dict:
        '''
        把cmd中的数据添加到resdict中，经过当量与符号初步计算
        :param cmd:指令列表
        :return: resdict:键为元素名称，值为元素数值（当量与符号初步计算）
        '''
        resdict = {}
        resdict['指令类型'] = 'ResCmd'
        data = xlrd.open_workbook(self.PATH_XLSX)
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        title_dict = {}
        for i in range(ncols):
            title_dict[table.cell_value(0, i)] = 0
        cmd_cnt = 0
        for i in range(1, nrows):
            for j in range(ncols):
                title_dict[table.cell_value(0, j)] = table.cell_value(i, j)
            len_cmd = int(title_dict['长度'])
            cmd_to_interp = cmd[cmd_cnt:cmd_cnt + len_cmd]
            cmd_cnt = cmd_cnt + len_cmd
            cmd_num = 0
            for j in range(len_cmd - 1, -1, -1):
                if int(title_dict['符号']) == 0:
                    cmd_num += cmd_to_interp[j] * (2 ** (j * 8))
                else:
                    cmd_num += ToolBox().buma_interpreter(cmd_to_interp[j] * (2 ** (j * 8)))
            cmd_num = cmd_num * float(title_dict['当量'])
            resdict[title_dict['元素']] = cmd_num
        return resdict

    def particular(self, cmd):
        resdict = self.xlsx_cmd_concate(cmd)
        return resdict

    def decode(self):
        cmd_list = ToolBox().read_log(self.PATH_LOG)
        workbook = xlwt.Workbook(encoding='ascii')
        worksheet = workbook.add_sheet('My Worksheet')
        for i0 in range(len(cmd_list)):
            cmd = cmd_list[i0]
            try:
                resdict = self.particular(cmd)
            except:
                resdict = {'指令类型': 'CtrlCmd'}
            if i0 == 0:
                i1 = 0
                for key, value in resdict.items():
                    worksheet.write(i0, i1, label=key)
                    worksheet.write(i0 + 1, i1, label=value)
                    i1 += 1
            else:
                i1 = 0
                for key, value in resdict.items():
                    worksheet.write(i0 + 1, i1, label=value)
                    i1 += 1
        workbook.save(self.PATH_SAVE)


if __name__ == '__main__':
    PATH_XLSX = 'example/Infomation_Handler/Recieve from I.xlsx'
    cmd_str = Data2Cmd(PATH_XLSX).code()
    print(cmd_str)

    PATH_XLSX = 'example/Infomation_Handler/Send to S.xlsx'
    PATH_LOG = 'example/Infomation_Handler/log_S.txt'
    PATH_SAVE = 'example/Infomation_Handler/log_S_decode.xls'
    Cmd2Data(PATH_LOG, PATH_XLSX, PATH_SAVE).decode()
