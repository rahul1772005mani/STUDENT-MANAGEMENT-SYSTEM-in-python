import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QTabWidget, QCheckBox, QTextEdit, QComboBox
)
from PyQt5.QtCore import Qt


class StudentManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(850, 650)
        self.students = {}  # student_id -> {'name': str, 'grades': {}, 'attendance': set()}
        self.current_student_id = 0

        self.setStyleSheet(self.main_stylesheet())
        self.init_ui()

    def main_stylesheet(self):
        return """
        QWidget {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 14px;
            color: #333;
        }
        QTabWidget::pane {
            border: 2px solid #0078D7;
            border-radius: 8px;
            margin-top: 10px;
            background-color: #f9f9f9;
        }
        QTabBar::tab {
            background: #e1e1e1;
            border: 1px solid #999999;
            padding: 10px 20px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            min-width: 90px;
            margin-right: 2px;
            font-weight: 600;
            color: #555555;
        }
        QTabBar::tab:selected {
            background: #0078D7;
            color: white;
            font-weight: bold;
            border-bottom: 0;
        }
        QPushButton {
            background-color: #0078D7;
            color: white;
            border-radius: 6px;
            padding: 10px 15px;
            font-weight: 600;
            transition: background-color 0.3s ease;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        QLabel {
            font-weight: 600;
        }
        QLineEdit, QComboBox, QTextEdit {
            border: 1.5px solid #bbb;
            border-radius: 6px;
            padding: 6px 8px;
            selection-background-color: #0078D7;
        }
        QTableWidget {
            border: 1.5px solid #0078D7;
            border-radius: 8px;
            gridline-color: #ddd;
        }
        QTableWidget::item:selected {
            background-color: #cce4f7;
            color: #0078D7;
            font-weight: bold;
        }
        QHeaderView::section {
            background-color: #0078D7;
            color: white;
            padding: 6px;
            border: none;
            font-weight: 700;
        }
        QCheckBox {
            spacing: 10px;
            margin-left: 8px;
        }
        """

    def init_ui(self):
        # Central widget and layout
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tabs
        self.enrollment_tab = QWidget()
        self.attendance_tab = QWidget()
        self.grades_tab = QWidget()
        self.communication_tab = QWidget()

        self.tabs.addTab(self.enrollment_tab, "Student Enrollment")
        self.tabs.addTab(self.attendance_tab, "Attendance Tracking")
        self.tabs.addTab(self.grades_tab, "Grade Management")
        self.tabs.addTab(self.communication_tab, "Communication")

        self.init_enrollment_tab()
        self.init_attendance_tab()
        self.init_grades_tab()
        self.init_communication_tab()

    # === Enrollment Tab ===
    def init_enrollment_tab(self):
        layout = QVBoxLayout()

        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Student Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Student Name:")
        name_label.setFixedWidth(120)
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)

        # Age
        age_layout = QHBoxLayout()
        age_label = QLabel("Age:")
        age_label.setFixedWidth(120)
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Enter age")
        age_layout.addWidget(age_label)
        age_layout.addWidget(self.age_input)
        form_layout.addLayout(age_layout)

        # Class/Grade
        class_layout = QHBoxLayout()
        class_label = QLabel("Class / Grade:")
        class_label.setFixedWidth(120)
        self.class_input = QLineEdit()
        class_layout.addWidget(class_label)
        class_layout.addWidget(self.class_input)
        form_layout.addLayout(class_layout)

        # Button to add student
        self.add_student_button = QPushButton("Add Student")
        self.add_student_button.clicked.connect(self.add_student)
        form_layout.addWidget(self.add_student_button)

        # Student List Table
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(4)
        self.student_table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Class"])
        self.student_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.student_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.student_table.setSelectionMode(QTableWidget.SingleSelection)
        self.student_table.setAlternatingRowColors(True)
        self.student_table.verticalHeader().setVisible(False)

        layout.addLayout(form_layout)
        layout.addWidget(QLabel("Enrolled Students:"))
        layout.addWidget(self.student_table)

        self.enrollment_tab.setLayout(layout)

    def add_student(self):
        name = self.name_input.text().strip()
        age = self.age_input.text().strip()
        class_grade = self.class_input.text().strip()

        if not name or not age or not class_grade:
            QMessageBox.warning(self, "Incomplete Data", "Please fill all student details.")
            return
        if not age.isdigit() or int(age) <= 0:
            QMessageBox.warning(self, "Invalid Age", "Please enter a valid positive age.")
            return

        self.current_student_id += 1
        student_id = self.current_student_id
        self.students[student_id] = {
            'name': name,
            'age': int(age),
            'class_grade': class_grade,
            'grades': {},
            'attendance': set(),
        }

        self.update_student_table()
        self.clear_enrollment_form()
        self.update_attendance_table()
        self.update_grades_student_combobox()

    def clear_enrollment_form(self):
        self.name_input.clear()
        self.age_input.clear()
        self.class_input.clear()

    def update_student_table(self):
        self.student_table.setRowCount(0)
        for student_id, data in self.students.items():
            row_position = self.student_table.rowCount()
            self.student_table.insertRow(row_position)
            self.student_table.setItem(row_position, 0, QTableWidgetItem(str(student_id)))
            self.student_table.setItem(row_position, 1, QTableWidgetItem(data['name']))
            self.student_table.setItem(row_position, 2, QTableWidgetItem(str(data['age'])))
            self.student_table.setItem(row_position, 3, QTableWidgetItem(data['class_grade']))

    # === Attendance Tab ===
    def init_attendance_tab(self):
        layout = QVBoxLayout()

        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(3)
        self.attendance_table.setHorizontalHeaderLabels(["ID", "Name", "Present"])
        self.attendance_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.attendance_table.setAlternatingRowColors(True)
        self.attendance_table.verticalHeader().setVisible(False)

        mark_attendance_button = QPushButton("Save Attendance")
        mark_attendance_button.clicked.connect(self.save_attendance)

        layout.addWidget(self.attendance_table)
        layout.addWidget(mark_attendance_button)

        self.attendance_tab.setLayout(layout)
        self.update_attendance_table()

    def update_attendance_table(self):
        self.attendance_table.setRowCount(0)
        for student_id, data in self.students.items():
            row_position = self.attendance_table.rowCount()
            self.attendance_table.insertRow(row_position)
            self.attendance_table.setItem(row_position, 0, QTableWidgetItem(str(student_id)))
            self.attendance_table.setItem(row_position, 1, QTableWidgetItem(data['name']))

            checkbox = QCheckBox()
            checkbox.setChecked(False)
            self.attendance_table.setCellWidget(row_position, 2, checkbox)

    def save_attendance(self):
        for row in range(self.attendance_table.rowCount()):
            student_id = int(self.attendance_table.item(row, 0).text())
            checkbox = self.attendance_table.cellWidget(row, 2)
            if checkbox.isChecked():
                self.students[student_id]['attendance'].add(self.current_date())
            else:
                self.students[student_id]['attendance'].discard(self.current_date())
        QMessageBox.information(self, "Attendance Saved", "Attendance has been saved for today.")

    def current_date(self):
        from datetime import date
        return date.today().isoformat()

    # === Grades Tab ===
    def init_grades_tab(self):
        layout = QVBoxLayout()

        student_select_layout = QHBoxLayout()
        student_label = QLabel("Select Student:")
        student_label.setFixedWidth(120)
        self.grades_student_combo = QComboBox()
        self.grades_student_combo.currentIndexChanged.connect(self.load_student_grades)
        student_select_layout.addWidget(student_label)
        student_select_layout.addWidget(self.grades_student_combo)

        layout.addLayout(student_select_layout)

        # Grades Table with subjects and grades
        self.grades_table = QTableWidget()
        self.grades_table.setColumnCount(2)
        self.grades_table.setHorizontalHeaderLabels(["Subject", "Grade"])
        self.grades_table.setAlternatingRowColors(True)
        self.grades_table.verticalHeader().setVisible(False)

        add_subject_layout = QHBoxLayout()
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Subject Name")
        add_grade_button = QPushButton("Add / Update Grade")
        add_grade_button.clicked.connect(self.add_update_grade)
        add_subject_layout.addWidget(self.subject_input)
        add_subject_layout.addWidget(add_grade_button)

        layout.addWidget(self.grades_table)
        layout.addLayout(add_subject_layout)

        self.grades_tab.setLayout(layout)
        self.update_grades_student_combobox()

    def update_grades_student_combobox(self):
        self.grades_student_combo.clear()
        for student_id, data in self.students.items():
            self.grades_student_combo.addItem(f"{data['name']} (ID: {student_id})", student_id)
        self.load_student_grades()

    def load_student_grades(self):
        self.grades_table.setRowCount(0)
        student_id = self.grades_student_combo.currentData()
        if student_id is None or student_id not in self.students:
            return
        grades = self.students[student_id]['grades']
        for subject, grade in grades.items():
            row_position = self.grades_table.rowCount()
            self.grades_table.insertRow(row_position)
            self.grades_table.setItem(row_position, 0, QTableWidgetItem(subject))
            self.grades_table.setItem(row_position, 1, QTableWidgetItem(str(grade)))

    def add_update_grade(self):
        subject = self.subject_input.text().strip()
        if not subject:
            QMessageBox.warning(self, "Input Error", "Please enter a subject name.")
            return
        try:
            grade_text = self.grades_table.item(self.grades_table.currentRow(), 1).text() if self.grades_table.currentRow() != -1 else ''
            grade, ok = self.get_grade_from_user()
            if not ok:
                return
        except:
            grade, ok = self.get_grade_from_user()
            if not ok:
                return

        student_id = self.grades_student_combo.currentData()
        if student_id is None or student_id not in self.students:
            return

        self.students[student_id]['grades'][subject] = grade
        self.load_student_grades()
        self.subject_input.clear()

    def get_grade_from_user(self):
        from PyQt5.QtWidgets import QInputDialog
        grade, ok = QInputDialog.getText(self, "Grade Input", "Enter grade for the subject:")
        if ok:
            try:
                # Validate grade - allow string grades too (like A, B, etc.)
                if grade.strip() == '':
                    QMessageBox.warning(self, "Input Error", "Grade cannot be empty.")
                    return None, False
                return grade.strip(), True
            except Exception:
                QMessageBox.warning(self, "Input Error", "Invalid grade entered.")
                return None, False
        return None, False

    # === Communication Tab ===
    def init_communication_tab(self):
        layout = QVBoxLayout()

        self.communication_log = QTextEdit()
        self.communication_log.setReadOnly(True)

        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.setFixedHeight(80)

        send_button = QPushButton("Send Message")
        send_button.clicked.connect(self.send_message)
        send_button.setFixedWidth(140)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(send_button)

        layout.addWidget(QLabel("Message Log:"))
        layout.addWidget(self.communication_log)
        layout.addWidget(QLabel("New Message:"))
        layout.addWidget(self.message_input)
        layout.addLayout(btn_layout)

        self.communication_tab.setLayout(layout)

    def send_message(self):
        message = self.message_input.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "Empty Message", "Please enter a message to send.")
            return
        # For demo, just append it to the log
        self.communication_log.append(f"You: {message}")
        self.message_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentManagementSystem()
    window.show()
    sys.exit(app.exec_())


