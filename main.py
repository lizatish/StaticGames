import sys

import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

import design


class ExampleApp(QtWidgets.QWidget, design.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.saddle_points = []
        self.data = []
        self.transpose_data = []

        self.loadDataButton.clicked.connect(self.load_data)

        self.saveTableValuesButton.clicked.connect(self.save_table_values)
        self.changeTableSizeButton.clicked.connect(self.change_table_size)

        self.get_azart_player_strategy.clicked.connect(self.count_azart_player_strategy)
        self.get_maximin_strategy.clicked.connect(self.count_maximin_strategy)
        self.get_gurvits_strategy.clicked.connect(self.count_gurvits_strategy)
        self.get_sevidg_strategy.clicked.connect(self.count_sevidg_strategy)
        self.get_baies_strategy.clicked.connect(self.count_baies_strategy)
        self.get_laplass_strategy.clicked.connect(self.count_laplass_strategy)
        self.get_hodges_leman_strategy.clicked.connect(self.count_hodges_leman_strategy)

    def count_hodges_leman_strategy(self):
        if self.data:
            p = [float(elem) for elem in self.hodges_leman_weights.toPlainText().split()]
            beta = self.beta.value()

            if p and beta:
                L = []
                for row in self.data:
                    m = 0
                    for i, elem in enumerate(row):
                        m += elem * p[i]
                    l = beta * m + (1 - beta) * min(row)
                    L.append(l)

                    index = L.index(max(L))
                    self.win_row.setText(f'a{index + 1}')

    def count_laplass_strategy(self):
        if self.data:
            sum_matrix = []
            for row in self.data:
                sum_matrix.append(sum(row))

            index = sum_matrix.index(max(sum_matrix))
            self.win_row.setText(f'a{index + 1}')

    def count_baies_strategy(self):
        if self.data:
            p = [float(elem) for elem in self.baies_weights.toPlainText().split()]
            if p:
                M = []
                for row in self.data:
                    m = 0
                    for i, elem in enumerate(row):
                        m += elem * p[i]
                    M.append(m)

                index = M.index(max(M))
                self.win_row.setText(f'a{index + 1}')

    def count_sevidg_strategy(self):
        if self.data:
            max_values = self.get_max_col_array()

            risks = []
            for ix, col in enumerate(self.transpose_data):
                row = []
                for elem in col:
                    row.append(max_values[ix] - elem)
                risks.append(row)
            risks = list(map(list, zip(*risks)))
            index = risks.index(min(risks))
            self.win_row.setText(f'a{index + 1}')

    def count_gurvits_strategy(self):
        if self.data:
            alpha = self.alpha.value()
            values = []
            for row in self.data:
                value = alpha * min(row) + (1 - alpha) * max(row)
                values.append(value)
            index = values.index(max(values))
            self.win_row.setText(f'a{index + 1}')

    def count_maximin_strategy(self):
        if self.data:
            min_values = self.get_min_row_array()
            index = min_values.index(max(min_values))
            self.win_row.setText(f'a{index + 1}')

    def count_azart_player_strategy(self):
        if self.data:
            max_values = self.get_max_row_array()
            index = max_values.index(max(max_values))
            self.win_row.setText(f'a{index + 1}')

    def get_max_col_array(self):
        transpose_data = self.transpose_data.copy()
        max_col_vals = []
        for row in range(len(transpose_data)):
            max_col_vals.append(max(transpose_data[row]))
        return max_col_vals

    def get_max_row_array(self):
        data = self.data.copy()
        max_row_vals = []
        for row in range(len(data)):
            max_row_vals.append(max(data[row]))
        return max_row_vals

    def get_min_row_array(self):
        data = self.data.copy()
        min_row_vals = []
        for row in range(len(data)):
            min_row_vals.append(min(data[row]))
        return min_row_vals

    def change_table_size(self):
        self.table.setRowCount(self.row_num.value())
        self.table.setColumnCount(self.col_num.value())

    def change_table_size_to(self, row_num, col_num):
        self.row_num.setValue(row_num)
        self.col_num.setValue(col_num)

    def load_data(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл (txt, csv)",
                                                         "/home/liza/PycharmProjects/gameTheory",
                                                         "txt (*.txt);; xlsx (*.xlsx)")

        filename = filename[0]
        ext = filename.split('.')[-1]
        if ext == 'txt':
            data = self.read_data_from_txt(filename)
        else:
            data = self.read_data_from_xlsx(filename)

        self.data = data
        self.transpose_data = list(map(list, zip(*data)))

        self.set_table_data(self.data)

    def read_data_from_xlsx(self, filename, type='int'):
        if filename:
            df = pd.read_excel(filename, header=None)
            data = df.values.tolist()
            if type == 'float':
                data = [[float(elem) for elem in line.split()] for line in data]

            return data

    def read_data_from_txt(self, filename, type='int'):
        if filename:
            f = open(filename, 'r')
            with f:
                data = f.read()
        data = data.split('\n')[:-1]
        if type == 'float':
            data = [[float(elem) for elem in line.split()] for line in data]
        else:
            data = [[int(elem) for elem in line.split()] for line in data]
        return data

    def set_table_data(self, data):
        self.transpose_data = list(map(list, zip(*data)))

        numrows = len(data)
        numcols = len(data[0])

        self.table.setColumnCount(numcols)
        self.table.setRowCount(numrows)
        self.change_table_size_to(numrows, numcols)

        self.table.clear()
        for row in range(numrows):
            for column in range(numcols):
                self.table.setItem(row, column, QTableWidgetItem((str(data[row][column]))))

        cols_name = [f'b{i + 1}' for i in range(numcols)]
        self.table.setHorizontalHeaderLabels(cols_name)
        rows_name = [f'a{i + 1}' for i in range(numrows)]
        self.table.setVerticalHeaderLabels(rows_name)

    def save_table_values(self):
        self.data.clear()
        for row in range(self.table.rowCount()):
            temp_row = []
            for column in range(self.table.columnCount()):
                item_val = QTableWidgetItem(self.table.item(row, column)).text()
                temp_row.append(int(item_val))
            self.data.append(temp_row)

        self.set_table_data(self.data)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
