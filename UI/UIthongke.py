from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_ThongKe(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        
        # --- SIDEBAR (Đồng bộ hệ thống) ---
        self.sidebar = QtWidgets.QFrame(parent=self.centralwidget)
        self.sidebar.setMinimumSize(QtCore.QSize(230, 0))
        self.sidebar.setMaximumSize(QtCore.QSize(230, 16777215))
        self.sidebar.setStyleSheet("background-color:#2c3e50; color:white;")
        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        
        self.labelLogo = QtWidgets.QLabel("LIBRARY PRO")
        self.labelLogo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelLogo.setStyleSheet("font-size:20px; font-weight:bold; padding:20px; color:#ecf0f1;")
        self.sidebarLayout.addWidget(self.labelLogo)
        
        # Các nút Sidebar (Giữ nguyên tên biến để main.py không lỗi)
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
        
        self.btnThongKe.setStyleSheet(btn_sidebar_style + "background:#3498db; color:white; font-weight:bold; border-radius:5px;")
        
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
        
        self.labelTitle = QtWidgets.QLabel("BÁO CÁO THỐNG KÊ CHI TIẾT")
        self.labelTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setStyleSheet("font-size:24px; font-weight:bold; color: #2f3640;")
        self.contentLayout.addWidget(self.labelTitle)

        # 1. BỘ LỌC THỐNG KÊ (FILTER BAR)
        self.filterContainer = QtWidgets.QFrame()
        self.filterContainer.setStyleSheet("background: white; border-radius: 8px; border: 1px solid #dcdde1;")
        self.filterLayout = QtWidgets.QHBoxLayout(self.filterContainer)
        self.filterLayout.setContentsMargins(15, 10, 15, 10)

        self.cbLoaiThongKe = QtWidgets.QComboBox()
        self.cbLoaiThongKe.addItems(["Sách được mượn nhiều nhất", "Tỉ lệ trả sách (Đúng hẹn/Trễ)"])
        
        self.cbThoiGian = QtWidgets.QComboBox()
        self.cbThoiGian.addItems(["Tất cả thời gian", "Hôm nay", "Tháng này", "Năm nay"])

        self.btnXemBaoCao = QtWidgets.QPushButton("🔍 Xem báo cáo")
        self.btnXemBaoCao.setStyleSheet("background:#3498db; color:white; font-weight:bold; height:35px; padding: 0 20px; border-radius:5px; border:none;")

        self.filterLayout.addWidget(QtWidgets.QLabel("Tiêu chí:"))
        self.filterLayout.addWidget(self.cbLoaiThongKe)
        self.filterLayout.addSpacing(20)
        self.filterLayout.addWidget(QtWidgets.QLabel("Thời gian:"))
        self.filterLayout.addWidget(self.cbThoiGian)
        self.filterLayout.addStretch()
        self.filterLayout.addWidget(self.btnXemBaoCao)

        self.contentLayout.addWidget(self.filterContainer)

        # 2. KHU VỰC BIỂU ĐỒ (CHART AREA)
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("border: none; background: transparent;")
        
        self.scrollWidget = QtWidgets.QWidget()
        self.chartsLayout = QtWidgets.QVBoxLayout(self.scrollWidget)
        self.chartsLayout.setSpacing(20)

        # Frame cho Biểu đồ cột
        self.barFrame = QtWidgets.QFrame()
        self.barFrame.setMinimumHeight(350)
        self.barFrame.setStyleSheet("background: white; border-radius: 10px; border: 1px solid #dcdde1;")
        self.barVLayout = QtWidgets.QVBoxLayout(self.barFrame)
        self.barVLayout.addWidget(QtWidgets.QLabel("BIỂU ĐỒ CỘT DỮ LIỆU", alignment=QtCore.Qt.AlignmentFlag.AlignCenter))
        
        # Frame cho Biểu đồ tròn
        self.pieFrame = QtWidgets.QFrame()
        self.pieFrame.setMinimumHeight(350)
        self.pieFrame.setStyleSheet("background: white; border-radius: 10px; border: 1px solid #dcdde1;")
        self.pieVLayout = QtWidgets.QVBoxLayout(self.pieFrame)
        self.pieVLayout.addWidget(QtWidgets.QLabel("BIỂU ĐỒ TRÒN TỈ LỆ", alignment=QtCore.Qt.AlignmentFlag.AlignCenter))

        self.chartsLayout.addWidget(self.barFrame)
        self.chartsLayout.addWidget(self.pieFrame)
        
        self.scrollArea.setWidget(self.scrollWidget)
        self.contentLayout.addWidget(self.scrollArea)

        self.mainLayout.addWidget(self.content)
        MainWindow.setCentralWidget(self.centralwidget)

        # Style cho ComboBox - Cập nhật để tránh lỗi bôi trắng khi hover
        self.cbLoaiThongKe.setView(QtWidgets.QListView()) # Thêm dòng này để xử lý view cho item
        self.cbThoiGian.setView(QtWidgets.QListView())    # Thêm dòng này để xử lý view cho item
        
        cb_style = """
            QComboBox {
                height: 30px; 
                border: 1px solid #dcdde1; 
                border-radius: 5px; 
                padding-left: 10px; 
                min-width: 200px;
                background: white;
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid #dcdde1;
                selection-background-color: #f1f2f6; /* Màu nền khi di chuột (xám nhẹ) */
                selection-color: #3498db;           /* Màu chữ khi di chuột (xanh) */
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                min-height: 35px;
                padding-left: 10px;
            }
        """
        self.cbLoaiThongKe.setStyleSheet(cb_style)
        self.cbThoiGian.setStyleSheet(cb_style)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_ThongKe()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())