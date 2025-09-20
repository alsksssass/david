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
        self.display_text = "0"
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
        self.display = QLabel(self.display_text)
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

        # 버튼 배치 정의 (5행 × 4열)
        buttons = [
            ["<-", "AC", "%", "÷"],
            ["7", "8", "9", "×"],
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
        elif button_text in ["÷", "×", "-", "+", "="]:
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

    def button_clicked(self, button_text):
        pass

    #     """버튼 클릭 이벤트 처리"""
    #     print(f"Button clicked: {button_text}")

    #     # AC 버튼 처리
    #     if button_text == 'AC':
    #         self.display_text = "0"

    #     # 숫자 버튼 처리
    #     elif button_text.isdigit():
    #         if self.display_text == "0":
    #             self.display_text = button_text
    #         else:
    #             self.display_text += button_text

    #     # 소수점 버튼 처리
    #     elif button_text == '.':
    #         if '.' not in self.display_text:
    #             self.display_text += button_text

    #     # 기타 버튼 처리 (현재는 디스플레이에 표시만)
    #     else:
    #         if self.display_text == "0":
    #             self.display_text = button_text
    #         else:
    #             self.display_text += " " + button_text

    #     # 디스플레이 업데이트
    #     self.display.setText(self.display_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
