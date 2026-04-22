from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_RegisterForm(object):
    def setupUi(self, RegisterForm):
        RegisterForm.setObjectName("RegisterForm")
        RegisterForm.resize(450, 520)
        
        # Thiết lập nền trong suốt và không viền để đồng bộ với giao diện Đăng nhập
        RegisterForm.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        RegisterForm.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.mainLayout = QtWidgets.QVBoxLayout(RegisterForm)
        self.mainLayout.setContentsMargins(15, 15, 15, 15)
        self.mainLayout.setObjectName("mainLayout")

        # Container chính để vẽ nền trắng và bo góc
        self.container = QtWidgets.QFrame(parent=RegisterForm)
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            #container {
                background-color: white;
                border-radius: 20px;
                border: 1px solid #dcdde1;
            }
        """)
        
        self.vboxlayout = QtWidgets.QVBoxLayout(self.container)
        self.vboxlayout.setContentsMargins(40, 30, 40, 40)
        self.vboxlayout.setSpacing(15)
        self.vboxlayout.setObjectName("vboxlayout")

        # --- ICON ---
        self.labelIcon = QtWidgets.QLabel(parent=self.container)
        self.labelIcon.setText("👤")
        self.labelIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelIcon.setStyleSheet("font-size: 50px; border: none; margin-bottom: 5px;")
        self.vboxlayout.addWidget(self.labelIcon)

        # --- TIÊU ĐỀ ---
        self.label = QtWidgets.QLabel(parent=self.container)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        # --- TÊN ĐĂNG NHẬP ---
        self.txtUser = QtWidgets.QLineEdit(parent=self.container)
        self.txtUser.setMinimumHeight(45)
        self.txtUser.setObjectName("txtUser")
        self.vboxlayout.addWidget(self.txtUser)

        # --- MẬT KHẨU ---
        self.txtPass = QtWidgets.QLineEdit(parent=self.container)
        self.txtPass.setMinimumHeight(45)
        self.txtPass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txtPass.setObjectName("txtPass")
        self.vboxlayout.addWidget(self.txtPass)

        # --- VAI TRÒ (ComboBox) ---
        self.cboRole = QtWidgets.QComboBox(parent=self.container)
        self.cboRole.setMinimumHeight(45)
        self.cboRole.setObjectName("cboRole")
        self.cboRole.addItem("")
        self.cboRole.addItem("") # Thêm Admin nếu cần
        self.vboxlayout.addWidget(self.cboRole)

        # --- NÚT TẠO TÀI KHOẢN ---
        self.btnCreate = QtWidgets.QPushButton(parent=self.container)
        self.btnCreate.setMinimumHeight(50)
        self.btnCreate.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnCreate.setObjectName("btnCreate")
        self.vboxlayout.addWidget(self.btnCreate)

        # --- NÚT ĐÓNG/HỦY ---
        self.btnCancel = QtWidgets.QPushButton("Hủy bỏ", parent=self.container)
        self.btnCancel.setMinimumHeight(30)
        self.btnCancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnCancel.setStyleSheet("border: none; color: #7f8c8d; text-decoration: underline;")
        self.vboxlayout.addWidget(self.btnCancel)

        self.mainLayout.addWidget(self.container)

        self.retranslateUi(RegisterForm)
        QtCore.QMetaObject.connectSlotsByName(RegisterForm)

    def retranslateUi(self, RegisterForm):
        _translate = QtCore.QCoreApplication.translate
        RegisterForm.setWindowTitle(_translate("RegisterForm", "Đăng ký tài khoản"))
        
        # Style cho Tiêu đề (Đồng bộ font và màu xanh đậm)
        self.label.setText(_translate("RegisterForm", "ĐĂNG KÝ "))
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; border: none; margin-bottom: 10px;")

        # Style cho Input và ComboBox (Đồng bộ với các form nhập liệu)
        input_style = """
            QLineEdit, QComboBox {
                border: 2px solid #ecf0f1;
                border-radius: 10px;
                padding-left: 15px;
                background-color: #f9f9f9;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #3498db;
                background-color: white;
            }
        """
        self.txtUser.setStyleSheet(input_style)
        self.txtPass.setStyleSheet(input_style)
        self.cboRole.setStyleSheet(input_style)

        self.txtUser.setPlaceholderText(_translate("RegisterForm", "Tên đăng nhập mới"))
        self.txtPass.setPlaceholderText(_translate("RegisterForm", "Mật khẩu"))
        self.cboRole.setItemText(0, _translate("RegisterForm", "Nhân Viên"))
        self.cboRole.setItemText(1, _translate("RegisterForm", "Quản Trị Viên"))

        # Style cho nút bấm (Màu xanh Blue chủ đạo)
        self.btnCreate.setText(_translate("RegisterForm", "TẠO TÀI KHOẢN"))
        self.btnCreate.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 10px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RegisterForm = QtWidgets.QWidget()
    ui = Ui_RegisterForm()
    ui.setupUi(RegisterForm)
    RegisterForm.show()
    sys.exit(app.exec())