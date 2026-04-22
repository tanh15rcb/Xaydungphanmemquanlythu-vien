from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 750)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # --- SIDEBAR (Đồng bộ với các giao diện trước) ---
        self.sidebar = QtWidgets.QFrame(parent=self.centralwidget)
        self.sidebar.setMinimumSize(QtCore.QSize(220, 0))
        self.sidebar.setMaximumSize(QtCore.QSize(220, 16777215))
        self.sidebar.setStyleSheet("background-color:#2c3e50; color:white;")
        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        
        self.labelLogo = QtWidgets.QLabel("LIBRARY PRO")
        self.labelLogo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelLogo.setStyleSheet("font-size:20px; font-weight:bold; padding:20px; color:#ecf0f1;")
        self.sidebarLayout.addWidget(self.labelLogo)
        
        # Các nút trên Sidebar
        self.btnTrangChu = QtWidgets.QPushButton("🏠 Trang chủ")
        self.btnSach = QtWidgets.QPushButton("📚 Quản lý Sách")
        self.btnMuonTra = QtWidgets.QPushButton("📖 Quản lý Mượn Sách")
        self.btnNhanVien = QtWidgets.QPushButton("👥 Quản lý Nhân viên") # Nút hiện tại
        self.btnNhap = QtWidgets.QPushButton("📦 Nhập hàng")
        self.btnNCC = QtWidgets.QPushButton("🏢 Nhà cung cấp")
        self.btnUser = QtWidgets.QPushButton("👤 Tài khoản")
        
        # Style cho nút Sidebar
        btn_sidebar_style = """
            QPushButton {
                text-align: left; 
                padding-left: 15px; 
                height: 40px; 
                border:none; 
                color: #bdc3c7;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #34495e;
                color: white;
            }
        """
        for btn in [self.btnTrangChu, self.btnSach, self.btnMuonTra, self.btnNhanVien, self.btnNhap, self.btnNCC, self.btnUser]:
            btn.setStyleSheet(btn_sidebar_style)
            self.sidebarLayout.addWidget(btn)
        
        # Highlight nút Nhân viên (vì đang ở trang này)
        self.btnNhanVien.setStyleSheet(btn_sidebar_style + "background:#3498db; color:white; font-weight:bold;")

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
        
        self.labelTitle = QtWidgets.QLabel("QUẢN LÝ NHÂN VIÊN")
        self.labelTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setStyleSheet("font-size:24px; font-weight:bold; color: #2f3640; margin-top: 10px;")
        self.contentLayout.addWidget(self.labelTitle)

        # 1. KHỐI NHẬP LIỆU
        self.formContainer = QtWidgets.QFrame()
        self.formContainer.setStyleSheet("background: white; border-radius: 8px; border: 1px solid #dcdde1;")
        self.formLayout = QtWidgets.QGridLayout(self.formContainer)
        self.formLayout.setContentsMargins(25, 25, 25, 25)
        self.formLayout.setSpacing(15)

        self.txtTenNV = QtWidgets.QLineEdit()
        self.txtTenNV.setPlaceholderText("Nhập đầy đủ họ tên...")
        self.cboGioiTinh = QtWidgets.QComboBox()
        self.cboGioiTinh.addItems(["Nam", "Nữ", "Khác"])
        self.txtSdt = QtWidgets.QLineEdit()
        self.txtEmail = QtWidgets.QLineEdit()
        self.txtDiaChi = QtWidgets.QLineEdit()

        # Add widgets to form
        self.formLayout.addWidget(QtWidgets.QLabel("Họ và Tên:"), 0, 0)
        self.formLayout.addWidget(self.txtTenNV, 0, 1)
        self.formLayout.addWidget(QtWidgets.QLabel("Giới tính:"), 0, 2)
        self.formLayout.addWidget(self.cboGioiTinh, 0, 3)
        
        self.formLayout.addWidget(QtWidgets.QLabel("Số điện thoại:"), 1, 0)
        self.formLayout.addWidget(self.txtSdt, 1, 1)
        self.formLayout.addWidget(QtWidgets.QLabel("Email:"), 1, 2)
        self.formLayout.addWidget(self.txtEmail, 1, 3)

        self.formLayout.addWidget(QtWidgets.QLabel("Địa chỉ:"), 2, 0)
        self.formLayout.addWidget(self.txtDiaChi, 2, 1, 1, 3)
        
        self.contentLayout.addWidget(self.formContainer)

        # 2. NÚT CHỨC NĂNG (Thêm, Sửa, Xóa)
        self.btnActionLayout = QtWidgets.QHBoxLayout()
        self.btnThem = QtWidgets.QPushButton("➕ Thêm mới")
        self.btnSua = QtWidgets.QPushButton("🔧 Cập nhật")
        self.btnXoa = QtWidgets.QPushButton("🗑️ Xóa nhân viên")
        
        btn_action_style = "height: 40px; border-radius: 5px; font-weight: bold; color: white; min-width: 130px; border:none;"
        self.btnThem.setStyleSheet(btn_action_style + "background-color: #2ecc71;")
        self.btnSua.setStyleSheet(btn_action_style + "background-color: #f1c40f;")
        self.btnXoa.setStyleSheet(btn_action_style + "background-color: #e74c3c;")

        self.btnActionLayout.addWidget(self.btnThem)
        self.btnActionLayout.addWidget(self.btnSua)
        self.btnActionLayout.addWidget(self.btnXoa)
        self.btnActionLayout.addStretch()
        self.contentLayout.addLayout(self.btnActionLayout)

        # 3. TÌM KIẾM
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.txtTimKiem = QtWidgets.QLineEdit()
        self.txtTimKiem.setPlaceholderText("Nhập từ khóa tìm kiếm...")
        self.btnTimKiem = QtWidgets.QPushButton("🔍 Tìm kiếm")
        self.btnTimKiem.setFixedWidth(120)
        self.btnTimKiem.setStyleSheet("background-color: #34495e; color: white; height: 35px; border-radius: 5px; font-weight: bold;")
        
        self.searchLayout.addWidget(self.txtTimKiem)
        self.searchLayout.addWidget(self.btnTimKiem)
        self.contentLayout.addLayout(self.searchLayout)

        # 4. BẢNG DỮ LIỆU
        self.tableNV = QtWidgets.QTableWidget()
        self.tableNV.setColumnCount(6)
        self.tableNV.setHorizontalHeaderLabels(["ID", "Họ Tên", "Giới Tính", "SĐT", "Email", "Địa Chỉ"])
        self.tableNV.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableNV.setStyleSheet("background: white; border-radius: 8px; border: 1px solid #dcdde1;")
        self.contentLayout.addWidget(self.tableNV)

        self.mainLayout.addWidget(self.content)
        MainWindow.setCentralWidget(self.centralwidget)

        # Style các ô nhập liệu chung
        input_style = "height: 35px; border-radius: 5px; border: 1px solid #dcdde1; background: white; padding-left: 10px;"
        for ipt in [self.txtTenNV, self.txtSdt, self.txtEmail, self.txtDiaChi, self.txtTimKiem, self.cboGioiTinh]:
            ipt.setStyleSheet(input_style)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())