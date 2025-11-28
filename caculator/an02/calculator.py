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
            sign = "-" if self.is_input_nagative else ""
            value = sign + str(value)
            self.expression.append(value)
            self.is_input_nagative = False
            self.input = ""

    def count_persent(self, express: str):
        temp = express
        count = 0
        while temp.endswith("%"):
            temp = temp[:-1]
            count += 1
        return count

    def tokenize(self, expression: str):
        """수학식 문자열을 토큰으로 분리"""
        tokens = []
        i = 0
        while i < len(expression):
            if expression[i].isspace():
                i += 1
                continue

            # 숫자 토큰 (정수 및 소수)
            if expression[i].isdigit() or expression[i] == ".":
                num = ""
                while i < len(expression) and (
                    expression[i].isdigit() or expression[i] == "."
                ):
                    num += expression[i]
                    i += 1
                tokens.append(float(num) if "." in num else int(num))

            # 음수 처리
            elif expression[i] == "-" and (i == 0 or expression[i - 1] in "(+*/"):
                num = "-"
                i += 1
                while i < len(expression) and (
                    expression[i].isdigit() or expression[i] == "."
                ):
                    num += expression[i]
                    i += 1
                tokens.append(float(num) if "." in num else int(num))

            # 괄호와 연산자
            elif expression[i] in "()+-*/":
                tokens.append(expression[i])
                i += 1
            else:
                i += 1

        return tokens

    def infix_to_postfix(self, tokens):
        """중위표기법을 후위표기법으로 변환 (Shunting Yard Algorithm)"""
        precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
        output = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, (int, float)):
                output.append(token)
            elif token == "(":
                operator_stack.append(token)
            elif token == ")":
                while operator_stack and operator_stack[-1] != "(":
                    output.append(operator_stack.pop())
                if operator_stack:
                    operator_stack.pop()  # '(' 제거
            elif token in precedence:
                while (
                    operator_stack
                    and operator_stack[-1] != "("
                    and operator_stack[-1] in precedence
                    and precedence[operator_stack[-1]] >= precedence[token]
                ):
                    output.append(operator_stack.pop())
                operator_stack.append(token)

        while operator_stack:
            output.append(operator_stack.pop())

        return output

    def evaluate_postfix(self, postfix):
        """후위표기법 수식 계산"""
        stack = []

        for token in postfix:
            if isinstance(token, (int, float)):
                stack.append(token)
            elif token in "+-*/":
                if len(stack) < 2:
                    raise ValueError("잘못된 수식입니다")

                b = stack.pop()
                a = stack.pop()

                if token == "+":
                    result = a + b
                elif token == "-":
                    result = a - b
                elif token == "*":
                    result = a * b
                elif token == "/":
                    if b == 0:
                        raise ZeroDivisionError("0으로 나눌 수 없습니다")
                    result = a / b

                stack.append(result)

        if len(stack) != 1:
            raise ValueError("잘못된 수식입니다")

        return stack[0]

    def safe_calculate(self, expression: str):
        """eval() 대신 안전한 수학식 계산"""
        try:
            tokens = self.tokenize(expression)
            if not tokens:
                return 0

            postfix = self.infix_to_postfix(tokens)
            result = self.evaluate_postfix(postfix)
            return result
        except (ValueError, ZeroDivisionError):
            return 0

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
            answer = round(self.safe_calculate(expression), 6)
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
