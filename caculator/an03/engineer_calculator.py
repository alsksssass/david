import sys
import math
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
try:
    from calculator import Calculator
except ImportError:
    # 기본 Calculator 클래스를 정의 (calculator.py가 없는 경우)
    from PyQt6.QtWidgets import QMainWindow

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

        def process(self):
            if self.input != "":
                if self.is_input_nagative:
                    self.expression.append("(-" + self.input + ")")
                    self.is_input_nagative = False
                else:
                    self.expression.append(self.input)
                self.input = ""
            expression = "".join(x for x in self.expression)
            try:
                answer = round(eval(expression), 6)
            except ZeroDivisionError:
                answer = 0
            self.expression.clear()
            self.expression = [str(answer)]

        def is_last_operator(self):
            if self.last_object() in self.operator:
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

        def reset(self):
            self.expression.clear()
            self.input = "0"

        def update_display(self):
            pass

        def negative_positive(self):
            self.is_input_nagative = not self.is_input_nagative

        def delete_express(self):
            if self.input != "":
                self.input = self.input[:-1]
            elif self.expression:
                self.input = self.expression.pop()[:-1]

        def button_clicked(self, button_text):
            pass


class EngineerCalculator(Calculator):
    def __init__(self):
        self.angle_mode = "Rad"  # Rad, Deg
        self.memory_value = 0
        super().__init__()

    def setup_ui(self):
        # 메인 윈도우 설정
        self.setWindowTitle("공학용 계산기")
        self.setFixedSize(420, 800)
        self.setStyleSheet("background-color: #000000;")

        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(10, 40, 10, 10)

        # 디스플레이 영역 설정
        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.display.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                background-color: transparent;
                padding: 20px;
                font-size: 80px;
                font-weight: 200;
            }
        """)
        self.display.setMinimumHeight(160)
        main_layout.addWidget(self.display)

        # 버튼 영역
        button_widget = QWidget()
        button_layout = QGridLayout(button_widget)
        button_layout.setSpacing(8)

        # iOS 스타일 공학용 계산기 버튼 배치
        buttons = self.get_ios_scientific_buttons()

        # 버튼 생성 및 배치
        for row in range(len(buttons)):
            for col in range(len(buttons[row])):
                button_info = buttons[row][col]
                if not button_info:  # 빈 공간
                    continue

                button_text = button_info["text"]
                button_type = button_info.get("type", "number")
                colspan = button_info.get("colspan", 1)

                button = QPushButton(button_text)

                # 버튼 크기 설정 (iOS 스타일)
                if colspan == 2:
                    button.setFixedSize(178, 80)  # 0버튼용 가로 길이
                else:
                    button.setFixedSize(85, 80)

                # 버튼 스타일 설정
                button.setStyleSheet(self.get_ios_button_style(button_type))

                # 폰트 설정
                font = QFont("SF Pro Display", 32)
                if button_type == "function":
                    font.setPointSize(20)
                button.setFont(font)

                # 버튼 클릭 이벤트 연결
                button.clicked.connect(
                    lambda _, text=button_text: self.engineer_button_clicked(text)
                )

                # 그리드에 버튼 추가
                if colspan == 2:
                    button_layout.addWidget(button, row, col, 1, 2)
                else:
                    button_layout.addWidget(button, row, col)

        main_layout.addWidget(button_widget)

    def get_ios_scientific_buttons(self):
        """iOS 스타일 공학용 계산기 버튼 배치"""
        return [
            # 1행: 괄호와 메모리
            [
                {"text": "(", "type": "function"},
                {"text": ")", "type": "function"},
                {"text": "mc", "type": "function"},
                {"text": "m+", "type": "function"},
                {"text": "m-", "type": "function"},
                {"text": "mr", "type": "function"}
            ],
            # 2행: 2nd, 지수, 거듭제곱
            [
                {"text": "2nd", "type": "function"},
                {"text": "x²", "type": "function"},
                {"text": "x³", "type": "function"},
                {"text": "xʸ", "type": "function"},
                {"text": "eˣ", "type": "function"},
                {"text": "10ˣ", "type": "function"}
            ],
            # 3행: 역수, 제곱근
            [
                {"text": "1/x", "type": "function"},
                {"text": "²√x", "type": "function"},
                {"text": "³√x", "type": "function"},
                {"text": "ʸ√x", "type": "function"},
                {"text": "ln", "type": "function"},
                {"text": "log₁₀", "type": "function"}
            ],
            # 4행: 팩토리얼, 삼각함수
            [
                {"text": "x!", "type": "function"},
                {"text": "sin", "type": "function"},
                {"text": "cos", "type": "function"},
                {"text": "tan", "type": "function"},
                {"text": "e", "type": "function"},
                {"text": "EE", "type": "function"}
            ],
            # 5행: 랜덤, 쌍곡함수
            [
                {"text": "Rand", "type": "function"},
                {"text": "sinh", "type": "function"},
                {"text": "cosh", "type": "function"},
                {"text": "tanh", "type": "function"},
                {"text": "π", "type": "function"},
                {"text": "Rad", "type": "function"}
            ],
            # 6행: 기능 버튼
            [
                {"text": "⌫", "type": "clear", "colspan": 2},
                None,
                {"text": "AC", "type": "clear"},
                {"text": "%", "type": "clear"},
                {"text": "÷", "type": "operator"}
            ],
            # 7행: 숫자 7,8,9와 곱셈
            [
                {"text": "7", "type": "number"},
                {"text": "8", "type": "number"},
                {"text": "9", "type": "number"},
                None,
                {"text": "×", "type": "operator"}
            ],
            # 8행: 숫자 4,5,6와 뺄셈
            [
                {"text": "4", "type": "number"},
                {"text": "5", "type": "number"},
                {"text": "6", "type": "number"},
                None,
                {"text": "−", "type": "operator"}
            ],
            # 9행: 숫자 1,2,3와 덧셈
            [
                {"text": "1", "type": "number"},
                {"text": "2", "type": "number"},
                {"text": "3", "type": "number"},
                None,
                {"text": "+", "type": "operator"}
            ],
            # 10행: +/-, 0, 소수점, 등호
            [
                {"text": "+/−", "type": "number"},
                {"text": "0", "type": "number"},
                {"text": ".", "type": "number"},
                None,
                {"text": "=", "type": "operator"}
            ]
        ]

    def get_ios_button_style(self, button_type):
        """iOS 스타일 버튼 디자인"""
        base_style = """
            QPushButton {
                border: none;
                border-radius: 40px;
                font-weight: 400;
                color: #FFFFFF;
            }
            QPushButton:pressed {
                opacity: 0.7;
            }
        """

        if button_type == "number":
            # 숫자 버튼 (진한 회색)
            return base_style + """
                QPushButton {
                    background-color: #333333;
                    color: #FFFFFF;
                }
                QPushButton:pressed {
                    background-color: #666666;
                }
            """
        elif button_type == "operator":
            # 연산자 버튼 (주황색)
            return base_style + """
                QPushButton {
                    background-color: #FF9500;
                    color: #FFFFFF;
                }
                QPushButton:pressed {
                    background-color: #FFCC80;
                }
            """
        elif button_type == "clear":
            # 클리어 버튼 (밝은 회색)
            return base_style + """
                QPushButton {
                    background-color: #A6A6A6;
                    color: #000000;
                }
                QPushButton:pressed {
                    background-color: #D4D4D4;
                }
            """
        else:  # function
            # 기능 버튼 (검은색)
            return base_style + """
                QPushButton {
                    background-color: #000000;
                    color: #FFFFFF;
                    border: 1px solid #666666;
                }
                QPushButton:pressed {
                    background-color: #333333;
                }
            """

    def engineer_button_clicked(self, button_text):
        """공학용 계산기 버튼 클릭 이벤트"""

        # 각도 모드 전환
        if button_text == "Rad":
            self.angle_mode = "Deg" if self.angle_mode == "Rad" else "Rad"
            return

        # 메모리 기능
        elif button_text == "mc":
            self.memory_value = 0
        elif button_text == "m+":
            self.memory_value += float(self.input) if self.input else 0
        elif button_text == "m-":
            self.memory_value -= float(self.input) if self.input else 0
        elif button_text == "mr":
            self.input = str(self.memory_value)

        # 클리어 버튼
        elif button_text == "AC":
            self.reset()

        # 백스페이스
        elif button_text == "⌫":
            self.delete_express()

        # 상수
        elif button_text == "π":
            self.add_constant(str(math.pi))
        elif button_text == "e":
            self.add_constant(str(math.e))

        # 삼각함수
        elif button_text == "sin":
            self.apply_function(self.sin_func)
        elif button_text == "cos":
            self.apply_function(self.cos_func)
        elif button_text == "tan":
            self.apply_function(self.tan_func)

        # 쌍곡함수
        elif button_text == "sinh":
            self.apply_function(lambda x: math.sinh(float(x)))
        elif button_text == "cosh":
            self.apply_function(lambda x: math.cosh(float(x)))
        elif button_text == "tanh":
            self.apply_function(lambda x: math.tanh(float(x)))

        # 지수/로그
        elif button_text == "ln":
            self.apply_function(lambda x: math.log(float(x)))
        elif button_text == "log₁₀":
            self.apply_function(lambda x: math.log10(float(x)))
        elif button_text == "eˣ":
            self.apply_function(lambda x: math.exp(float(x)))
        elif button_text == "10ˣ":
            self.apply_function(lambda x: math.pow(10, float(x)))

        # 제곱/제곱근
        elif button_text == "x²":
            self.apply_function(lambda x: math.pow(float(x), 2))
        elif button_text == "x³":
            self.apply_function(lambda x: math.pow(float(x), 3))
        elif button_text == "²√x":
            self.apply_function(lambda x: math.sqrt(float(x)))
        elif button_text == "³√x":
            self.apply_function(lambda x: math.pow(float(x), 1/3))

        # 기타 함수
        elif button_text == "1/x":
            self.apply_function(lambda x: 1/float(x))
        elif button_text == "x!":
            self.apply_function(lambda x: math.factorial(int(float(x))))

        # 랜덤
        elif button_text == "Rand":
            import random
            self.input = str(round(random.random(), 10))

        # EE (과학적 표기법)
        elif button_text == "EE":
            if "e" not in self.input:
                self.input += "e"

        # 연산자 변환
        elif button_text == "÷":
            super().button_clicked("/")
        elif button_text == "×":
            super().button_clicked("*")
        elif button_text == "−":
            super().button_clicked("-")
        elif button_text == "+/−":
            super().button_clicked("+/-")

        # 괄호
        elif button_text == "(":
            self.add_parenthesis("(")
        elif button_text == ")":
            self.add_parenthesis(")")

        # 기본 계산기 기능
        else:
            super().button_clicked(button_text)

        self.update_display()

    def sin_func(self, x):
        """사인 함수 (각도 모드 고려)"""
        val = float(x)
        if self.angle_mode == "Deg":
            val = math.radians(val)
        return math.sin(val)

    def cos_func(self, x):
        """코사인 함수 (각도 모드 고려)"""
        val = float(x)
        if self.angle_mode == "Deg":
            val = math.radians(val)
        return math.cos(val)

    def tan_func(self, x):
        """탄젠트 함수 (각도 모드 고려)"""
        val = float(x)
        if self.angle_mode == "Deg":
            val = math.radians(val)
        return math.tan(val)

    def add_constant(self, value):
        """상수 추가"""
        if self.input == "0" or self.input == "":
            self.input = value
        else:
            self.input_append_expression()
            self.expression.append("*")
            self.input = value

    def apply_function(self, func):
        """함수 적용"""
        try:
            if self.input and self.input != "0":
                result = func(self.input)
                self.input = str(round(result, 10))
            elif self.expression:
                # expression의 마지막 숫자에 함수 적용
                if self.expression and self.expression[-1] not in self.operator:
                    last_val = self.expression[-1]
                    result = func(last_val)
                    self.expression[-1] = str(round(result, 10))
        except (ValueError, OverflowError, ZeroDivisionError):
            self.input = "Error"

    def add_parenthesis(self, paren):
        """괄호 추가"""
        if paren == "(":
            if self.input == "0" or self.input == "":
                self.expression.append("(")
            else:
                self.input_append_expression()
                self.expression.append("*")
                self.expression.append("(")
        else:  # paren == ")"
            if self.input and self.input != "0":
                self.input_append_expression()
            self.expression.append(")")

    def update_display(self):
        """디스플레이 업데이트"""
        if hasattr(self, 'display'):
            base = ""
            if self.expression:
                if self.expression[0] == "0" and len(self.expression) > 1:
                    self.expression = self.expression[1:]
                base = "".join(str(x) for x in self.expression)

            input_txt = self.input if self.input != "" else "0"
            if self.is_input_nagative and self.input != "":
                input_txt = "(-" + self.input + ")"

            display_text = base + input_txt
            if display_text == "":
                display_text = "0"

            self.display.setText(display_text)

    def reset(self):
        """초기화 (부모 클래스 오버라이드)"""
        super().reset()
        if hasattr(self, 'display'):
            self.display.setText("0")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = EngineerCalculator()
    calculator.show()
    sys.exit(app.exec())