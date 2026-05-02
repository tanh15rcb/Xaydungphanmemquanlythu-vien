from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_ThongKe(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 850)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        
        # --- SIDEBAR (Giữ nguyên cấu trúc) ---
        self.sidebar = QtWidgets.QFrame(parent=self.centralwidget)
        self.sidebar.setMinimumSize(QtCore.QSize(230, 0))
        self.sidebar.setMaximumSize(QtCore.QSize(230, 16777215))
        self.sidebar.setStyleSheet("background-color:#2c3e50; color:white;")
        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        
        self.labelLogo = QtWidgets.QLabel("LIBRARY PRO")
        self.labelLogo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelLogo.setStyleSheet("font-size:20px; font-weight:bold; padding:20px; color:#ecf0f1;")
        self.sidebarLayout.addWidget(self.labelLogo)
        
        # Các nút Menu
        self.btnTrangChu = QtWidgets.QPushButton("🏠   Trang chủ")
        self.btnSach = QtWidgets.QPushButton("📚   Quản lý sách")
        self.btnMuonSach = QtWidgets.QPushButton("📖   Quản lý mượn sách")
        self.btnTraSach = QtWidgets.QPushButton("🔄   Quản lý trả sách")
        self.btnNhapHang = QtWidgets.QPushButton("📦   Nhập hàng")
        self.btnNCC = QtWidgets.QPushButton("🏢   Nhà cung cấp")
        self.btnNhanVien = QtWidgets.QPushButton("👥   Quản lý Nhân viên")
        self.btnThongKe = QtWidgets.QPushButton("📊   Thống kê báo cáo")
        self.btnTaiKhoan = QtWidgets.QPushButton("👤   Quản lý tài khoản")
        
        sidebar_btns = [self.btnTrangChu, self.btnSach, self.btnMuonSach, self.btnTraSach, 
                        self.btnNhapHang, self.btnNCC, self.btnNhanVien, self.btnThongKe, self.btnTaiKhoan]
        
        btn_style = "text-align: left; padding-left: 15px; height: 40px; border:none; color: #bdc3c7; font-size: 13px;"
        for btn in sidebar_btns:
            btn.setStyleSheet(btn_style)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            self.sidebarLayout.addWidget(btn)
        
        self.btnThongKe.setStyleSheet(btn_style + "background:#3498db; color:white; font-weight:bold; border-radius:5px;")
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
        self.contentLayout.setSpacing(10) # Thu hẹp khoảng cách giữa các phần
        
        self.labelTitle = QtWidgets.QLabel("BÁO CÁO THỐNG KÊ CHI TIẾT")
        self.labelTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setStyleSheet("font-size:24px; font-weight:bold; color: #2f3640; margin-bottom: 5px;")
        self.contentLayout.addWidget(self.labelTitle)

        # 1. BỘ LỌC THỜI GIAN
        self.filterContainer = QtWidgets.QFrame()
        self.filterContainer.setStyleSheet("background: white; border-radius: 8px; border: 1px solid #dcdde1;")
        self.filterLayout = QtWidgets.QHBoxLayout(self.filterContainer)
        self.cbThoiGian = QtWidgets.QComboBox()
        self.cbThoiGian.addItems(["Tất cả thời gian", "Hôm nay", "Tháng này", "Năm nay"])
        self.cbThoiGian.setStyleSheet("height: 30px; border: 1px solid #dcdde1; border-radius: 5px; padding-left: 10px; min-width: 200px;")
        
        self.filterLayout.addWidget(QtWidgets.QLabel("Lọc theo thời gian:"))
        self.filterLayout.addWidget(self.cbThoiGian)
        self.filterLayout.addStretch()
        self.contentLayout.addWidget(self.filterContainer)

        # 2. KHU VỰC BIỂU ĐỒ (Scroll Area)
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("border: none; background: transparent;")
        self.scrollWidget = QtWidgets.QWidget()
        self.chartsLayout = QtWidgets.QVBoxLayout(self.scrollWidget)
        self.chartsLayout.setContentsMargins(0, 10, 10, 10)
        self.chartsLayout.setSpacing(15)

        # --- PHẦN 1: SÁCH ĐƯỢC MƯỢN NHIỀU NHẤT ---
        # Tên biểu đồ 1 (Nằm ngoài khung trắng, đúng vị trí khoanh)
        self.lblBarTitle = QtWidgets.QLabel("Sách được mượn nhiều nhất")
        self.lblBarTitle.setStyleSheet("font-size: 17px; font-weight: bold; color: #34495e; padding-left: 5px;")
        self.chartsLayout.addWidget(self.lblBarTitle)

        # Khung trắng chứa biểu đồ 1
        self.barFrame = QtWidgets.QFrame()
        self.barFrame.setMinimumHeight(400)
        self.barFrame.setStyleSheet("background: white; border-radius: 10px; border: 1px solid #dcdde1;")
        self.barVLayout = QtWidgets.QVBoxLayout(self.barFrame)
        self.barVLayout.setContentsMargins(15, 15, 15, 15)
        # (Đây là nơi bạn sẽ add biểu đồ Matplotlib vào barVLayout trong file main)
        self.chartsLayout.addWidget(self.barFrame)

        # Thêm một khoảng giãn nhỏ giữa 2 phần
        self.chartsLayout.addSpacing(20)

        # --- PHẦN 2: TỈ LỆ TRẢ SÁCH (ĐÚNG HẸN/TRỄ) ---
        # Tên biểu đồ 2 (Nằm ngoài khung trắng, đúng vị trí khoanh)
        self.lblPieTitle = QtWidgets.QLabel("Tỉ lệ trả sách (Đúng hẹn/Trễ)")
        self.lblPieTitle.setStyleSheet("font-size: 17px; font-weight: bold; color: #34495e; padding-left: 5px;")
        self.chartsLayout.addWidget(self.lblPieTitle)

        # Khung trắng chứa biểu đồ 2
        self.pieFrame = QtWidgets.QFrame()
        self.pieFrame.setMinimumHeight(400)
        self.pieFrame.setStyleSheet("background: white; border-radius: 10px; border: 1px solid #dcdde1;")
        self.pieVLayout = QtWidgets.QVBoxLayout(self.pieFrame)
        self.pieVLayout.setContentsMargins(15, 15, 15, 15)
        # (Đây là nơi bạn sẽ add biểu đồ Matplotlib vào pieVLayout trong file main)
        self.chartsLayout.addWidget(self.pieFrame)

        self.scrollArea.setWidget(self.scrollWidget)
        self.contentLayout.addWidget(self.scrollArea)

        self.mainLayout.addWidget(self.content)
        MainWindow.setCentralWidget(self.centralwidget)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_ThongKe()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())