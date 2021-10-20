import sys

import os

from PyQt5.QtWidgets import QMainWindow, QApplication

from front import *


class MyFront(QMainWindow):
    def __init__(self):
        super(MyFront, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.id_field.setFocus()
        self.load_data()
        self.ui.add_button.clicked.connect(self.add_function)
        self.ui.modify_button.clicked.connect(self.modify_function)
        self.ui.delete_button.clicked.connect(self.delete_function)
        self.ui.search_button.clicked.connect(self.search_function)
        self.ui.showall_button.clicked.connect(self.load_data)
        self.show()

    def add_function(self):
        check = 0
        f = open("Students.txt", 'r')
        for line in f:
            data_list = line.split("\t")
            data_list.pop(len(data_list)-1)
            if self.ui.id_field.text() in data_list:
                check = 1
                break
        f.close()
        if check == 0:
            students = [self.ui.id_field.text(),
                        self.ui.name_field.text(),
                        self.ui.email_field.text(),
                        self.ui.phoneno_field.text(),
                        self.date_filter(str(self.ui.date_field.date())),
                        self.ui.gender_field.currentText(),
                        self.ui.address_field.toPlainText()]
            f = open("Students.txt", 'a')
            for student in students:
                f.write(student+"\t")
            f.write("\n")
            self.ui.error_mod.setText("Student Added.")
            f.close()
            self.line_edit_cleaner()
        else:
            self.ui.error_mod.setText("ID no. is not available.")
            self.ui.id_field.setText("")

    def modify_function(self):
        f = open("Students.txt", 'r')
        temp = open("temp.txt", 'w')
        count = 0
        student_id = self.ui.id_field.text()
        for line in f:
            student_list = line.split("\t")
            student_list.pop(len(student_list)-1)
            if student_id != student_list[0]:
                for student in student_list:
                    temp.write(student+"\t")
                temp.write("\n")
            else:
                count += 1
                new_data = [self.ui.id_field.text(),
                            self.ui.name_field.text(),
                            self.ui.email_field.text(),
                            self.ui.phoneno_field.text(),
                            self.date_filter(str(self.ui.date_field.date())),
                            self.ui.gender_field.currentText(),
                            self.ui.address_field.toPlainText()]
                for data in new_data:
                    temp.write(data+"\t")
                temp.write("\n")
                self.line_edit_cleaner()
        if count == 0:
            self.ui.error_mod.setText("Record doesn't exist.")
        else:
            self.ui.error_mod.setText("Record modified.")
        f.close()
        temp.close()
        os.remove("Students.txt")
        os.rename("temp.txt", "Students.txt")

    def delete_function(self):
        f = open("Students.txt", 'r')
        temp = open("temp.txt", 'w')
        student_id = self.ui.id_field.text()
        count = 0
        for line in f:
            student_list = line.split("\t")
            student_list.pop(len(student_list)-1)
            if student_id != student_list[0]:
                for student in student_list:
                    temp.write(student+"\t")
                temp.write("\n")
            else:
                count += 1
        if count != 0:
            self.ui.error_mod.setText("Record Deleted.")
        else:
            self.ui.error_mod.setText("No such record exists.")
        f.close()
        temp.close()
        os.remove("Students.txt")
        os.rename("temp.txt", "Students.txt")
        self.line_edit_cleaner()

    def search_function(self):
        self.ui.tableWidget.clear()
        f = open("Students.txt", 'r')
        row = 0
        item = self.ui.search_field.text()
        count = 0
        for line in f:
            student_list = line.split('\t')
            student_list.pop(len(student_list)-1)
            if item in student_list:
                count += 1
                column = 0
                for students in student_list:
                    self.ui.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(students))
                    column += 1
        if count == 0:
            self.ui.error_search.setText("Record does not exist.")
        else:
            self.ui.error_search.setText("Record Found.")
        f.close()

    def load_data(self):
        f = open("Students.txt", 'r')
        self.ui.error_mod.clear()
        self.ui.error_search.clear()
        self.ui.tableWidget.setRowCount(48)
        self.ui.tableWidget.setColumnCount(7)
        row = 0
        for line in f:
            student_list = line.split('\t')
            student_list.pop(len(student_list)-1)
            column = 0
            for students in student_list:
                self.ui.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(students))
                column += 1
            row += 1
        f.close()

    def date_filter(self, birth_date):
        cond = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ",", " "]
        date = ""
        i = 0
        for letter in birth_date:
            if i >= 19:
                if letter in cond:
                    date += letter
            i += 1
        return date

    def line_edit_cleaner(self):
        self.ui.id_field.clear()
        self.ui.name_field.clear()
        self.ui.email_field.clear()
        self.ui.phoneno_field.setText("")
        self.ui.date_field.date()
        self.ui.gender_field.placeholderText()
        self.ui.address_field.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyFront()
    w.show()
    sys.exit(app.exec_())
