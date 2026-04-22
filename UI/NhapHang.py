from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_NhapHang(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 750)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        
        # --- SIDEBAR (Đồng bộ 9 nút hệ thống) ---
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
        
        # Active style cho trang Nhập hàng
        self.btnNhapHang.setStyleSheet(btn_sidebar_style + "background:#3498db; color:white; font-weight:bold; border-radius:5px;")
        
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
        
        self.labelTitle = QtWidgets.QLabel("QUẢN LÝ NHẬP HÀNG")
        self.labelTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setStyleSheet("font-size:24px; font-weight:bold; color: #2f3640;")
        self.contentLayout.addWidget(self.labelTitle)

        # 1. PHẦN NHẬP LIỆU (FORM)
        self.formContainer = QtWidgets.QFrame()
        self.formContainer.setStyleSheet("background: white; border-radius: 8px; border: 1px solid #dcdde1;")
        self.formLayout = QtWidgets.QGridLayout(self.formContainer)
        self.formLayout.setContentsMargins(25, 20, 25, 20)
        self.formLayout.setSpacing(15)

        self.cbNCC = QtWidgets.QComboBox()
        self.cbNCC.addItems(["-- Chọn Nhà Cung Cấp --", "NXB Trẻ", "NXB Kim Đồng", "NXB Giáo Dục"])
        
        self.txtTenSach = QtWidgets.QLineEdit()
        self.txtTenSach.setPlaceholderText("Gõ để tìm tên sách hoặc nhập mới...")
        
        # AutoComplete
        self.listSach = ["Dế Mèn Phiêu Lưu Ký", "Đắc Nhân Tâm", "Nhà Giả Kim", "Số Đỏ", "Lão Hạc"]
        self.completer = QtWidgets.QCompleter(self.listSach)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        self.txtTenSach.setCompleter(self.completer)

        self.txtSoLuong = QtWidgets.QLineEdit()
        self.txtDonGia = QtWidgets.QLineEdit()

        # Grid sắp xếp
        self.formLayout.addWidget(QtWidgets.QLabel("Nhà cung cấp:"), 0, 0)
        self.formLayout.addWidget(self.cbNCC, 0, 1)
        self.formLayout.addWidget(QtWidgets.QLabel("Tên sách:"), 0, 2)
        self.formLayout.addWidget(self.txtTenSach, 0, 3)
        
        self.formLayout.addWidget(QtWidgets.QLabel("Số lượng nhập:"), 1, 0)
        self.formLayout.addWidget(self.txtSoLuong, 1, 1)
        self.formLayout.addWidget(QtWidgets.QLabel("Đơn giá (VNĐ):"), 1, 2)
        self.formLayout.addWidget(self.txtDonGia, 1, 3)

        self.contentLayout.addWidget(self.formContainer)

        # 2. NÚT CHỨC NĂNG (Đã bỏ nút Làm mới)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.btnThem = QtWidgets.QPushButton("➕ Thêm vào phiếu")
        self.btnXoa = QtWidgets.QPushButton("🗑️ Xóa dòng chọn")
        
        btn_action_style = "height: 40px; border-radius: 5px; font-weight: bold; color: white; min-width: 150px; border:none;"
        self.btnThem.setStyleSheet(btn_action_style + "background-color: #2ecc71;")
        self.btnXoa.setStyleSheet(btn_action_style + "background-color: #e74c3c;")

        self.buttonLayout.addWidget(self.btnThem)
        self.buttonLayout.addWidget(self.btnXoa)
        self.buttonLayout.addStretch() # Đẩy các nút sang trái
        self.contentLayout.addLayout(self.buttonLayout)

        # 3. BẢNG PHIẾU NHẬP
        self.tableNhap = QtWidgets.QTableWidget()
        self.tableNhap.setColumnCount(5)
        self.tableNhap.setHorizontalHeaderLabels(["STT", "Nhà Cung Cấp", "Tên Sách", "Số Lượng", "Đơn Giá"])
        self.tableNhap.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableNhap.setStyleSheet("background: white; border-radius: 8px; border: 1px solid #dcdde1;")
        self.tableNhap.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.contentLayout.addWidget(self.tableNhap)
        
        # 4. NÚT XÁC NHẬN NHẬP KHO
        self.btnXacNhan = QtWidgets.QPushButton("📦 XÁC NHẬN NHẬP KHO")
        self.btnXacNhan.setStyleSheet("background-color: #27ae60; color: white; height: 50px; font-size: 16px; font-weight: bold; border-radius: 8px; border: none;")
        self.contentLayout.addWidget(self.btnXacNhan)

        self.mainLayout.addWidget(self.content)
        MainWindow.setCentralWidget(self.centralwidget)

        # Style chung cho Input
        input_style = "height: 35px; border-radius: 5px; border: 1px solid #dcdde1; background: white; padding-left: 10px;"
        for ipt in [self.txtTenSach, self.txtSoLuong, self.txtDonGia, self.cbNCC]:
            ipt.setStyleSheet(input_style)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_NhapHang()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())