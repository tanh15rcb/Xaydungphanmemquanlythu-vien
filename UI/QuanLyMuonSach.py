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
        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        
        self.labelLogo = QtWidgets.QLabel("LIBRARY PRO")
        self.labelLogo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sidebarLayout.addWidget(self.labelLogo)
        
        self.btnTrangChu = QtWidgets.QPushButton("🏠 Trang chủ")
        self.btnSach = QtWidgets.QPushButton("📚 Quản lý Sách")
        self.btnMuonTra = QtWidgets.QPushButton("📖 Quản lý Mượn Sách")
        self.btnNhap = QtWidgets.QPushButton("📦 Nhập hàng")
        self.btnNCC = QtWidgets.QPushButton("🏢 Nhà cung cấp")
        self.btnUser = QtWidgets.QPushButton("👤 Tài khoản")
        
        for btn in [self.btnTrangChu, self.btnSach, self.btnMuonTra, self.btnNhap, self.btnNCC, self.btnUser]:
            self.sidebarLayout.addWidget(btn)
        
        self.sidebarLayout.addStretch()
        self.btnLogout = QtWidgets.QPushButton("🚪 Đăng xuất")
        self.sidebarLayout.addWidget(self.btnLogout)
        self.mainLayout.addWidget(self.sidebar)

        # --- CONTENT AREA ---
        self.content = QtWidgets.QFrame(parent=self.centralwidget)
        self.contentLayout = QtWidgets.QVBoxLayout(self.content)
        self.contentLayout.setContentsMargins(30, 20, 30, 20)
        self.contentLayout.setSpacing(15)
        
        self.labelTitle = QtWidgets.QLabel(" QUẢN LÝ MƯỢN SÁCH")
        self.labelTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setStyleSheet("font-size:24px; font-weight:bold; color: #2f3640;")
        self.contentLayout.addWidget(self.labelTitle)

        # 1. KHỐI NHẬP LIỆU
        self.formContainer = QtWidgets.QFrame()
        self.formContainer.setStyleSheet("background: white; border-radius: 8px; border: 1px solid #dcdde1;")
        self.formLayout = QtWidgets.QGridLayout(self.formContainer)
        self.formLayout.setContentsMargins(25, 25, 25, 25)
        self.formLayout.setSpacing(15)

        # Inputs
        self.txtMaSV = QtWidgets.QLineEdit()
        self.txtHoTen = QtWidgets.QLineEdit()
        
        # Ô Tên Sách (Giữ LineEdit để sau này gán QCompleter logic gợi ý)
        self.txtTenSach = QtWidgets.QLineEdit()
        self.txtTenSach.setPlaceholderText("Gõ để tìm tên sách...")
        
        self.txtSoLuong = QtWidgets.QLineEdit()
        
        # Ô Hạn Trả (Chuyển sang QDateEdit có hiển thị Lịch)
        self.txtNgayTra = QtWidgets.QDateEdit()
        self.txtNgayTra.setCalendarPopup(True) # Quan trọng: Cho phép hiện lịch khi ấn vào
        self.txtNgayTra.setDateTime(QtCore.QDateTime.currentDateTime()) # Mặc định là ngày hiện tại
        self.txtNgayTra.setDisplayFormat("yyyy-MM-dd") # Định dạng hiển thị

        self.formLayout.addWidget(QtWidgets.QLabel("Mã Sinh Viên:"), 0, 0)
        self.formLayout.addWidget(self.txtMaSV, 0, 1)
        self.formLayout.addWidget(QtWidgets.QLabel("Tên Sách:"), 0, 2)
        self.formLayout.addWidget(self.txtTenSach, 0, 3)
        
        self.formLayout.addWidget(QtWidgets.QLabel("Họ và Tên:"), 1, 0)
        self.formLayout.addWidget(self.txtHoTen, 1, 1)
        self.formLayout.addWidget(QtWidgets.QLabel("Số lượng mượn:"), 1, 2)
        self.formLayout.addWidget(self.txtSoLuong, 1, 3)

        self.formLayout.addWidget(QtWidgets.QLabel("Hạn trả:"), 2, 2)
        self.formLayout.addWidget(self.txtNgayTra, 2, 3)
        
        self.contentLayout.addWidget(self.formContainer)

        # 2. NÚT XÁC NHẬN
        self.actionLayout = QtWidgets.QHBoxLayout()
        self.actionLayout.addStretch()
        self.btnMuon = QtWidgets.QPushButton("Xác Nhận Cho Mượn")
        self.btnMuon.setFixedWidth(200)
        self.actionLayout.addWidget(self.btnMuon)
        self.contentLayout.addLayout(self.actionLayout)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setStyleSheet("color: #dcdde1;")
        self.contentLayout.addWidget(line)

        # 3. PHẦN TÌM KIẾM
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.txtTimKiem = QtWidgets.QLineEdit()
        self.txtTimKiem.setPlaceholderText("Nhập từ khóa tìm kiếm...")
        self.btnTimKiem = QtWidgets.QPushButton("🔍 Tìm kiếm")
        self.btnTimKiem.setFixedWidth(120)
        
        self.searchLayout.addWidget(self.txtTimKiem)
        self.searchLayout.addWidget(self.btnTimKiem)
        self.contentLayout.addLayout(self.searchLayout)

        # 4. BẢNG DỮ LIỆU
        self.tableMuon = QtWidgets.QTableWidget()
        self.tableMuon.setColumnCount(6)
        self.tableMuon.setHorizontalHeaderLabels(["Mã SV", "Họ Tên", "Tên Sách", "Số Lượng", "Ngày Mượn", "Hạn Trả"])
        self.tableMuon.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.contentLayout.addWidget(self.tableMuon)

        self.mainLayout.addWidget(self.content)
        MainWindow.setCentralWidget(self.centralwidget)

        self.applyStyles()

    def applyStyles(self):
        # Sidebar & Content Background
        self.sidebar.setStyleSheet("background-color:#2c3e50; color:white;")
        self.content.setStyleSheet("background:#f5f6fa;")
        
        # Styles cho inputs và date edit
        input_style = """
            QLineEdit, QDateEdit {
                height: 35px; 
                border-radius: 5px; 
                border: 1px solid #dcdde1; 
                background: white; 
                padding-left: 10px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: 1px solid #dcdde1;
            }
        """
        for ipt in [self.txtMaSV, self.txtHoTen, self.txtTenSach, self.txtSoLuong, self.txtNgayTra, self.txtTimKiem]:
            ipt.setStyleSheet(input_style)
        
        # Style cho nút bấm
        self.btnMuon.setStyleSheet("background-color: #2ecc71; color: white; height: 40px; border-radius: 5px; font-weight: bold;")
        self.btnTimKiem.setStyleSheet("background-color: #34495e; color: white; height: 35px; border-radius: 5px; font-weight: bold;")
        
        # Sidebar buttons... (giữ nguyên các phần style cũ của bạn)
        btn_style = "text-align: left; padding-left: 15px; height: 40px; border:none; color: white;"
        for btn in [self.btnTrangChu, self.btnSach, self.btnMuonTra, self.btnNhap, self.btnNCC, self.btnUser]:
            btn.setStyleSheet(btn_style)
        self.btnMuonTra.setStyleSheet(btn_style + "background:#3498db; font-weight:bold;")
        self.btnLogout.setStyleSheet("background:#e74c3c; color:white; height: 40px; border:none; font-weight:bold;")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())