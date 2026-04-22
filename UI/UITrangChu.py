from PyQt6 import QtCore, QtGui, QtWidgets
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 750)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.hbox_main = QtWidgets.QHBoxLayout(self.centralwidget)
        self.hbox_main.setContentsMargins(0, 0, 0, 0)
        self.hbox_main.setSpacing(0)

        # ================= SIDEBAR (THANH CÔNG CỤ CỐ ĐỊNH) =================
        self.sidebar = QtWidgets.QFrame(parent=self.centralwidget)
        self.sidebar.setMinimumSize(QtCore.QSize(280, 0))
        self.sidebar.setStyleSheet("background-color: #2c3e50; color: white;")
        self.vbox_menu = QtWidgets.QVBoxLayout(self.sidebar)
        self.vbox_menu.setContentsMargins(0, 0, 0, 20)
        self.vbox_menu.setSpacing(0)

        self.lbl_logo = QtWidgets.QLabel("LIBRARY PRO")
        self.lbl_logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_logo.setStyleSheet("font-size: 22pt; font-weight: bold; padding: 40px; color: #ecf0f1;")
        self.vbox_menu.addWidget(self.lbl_logo)

        # Style menu
        menu_btn_style = """
            QPushButton {
                text-align: left; padding: 15px 30px; font-size: 12pt; border: none; color: #bdc3c7; background-color: transparent;
            }
            QPushButton:hover { background-color: #34495e; color: white; border-left: 5px solid #3498db; }
            QPushButton:checked { background-color: #34495e; color: white; border-left: 5px solid #3498db; }
        """

        # Các nút chức năng
        self.btnTrangChu = QtWidgets.QPushButton("🏠  Trang chủ")
        self.btnSach = QtWidgets.QPushButton("📚  Quản lý sách")
        self.btnMuonSach = QtWidgets.QPushButton("📖  Quản lý mượn sách")
        self.btnTraSach = QtWidgets.QPushButton("🔄  Quản lý trả sách")
        self.btnNhapHang = QtWidgets.QPushButton("📦  Nhập hàng")
        self.btnNCC = QtWidgets.QPushButton("🏢  Nhà cung cấp")
        self.btnNhanVien = QtWidgets.QPushButton("👥 Quản lý Nhân viên")
        self.btnThongKe = QtWidgets.QPushButton("📊  Thống kê báo cáo")
        self.btnTaiKhoan = QtWidgets.QPushButton("👤  Quản lý tài khoản")

        self.menu_buttons = [self.btnTrangChu, self.btnSach, self.btnMuonSach, self.btnTraSach, 
                             self.btnNhapHang, self.btnNCC, self.btnNhanVien, self.btnThongKe, self.btnTaiKhoan]

        for btn in self.menu_buttons:
            btn.setCheckable(True) # Để có thể đánh dấu nút đang chọn
            btn.setAutoExclusive(True) # Chỉ một nút được sáng lên tại một thời điểm
            btn.setStyleSheet(menu_btn_style)
            self.vbox_menu.addWidget(btn)

        self.vbox_menu.addStretch()

        self.btnLogout = QtWidgets.QPushButton("🚪  Đăng xuất")
        self.btnLogout.setStyleSheet("background-color: #e74c3c; color: white; padding: 15px; font-weight: bold; border: none;")
        self.vbox_menu.addWidget(self.btnLogout)

        self.hbox_main.addWidget(self.sidebar)

        # ================= VÙNG NỘI DUNG THAY ĐỔI (STACKED WIDGET) =================
        self.StackedWidget = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.StackedWidget.setStyleSheet("background-color: #f5f6fa;")
        
        # Trang 1: Giao diện Trang Chủ mặc định (Thống kê + Table)
        self.page_home = QtWidgets.QWidget()
        self.setup_home_page(self.page_home)
        self.StackedWidget.addWidget(self.page_home)

        self.hbox_main.addWidget(self.StackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

    def setup_home_page(self, page):
        """Thiết kế nội dung trang chủ mặc định"""
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        title = QtWidgets.QLabel("TRANG CHỦ")
        title.setStyleSheet("font-size:24px; font-weight:bold; color: #2f3640;")
        layout.addWidget(title)
        layout.setAlignment(title, QtCore.Qt.AlignmentFlag.AlignCenter)

        # Thẻ thống kê nhanh
        stats_layout = QtWidgets.QHBoxLayout()
        stats_layout.addWidget(self.create_box("TỔNG SÁCH", "1,520", "#1abc9c"))
        stats_layout.addWidget(self.create_box("ĐANG MƯỢN", "84", "#f1c40f"))
        stats_layout.addWidget(self.create_box("QUÁ HẠN", "09", "#e74c3c"))
        layout.addLayout(stats_layout)

        # Bảng danh sách
        self.tableSach = QtWidgets.QTableWidget()
        self.tableSach.setColumnCount(4)
        self.tableSach.setHorizontalHeaderLabels(["ID", "Tên sách", "Tác giả", "Số lượng"])
        self.tableSach.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableSach.setStyleSheet("background-color: white; border-radius: 10px;")
        layout.addWidget(self.tableSach)

    def create_box(self, title, value, color):
        box = QtWidgets.QFrame()
        box.setStyleSheet(f"background-color: {color}; border-radius: 15px; min-height: 120px;")
        l = QtWidgets.QVBoxLayout(box)
        t = QtWidgets.QLabel(title); t.setStyleSheet("color: white; font-weight: bold;")
        v = QtWidgets.QLabel(value); v.setStyleSheet("color: white; font-size: 24pt; font-weight: bold;")
        l.addWidget(t); l.addWidget(v)
        return box

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())