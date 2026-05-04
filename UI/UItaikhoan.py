from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 750)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # --- SIDEBAR ---
        self.sidebar = QtWidgets.QFrame(parent=self.centralwidget)
        self.sidebar.setMinimumSize(QtCore.QSize(220, 0))
        self.sidebar.setMaximumSize(QtCore.QSize(220, 16777215))
        self.sidebar.setStyleSheet("background-color:#2c3e50; color:white;")
        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        
        self.labelLogo = QtWidgets.QLabel("LIBRARY PRO")
        self.labelLogo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelLogo.setStyleSheet("font-size:20px; font-weight:bold; padding:20px; color:#ecf0f1;")
        self.sidebarLayout.addWidget(self.labelLogo)
        
        # Các nút Sidebar
        self.btnTrangChu = QtWidgets.QPushButton("🏠 Trang chủ")
        self.btnSach = QtWidgets.QPushButton("📚 Quản lý Sách")
        self.btnMuonTra = QtWidgets.QPushButton("📖 Quản lý Mượn Sách")
        self.btnNhanVien = QtWidgets.QPushButton("👥 Quản lý Nhân viên")
        self.btnNhap = QtWidgets.QPushButton("📦 Nhập hàng")
        self.btnNCC = QtWidgets.QPushButton("🏢 Nhà cung cấp")
        self.btnUser = QtWidgets.QPushButton("👤 Tài khoản")
        
        btn_sidebar_style = """
            QPushButton {
                text-align: left; padding-left: 15px; height: 40px; 
                border:none; color: #bdc3c7; font-size: 13px;
            }
            QPushButton:hover { background-color: #34495e; color: white; }
        """
        for btn in [self.btnTrangChu, self.btnSach, self.btnMuonTra, self.btnNhanVien, self.btnNhap, self.btnNCC, self.btnUser]:
            btn.setStyleSheet(btn_sidebar_style)
            self.sidebarLayout.addWidget(btn)
        
        self.btnUser.setStyleSheet(btn_sidebar_style + "background:#3498db; color:white; font-weight:bold;")
        self.sidebarLayout.addStretch()
        
        self.btnLogout = QtWidgets.QPushButton("🚪 Đăng xuất")
        self.btnLogout.setStyleSheet("background:#e74c3c; color:white; height: 40px; border:none; font-weight:bold;")
        self.sidebarLayout.addWidget(self.btnLogout)
        self.mainLayout.addWidget(self.sidebar)

        # --- CONTENT AREA ---
        self.content = QtWidgets.QFrame(parent=self.centralwidget)
        self.content.setStyleSheet("background:#f5f6fa;")
        self.contentLayout = QtWidgets.QVBoxLayout(self.content)
        self.contentLayout.setContentsMargins(30, 20, 30, 20)
        self.contentLayout.setSpacing(15)
        
        self.labelTitle = QtWidgets.QLabel("HỆ THỐNG QUẢN LÝ TÀI KHOẢN")
        self.labelTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setStyleSheet("font-size:24px; font-weight:bold; color: #2f3640; margin-top: 10px;")
        self.contentLayout.addWidget(self.labelTitle)

        # 1. KHỐI NHẬP LIỆU
        self.formContainer = QtWidgets.QFrame()
        self.formContainer.setStyleSheet("background: white; border-radius: 8px; border: 1px solid #dcdde1;")
        self.formLayout = QtWidgets.QGridLayout(self.formContainer)
        self.formLayout.setContentsMargins(25, 25, 25, 25)
        self.formLayout.setSpacing(15)

        self.txtUsername = QtWidgets.QLineEdit()
        self.txtUsername.setPlaceholderText("Tên đăng nhập...")
        self.txtPassword = QtWidgets.QLineEdit()
        self.txtPassword.setPlaceholderText("Mật khẩu...")
        self.txtPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        
        self.cboRole = QtWidgets.QComboBox()
        self.cboRole.addItems(["Admin", "NhanVien"])
        
        self.txtMaNV = QtWidgets.QLineEdit()
        self.txtMaNV.setPlaceholderText("Mã nhân viên (ID)...")

        self.formLayout.addWidget(QtWidgets.QLabel("Tên đăng nhập:"), 0, 0)
        self.formLayout.addWidget(self.txtUsername, 0, 1)
        self.formLayout.addWidget(QtWidgets.QLabel("Mật khẩu:"), 0, 2)
        self.formLayout.addWidget(self.txtPassword, 0, 3)
        
        self.formLayout.addWidget(QtWidgets.QLabel("Vai trò:"), 1, 0)
        self.formLayout.addWidget(self.cboRole, 1, 1)
        self.formLayout.addWidget(QtWidgets.QLabel("Mã nhân viên:"), 1, 2)
        self.formLayout.addWidget(self.txtMaNV, 1, 3)
        
        self.contentLayout.addWidget(self.formContainer)

        # 2. NÚT CHỨC NĂNG
        self.btnActionLayout = QtWidgets.QHBoxLayout()
        self.btnThem = QtWidgets.QPushButton("➕ Thêm tài khoản")
        self.btnSua = QtWidgets.QPushButton("🔧 Cập nhật")
        self.btnXoa = QtWidgets.QPushButton("🗑️ Xóa tài khoản")
        
        btn_action_style = "height: 40px; border-radius: 5px; font-weight: bold; color: white; min-width: 150px; border:none;"
        self.btnThem.setStyleSheet(btn_action_style + "background-color: #2ecc71;")
        self.btnSua.setStyleSheet(btn_action_style + "background-color: #f1c40f;")
        self.btnXoa.setStyleSheet(btn_action_style + "background-color: #e74c3c;")

        self.btnActionLayout.addWidget(self.btnThem)
        self.btnActionLayout.addWidget(self.btnSua)
        self.btnActionLayout.addWidget(self.btnXoa)
        self.btnActionLayout.addStretch()
        self.contentLayout.addLayout(self.btnActionLayout)

        # 3. BẢNG DỮ LIỆU (Đã sửa tiêu đề tiếng Việt)
        self.tableUser = QtWidgets.QTableWidget()
        self.tableUser.setColumnCount(5)
        # Thiết lập tiêu đề cột theo đúng thứ tự bạn yêu cầu
        self.tableUser.setHorizontalHeaderLabels([
            "Mã tài khoản", 
            "Tên đăng nhập", 
            "Mật khẩu", 
            "Vai trò", 
            "Mã nhân viên"
        ])
        
        # Style cho bảng
        self.tableUser.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableUser.setStyleSheet("""
            QTableWidget { background: white; border-radius: 8px; border: 1px solid #dcdde1; }
            QHeaderView::section { background-color: #34495e; color: white; font-weight: bold; height: 35px; border: none; }
        """)
        self.tableUser.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.contentLayout.addWidget(self.tableUser)

        self.mainLayout.addWidget(self.content)
        MainWindow.setCentralWidget(self.centralwidget)

        # Style chung cho Input
        input_style = "height: 35px; border-radius: 5px; border: 1px solid #bdc3c7; background: white; padding-left: 10px;"
        for ipt in [self.txtUsername, self.txtPassword, self.txtMaNV, self.cboRole]:
            ipt.setStyleSheet(input_style)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())