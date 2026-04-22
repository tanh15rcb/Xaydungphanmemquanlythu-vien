from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_QuanLyTraSach(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 750)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # --- SIDEBAR (Giữ nguyên) ---
        self.sidebar = QtWidgets.QFrame(parent=self.centralwidget)
        self.sidebar.setMinimumSize(QtCore.QSize(230, 0))
        self.sidebar.setMaximumSize(QtCore.QSize(230, 16777215))
        self.sidebar.setStyleSheet("background-color:#2c3e50; color:white;")
        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        
        self.labelLogo = QtWidgets.QLabel("LIBRARY PRO")
        self.labelLogo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelLogo.setStyleSheet("font-size:20px; font-weight:bold; padding:20px; color:#ecf0f1;")
        self.sidebarLayout.addWidget(self.labelLogo)
        
        self.btnTrangChu = QtWidgets.QPushButton("🏠  Trang chủ")
        self.btnSach = QtWidgets.QPushButton("📚  Quản lý sách")
        self.btnMuonSach = QtWidgets.QPushButton("📖  Quản lý mượn sách")
        self.btnTraSach = QtWidgets.QPushButton("🔄  Quản lý trả sách")
        self.btnNhapHang = QtWidgets.QPushButton("📦  Nhập hàng")
        self.btnNCC = QtWidgets.QPushButton("🏢  Nhà cung cấp")
        self.btnNhanVien = QtWidgets.QPushButton("👥 Quản lý Nhân viên")
        self.btnThongKe = QtWidgets.QPushButton("📊  Thống kê báo cáo")
        self.btnTaiKhoan = QtWidgets.QPushButton("👤  Quản lý tài khoản")
        
        self.sidebar_buttons = [
            self.btnTrangChu, self.btnSach, self.btnMuonSach, self.btnTraSach,
            self.btnNhapHang, self.btnNCC, self.btnNhanVien, self.btnThongKe, self.btnTaiKhoan
        ]
        
        btn_sidebar_style = """
            QPushButton {
                text-align: left; padding-left: 15px; height: 40px; 
                border:none; color: #bdc3c7; font-size: 13px;
            }
            QPushButton:hover { background-color: #34495e; color: white; }
        """
        for btn in self.sidebar_buttons:
            btn.setStyleSheet(btn_sidebar_style)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            self.sidebarLayout.addWidget(btn)
        
        self.btnTraSach.setStyleSheet(btn_sidebar_style + "background:#3498db; color:white; font-weight:bold; border-radius:5px;")
        self.sidebarLayout.addStretch()
        self.btnLogout = QtWidgets.QPushButton("🚪  Đăng xuất")
        self.btnLogout.setStyleSheet("background:#e74c3c; color:white; height: 40px; border:none; font-weight:bold; margin: 10px; border-radius:5px;")
        self.sidebarLayout.addWidget(self.btnLogout)
        self.mainLayout.addWidget(self.sidebar)

        # --- CONTENT AREA ---
        self.content = QtWidgets.QFrame(parent=self.centralwidget)
        self.content.setStyleSheet("background:#f5f6fa;")
        self.contentLayout = QtWidgets.QVBoxLayout(self.content)
        self.contentLayout.setContentsMargins(30, 20, 30, 20)
        self.contentLayout.setSpacing(15)
        
        self.labelTitle = QtWidgets.QLabel("QUẢN LÝ TRẢ SÁCH")
        self.labelTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setStyleSheet("font-size:24px; font-weight:bold; color: #2f3640; margin-bottom: 5px;")
        self.contentLayout.addWidget(self.labelTitle)

        # 1. KHỐI NHẬP LIỆU (FORM)
        self.formContainer = QtWidgets.QFrame()
        self.formContainer.setStyleSheet("background: white; border-radius: 8px; border: 1px solid #dcdde1;")
        self.formLayout = QtWidgets.QGridLayout(self.formContainer)
        self.formLayout.setContentsMargins(25, 25, 25, 25)
        self.formLayout.setSpacing(15)

        # --- PHẦN CHỈNH SỬA Ô TÊN SÁCH ---
        self.txtSach = QtWidgets.QLineEdit()
        self.txtSach.setPlaceholderText("Gõ để tìm tên sách...")
        
        # Danh sách sách mẫu (Sau này bạn có thể thay bằng list lấy từ Database)
        self.danh_sach_sach = ["Dế Mèn Phiêu Lưu Ký", "Đắc Nhân Tâm", "Nhà Giả Kim", "Số Đỏ", "Lão Hạc", "Tắt Đèn"]
        
        # Khởi tạo bộ gợi ý (Completer)
        self.completer = QtWidgets.QCompleter(self.danh_sach_sach)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive) # Không phân biệt hoa thường
        self.completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains) # Tìm kiếm chuỗi con bất kỳ
        self.txtSach.setCompleter(self.completer)
        # ---------------------------------

        self.txtMaSV = QtWidgets.QLineEdit()
        self.txtTenSV = QtWidgets.QLineEdit()
        self.dateMuon = QtWidgets.QDateEdit(); self.dateMuon.setCalendarPopup(True)
        self.dateHanTra = QtWidgets.QDateEdit(); self.dateHanTra.setCalendarPopup(True)
        self.dateTra = QtWidgets.QDateEdit(); self.dateTra.setCalendarPopup(True); self.dateTra.setDate(QtCore.QDate.currentDate())
        self.txtTre = QtWidgets.QLineEdit(); self.txtTre.setPlaceholderText("0")
        self.txtPhatNgay = QtWidgets.QLineEdit(); self.txtPhatNgay.setText("2000")
        self.txtTongPhat = QtWidgets.QLineEdit(); self.txtTongPhat.setStyleSheet("font-weight: bold; color: #e74c3c; background: #fff5f5;")

        self.formLayout.addWidget(QtWidgets.QLabel("Mã Sinh viên:"), 0, 0)
        self.formLayout.addWidget(self.txtMaSV, 0, 1)
        self.formLayout.addWidget(QtWidgets.QLabel("Họ tên:"), 0, 2)
        self.formLayout.addWidget(self.txtTenSV, 0, 3)

        self.formLayout.addWidget(QtWidgets.QLabel("Tên sách:"), 1, 0)
        self.formLayout.addWidget(self.txtSach, 1, 1, 1, 3)

        self.formLayout.addWidget(QtWidgets.QLabel("Ngày mượn:"), 2, 0)
        self.formLayout.addWidget(self.dateMuon, 2, 1)
        self.formLayout.addWidget(QtWidgets.QLabel("Hạn trả:"), 2, 2)
        self.formLayout.addWidget(self.dateHanTra, 2, 3)

        self.formLayout.addWidget(QtWidgets.QLabel("Ngày trả thực tế:"), 3, 0)
        self.formLayout.addWidget(self.dateTra, 3, 1)
        self.formLayout.addWidget(QtWidgets.QLabel("Số ngày trễ:"), 3, 2)
        self.formLayout.addWidget(self.txtTre, 3, 3)

        self.formLayout.addWidget(QtWidgets.QLabel("Phạt/Ngày (VNĐ):"), 4, 0)
        self.formLayout.addWidget(self.txtPhatNgay, 4, 1)
        self.formLayout.addWidget(QtWidgets.QLabel("Tổng tiền phạt:"), 4, 2)
        self.formLayout.addWidget(self.txtTongPhat, 4, 3)

        self.contentLayout.addWidget(self.formContainer)

        # 2. KHỐI NÚT CHỨC NĂNG
        self.btnLayout = QtWidgets.QHBoxLayout()
        self.btnTinh = QtWidgets.QPushButton("💰 Tính tiền phạt")
        self.btnTra = QtWidgets.QPushButton("🔄 Xác nhận Trả sách")
        
        btn_style = "height: 42px; border-radius: 5px; font-weight: bold; color: white; min-width: 160px; border:none;"
        self.btnTinh.setStyleSheet(btn_style + "background-color: #f1c40f;")
        self.btnTra.setStyleSheet(btn_style + "background-color: #2ecc71;")
        
        self.btnLayout.addWidget(self.btnTinh)
        self.btnLayout.addWidget(self.btnTra)
        self.btnLayout.addStretch()
        self.contentLayout.addLayout(self.btnLayout)

        # 3. BẢNG DỮ LIỆU
        self.tableMuonTra = QtWidgets.QTableWidget()
        self.tableMuonTra.setColumnCount(8)
        self.tableMuonTra.setHorizontalHeaderLabels(["ID Phiếu", "Mã SV", "Họ Tên", "Sách", "Ngày Mượn", "Hạn Trả", "Ngày Trả", "Tiền Phạt"])
        self.tableMuonTra.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableMuonTra.setStyleSheet("background: white; border-radius: 8px; border: 1px solid #dcdde1;")
        self.contentLayout.addWidget(self.tableMuonTra)

        self.mainLayout.addWidget(self.content)
        MainWindow.setCentralWidget(self.centralwidget)

        # Style chung cho Input
        input_style = "height: 35px; border-radius: 5px; border: 1px solid #dcdde1; padding-left: 10px; background: white;"
        widgets = [self.txtMaSV, self.txtTenSV, self.txtSach, self.dateMuon, 
                   self.dateHanTra, self.dateTra, self.txtTre, self.txtPhatNgay, self.txtTongPhat]
        for w in widgets:
            w.setStyleSheet(input_style)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_QuanLyTraSach()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())