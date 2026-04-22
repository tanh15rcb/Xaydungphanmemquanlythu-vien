from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_NhaCungCap(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 750)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        
        # --- SIDEBAR (9 nút đồng bộ hệ thống) ---
        self.sidebar = QtWidgets.QFrame(parent=self.centralwidget)
        self.sidebar.setMinimumSize(QtCore.QSize(230, 0))
        self.sidebar.setMaximumSize(QtCore.QSize(230, 16777215))
        self.sidebar.setStyleSheet("background-color:#2c3e50; color:white;")
        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        
        self.labelLogo = QtWidgets.QLabel("LIBRARY PRO")
        self.labelLogo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelLogo.setStyleSheet("font-size:20px; font-weight:bold; padding:20px; color:#ecf0f1;")
        self.sidebarLayout.addWidget(self.labelLogo)
        
        # Các nút Sidebar
        self.btnTrangChu = QtWidgets.QPushButton("🏠   Trang chủ")
        self.btnSach = QtWidgets.QPushButton("📚   Quản lý sách")
        self.btnMuonSach = QtWidgets.QPushButton("📖   Quản lý mượn sách")
        self.btnTraSach = QtWidgets.QPushButton("🔄   Quản lý trả sách")
        self.btnNhapHang = QtWidgets.QPushButton("📦   Nhập hàng")
        self.btnNCC = QtWidgets.QPushButton("🏢   Nhà cung cấp")
        self.btnNhanVien = QtWidgets.QPushButton("👥  Quản lý Nhân viên")
        self.btnThongKe = QtWidgets.QPushButton("📊   Thống kê báo cáo")
        self.btnTaiKhoan = QtWidgets.QPushButton("👤   Quản lý tài khoản")
        
        sidebar_btns = [self.btnTrangChu, self.btnSach, self.btnMuonSach, self.btnTraSach, 
                        self.btnNhapHang, self.btnNCC, self.btnNhanVien, self.btnThongKe, self.btnTaiKhoan]
        
        btn_sidebar_style = "text-align: left; padding-left: 15px; height: 40px; border:none; color: #bdc3c7; font-size: 13px;"
        for btn in sidebar_btns:
            btn.setStyleSheet(btn_sidebar_style)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            self.sidebarLayout.addWidget(btn)
        
        # Active style cho trang Nhà cung cấp
        self.btnNCC.setStyleSheet(btn_sidebar_style + "background:#3498db; color:white; font-weight:bold; border-radius:5px;")
        
        self.sidebarLayout.addStretch()
        self.btnLogout = QtWidgets.QPushButton("🚪   Đăng xuất")
        self.btnLogout.setStyleSheet("background:#e74c3c; color:white; height: 40px; border:none; font-weight:bold; margin: 10px; border-radius:5px;")
        self.sidebarLayout.addWidget(self.btnLogout)
        self.mainLayout.addWidget(self.sidebar)

        # --- CONTENT AREA ---
        self.content = QtWidgets.QFrame(parent=self.centralwidget)
        self.content.setStyleSheet("background:#f5f6fa;")
        self.contentLayout = QtWidgets.QVBoxLayout(self.content)
        self.contentLayout.setContentsMargins(30, 20, 30, 20)
        self.contentLayout.setSpacing(15)
        
        self.labelTitle = QtWidgets.QLabel("QUẢN LÝ NHÀ CUNG CẤP")
        self.labelTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setStyleSheet("font-size:24px; font-weight:bold; color: #2f3640;")
        self.contentLayout.addWidget(self.labelTitle)

        # 1. PHẦN NHẬP LIỆU (FORM) - Thêm dòng Email
        self.formContainer = QtWidgets.QFrame()
        self.formContainer.setStyleSheet("background: white; border-radius: 8px; border: 1px solid #dcdde1;")
        self.formLayout = QtWidgets.QGridLayout(self.formContainer)
        self.formLayout.setContentsMargins(25, 20, 25, 20)
        self.formLayout.setSpacing(15)

        self.txtTenNCC = QtWidgets.QLineEdit()
        self.txtSDT = QtWidgets.QLineEdit()
        self.txtDiaChi = QtWidgets.QLineEdit()
        self.txtEmail = QtWidgets.QLineEdit()

        # Grid sắp xếp 2x2
        self.formLayout.addWidget(QtWidgets.QLabel("Tên nhà cung cấp:"), 0, 0)
        self.formLayout.addWidget(self.txtTenNCC, 0, 1)
        self.formLayout.addWidget(QtWidgets.QLabel("Số điện thoại:"), 0, 2)
        self.formLayout.addWidget(self.txtSDT, 0, 3)
        
        self.formLayout.addWidget(QtWidgets.QLabel("Địa chỉ:"), 1, 0)
        self.formLayout.addWidget(self.txtDiaChi, 1, 1)
        self.formLayout.addWidget(QtWidgets.QLabel("Email liên hệ:"), 1, 2)
        self.formLayout.addWidget(self.txtEmail, 1, 3)

        self.contentLayout.addWidget(self.formContainer)

        # 2. NÚT CHỨC NĂNG
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.btnThem = QtWidgets.QPushButton("➕ Thêm mới")
        self.btnSua = QtWidgets.QPushButton("🔧 Sửa thông tin")
        self.btnXoa = QtWidgets.QPushButton("🗑️ Xóa đối tác")
        
        btn_action_style = "height: 40px; border-radius: 5px; font-weight: bold; color: white; min-width: 130px; border:none;"
        self.btnThem.setStyleSheet(btn_action_style + "background-color: #2ecc71;")
        self.btnSua.setStyleSheet(btn_action_style + "background-color: #f1c40f;")
        self.btnXoa.setStyleSheet(btn_action_style + "background-color: #e74c3c;")

        self.buttonLayout.addWidget(self.btnThem)
        self.buttonLayout.addWidget(self.btnSua)
        self.buttonLayout.addWidget(self.btnXoa)
        self.buttonLayout.addStretch()
        self.contentLayout.addLayout(self.buttonLayout)

        # 3. BẢNG DỮ LIỆU (Cập nhật 5 cột bao gồm Email)
        self.tableNCC = QtWidgets.QTableWidget()
        self.tableNCC.setColumnCount(5)
        self.tableNCC.setHorizontalHeaderLabels(["Mã NCC", "Tên Nhà Cung Cấp", "Địa Chỉ", "Số Điện Thoại", "Email"])
        self.tableNCC.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableNCC.setStyleSheet("background: white; border-radius: 8px; border: 1px solid #dcdde1;")
        self.tableNCC.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.contentLayout.addWidget(self.tableNCC)

        self.mainLayout.addWidget(self.content)
        MainWindow.setCentralWidget(self.centralwidget)

        # Style chung cho Input
        input_style = "height: 35px; border-radius: 5px; border: 1px solid #dcdde1; background: white; padding-left: 10px;"
        for ipt in [self.txtTenNCC, self.txtSDT, self.txtDiaChi, self.txtEmail]:
            ipt.setStyleSheet(input_style)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_NhaCungCap()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())