from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_LoginForm(object):
    def setupUi(self, LoginForm):
        LoginForm.setObjectName("LoginForm")
        LoginForm.resize(450, 500)
        
        # Thiết lập nền trong suốt và không viền để bo góc đẹp
        LoginForm.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        LoginForm.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.mainLayout = QtWidgets.QVBoxLayout(LoginForm)
        self.mainLayout.setContentsMargins(15, 15, 15, 15)

        # Frame chứa nội dung chính để vẽ nền trắng
        self.container = QtWidgets.QFrame(parent=LoginForm)
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
        self.vboxlayout.setSpacing(20)

        # Icon và Tiêu đề
        self.labelIcon = QtWidgets.QLabel("🔐")
        self.labelIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelIcon.setStyleSheet("font-size: 60px; border: none;")
        self.vboxlayout.addWidget(self.labelIcon)

        self.label = QtWidgets.QLabel("HỆ THỐNG THƯ VIỆN")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50; border: none;")
        self.vboxlayout.addWidget(self.label)

        # Input
        self.txtUser = QtWidgets.QLineEdit()
        self.txtUser.setPlaceholderText("Tên đăng nhập")
        self.txtUser.setMinimumHeight(45)
        self.txtUser.setStyleSheet("border: 2px solid #ecf0f1; border-radius: 10px; padding-left: 15px;")
        self.vboxlayout.addWidget(self.txtUser)

        self.txtPass = QtWidgets.QLineEdit()
        self.txtPass.setPlaceholderText("Mật khẩu")
        self.txtPass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txtPass.setMinimumHeight(45)
        self.txtPass.setStyleSheet("border: 2px solid #ecf0f1; border-radius: 10px; padding-left: 15px;")
        self.vboxlayout.addWidget(self.txtPass)

        # Button
        self.btnLogin = QtWidgets.QPushButton("ĐĂNG NHẬP")
        self.btnLogin.setMinimumHeight(50)
        self.btnLogin.setStyleSheet("background-color: #3498db; color: white; border-radius: 10px; font-weight: bold;")
        self.vboxlayout.addWidget(self.btnLogin)

        self.btnClose = QtWidgets.QPushButton("Thoát ứng dụng")
        self.btnClose.setStyleSheet("border: none; color: #7f8c8d; text-decoration: underline;")
        self.vboxlayout.addWidget(self.btnClose)

        self.mainLayout.addWidget(self.container)