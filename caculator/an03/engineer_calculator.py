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
from PyQt6.QtGui import QFont, QFontMetrics
from calculator import Calculator


class EngineerCalculator(Calculator):
    def __init__(self):
        self.angle_mode = "Rad"  # Rad, Deg
        self.memory_value = 0
        super().__init__()

    def setup_ui(self):
        # 메인 윈도우 설정
        self.setWindowTitle("공학용 계산기")
        self.setFixedSize(400, 780)
        self.setStyleSheet("background-color: #000000;")

        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(8, 35, 8, 8)

        # 디스플레이 영역 설정
        self.display = QLabel("0")
        self.display.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom
        )
        self.display.setStyleSheet(
            """
            QLabel {
                color: #FFFFFF;
                background-color: transparent;
                padding: 20px;
            }
        """
        )
        self.display.setMinimumHeight(160)
        self.display.setWordWrap(False)  # 텍스트 줄바꿈 방지

        # 초기 폰트 설정 - 기본 10으로 설정
        initial_font = QFont("SF Pro Display", 15)
        initial_font.setWeight(200)
        self.display.setFont(initial_font)

        main_layout.addWidget(self.display)

        # 버튼 영역
        button_widget = QWidget()
        button_layout = QGridLayout(button_widget)
        button_layout.setSpacing(6)  # 버튼 간격 균일화
        button_layout.setContentsMargins(0, 0, 0, 0)

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

                # 버튼 크기 설정 (균일한 크기)
                button_width = 62  # 전체 너비에 맞게 조정
                button_height = 62  # 정사각형에 가까운 비율

                if colspan == 2:
                    button.setFixedSize(
                        button_width * 2 + 6, button_height
                    )  # colspan 고려
                else:
                    button.setFixedSize(button_width, button_height)

                # 버튼 스타일 설정
                button.setStyleSheet(self.get_ios_button_style(button_type))

                # 폰트 설정 (버튼 크기에 맞게 조정)
                font = QFont("SF Pro Display", 28)
                if button_type == "function":
                    font.setPointSize(16)  # 기능 버튼은 더 작은 폰트
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
                {"text": "mr", "type": "function"},
            ],
            # 2행: 2nd, 지수, 거듭제곱
            [
                {"text": "2nd", "type": "function"},
                {"text": "x²", "type": "function"},
                {"text": "x³", "type": "function"},
                {"text": "xʸ", "type": "function"},
                {"text": "eˣ", "type": "function"},
                {"text": "10ˣ", "type": "function"},
            ],
            # 3행: 역수, 제곱근
            [
                {"text": "1/x", "type": "function"},
                {"text": "²√x", "type": "function"},
                {"text": "³√x", "type": "function"},
                {"text": "ʸ√x", "type": "function"},
                {"text": "ln", "type": "function"},
                {"text": "log₁₀", "type": "function"},
            ],
            # 4행: 팩토리얼, 삼각함수
            [
                {"text": "x!", "type": "function"},
                {"text": "sin", "type": "function"},
                {"text": "cos", "type": "function"},
                {"text": "tan", "type": "function"},
                {"text": "e", "type": "function"},
                {"text": "EE", "type": "function"},
            ],
            # 5행: 랜덤, 쌍곡함수
            [
                {"text": "Rand", "type": "function"},
                {"text": "sinh", "type": "function"},
                {"text": "cosh", "type": "function"},
                {"text": "tanh", "type": "function"},
                {"text": "π", "type": "function"},
                {"text": "Rad", "type": "function"},
            ],
            # 6행: 기능 버튼
            [
                {"text": "⌫", "type": "clear", "colspan": 2},
                None,
                {"text": "AC", "type": "clear"},
                {"text": "%", "type": "clear"},
                {"text": "÷", "type": "operator"},
            ],
            # 7행: 숫자 7,8,9와 곱셈
            [
                {"text": "7", "type": "number"},
                {"text": "8", "type": "number"},
                {"text": "9", "type": "number"},
                {"text": "×", "type": "operator"},
            ],
            # 8행: 숫자 4,5,6와 뺄셈
            [
                {"text": "4", "type": "number"},
                {"text": "5", "type": "number"},
                {"text": "6", "type": "number"},
                {"text": "−", "type": "operator"},
            ],
            # 9행: 숫자 1,2,3와 덧셈
            [
                {"text": "1", "type": "number"},
                {"text": "2", "type": "number"},
                {"text": "3", "type": "number"},
                {"text": "+", "type": "operator"},
            ],
            # 10행: +/-, 0, 소수점, 등호
            [
                {"text": "+/−", "type": "number"},
                {"text": "0", "type": "number"},
                {"text": ".", "type": "number"},
                {"text": "=", "type": "operator"},
            ],
        ]

    def get_ios_button_style(self, button_type):
        """iOS 스타일 버튼 디자인"""
        base_style = """
            QPushButton {
                border: none;
                border-radius: 31px;
                font-weight: 400;
                color: #FFFFFF;
            }
            QPushButton:pressed {
                opacity: 0.7;
            }
        """

        if button_type == "number":
            # 숫자 버튼 (진한 회색)
            return (
                base_style
                + """
                QPushButton {
                    background-color: #333333;
                    color: #FFFFFF;
                }
                QPushButton:pressed {
                    background-color: #666666;
                }
            """
            )
        elif button_type == "operator":
            # 연산자 버튼 (주황색)
            return (
                base_style
                + """
                QPushButton {
                    background-color: #FF9500;
                    color: #FFFFFF;
                }
                QPushButton:pressed {
                    background-color: #FFCC80;
                }
            """
            )
        elif button_type == "clear":
            # 클리어 버튼 (밝은 회색)
            return (
                base_style
                + """
                QPushButton {
                    background-color: #A6A6A6;
                    color: #000000;
                }
                QPushButton:pressed {
                    background-color: #D4D4D4;
                }
            """
            )
        else:  # function
            # 기능 버튼 (검은색)
            return (
                base_style
                + """
                QPushButton {
                    background-color: #000000;
                    color: #FFFFFF;
                    border: 1px solid #666666;
                }
                QPushButton:pressed {
                    background-color: #333333;
                }
            """
            )

    def engineer_button_clicked(self, button_text):
        pass

    def update_display(self):
        """디스플레이 업데이트 - 스마트 텍스트 처리 및 동적 폰트 크기 조정"""
        if hasattr(self, "display"):
            # 기본 텍스트 구성
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

            # 텍스트 포맷팅 (숫자인 경우 반올림)
            formatted_text = self.format_display_text(display_text)

            # 폰트 크기는 항상 10으로 고정
            font = QFont("SF Pro Display", 10)
            font.setWeight(200)
            self.display.setFont(font)
            self.display.setText(formatted_text)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    calculator = EngineerCalculator()
    calculator.show()

    sys.exit(app.exec())
