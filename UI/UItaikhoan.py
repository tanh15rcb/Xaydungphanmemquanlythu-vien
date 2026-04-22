from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 700)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setContentsMargins(20, 20, 20, 20)
        self.vboxlayout.setSpacing(15)
        self.vboxlayout.setObjectName("vboxlayout")

        # --- TIÊU ĐỀ ---
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        # --- KHUNG NHẬP LIỆU (FORM) ---
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setObjectName("frame")
        self.gridlayout = QtWidgets.QGridLayout(self.frame)
        self.gridlayout.setContentsMargins(25, 25, 25, 25)
        self.gridlayout.setHorizontalSpacing(20)
        self.gridlayout.setVerticalSpacing(15)
        self.gridlayout.setObjectName("gridlayout")

        # Tên đăng nhập
        self.label1 = QtWidgets.QLabel(parent=self.frame)
        self.label1.setObjectName("label1")
        self.gridlayout.addWidget(self.label1, 0, 0, 1, 1)
        self.txt_username = QtWidgets.QLineEdit(parent=self.frame)
        self.txt_username.setObjectName("txt_username")
        self.gridlayout.addWidget(self.txt_username, 0, 1, 1, 1)

        # Mật khẩu
        self.label2 = QtWidgets.QLabel(parent=self.frame)
        self.label2.setObjectName("label2")
        self.gridlayout.addWidget(self.label2, 0, 2, 1, 1)
        self.txt_password = QtWidgets.QLineEdit(parent=self.frame)
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txt_password.setObjectName("txt_password")
        self.gridlayout.addWidget(self.txt_password, 0, 3, 1, 1)

        # Vai trò
        self.label3 = QtWidgets.QLabel(parent=self.frame)
        self.label3.setObjectName("label3")
        self.gridlayout.addWidget(self.label3, 1, 0, 1, 1)
        self.cb_role = QtWidgets.QComboBox(parent=self.frame)
        self.cb_role.setObjectName("cb_role")
        self.cb_role.addItem("")
        self.cb_role.addItem("")
        self.gridlayout.addWidget(self.cb_role, 1, 1, 1, 1)

        # Mã nhân viên (Thay thế cho Trạng thái)
        self.label4 = QtWidgets.QLabel(parent=self.frame)
        self.label4.setObjectName("label4")
        self.gridlayout.addWidget(self.label4, 1, 2, 1, 1)
        self.txt_manv = QtWidgets.QLineEdit(parent=self.frame)
        self.txt_manv.setObjectName("txt_manv")
        self.gridlayout.addWidget(self.txt_manv, 1, 3, 1, 1)

        self.vboxlayout.addWidget(self.frame)

        # --- NHÓM NÚT BẤM (Bỏ nút Làm mới) ---
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.hboxlayout.addStretch() # Đẩy các nút ra giữa

        self.btn_add = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_add.setMinimumSize(QtCore.QSize(120, 35))
        self.btn_add.setObjectName("btn_add")
        self.hboxlayout.addWidget(self.btn_add)

        self.btn_update = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_update.setMinimumSize(QtCore.QSize(120, 35))
        self.btn_update.setObjectName("btn_update")
        self.hboxlayout.addWidget(self.btn_update)

        self.btn_delete = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_delete.setMinimumSize(QtCore.QSize(120, 35))
        self.btn_delete.setObjectName("btn_delete")
        self.hboxlayout.addWidget(self.btn_delete)

        self.hboxlayout.addStretch()
        self.vboxlayout.addLayout(self.hboxlayout)

        # --- BẢNG DỮ LIỆU ---
        self.table_accounts = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.table_accounts.setObjectName("table_accounts")
        self.table_accounts.setColumnCount(4)
        self.table_accounts.setRowCount(0)
        self.table_accounts.horizontalHeader().setStretchLastSection(True)
        self.table_accounts.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        # Tiêu đề bảng
        for i in range(4):
            item = QtWidgets.QTableWidgetItem()
            self.table_accounts.setHorizontalHeaderItem(i, item)
            
        self.vboxlayout.addWidget(self.table_accounts)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Quản lý tài khoản"))
        
        # Style cho Tiêu đề
        self.label.setText(_translate("MainWindow", "QUẢN LÝ TÀI KHOẢN HỆ THỐNG"))
        self.label.setStyleSheet("font-size:24px; font-weight:bold; color:#2c3e50; margin-bottom:10px;")
        
        # Style cho Frame và Input
        self.frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: 1px solid #dcdde1;
            }
            QLabel {
                border: none;
                font-weight: bold;
                color: #34495e;
            }
            QLineEdit, QComboBox {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 6px;
                background: #fdfdfd;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)

        self.label1.setText(_translate("MainWindow", "Tên đăng nhập:"))
        self.label2.setText(_translate("MainWindow", "Mật khẩu:"))
        self.label3.setText(_translate("MainWindow", "Vai trò:"))
        self.cb_role.setItemText(0, _translate("MainWindow", "Admin"))
        self.cb_role.setItemText(1, _translate("MainWindow", "Nhân viên"))
        self.label4.setText(_translate("MainWindow", "Mã nhân viên:"))
        
        # Style nút bấm
        self.btn_add.setText(_translate("MainWindow", " Thêm mới"))
        self.btn_add.setStyleSheet("background:#2ecc71; color:white; font-weight:bold; border-radius:6px;")
        
        self.btn_update.setText(_translate("MainWindow", " Cập nhật"))
        self.btn_update.setStyleSheet("background:#3498db; color:white; font-weight:bold; border-radius:6px;")
        
        self.btn_delete.setText(_translate("MainWindow", " Xóa tài khoản"))
        self.btn_delete.setStyleSheet("background:#e74c3c; color:white; font-weight:bold; border-radius:6px;")

        # Tiêu đề cột bảng
        self.table_accounts.horizontalHeaderItem(0).setText(_translate("MainWindow", "Tên đăng nhập"))
        self.table_accounts.horizontalHeaderItem(1).setText(_translate("MainWindow", "Vai trò"))
        self.table_accounts.horizontalHeaderItem(2).setText(_translate("MainWindow", "Mã nhân viên"))
        self.table_accounts.horizontalHeaderItem(3).setText(_translate("MainWindow", "Ngày tạo"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())