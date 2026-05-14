from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_QuanLyGopY(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 750)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # --- SIDEBAR (Đồng bộ hoàn toàn) ---
        self.sidebar = QtWidgets.QFrame(parent=self.centralwidget)
        self.sidebar.setMinimumSize(QtCore.QSize(220, 0))
        self.sidebar.setMaximumSize(QtCore.QSize(220, 16777215))
        self.sidebar.setStyleSheet("background-color:#2c3e50; color:white;")
        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        
        self.labelLogo = QtWidgets.QLabel("LIBRARY PRO")
        self.labelLogo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelLogo.setStyleSheet("font-size:20px; font-weight:bold; padding:20px; color:#ecf0f1;")
        self.sidebarLayout.addWidget(self.labelLogo)
        
        # Danh sách nút Sidebar
        self.btnTrangChu = QtWidgets.QPushButton("🏠 Trang chủ")
        self.btnSach = QtWidgets.QPushButton("📚 Quản lý Sách")
        self.btnMuonTra = QtWidgets.QPushButton("📖 Quản lý Mượn Sách")
        self.btnNhanVien = QtWidgets.QPushButton("👥 Quản lý Nhân viên")
        self.btnNhap = QtWidgets.QPushButton("📦 Nhập hàng")
        self.btnNCC = QtWidgets.QPushButton("🏢 Nhà cung cấp")
        self.btnUser = QtWidgets.QPushButton("👤 Tài khoản")
        self.btnGopY = QtWidgets.QPushButton("💬 Góp ý Sinh viên") # Nút mới thêm

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
        
        self.buttons = [self.btnTrangChu, self.btnSach, self.btnMuonTra, 
                        self.btnNhanVien, self.btnNhap, self.btnNCC, self.btnUser, self.btnGopY]

        for btn in self.buttons:
            btn.setStyleSheet(btn_sidebar_style)
            self.sidebarLayout.addWidget(btn)
        
        # Highlight nút Góp ý
        self.btnGopY.setStyleSheet(btn_sidebar_style + "background:#3498db; color:white; font-weight:bold;")

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
        
        # Tiêu đề trang
        self.labelTitle = QtWidgets.QLabel("QUẢN LÝ GÓP Ý SINH VIÊN")
        self.labelTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setStyleSheet("font-size:24px; font-weight:bold; color: #2f3640; margin-top: 10px;")
        self.contentLayout.addWidget(self.labelTitle)

        # Khối điều khiển (Làm mới)
        self.actionLayout = QtWidgets.QHBoxLayout()
        self.btnRefresh = QtWidgets.QPushButton("🔄 Làm mới danh sách")
        self.btnRefresh.setFixedWidth(200)
        self.btnRefresh.setStyleSheet("""
            background-color: #2ecc71; 
            color: white; 
            height: 40px; 
            border-radius: 5px; 
            font-weight: bold;
            border: none;
        """)
        self.actionLayout.addStretch()
        self.actionLayout.addWidget(self.btnRefresh)
        self.contentLayout.addLayout(self.actionLayout)

        # Bảng dữ liệu
        self.tableGopY = QtWidgets.QTableWidget()
        self.tableGopY.setColumnCount(3)
        self.tableGopY.setHorizontalHeaderLabels(["ID", "Nội dung góp ý", "Thời gian gửi"])
        
        # Cấu hình bảng
        header = self.tableGopY.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch) # Nội dung giãn rộng nhất
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        
        self.tableGopY.setStyleSheet("""
            QTableWidget {
                background: white; 
                border-radius: 8px; 
                border: 1px solid #dcdde1;
                gridline-color: #f1f2f6;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                font-weight: bold;
                height: 35px;
                border: none;
            }
        """)
        self.tableGopY.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableGopY.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        
        self.contentLayout.addWidget(self.tableGopY)

        self.mainLayout.addWidget(self.content)
        MainWindow.setCentralWidget(self.centralwidget)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_QuanLyGopY()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())