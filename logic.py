from PyQt6.QtWidgets import *
from gui import Ui_MainWindow
import csv

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_submit.clicked.connect(self.submit_vote)
        self.button_results.clicked.connect(self.submit_result)
    def submit_vote(self):
        """
        Confirms id only contains numbers
        """
        self.label_directions.clear()
        voter_id = self.Input_ID.text().strip()
        if voter_id == '':
            self.label_directions.setText("Please enter an ID")
            self.label_directions.setStyleSheet("color: red;")
            return
        elif voter_id.isdigit() == False:
            self.label_directions.setText("Please only enter numbers in ID")
            self.label_directions.setStyleSheet("color: red;")
            return
        """
        Confirms a candidate has been selected
        """

        if self.radio_John.isChecked():
            candidate = 'John'
        elif self.radio_Jane.isChecked():
            candidate = 'Jane'
        else:
            self.label_directions.setText("Please select a candidate")
            self.label_directions.setStyleSheet("color: red;")
            return
        """
        Check whether the id has already voted
        """
        try:
            with open('result.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] == voter_id:
                        self.label_directions.setText("This ID already voted")
                        self.label_directions.setStyleSheet("color: red;")
                        return
        except FileNotFoundError:
            pass
        with open('result.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([voter_id, candidate])


        """
        Confirmation message that vote has been submitted successfully
        """
        self.label_directions.setText("Thanks for voting")
        self.label_directions.setStyleSheet("color: green;")

        self.Input_ID.clear()
        self.radio_John.setAutoExclusive(False)
        self.radio_John.setChecked(False)
        self.radio_Jane.setChecked(False)
        self.radio_Jane.setAutoExclusive(True)
        return
    def submit_result(self):
        John_votes = 0
        Jane_votes = 0
        try:
            with open('result.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    candidate = row[1]
                    if candidate == 'John':
                        John_votes += 1
                    elif candidate == 'Jane':
                        Jane_votes += 1
                    self.label_directions.setText(f"John has {John_votes} votes "
                                                  f"Jane has {Jane_votes} votes")
                    self.label_directions.setStyleSheet("color: green;")
        except FileNotFoundError:
            self.label_directions.setText("No one has voted")
            self.label_directions.setStyleSheet("color: red;")