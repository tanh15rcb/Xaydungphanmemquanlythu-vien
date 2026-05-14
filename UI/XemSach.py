from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        MainWindow.setStyleSheet("background-color: #f5f6fa;")
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(40, 30, 40, 30)
        self.mainLayout.setSpacing(20)
        self.mainLayout.setObjectName("mainLayout")

        # --- TIÊU ĐỀ CHÍNH ---
        self.labelTitle = QtWidgets.QLabel("HỆ THỐNG TRA CỨU SÁCH THƯ VIỆN")
        self.labelTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #2c3e50; 
            padding-bottom: 10px;
            border-bottom: 3px solid #3498db;
        """)
        self.mainLayout.addWidget(self.labelTitle)

        # --- PHẦN 1: TÌM KIẾM ---
        self.searchContainer = QtWidgets.QFrame()
        self.searchContainer.setStyleSheet("background: white; border-radius: 10px; border: 1px solid #dcdde1;")
        self.searchLayout = QtWidgets.QHBoxLayout(self.searchContainer)
        self.searchLayout.setContentsMargins(15, 10, 15, 10)
        
        self.txtTimKiem = QtWidgets.QLineEdit()
        self.txtTimKiem.setPlaceholderText("Nhập tên sách, tác giả hoặc thể loại để tìm kiếm...")
        self.txtTimKiem.setStyleSheet("height: 40px; border: none; font-size: 14px; background: transparent;")
        self.txtTimKiem.setObjectName("txtTimKiem")
        
        self.btnTimKiem = QtWidgets.QPushButton("🔍 Tìm kiếm")
        self.btnTimKiem.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnTimKiem.setStyleSheet("""
            QPushButton {
                background-color: #3498db; 
                color: white; 
                font-weight: bold; 
                border-radius: 5px; 
                padding: 0 25px; 
                height: 40px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        self.btnTimKiem.setObjectName("btnTimKiem")
        
        self.searchLayout.addWidget(self.txtTimKiem)
        self.searchLayout.addWidget(self.btnTimKiem)
        self.mainLayout.addWidget(self.searchContainer)

        # --- PHẦN 2: DANH SÁCH SÁCH (TABLE) ---
        self.tableSach = QtWidgets.QTableWidget()
        self.tableSach.setObjectName("tableSach")
        # Tăng số cột lên 7 để thêm cột Số lượng
        self.tableSach.setColumnCount(7)
        # Thêm "Số lượng" vào sau "Thể loại"
        self.tableSach.setHorizontalHeaderLabels(["Mã", "Tên sách", "Tác giả", "Thể loại", "Số lượng", "NXB", "Năm XB"])
        
        self.tableSach.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableSach.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableSach.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableSach.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 8px;
                gridline-color: #f1f2f6;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                font-weight: bold;
                height: 35px;
                border: none;
            }
        """)
        self.mainLayout.addWidget(self.tableSach)

        # --- PHẦN 3: GÓP Ý ---
        self.gopYContainer = QtWidgets.QFrame()
        self.gopYContainer.setStyleSheet("background: #ecf0f1; border-radius: 10px; border: 1px solid #bdc3c7;")
        self.gopYLayout = QtWidgets.QVBoxLayout(self.gopYContainer)
        
        self.labelGopY = QtWidgets.QLabel("✍️ Gửi góp ý cho thư viện:")
        self.labelGopY.setStyleSheet("font-weight: bold; color: #34495e; font-size: 15px; border: none;")
        
        self.txtGopY = QtWidgets.QPlainTextEdit()
        self.txtGopY.setPlaceholderText("Nhập nội dung góp ý của bạn tại đây...")
        self.txtGopY.setStyleSheet("background: white; border-radius: 5px; border: 1px solid #dcdde1; padding: 10px;")
        self.txtGopY.setMaximumHeight(100)
        self.txtGopY.setObjectName("txtGopY")
        
        self.btnGuiGopY = QtWidgets.QPushButton("Gửi góp ý ngay")
        self.btnGuiGopY.setObjectName("btnGuiGopY")
        self.btnGuiGopY.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnGuiGopY.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; 
                color: white; 
                font-weight: bold; 
                height: 35px; 
                border-radius: 5px;
                padding: 0 20px;
                border: none;
            }
            QPushButton:hover { background-color: #27ae60; }
        """)
        
        self.gopYLayout.addWidget(self.labelGopY)
        self.gopYLayout.addWidget(self.txtGopY)
        self.gopYLayout.addWidget(self.btnGuiGopY, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        
        self.mainLayout.addWidget(self.gopYContainer)

        # --- NÚT QUAY LẠI ---
        self.btnBack = QtWidgets.QPushButton("🚪 Quay lại Đăng nhập")
        self.btnBack.setObjectName("btnBack")
        self.btnBack.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btnBack.setStyleSheet("""
            QPushButton {
                color: #7f8c8d; 
                border: none; 
                font-weight: bold; 
                font-size: 14px;
                padding: 10px;
            }
            QPushButton:hover { color: #2c3e50; text-decoration: underline; }
        """)
        self.mainLayout.addWidget(self.btnBack, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        MainWindow.setCentralWidget(self.centralwidget)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tra Cứu Sách Thư Viện - Sinh Viên"))