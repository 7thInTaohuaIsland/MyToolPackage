import xlrd


class HeadFile_Gnerator:
    def __init__(self, PATH_XLSX, PATH_SAVE):
        '''
        :param PATH_XLSX: xlsx文件路径
        :param PATH_SAVE: 文件（可以是txt,h,c）要保存的路径
        '''
        self.PATH_XLSX = PATH_XLSX
        self.PATH_SAVE = PATH_SAVE
        self.length_dict = {'1.0': 'char',
                            '2.0': 'short',
                            '4.0': 'int'}
        self.sign_dict = {'0.0': 'unsigned',
                          '1.0': ''}

    def generate(self):
        file_save = open(self.PATH_SAVE, 'w')
        self.__xlsx_interpreter(self.PATH_XLSX, file_save)
        file_save.close()

    def __xlsx_interpreter(self, PATH_XLSX, file_save):
        data = xlrd.open_workbook(PATH_XLSX)
        tables = data.sheets()
        title_dict = {}
        for i in range(len(tables)):
            table = tables[i]
            nrows = table.nrows
            ncols = table.ncols
            file_save.write(table.name + '\n')
            file_save.write('typedef struct\n{\n')
            for i in range(ncols):
                title_dict[table.cell_value(0, i)] = 0
            cnt = 1
            for i in range(1, nrows):
                for j in range(ncols):
                    title_dict[table.cell_value(0, j)] = str(table.cell_value(i, j))
                cnt_start = str(cnt)
                cnt_end = str(int(cnt + float(title_dict['长度']) - 1))
                if float(title_dict['长度']) == 1:
                    cnt_str = cnt_start
                else:
                    cnt_str = cnt_start + '-' + cnt_end
                cnt = int(cnt + float(title_dict['长度']))
                if title_dict['符号'] == '0.0' or title_dict['符号'] == '1.0':
                    length = self.length_dict[title_dict['长度']]
                    sign = self.sign_dict[title_dict['符号']]
                    type = sign + ' ' + length
                    abbr = length[0] if title_dict['符号'] == '1.0' else sign[0] + length[0]
                else:
                    abbr = ''
                    type = title_dict['符号']
                if title_dict['符号'] == '1.0':
                    a = 1
                code_explain = '0x' + title_dict['内容'] if title_dict['内容'] else ''
                if title_dict['当量'] != '1.0':
                    code_explain = code_explain + ' ' + str(title_dict['备注']) + ' 当量：' + title_dict['当量']
                else:
                    code_explain = code_explain + ' ' + str(title_dict['备注'])
                code = '\t' + type + ' ' + abbr + title_dict['参数符号'] + ';\t\t\t\t//' + cnt_str + ' ' + title_dict[
                    '参数名'] + '  ' + code_explain
                file_save.write(code + '\n')
            file_save.write('}' + table.name + '_Struct;')
            file_save.write('\n')


if __name__ == '__main__':
    PATH_XLSX = 'example/Code Generator/from upper.xlsx'
    PATH_SAVE = 'example/Code Generator/from upper.h'
    HeadFile_Gnerator(PATH_XLSX, PATH_SAVE).generate()
