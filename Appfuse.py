import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QFileDialog, QLabel, QStackedWidget

from functools import partial

class CalculatorScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.result = QLineEdit()
        self.result.setReadOnly(True)
        self.result.setAlignment(Qt.AlignRight)
        self.result.setFontPointSize(32)

        button_grid = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"]
        ]

        button_layout = QVBoxLayout()

        for row in button_grid:
            row_layout = QHBoxLayout()
            for label in row:
                button = QPushButton(label)
                button.clicked.connect(partial(self.on_button_press, label))
                row_layout.addWidget(button)
            button_layout.addLayout(row_layout)

        equals_button = QPushButton("=")
        equals_button.clicked.connect(self.on_solution)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.result)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(equals_button)

        back_button = QPushButton("BACK")
        back_button.clicked.connect(self.switch_to_main)
        main_layout.addWidget(back_button)

        self.setLayout(main_layout)

    def on_button_press(self, text):
        current = self.result.text()
        if text == "C":
            self.result.clear()
        else:
            new_text = current + text
            self.result.setText(new_text)

    def on_solution(self):
        text = self.result.text()
        try:
            solution = str(eval(text))
            self.result.setText(solution)
        except Exception:
            self.result.setText("Error")

    def switch_to_main(self):
        self.parent().setCurrentIndex(0)


class TextEditorScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.text_input = QTextEdit()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_file)
        self.saved_label = QLabel("")

        back_button = QPushButton("BACK")
        back_button.clicked.connect(self.switch_to_main)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.text_input)
        main_layout.addWidget(self.save_button)
        main_layout.addWidget(self.saved_label)
        main_layout.addWidget(back_button)

        self.setLayout(main_layout)

    def save_file(self):
        text = self.text_input.toPlainText()
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(text)
                self.saved_label.setText(f"File saved successfully: {file_path}")
            except Exception as e:
                self.saved_label.setText(f"Error saving file: {str(e)}")

    def switch_to_main(self):
        self.parent().setCurrentIndex(0)


class MainApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.screen_manager = None
        self.setupUI()

    def setupUI(self):
        self.screen_manager = QStackedWidget()
        main_screen = QWidget()

        calculator_button = QPushButton("Calculator")
        text_editor_button = QPushButton("Text Editor")

        calculator_button.clicked.connect(self.switch_to_calculator)
        text_editor_button.clicked.connect(self.switch_to_text_editor)

        main_layout = QVBoxLayout()
        main_layout.addWidget(calculator_button)
        main_layout.addWidget(text_editor_button)
        main_screen.setLayout(main_layout)

        self.screen_manager.addWidget(main_screen)

    def switch_to_calculator(self):
        calculator_screen = CalculatorScreen()
        self.screen_manager.addWidget(calculator_screen)
        self.screen_manager.setCurrentWidget(calculator_screen)

    def switch_to_text_editor(self):
        text_editor_screen = TextEditorScreen()
        self.screen_manager.addWidget(text_editor_screen)
        self.screen_manager.setCurrentWidget(text_editor_screen)


if __name__ == '__main__':
    app = MainApp()
    app.exec_()
