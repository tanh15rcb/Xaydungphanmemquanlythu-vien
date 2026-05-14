import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QCompleter
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

# --- IMPORT BIỂU ĐỒ ---
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# --- IMPORT UI ---
from UI.UIDangNhap import Ui_LoginForm
from UI.UITrangChu import Ui_MainWindow as Ui_MainFrame
from UI.QuanLySach import Ui_MainWindow as Ui_QuanLySach
from UI.QuanLyMuonSach import Ui_MainWindow as Ui_QuanLyMuon
from UI.QuanLyNhanVien import Ui_MainWindow as Ui_QuanLyNhanVien 
from UI.QuanLyTraSach import Ui_QuanLyTraSach 
from UI.NhapHang import Ui_NhapHang
from UI.NhaCungCap import Ui_NhaCungCap
from UI.UIthongke import Ui_ThongKe 
from UI.UItaikhoan import Ui_MainWindow as Ui_TaiKhoan 
from UI.XemSach import Ui_MainWindow as Ui_XemSach
from UI.QuanLyGopY import Ui_QuanLyGopY

# --- IMPORT SERVICE ---
from Service.DangNhap import dich_vu_dang_nhap
from Service.TrangChu import dich_vu_trang_chu 
from Service.QuanLySach import dich_vu_quan_ly_sach
from Service.QuanLyMuonSach import dich_vu_muon_sach
from Service.QuanLyTraSach import dich_vu_tra_sach
from Service.NhapHang import dich_vu_nhap_hang
from Service.NhaCungCap import dich_vu_ncc
from Service.QuanLyNhanVien import dich_vu_nv 
from Service.ThongKe import dich_vu_tk 
from Service.QuanLyTaiKhoan import dich_vu_tai_khoan
from Service.XemSachService import dich_vu_xem_sach
from Service.QuanLyGopYService import dich_vu_quan_ly_gop_y

# ================================================================
# LỚP XEM SÁCH DÀNH CHO SINH VIÊN (TÁCH BIỆT)
# ================================================================
class StudentViewWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_XemSach()
        self.ui.setupUi(self)
        self.setWindowTitle("Tra Cứu Sách Thư Viện")

        # Kết nối sự kiện
        self.ui.btnTimKiem.clicked.connect(self.handle_search)
        self.ui.btnGuiGopY.clicked.connect(self.handle_send_feedback)
        self.ui.btnBack.clicked.connect(self.handle_back)

        # Load dữ liệu ban đầu
        self.handle_search()

    def handle_search(self):
        tu_khoa = self.ui.txtTimKiem.text().strip()
        data = dich_vu_quan_ly_sach.tim_kiem_sach(tu_khoa)
        
        self.ui.tableSach.setRowCount(0)
        for r, row_d in enumerate(data):
            self.ui.tableSach.insertRow(r)
            # Hiển thị các cột: Mã, Tên, Tác giả, Thể loại, Số lượng, NXB, Năm XB
            for i in range(7):
                val = str(row_d[i])
                item = QtWidgets.QTableWidgetItem(val)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ui.tableSach.setItem(r, i, item)

    def handle_send_feedback(self):
        # 1. Lấy nội dung từ ô nhập liệu (txtGopY là tên object trong file XemSach.py)
        noi_dung = self.ui.txtGopY.toPlainText().strip()
        
        # 2. Kiểm tra nếu nội dung rỗng
        if not noi_dung:
            QtWidgets.QMessageBox.warning(self, "Thông báo", "Vui lòng nhập nội dung góp ý!")
            return
        
        # 3. Gọi service đã import (dich_vu_xem_sach) để lưu vào database
        # Hàm gui_gop_y này đã được định nghĩa trong XemSachService của bạn
        success = dich_vu_xem_sach.gui_gop_y(noi_dung)
        
        if success:
            QtWidgets.QMessageBox.information(self, "Thành công", "Cảm ơn bạn đã gửi góp ý cho thư viện!")
            self.ui.txtGopY.clear()  # Xóa nội dung sau khi gửi thành công
        else:
            QtWidgets.QMessageBox.critical(self, "Lỗi", "Không thể gửi góp ý lúc này. Vui lòng thử lại sau!")

    def handle_back(self):
        self.close()

# ================================================================
# LỚP ĐĂNG NHẬP
# ================================================================
class LoginWindow(QtWidgets.QWidget):
    login_success = QtCore.pyqtSignal(dict) 

    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginForm()
        self.ui.setupUi(self)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.ui.container.setGraphicsEffect(shadow)
        self.ui.btnLogin.clicked.connect(self.handle_login)
        self.ui.btnStudentLogin.clicked.connect(self.handle_student_view)
        self.ui.btnClose.clicked.connect(QtWidgets.QApplication.quit)
        self.ui.txtPass.returnPressed.connect(self.handle_login)

    def handle_login(self):
        tai_khoan = self.ui.txtUser.text().strip()
        mat_khau = self.ui.txtPass.text().strip()
        if not tai_khoan or not mat_khau:
            QtWidgets.QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ tài khoản và mật khẩu!")
            return
        ket_qua_dang_nhap = dich_vu_dang_nhap.thuc_hien_dang_nhap(tai_khoan, mat_khau)
        if ket_qua_dang_nhap["ket_qua"] == "thanh_cong":
            self.login_success.emit(ket_qua_dang_nhap["thong_tin"])
            self.hide() 
        else:
            QtWidgets.QMessageBox.warning(self, "Lỗi đăng nhập", ket_qua_dang_nhap["noi_dung"])
            
    def handle_student_view(self):
        self.student_win = StudentViewWindow()
        self.student_win.show()

# ================================================================
# LỚP QUẢN LÝ CHÍNH
# ================================================================
class LibraryManager(QtWidgets.QMainWindow):
    logout_requested = QtCore.pyqtSignal() 

    def __init__(self, user_info=None):
        super().__init__()
        self.ui = Ui_MainFrame()
        self.ui.setupUi(self)
        self.setWindowTitle("Hệ Thống Quản Lý Thư Viện Pro")
        self.user_info = user_info 

        self.init_sub_pages()
        self.connect_sidebar_buttons()
        self.connect_quan_ly_sach_events()
        self.connect_quan_ly_muon_events()
        self.connect_quan_ly_tra_events() 
        self.connect_nhap_hang_events()
        self.connect_nha_cung_cap_events()
        self.connect_quan_ly_nhan_vien_events() 
        self.connect_thong_ke_events() 
        self.connect_quan_ly_tai_khoan_events() 
        self.connect_quan_ly_gop_y_events()

        if hasattr(self.ui, 'btnLogout'):
            self.ui.btnLogout.clicked.connect(self.handle_logout)

        self.ui.StackedWidget.setCurrentIndex(0)
        self.cap_nhat_du_lieu_trang_chu()

    def handle_logout(self):
        msg = QtWidgets.QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn đăng xuất?", 
                                             QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if msg == QtWidgets.QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()
            self.close()

    def _embed_page(self, ui_class, index):
        temp_window = QtWidgets.QMainWindow()
        ui_instance = ui_class()
        ui_instance.setupUi(temp_window)
        if hasattr(ui_instance, 'sidebar'):
            ui_instance.sidebar.hide()
        self.ui.StackedWidget.insertWidget(index, ui_instance.centralwidget)
        return ui_instance

    def init_sub_pages(self):
        self.ui_sach = self._embed_page(Ui_QuanLySach, 1)
        self.ui_muon = self._embed_page(Ui_QuanLyMuon, 2)
        self.ui_tra = self._embed_page(Ui_QuanLyTraSach, 3)
        self.ui_nhap = self._embed_page(Ui_NhapHang, 4)
        self.ui_ncc = self._embed_page(Ui_NhaCungCap, 5)
        self.ui_nv = self._embed_page(Ui_QuanLyNhanVien, 6)
        self.ui_thongke = self._embed_page(Ui_ThongKe, 7)
        self.ui_taikhoan = self._embed_page(Ui_TaiKhoan, 8)
        self.ui_gopy = self._embed_page(Ui_QuanLyGopY, 9)

    # --- QUẢN LÝ TÀI KHOẢN ---
    def connect_quan_ly_tai_khoan_events(self):
        self.ui_taikhoan.btnThem.clicked.connect(self.handle_them_tk)
        self.ui_taikhoan.btnSua.clicked.connect(self.handle_sua_tk)
        self.ui_taikhoan.btnXoa.clicked.connect(self.handle_xoa_tk)
        self.ui_taikhoan.tableUser.itemClicked.connect(self.handle_table_tk_click)

    def load_data_tk(self):
        data = dich_vu_tai_khoan.lay_tat_ca_tai_khoan()
        self.ui_taikhoan.tableUser.setRowCount(0)
        for r, row_d in enumerate(data):
            self.ui_taikhoan.tableUser.insertRow(r)
            for c, val in enumerate(row_d):
                self.ui_taikhoan.tableUser.setItem(r, c, QtWidgets.QTableWidgetItem(str(val)))

    def handle_table_tk_click(self, item):
        row = item.row()
        self.ui_taikhoan.formContainer.setProperty("current_user_id", self.ui_taikhoan.tableUser.item(row, 0).text())
        self.ui_taikhoan.txtUsername.setText(self.ui_taikhoan.tableUser.item(row, 1).text())
        self.ui_taikhoan.txtPassword.setText(self.ui_taikhoan.tableUser.item(row, 2).text())
        self.ui_taikhoan.cboRole.setCurrentText(self.ui_taikhoan.tableUser.item(row, 3).text())
        self.ui_taikhoan.txtMaNV.setText(self.ui_taikhoan.tableUser.item(row, 4).text())

    def handle_them_tk(self):
        if self.user_info.get("vai_tro") != "Admin":
            QtWidgets.QMessageBox.warning(self, "Quyền hạn", "Bạn không có quyền thực hiện thao tác này!")
            return
        success, msg = dich_vu_tai_khoan.them_tai_khoan(self.ui_taikhoan.txtUsername.text().strip(), self.ui_taikhoan.txtPassword.text().strip(), self.ui_taikhoan.cboRole.currentText(), self.ui_taikhoan.txtMaNV.text().strip())
        if success:
            QtWidgets.QMessageBox.information(self, "Thông báo", msg)
            self.load_data_tk()
        else:
            QtWidgets.QMessageBox.critical(self, "Lỗi", msg)

    def handle_sua_tk(self):
        if self.user_info.get("vai_tro") != "Admin":
            QtWidgets.QMessageBox.warning(self, "Quyền hạn", "Bạn không có quyền thực hiện thao tác này!")
            return
        ma_user = self.ui_taikhoan.formContainer.property("current_user_id")
        if not ma_user: return
        success, msg = dich_vu_tai_khoan.sua_tai_khoan(ma_user, self.ui_taikhoan.txtUsername.text().strip(), self.ui_taikhoan.txtPassword.text().strip(), self.ui_taikhoan.cboRole.currentText(), self.ui_taikhoan.txtMaNV.text().strip())
        if success:
            QtWidgets.QMessageBox.information(self, "Thông báo", msg)
            self.load_data_tk()

    def handle_xoa_tk(self):
        if self.user_info.get("vai_tro") != "Admin":
            QtWidgets.QMessageBox.warning(self, "Quyền hạn", "Bạn không có quyền thực hiện thao tác này!")
            return
        ma_user = self.ui_taikhoan.formContainer.property("current_user_id")
        if ma_user and QtWidgets.QMessageBox.question(self, "Xác nhận", "Xóa tài khoản này?", QtWidgets.QMessageBox.StandardButton.Yes) == QtWidgets.QMessageBox.StandardButton.Yes:
            success, msg = dich_vu_tai_khoan.xoa_tai_khoan(ma_user)
            if success: self.load_data_tk()

    # --- QUẢN LÝ TRẢ SÁCH ---
    def connect_quan_ly_tra_events(self):
        self.ui_tra.dateTra.setDate(QtCore.QDate.currentDate())
        self.ui_tra.txtPhatNgay.setText("2000")
        self.ui_tra.txtMaSV.textChanged.connect(self.update_tra_sach_completer)
        self.ui_tra.btnTinh.clicked.connect(self.tinh_toan_tien_phat_ui)
        self.ui_tra.btnTra.clicked.connect(self.handle_xac_nhan_tra)

    def update_tra_sach_completer(self):
        ma_sv = self.ui_tra.txtMaSV.text().strip()
        if len(ma_sv) >= 1:
            self.du_lieu_muon_chua_tra = dich_vu_tra_sach.lay_danh_sach_chua_tra(ma_sv)
            ten_sach_list = list(set([str(row[3]) for row in self.du_lieu_muon_chua_tra]))
            completer = QCompleter(ten_sach_list)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            completer.activated[str].connect(self.fill_thong_tin_muon_tu_ten_sach)
            self.ui_tra.txtSach.setCompleter(completer)

    def fill_thong_tin_muon_tu_ten_sach(self, ten_sach):
        for row in self.du_lieu_muon_chua_tra:
            if str(row[3]) == ten_sach:
                self.ui_tra.txtTenSV.setText(str(row[2]))
                self.ui_tra.dateMuon.setDate(QtCore.QDate.fromString(str(row[4]), "yyyy-MM-dd"))
                self.ui_tra.dateHanTra.setDate(QtCore.QDate.fromString(str(row[5]), "yyyy-MM-dd"))
                ngay_han = self.ui_tra.dateHanTra.date()
                ngay_thuc = self.ui_tra.dateTra.date()
                tre = ngay_han.daysTo(ngay_thuc)
                self.ui_tra.txtTre.setText(str(tre if tre > 0 else 0))
                self.ui_tra.formContainer.setProperty("current_phieu_muon_id", row[0])
                self.tinh_toan_tien_phat_ui()
                break

    def tinh_toan_tien_phat_ui(self):
        try:
            tre = int(self.ui_tra.txtTre.text() or 0)
            phat_ngay = int(self.ui_tra.txtPhatNgay.text() or 0)
            self.ui_tra.txtTongPhat.setText(str(tre * phat_ngay))
        except: pass

    def handle_xac_nhan_tra(self):
        ma_pm = self.ui_tra.formContainer.property("current_phieu_muon_id")
        if not ma_pm:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng chọn sinh viên và sách mượn hợp lệ!")
            return
        ngay_tra = self.ui_tra.dateTra.date().toString("yyyy-MM-dd")
        so_tre = int(self.ui_tra.txtTre.text() or 0)
        tien_phat = float(self.ui_tra.txtTongPhat.text() or 0)
        thanh_cong, thong_bao = dich_vu_tra_sach.xac_nhan_tra_sach(ma_pm, ngay_tra, so_tre, tien_phat)
        if thanh_cong:
            QtWidgets.QMessageBox.information(self, "Thông báo", thong_bao)
            self.load_data_tra()
            self.cap_nhat_du_lieu_trang_chu()
        else:
            QtWidgets.QMessageBox.critical(self, "Lỗi", thong_bao)

    def load_data_tra(self):
        data = dich_vu_tra_sach.lay_lich_su_tra_sach()
        self.ui_tra.tableMuonTra.setRowCount(0)
        for r, row_d in enumerate(data):
            self.ui_tra.tableMuonTra.insertRow(r)
            for c, val in enumerate(row_d):
                self.ui_tra.tableMuonTra.setItem(r, c, QtWidgets.QTableWidgetItem(str(val)))

    # --- TRANG CHỦ & THỐNG KÊ ---
    def cap_nhat_du_lieu_trang_chu(self):
        tk = dich_vu_trang_chu.lay_thong_ke_tong_hop()
        if tk:
            try:
                self.ui.lbl_val_tong_sach.setText(f"{tk['tong_sach']:,}")
                self.ui.lbl_val_dang_muon.setText(f"{tk['dang_muon']:,}")
                self.ui.lbl_val_qua_han.setText(f"{tk['qua_han']:,}")
            except AttributeError: pass
        danh_sach = dich_vu_trang_chu.lay_danh_sach_muon_moi()
        if hasattr(self.ui, 'tableMuonSach'):
            self.ui.tableMuonSach.setRowCount(0)
            for row_idx, row_data in enumerate(danh_sach):
                self.ui.tableMuonSach.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.ui.tableMuonSach.setItem(row_idx, col_idx, item)

    def connect_thong_ke_events(self):
        self.ui_thongke.cbThoiGian.currentIndexChanged.connect(self.load_data_thong_ke)

    def load_data_thong_ke(self):
        def clear_layout(layout):
            if layout is not None:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget(): child.widget().deleteLater()
        lua_chon = self.ui_thongke.cbThoiGian.currentText()
        hom_nay = QtCore.QDate.currentDate()
        den_ngay = hom_nay.toString("yyyy-MM-dd")
        if lua_chon == "Hôm nay": tu_ngay = hom_nay.toString("yyyy-MM-dd")
        elif lua_chon == "Tháng này": tu_ngay = QtCore.QDate(hom_nay.year(), hom_nay.month(), 1).toString("yyyy-MM-dd")
        elif lua_chon == "Năm nay": tu_ngay = QtCore.QDate(hom_nay.year(), 1, 1).toString("yyyy-MM-dd")
        else: tu_ngay = "1900-01-01"
        clear_layout(self.ui_thongke.barVLayout); clear_layout(self.ui_thongke.pieVLayout)
        data_sach = dich_vu_tk.lay_data_bieu_do_cot(tu_ngay, den_ngay)
        fig_bar = Figure(figsize=(5, 4), dpi=100); ax_bar = fig_bar.add_subplot(111)
        if data_sach:
            names = [str(s[0]) for s in data_sach]; values = [int(s[1]) for s in data_sach]
            bars = ax_bar.bar(names, values, color='#3498db')
            ax_bar.set_title(f"Sách mượn nhiều nhất", fontsize=10, fontweight='bold')
            ax_bar.bar_label(bars, padding=3); fig_bar.autofmt_xdate()
        else: ax_bar.text(0.5, 0.5, "Không có dữ liệu", ha='center', va='center')
        self.ui_thongke.barVLayout.addWidget(FigureCanvas(fig_bar))
        data_tra = dich_vu_tk.lay_data_bieu_do_tron(tu_ngay, den_ngay)
        dung_hen = int(data_tra.get("DungHen", 0)); tre_han = int(data_tra.get("TreHan", 0)); tong = dung_hen + tre_han
        fig_pie = Figure(figsize=(5, 4), dpi=100); ax_pie = fig_pie.add_subplot(111)
        if tong > 0:
            labels = [f'Đúng hạn ({dung_hen})', f'Trễ hạn ({tre_han})']
            ax_pie.pie([dung_hen, tre_han], labels=labels, autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'], startangle=90, explode=(0.05, 0))
            ax_pie.set_title(f"Tỷ lệ trả sách ({lua_chon})", fontsize=10, fontweight='bold'); ax_pie.axis('equal')
        else: ax_pie.text(0.5, 0.5, "Không có dữ liệu trả sách", ha='center', va='center'); ax_pie.axis('off')
        self.ui_thongke.pieVLayout.addWidget(FigureCanvas(fig_pie))
    
    # --- QUẢN LÝ GÓP Ý ---
    def connect_quan_ly_gop_y_events(self):
        # Kết nối nút refresh trong giao diện QuanLyGopY
        if hasattr(self.ui_gopy, 'btnRefresh'):
            self.ui_gopy.btnRefresh.clicked.connect(self.load_data_gopy)

    def load_data_gopy(self):
        """Gọi service để lấy dữ liệu và đổ vào TableWidget"""
        data = dich_vu_quan_ly_gop_y.lay_danh_sach_gop_y()
        self.ui_gopy.tableGopY.setRowCount(0)
        for r, row_d in enumerate(data):
            self.ui_gopy.tableGopY.insertRow(r)
            for c, val in enumerate(row_d):
                item = QtWidgets.QTableWidgetItem(str(val))
                # Căn giữa cho ID và Thời gian
                if c != 1:
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ui_gopy.tableGopY.setItem(r, c, item)

    # --- QUẢN LÝ NHÂN VIÊN ---
    def connect_quan_ly_nhan_vien_events(self):
        self.ui_nv.btnThem.clicked.connect(self.handle_them_nv); self.ui_nv.btnSua.clicked.connect(self.handle_sua_nv)
        self.ui_nv.btnXoa.clicked.connect(self.handle_xoa_nv); self.ui_nv.btnTimKiem.clicked.connect(self.handle_tim_kiem_nv)
        self.ui_nv.tableNV.itemClicked.connect(self.handle_table_nv_click)

    def load_data_nv(self, data=None):
        if data is None: data = dich_vu_nv.lay_tat_ca_nv()
        self.ui_nv.tableNV.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.ui_nv.tableNV.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value)); item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ui_nv.tableNV.setItem(row_idx, col_idx, item)

    def handle_table_nv_click(self, item):
        row = item.row()
        self.ui_nv.formContainer.setProperty("current_nv_id", self.ui_nv.tableNV.item(row, 0).text())
        self.ui_nv.txtTenNV.setText(self.ui_nv.tableNV.item(row, 1).text())
        idx_gt = self.ui_nv.cboGioiTinh.findText(self.ui_nv.tableNV.item(row, 2).text())
        self.ui_nv.cboGioiTinh.setCurrentIndex(idx_gt if idx_gt >= 0 else 0)
        self.ui_nv.txtSdt.setText(self.ui_nv.tableNV.item(row, 3).text())
        self.ui_nv.txtEmail.setText(self.ui_nv.tableNV.item(row, 4).text())
        self.ui_nv.txtDiaChi.setText(self.ui_nv.tableNV.item(row, 5).text())

    def handle_them_nv(self):
        res = dich_vu_nv.them_nv(self.ui_nv.txtTenNV.text().strip(), self.ui_nv.cboGioiTinh.currentText(), self.ui_nv.txtSdt.text().strip(), self.ui_nv.txtEmail.text().strip(), self.ui_nv.txtDiaChi.text().strip())
        if res["ket_qua"] == "thanh_cong": self.load_data_nv()

    def handle_sua_nv(self):
        ma_nv = self.ui_nv.formContainer.property("current_nv_id")
        if ma_nv:
            res = dich_vu_nv.sua_nv(ma_nv, self.ui_nv.txtTenNV.text().strip(), self.ui_nv.cboGioiTinh.currentText(), self.ui_nv.txtSdt.text().strip(), self.ui_nv.txtEmail.text().strip(), self.ui_nv.txtDiaChi.text().strip())
            if res["ket_qua"] == "thanh_cong": self.load_data_nv()

    def handle_xoa_nv(self):
        ma_nv = self.ui_nv.formContainer.property("current_nv_id")
        if ma_nv and QtWidgets.QMessageBox.question(self, "Xác nhận", "Xóa nhân viên này?", QtWidgets.QMessageBox.StandardButton.Yes) == QtWidgets.QMessageBox.StandardButton.Yes:
            if dich_vu_nv.xoa_nv(ma_nv)["ket_qua"] == "thanh_cong": self.load_data_nv()

    def handle_tim_kiem_nv(self): self.load_data_nv(dich_vu_nv.tim_kiem_nv(self.ui_nv.txtTimKiem.text().strip()))

    # --- NHÀ CUNG CẤP ---
    def connect_nha_cung_cap_events(self):
        self.ui_ncc.btnThem.clicked.connect(self.handle_them_ncc); self.ui_ncc.btnSua.clicked.connect(self.handle_sua_ncc)
        self.ui_ncc.btnXoa.clicked.connect(self.handle_xoa_ncc); self.ui_ncc.tableNCC.itemClicked.connect(self.handle_table_ncc_click)

    def load_data_ncc(self):
        data = dich_vu_ncc.lay_tat_ca_ncc()
        self.ui_ncc.tableNCC.setRowCount(0)
        for r, row_d in enumerate(data):
            self.ui_ncc.tableNCC.insertRow(r)
            for c, val in enumerate(row_d): self.ui_ncc.tableNCC.setItem(r, c, QtWidgets.QTableWidgetItem(str(val)))

    def handle_table_ncc_click(self, item):
        row = item.row()
        self.ui_ncc.formContainer.setProperty("current_ncc_id", self.ui_ncc.tableNCC.item(row, 0).text())
        self.ui_ncc.txtTenNCC.setText(self.ui_ncc.tableNCC.item(row, 1).text())
        self.ui_ncc.txtDiaChi.setText(self.ui_ncc.tableNCC.item(row, 2).text())
        self.ui_ncc.txtSDT.setText(self.ui_ncc.tableNCC.item(row, 3).text())
        self.ui_ncc.txtEmail.setText(self.ui_ncc.tableNCC.item(row, 4).text())

    def handle_them_ncc(self):
        if dich_vu_ncc.them_ncc(self.ui_ncc.txtTenNCC.text().strip(), self.ui_ncc.txtDiaChi.text().strip(), self.ui_ncc.txtSDT.text().strip(), self.ui_ncc.txtEmail.text().strip())["ket_qua"] == "thanh_cong": self.load_data_ncc()

    def handle_sua_ncc(self):
        ma_ncc = self.ui_ncc.formContainer.property("current_ncc_id")
        if ma_ncc and dich_vu_ncc.sua_ncc(ma_ncc, self.ui_ncc.txtTenNCC.text().strip(), self.ui_ncc.txtDiaChi.text().strip(), self.ui_ncc.txtSDT.text().strip(), self.ui_ncc.txtEmail.text().strip())["ket_qua"] == "thanh_cong": self.load_data_ncc()

    def handle_xoa_ncc(self):
        ma_ncc = self.ui_ncc.formContainer.property("current_ncc_id")
        if ma_ncc and QtWidgets.QMessageBox.question(self, "Xác nhận", "Xóa đối tác này?", QtWidgets.QMessageBox.StandardButton.Yes) == QtWidgets.QMessageBox.StandardButton.Yes:
            if dich_vu_ncc.xoa_ncc(ma_ncc)["ket_qua"] == "thanh_cong": self.load_data_ncc()

    # --- NHẬP HÀNG ---
    def connect_nhap_hang_events(self):
        self.ui_nhap.btnThem.clicked.connect(self.handle_them_vao_bang_nhap); self.ui_nhap.btnXoa.clicked.connect(self.handle_xoa_dong_nhap)
        self.ui_nhap.btnXacNhan.clicked.connect(self.handle_xac_nhan_nhap_kho); self.refresh_nhap_hang_suggestions()

    def refresh_nhap_hang_suggestions(self):
        self.ui_nhap.cbNCC.clear(); self.ui_nhap.cbNCC.addItem("-- Chọn Nhà Cung Cấp --")
        self.ui_nhap.cbNCC.addItems(dich_vu_nhap_hang.lay_danh_sach_ncc())
        completer = QCompleter(dich_vu_nhap_hang.lay_danh_sach_ten_sach()); completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui_nhap.txtTenSach.setCompleter(completer)

    def handle_them_vao_bang_nhap(self):
        ten, sl, gia, ncc = self.ui_nhap.txtTenSach.text().strip(), self.ui_nhap.txtSoLuong.text().strip(), self.ui_nhap.txtDonGia.text().strip(), self.ui_nhap.cbNCC.currentText()
        if not ten or not sl or not gia or ncc == "-- Chọn Nhà Cung Cấp --": return
        row = self.ui_nhap.tableNhap.rowCount(); self.ui_nhap.tableNhap.insertRow(row)
        for i, val in enumerate([str(row+1), ncc, ten, sl, gia]): self.ui_nhap.tableNhap.setItem(row, i, QtWidgets.QTableWidgetItem(val))
        self.ui_nhap.txtTenSach.clear(); self.ui_nhap.txtSoLuong.clear(); self.ui_nhap.txtDonGia.clear()

    def handle_xoa_dong_nhap(self):
        row = self.ui_nhap.tableNhap.currentRow()
        if row >= 0:
            self.ui_nhap.tableNhap.removeRow(row)
            for i in range(self.ui_nhap.tableNhap.rowCount()): self.ui_nhap.tableNhap.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))

    def handle_xac_nhan_nhap_kho(self):
        row_count = self.ui_nhap.tableNhap.rowCount()
        if row_count == 0: return
        ten_ncc = self.ui_nhap.tableNhap.item(0, 1).text()
        list_h = [{'ten_sach': self.ui_nhap.tableNhap.item(i, 2).text(), 'so_luong': int(self.ui_nhap.tableNhap.item(i, 3).text()), 'gia_nhap': float(self.ui_nhap.tableNhap.item(i, 4).text())} for i in range(row_count)]
        if dich_vu_nhap_hang.xac_nhan_nhap_kho(ten_ncc, list_h)["ket_qua"] == "thanh_cong": self.ui_nhap.tableNhap.setRowCount(0); self.cap_nhat_du_lieu_trang_chu()

    # --- QUẢN LÝ SÁCH ---
    def connect_quan_ly_sach_events(self):
        self.ui_sach.btnThem.clicked.connect(self.handle_them_sach); self.ui_sach.btnSua.clicked.connect(self.handle_sua_sach)
        self.ui_sach.btnXoa.clicked.connect(self.handle_xoa_sach); self.ui_sach.btnTimKiem.clicked.connect(self.handle_tim_kiem_sach)
        self.ui_sach.tableSach.itemClicked.connect(self.handle_table_sach_click)

    def load_data_sach(self, data=None):
        if data is None: data = dich_vu_quan_ly_sach.lay_tat_ca_sach()
        self.ui_sach.tableSach.setRowCount(0)
        for r, row_d in enumerate(data):
            self.ui_sach.tableSach.insertRow(r)
            for c, val in enumerate(row_d): self.ui_sach.tableSach.setItem(r, c, QtWidgets.QTableWidgetItem(str(val)))

    def handle_table_sach_click(self, item):
        row = item.row()
        self.ui_sach.formContainer.setProperty("current_id", self.ui_sach.tableSach.item(row, 0).text())
        self.ui_sach.txtTenSach.setText(self.ui_sach.tableSach.item(row, 1).text())
        self.ui_sach.txtTacGia.setText(self.ui_sach.tableSach.item(row, 2).text()); self.ui_sach.txtTheLoai.setText(self.ui_sach.tableSach.item(row, 3).text())
        self.ui_sach.txtSoLuong.setText(self.ui_sach.tableSach.item(row, 4).text()); self.ui_sach.txtNXB.setText(self.ui_sach.tableSach.item(row, 5).text())
        self.ui_sach.txtNamXB.setText(self.ui_sach.tableSach.item(row, 6).text())

    def handle_them_sach(self):
        if dich_vu_quan_ly_sach.them_sach(self.ui_sach.txtTenSach.text().strip(), self.ui_sach.txtTacGia.text().strip(), self.ui_sach.txtTheLoai.text().strip(), self.ui_sach.txtNXB.text().strip(), int(self.ui_sach.txtNamXB.text() or 0))[0]: self.load_data_sach()

    def handle_sua_sach(self):
        ma = self.ui_sach.formContainer.property("current_id")
        if ma and dich_vu_quan_ly_sach.sua_sach(ma, self.ui_sach.txtTenSach.text().strip(), self.ui_sach.txtTacGia.text().strip(), self.ui_sach.txtTheLoai.text().strip(), int(self.ui_sach.txtSoLuong.text() or 0), self.ui_sach.txtNXB.text().strip(), int(self.ui_sach.txtNamXB.text() or 0))[0]: self.load_data_sach()

    def handle_xoa_sach(self):
        ma = self.ui_sach.formContainer.property("current_id")
        if ma and QtWidgets.QMessageBox.question(self, "Xác nhận", "Xóa?", QtWidgets.QMessageBox.StandardButton.Yes) == QtWidgets.QMessageBox.StandardButton.Yes:
            if dich_vu_quan_ly_sach.xoa_sach(ma)[0]: self.load_data_sach()

    def handle_tim_kiem_sach(self): self.load_data_sach(dich_vu_quan_ly_sach.tim_kiem_sach(self.ui_sach.txtTimKiem.text().strip()))

    # --- QUẢN LÝ MƯỢN ---
    def connect_quan_ly_muon_events(self):
        self.ui_muon.btnMuon.clicked.connect(self.handle_muon_sach); self.ui_muon.btnTimKiem.clicked.connect(self.handle_tim_kiem_muon)
        completer = QCompleter(dich_vu_muon_sach.lay_tat_ca_ten_sach()); completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui_muon.txtTenSach.setCompleter(completer)

    def load_data_muon(self, data=None):
        if data is None: data = dich_vu_muon_sach.lay_danh_sach_muon()
        self.ui_muon.tableMuon.setRowCount(0)
        for r, row_d in enumerate(data):
            self.ui_muon.tableMuon.insertRow(r)
            for c, val in enumerate(row_d): self.ui_muon.tableMuon.setItem(r, c, QtWidgets.QTableWidgetItem(str(val)))

    def handle_muon_sach(self):
        if dich_vu_muon_sach.cho_muon_sach(self.ui_muon.txtMaSV.text().strip(), self.ui_muon.txtHoTen.text().strip(), self.ui_muon.txtTenSach.text().strip(), int(self.ui_muon.txtSoLuong.text() or 0), self.ui_muon.txtNgayTra.date().toString("yyyy-MM-dd"))[0]: self.load_data_muon(); self.cap_nhat_du_lieu_trang_chu()

    def handle_tim_kiem_muon(self): self.load_data_muon(dich_vu_muon_sach.tim_kiem_tong_hop(self.ui_muon.txtTimKiem.text().strip()))

    # --- SIDEBAR & CHUYỂN TRANG ---
    def connect_sidebar_buttons(self):
        self.button_map = {self.ui.btnTrangChu: 0, self.ui.btnSach: 1, self.ui.btnMuonSach: 2, self.ui.btnTraSach: 3, self.ui.btnNhapHang: 4, self.ui.btnNCC: 5, self.ui.btnNhanVien: 6, self.ui.btnThongKe: 7, self.ui.btnTaiKhoan: 8, self.ui.btnGopY: 9}
        for btn, index in self.button_map.items():
            if btn: btn.clicked.connect(lambda checked, i=index: self.switch_page(i))

    def switch_page(self, index):
        self.ui.StackedWidget.setCurrentIndex(index)
        if index == 0: self.cap_nhat_du_lieu_trang_chu()
        elif index == 1: self.load_data_sach()
        elif index == 2: self.load_data_muon()
        elif index == 3: self.load_data_tra()
        elif index == 5: self.load_data_ncc()
        elif index == 6: self.load_data_nv()
        elif index == 7: self.load_data_thong_ke()
        elif index == 8: self.load_data_tk()
        elif index == 9: self.load_data_gopy()

# ================================================================
# CHƯƠNG TRÌNH CHÍNH
# ================================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    
    login_win = LoginWindow()
    main_win = LibraryManager()

    # Nhận thông tin đăng nhập thành công
    def on_login_success(user_info):
        main_win.user_info = user_info
        main_win.show()

    # Xử lý khi nhận signal đăng xuất từ main_win
    def on_logout_requested():
        login_win.ui.txtPass.clear() 
        login_win.show()

    login_win.login_success.connect(on_login_success)
    main_win.logout_requested.connect(on_logout_requested) 

    login_win.show()
    sys.exit(app.exec())