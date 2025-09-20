import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.expression = []
        self.input = "0"
        self.is_input_nagative = False
        self.operator = ["/", "*", "-", "+", "="]
        self.operator_method = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide,
            "=": self.process,
        }
        self.setup_ui()

    def setup_ui(self):
        # 메인 윈도우 설정
        self.setWindowTitle("Calculator")
        self.setFixedSize(400, 600)
        self.setStyleSheet("background-color: #000000;")

        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 디스플레이 영역 설정
        self.display = QLabel(self.input)
        self.display.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.display.setStyleSheet(
            """
            QLabel {
                color: #FFFFFF;
                background-color: transparent;
                padding: 20px;
                font-size: 60px;
                font-weight: 300;
            }
        """
        )
        self.display.setMinimumHeight(120)
        main_layout.addWidget(self.display)

        # 버튼 그리드 레이아웃
        button_widget = QWidget()
        button_layout = QGridLayout(button_widget)
        button_layout.setSpacing(15)

        # 버튼 배치 정의 (5행 * 4열)
        buttons = [
            ["<-", "AC", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["+/-", "0", ".", "="],
        ]

        # 버튼 생성 및 배치
        for row in range(len(buttons)):
            for col in range(len(buttons[row])):
                button_text = buttons[row][col]
                button = QPushButton(button_text)

                # 버튼 크기 설정
                button.setFixedSize(80, 80)

                # 버튼 스타일 설정
                button.setStyleSheet(self.get_button_style(button_text))

                # 폰트 설정
                font = QFont()
                font.setPointSize(24)
                font.setWeight(QFont.Weight.Normal)
                button.setFont(font)

                # 버튼 클릭 이벤트 연결
                button.clicked.connect(
                    lambda checked, text=button_text: self.button_clicked(text)
                )

                # 그리드에 버튼 추가
                button_layout.addWidget(button, row, col)

        main_layout.addWidget(button_widget)

    def get_button_style(self, button_text):
        """버튼 텍스트에 따라 적절한 스타일 반환"""
        base_style = """
            QPushButton {
                border: none;
                border-radius: 40px;
                font-weight: normal;
            }
            QPushButton:pressed {
                background-color: #FFFFFF;
                color: #000000;
            }
        """

        # 기능 버튼 (회색)
        if button_text in ["<-", "AC", "%", "+/-"]:
            return (
                base_style
                + """
                QPushButton {
                    background-color: #A6A6A6;
                    color: #000000;
                }
            """
            )

        # 연산자 버튼 (주황색)
        elif button_text in self.operator:
            return (
                base_style
                + """
                QPushButton {
                    background-color: #FF9500;
                    color: #FFFFFF;
                }
            """
            )

        # 숫자 및 소수점 버튼 (진회색)
        else:
            return (
                base_style
                + """
                QPushButton {
                    background-color: #333333;
                    color: #FFFFFF;
                }
            """
            )

    def last_object(self):
        if self.expression:
            return self.expression[-1]
        return None

    def input_append_expression(self):
        if self.input != "":
            value = 0
            if "." in self.input:
                value = float(self.input)
            else:
                value = int(self.input)
            self.expression.append(str(value))
            self.input = ""

    def count_persent(self, express: str):
        temp = express
        count = 0
        while temp.endswith("%"):
            temp = temp[:-1]
            count += 1
        return count

    def process(self):
        print(f"1process input if = {self.input}")
        if self.input != "":
            print(f"process input if = {self.input}")
            if self.is_input_nagative:
                self.expression.append("(-" + self.input + ")")
                self.is_input_nagative = False
            else:
                self.expression.append(self.input)
            self.input = ""
        expression = "".join(x for x in self.expression)
        print(f"process = {expression}")
        if expression.endswith("%"):
            count = self.count_persent(expression)
            print(f"count = {count}")
            expression = expression[:-count] + f"/100{count * "0"}"
            print(expression)
        try:
            answer = round(eval(expression), 6)
            print(f"answer = {answer}")
        except ZeroDivisionError:
            answer = 0
        self.expression.clear()
        self.expression = [str(answer)]
        print(f"process expression = {self.expression} anser = {answer}")

    def is_last_operator(self):
        if self.last_object in self.expression:
            return True
        return False

    def add(self):
        if self.is_last_operator():
            self.expression[-1] = "+"
        else:
            self.input_append_expression()
            self.expression.append("+")

    def subtract(self):
        if self.is_last_operator():
            self.expression[-1] = "-"
        else:
            self.input_append_expression()
            self.expression.append("-")

    def multiply(self):
        if self.is_last_operator():
            self.expression[-1] = "*"
        else:
            self.input_append_expression()
            self.expression.append("*")

    def divide(self):
        if self.is_last_operator():
            self.expression[-1] = "/"
        else:
            self.input_append_expression()
            self.expression.append("/")

    def persent(self):
        if self.is_last_operator():
            self.expression[-1] = "%"
        else:
            self.input_append_expression()
            self.expression.append("%")

    def reset(self):
        self.expression.clear()
        self.input = "0"

    def update_display(self):
        base = ""
        if self.expression:
            if self.expression[0] == "0" and len(self.expression) > 1:
                self.expression = self.expression[1:]
            base = "".join(x for x in self.expression)
        input_txt = self.input
        if self.is_input_nagative and self.input != "":
            input_txt = "(-" + self.input + ")"
        self.display.setText(str(base + input_txt))

    def negative_positive(self):
        self.is_input_nagative = not self.is_input_nagative

    def check_point(self):
        if "." in self.input:
            return
        self.input = self.input + "."

    def delete_express(self):
        if self.input != "":
            self.input = self.input[:-1]
        elif self.expression:
            self.input = self.expression.pop()[:-1]

    def button_clicked(self, button_text):
        if button_text == "AC":
            self.reset()
        elif button_text == "<-":
            self.delete_express()
        elif button_text.isdigit():
            print(f"input = {self.input}")
            if self.input != "":
                if "." in self.input:
                    self.input = str(float(self.input)) + button_text
                else:
                    self.input = str(int(self.input)) + button_text
            else:
                self.input += button_text
        elif button_text == ".":
            self.check_point()
        elif button_text == "+/-":
            self.negative_positive()
        elif button_text != "=" and button_text in self.operator:
            method = self.operator_method[button_text]
            method()
        elif button_text == "%":
            self.persent()
        elif button_text == "=" and (self.last_object()) and self.expression:
            print(self.expression)
            self.process()
        self.update_display()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
