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
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Lỗi đăng nhập", ket_qua_dang_nhap["noi_dung"])

# ================================================================
# LỚP QUẢN LÝ CHÍNH
# ================================================================
class LibraryManager(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainFrame()
        self.ui.setupUi(self)
        self.setWindowTitle("Hệ Thống Quản Lý Thư Viện Pro")

        self.init_sub_pages()
        self.connect_sidebar_buttons()
        self.connect_quan_ly_sach_events()
        self.connect_quan_ly_muon_events()
        self.connect_quan_ly_tra_events() 
        self.connect_nhap_hang_events()
        self.connect_nha_cung_cap_events()
        self.connect_quan_ly_nhan_vien_events() 

        self.ui.StackedWidget.setCurrentIndex(0)
        self.cap_nhat_du_lieu_trang_chu()

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

    # --- PHẦN TRANG CHỦ ---
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

    # ----------------------------------------------------------------
    # THỐNG KÊ & BIỂU ĐỒ (SỬA ĐỂ KHỚP VỚI SERVICE CỦA BẠN)
    # ----------------------------------------------------------------
    def load_data_thong_ke(self):
        """Vẽ biểu đồ cột (Top 10) và biểu đồ tròn (Tỉ lệ trả)"""
        
        def clear_layout(layout):
            if layout is not None:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

        # Xóa các biểu đồ cũ trong layout barVLayout và pieVLayout
        clear_layout(self.ui_thongke.barVLayout)
        clear_layout(self.ui_thongke.pieVLayout)

        # 1. VẼ BIỂU ĐỒ CỘT (Gọi đúng tên hàm lay_data_bieu_do_cot)
        data_sach = dich_vu_tk.lay_data_bieu_do_cot()
        fig_bar = Figure(figsize=(5, 3), dpi=100)
        canvas_bar = FigureCanvas(fig_bar)
        ax_bar = fig_bar.add_subplot(111)
        
        if data_sach:
            names = [s[0] for s in data_sach]
            values = [s[1] for s in data_sach]
            bars = ax_bar.bar(names, values, color='#3498db')
            ax_bar.set_title("Top 10 Sách Được Mượn Nhiều Nhất", fontsize=10, fontweight='bold')
            ax_bar.bar_label(bars, padding=3)
            fig_bar.autofmt_xdate()
        else:
            ax_bar.text(0.5, 0.5, "Không có dữ liệu", ha='center')
        
        self.ui_thongke.barVLayout.addWidget(canvas_bar)

        # 2. VẼ BIỂU ĐỒ TRÒN (Gọi đúng tên hàm lay_data_bieu_do_tron)
        data_tra = dich_vu_tk.lay_data_bieu_do_tron()
        fig_pie = Figure(figsize=(5, 3), dpi=100)
        canvas_pie = FigureCanvas(fig_pie)
        ax_pie = fig_pie.add_subplot(111)

        dung_hen = data_tra.get("DungHen", 0)
        tre_han = data_tra.get("TreHan", 0)

        if dung_hen > 0 or tre_han > 0:
            ax_pie.pie([dung_hen, tre_han], labels=['Đúng hạn', 'Trễ hạn'], 
                       autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'], startangle=90)
            ax_pie.set_title("Tỉ Lệ Trả Sách", fontsize=10, fontweight='bold')
            ax_pie.axis('equal')
        else:
            ax_pie.text(0.5, 0.5, "Không có dữ liệu", ha='center')

        self.ui_thongke.pieVLayout.addWidget(canvas_pie)

    # ----------------------------------------------------------------
    # CÁC PHẦN QUẢN LÝ KHÁC (GIỮ NGUYÊN 100%)
    # ----------------------------------------------------------------
    def connect_quan_ly_nhan_vien_events(self):
        self.ui_nv.btnThem.clicked.connect(self.handle_them_nv)
        self.ui_nv.btnSua.clicked.connect(self.handle_sua_nv)
        self.ui_nv.btnXoa.clicked.connect(self.handle_xoa_nv)
        self.ui_nv.btnTimKiem.clicked.connect(self.handle_tim_kiem_nv)
        self.ui_nv.tableNV.itemClicked.connect(self.handle_table_nv_click)
        self.ui_nv.txtTimKiem.returnPressed.connect(self.handle_tim_kiem_nv)

    def load_data_nv(self, data=None):
        if data is None: data = dich_vu_nv.lay_tat_ca_nv()
        self.ui_nv.tableNV.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.ui_nv.tableNV.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
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
        res = dich_vu_nv.them_nv(self.ui_nv.txtTenNV.text().strip(), self.ui_nv.cboGioiTinh.currentText(),
            self.ui_nv.txtSdt.text().strip(), self.ui_nv.txtEmail.text().strip(), self.ui_nv.txtDiaChi.text().strip())
        if res["ket_qua"] == "thanh_cong":
            QtWidgets.QMessageBox.information(self, "Thông báo", res["noi_dung"])
            self.load_data_nv()
            self.clear_form_nv()
        else: QtWidgets.QMessageBox.warning(self, "Lỗi", res["noi_dung"])

    def handle_sua_nv(self):
        ma_nv = self.ui_nv.formContainer.property("current_nv_id")
        if not ma_nv: return
        res = dich_vu_nv.sua_nv(ma_nv, self.ui_nv.txtTenNV.text().strip(), self.ui_nv.cboGioiTinh.currentText(),
            self.ui_nv.txtSdt.text().strip(), self.ui_nv.txtEmail.text().strip(), self.ui_nv.txtDiaChi.text().strip())
        if res["ket_qua"] == "thanh_cong":
            QtWidgets.QMessageBox.information(self, "Thông báo", res["noi_dung"])
            self.load_data_nv()
        else: QtWidgets.QMessageBox.warning(self, "Lỗi", res["noi_dung"])

    def handle_xoa_nv(self):
        ma_nv = self.ui_nv.formContainer.property("current_nv_id")
        if not ma_nv: return
        confirm = QtWidgets.QMessageBox.question(self, "Xác nhận", "Xóa nhân viên này?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            res = dich_vu_nv.xoa_nv(ma_nv)
            if res["ket_qua"] == "thanh_cong":
                self.load_data_nv()
                self.clear_form_nv()
            else: QtWidgets.QMessageBox.critical(self, "Lỗi", res["noi_dung"])

    def handle_tim_kiem_nv(self):
        tu_khoa = self.ui_nv.txtTimKiem.text().strip()
        self.load_data_nv(dich_vu_nv.tim_kiem_nv(tu_khoa))

    def clear_form_nv(self):
        for ipt in [self.ui_nv.txtTenNV, self.ui_nv.txtSdt, self.ui_nv.txtEmail, self.ui_nv.txtDiaChi]: ipt.clear()
        self.ui_nv.cboGioiTinh.setCurrentIndex(0)
        self.ui_nv.formContainer.setProperty("current_nv_id", None)

    def connect_nha_cung_cap_events(self):
        self.ui_ncc.btnThem.clicked.connect(self.handle_them_ncc)
        self.ui_ncc.btnSua.clicked.connect(self.handle_sua_ncc)
        self.ui_ncc.btnXoa.clicked.connect(self.handle_xoa_ncc)
        self.ui_ncc.tableNCC.itemClicked.connect(self.handle_table_ncc_click)

    def load_data_ncc(self):
        data = dich_vu_ncc.lay_tat_ca_ncc()
        self.ui_ncc.tableNCC.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.ui_ncc.tableNCC.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ui_ncc.tableNCC.setItem(row_idx, col_idx, item)

    def handle_table_ncc_click(self, item):
        row = item.row()
        self.ui_ncc.formContainer.setProperty("current_ncc_id", self.ui_ncc.tableNCC.item(row, 0).text())
        self.ui_ncc.txtTenNCC.setText(self.ui_ncc.tableNCC.item(row, 1).text())
        self.ui_ncc.txtDiaChi.setText(self.ui_ncc.tableNCC.item(row, 2).text())
        self.ui_ncc.txtSDT.setText(self.ui_ncc.tableNCC.item(row, 3).text())
        self.ui_ncc.txtEmail.setText(self.ui_ncc.tableNCC.item(row, 4).text())

    def handle_them_ncc(self):
        res = dich_vu_ncc.them_ncc(self.ui_ncc.txtTenNCC.text().strip(), self.ui_ncc.txtDiaChi.text().strip(), self.ui_ncc.txtSDT.text().strip(), self.ui_ncc.txtEmail.text().strip())
        if res["ket_qua"] == "thanh_cong":
            QtWidgets.QMessageBox.information(self, "Thành công", res["noi_dung"])
            self.load_data_ncc()
            self.clear_form_ncc()
        else: QtWidgets.QMessageBox.warning(self, "Lỗi", res["noi_dung"])

    def handle_sua_ncc(self):
        ma_ncc = self.ui_ncc.formContainer.property("current_ncc_id")
        if not ma_ncc: return
        res = dich_vu_ncc.sua_ncc(ma_ncc, self.ui_ncc.txtTenNCC.text().strip(), self.ui_ncc.txtDiaChi.text().strip(), self.ui_ncc.txtSDT.text().strip(), self.ui_ncc.txtEmail.text().strip())
        if res["ket_qua"] == "thanh_cong":
            QtWidgets.QMessageBox.information(self, "Thành công", res["noi_dung"])
            self.load_data_ncc()
        else: QtWidgets.QMessageBox.warning(self, "Lỗi", res["noi_dung"])

    def handle_xoa_ncc(self):
        ma_ncc = self.ui_ncc.formContainer.property("current_ncc_id")
        if not ma_ncc: return
        if QtWidgets.QMessageBox.question(self, "Xác nhận", "Xóa đối tác này?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No) == QtWidgets.QMessageBox.StandardButton.Yes:
            res = dich_vu_ncc.xoa_ncc(ma_ncc)
            if res["ket_qua"] == "thanh_cong":
                self.load_data_ncc()
                self.clear_form_ncc()
            else: QtWidgets.QMessageBox.critical(self, "Lỗi", res["noi_dung"])

    def clear_form_ncc(self):
        self.ui_ncc.txtTenNCC.clear(); self.ui_ncc.txtDiaChi.clear(); self.ui_ncc.txtSDT.clear(); self.ui_ncc.txtEmail.clear()
        self.ui_ncc.formContainer.setProperty("current_ncc_id", None)

    def connect_nhap_hang_events(self):
        self.ui_nhap.btnThem.clicked.connect(self.handle_them_vao_bang_nhap)
        self.ui_nhap.btnXoa.clicked.connect(self.handle_xoa_dong_nhap)
        self.ui_nhap.btnXacNhan.clicked.connect(self.handle_xac_nhan_nhap_kho)
        self.refresh_nhap_hang_suggestions()

    def refresh_nhap_hang_suggestions(self):
        self.ui_nhap.cbNCC.clear(); self.ui_nhap.cbNCC.addItem("-- Chọn Nhà Cung Cấp --")
        self.ui_nhap.cbNCC.addItems(dich_vu_nhap_hang.lay_danh_sach_ncc())
        completer = QCompleter(dich_vu_nhap_hang.lay_danh_sach_ten_sach())
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui_nhap.txtTenSach.setCompleter(completer)

    def handle_them_vao_bang_nhap(self):
        ten, sl, gia, ncc = self.ui_nhap.txtTenSach.text().strip(), self.ui_nhap.txtSoLuong.text().strip(), self.ui_nhap.txtDonGia.text().strip(), self.ui_nhap.cbNCC.currentText()
        if not ten or not sl or not gia or ncc == "-- Chọn Nhà Cung Cấp --": return
        row = self.ui_nhap.tableNhap.rowCount()
        self.ui_nhap.tableNhap.insertRow(row)
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
        res = dich_vu_nhap_hang.xac_nhan_nhap_kho(ten_ncc, list_h)
        if res["ket_qua"] == "thanh_cong":
            QtWidgets.QMessageBox.information(self, "Thành công", res["noi_dung"])
            self.ui_nhap.tableNhap.setRowCount(0); self.cap_nhat_du_lieu_trang_chu()

    def connect_quan_ly_tra_events(self):
        self.ui_tra.dateTra.setDate(QtCore.QDate.currentDate())
        self.ui_tra.btnTinh.clicked.connect(self.handle_tinh_tien_phat)
        self.ui_tra.btnTra.clicked.connect(self.handle_xac_nhan_tra)
        self.ui_tra.dateTra.dateChanged.connect(self.handle_tinh_so_ngay_tre)
        self.ui_tra.txtMaSV.editingFinished.connect(self.update_tra_sach_completer)

    def update_tra_sach_completer(self):
        ma_sv = self.ui_tra.txtMaSV.text().strip()
        if not ma_sv: return
        self.du_lieu_muon_chua_tra = dich_vu_tra_sach.lay_danh_sach_chua_tra(ma_sv)
        ten_sach_list = list(set([row[3] for row in self.du_lieu_muon_chua_tra]))
        completer = QCompleter(ten_sach_list)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.activated[str].connect(self.fill_thong_tin_muon)
        self.ui_tra.txtSach.setCompleter(completer)

    def fill_thong_tin_muon(self, ten_sach):
        for row in self.du_lieu_muon_chua_tra:
            if row[3] == ten_sach:
                self.ui_tra.txtTenSV.setText(str(row[2])); self.ui_tra.dateMuon.setDate(QtCore.QDate.fromString(str(row[4]), "yyyy-MM-dd"))
                self.ui_tra.dateHanTra.setDate(QtCore.QDate.fromString(str(row[5]), "yyyy-MM-dd"))
                self.ui_tra.formContainer.setProperty("current_phieu_muon_id", row[0]); self.handle_tinh_so_ngay_tre(); break

    def handle_tinh_so_ngay_tre(self):
        days = self.ui_tra.dateHanTra.date().daysTo(self.ui_tra.dateTra.date())
        self.ui_tra.txtTre.setText(str(days if days > 0 else 0)); self.handle_tinh_tien_phat()

    def handle_tinh_tien_phat(self):
        phat = int(self.ui_tra.txtTre.text() or 0) * 2000
        self.ui_tra.txtTongPhat.setText(str(phat)); self.ui_tra.formContainer.setProperty("raw_tien_phat", phat)

    def handle_xac_nhan_tra(self):
        ma_pm = self.ui_tra.formContainer.property("current_phieu_muon_id")
        if not ma_pm: return
        res, msg = dich_vu_tra_sach.xac_nhan_tra_sach(ma_pm, self.ui_tra.dateTra.date().toString("yyyy-MM-dd"), int(self.ui_tra.txtTre.text() or 0), self.ui_tra.formContainer.property("raw_tien_phat") or 0)
        if res:
            QtWidgets.QMessageBox.information(self, "Thành công", msg); self.load_data_tra()
            for ipt in [self.ui_tra.txtMaSV, self.ui_tra.txtTenSV, self.ui_tra.txtSach]: ipt.clear()
            self.ui_tra.txtTre.setText("0"); self.ui_tra.txtTongPhat.setText("0"); self.cap_nhat_du_lieu_trang_chu()

    def load_data_tra(self):
        data = dich_vu_tra_sach.lay_lich_su_tra_sach()
        self.ui_tra.tableMuonTra.setRowCount(0)
        for r, row_d in enumerate(data):
            self.ui_tra.tableMuonTra.insertRow(r)
            for c, val in enumerate(row_d): self.ui_tra.tableMuonTra.setItem(r, c, QtWidgets.QTableWidgetItem(str(val)))

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
        row = item.row(); self.ui_sach.txtTenSach.setText(self.ui_sach.tableSach.item(row, 1).text())
        self.ui_sach.txtTacGia.setText(self.ui_sach.tableSach.item(row, 2).text()); self.ui_sach.txtTheLoai.setText(self.ui_sach.tableSach.item(row, 3).text())
        self.ui_sach.txtSoLuong.setText(self.ui_sach.tableSach.item(row, 4).text()); self.ui_sach.txtNXB.setText(self.ui_sach.tableSach.item(row, 5).text())
        self.ui_sach.txtNamXB.setText(self.ui_sach.tableSach.item(row, 6).text()); self.ui_sach.formContainer.setProperty("current_id", self.ui_sach.tableSach.item(row, 0).text())

    def handle_them_sach(self):
        res, msg = dich_vu_quan_ly_sach.them_sach(self.ui_sach.txtTenSach.text().strip(), self.ui_sach.txtTacGia.text().strip(), self.ui_sach.txtTheLoai.text().strip(), self.ui_sach.txtNXB.text().strip(), int(self.ui_sach.txtNamXB.text() or 0))
        if res: self.load_data_sach()

    def handle_sua_sach(self):
        ma = self.ui_sach.formContainer.property("current_id")
        if ma:
            res, msg = dich_vu_quan_ly_sach.sua_sach(ma, self.ui_sach.txtTenSach.text().strip(), self.ui_sach.txtTacGia.text().strip(), self.ui_sach.txtTheLoai.text().strip(), int(self.ui_sach.txtSoLuong.text() or 0), self.ui_sach.txtNXB.text().strip(), int(self.ui_sach.txtNamXB.text() or 0))
            if res: self.load_data_sach()

    def handle_xoa_sach(self):
        ma = self.ui_sach.formContainer.property("current_id")
        if ma and QtWidgets.QMessageBox.question(self, "Xác nhận", "Xóa?", QtWidgets.QMessageBox.StandardButton.Yes) == QtWidgets.QMessageBox.StandardButton.Yes:
            res, msg = dich_vu_quan_ly_sach.xoa_sach(ma)
            if res: self.load_data_sach()

    def handle_tim_kiem_sach(self): self.load_data_sach(dich_vu_quan_ly_sach.tim_kiem_sach(self.ui_sach.txtTimKiem.text().strip()))

    def connect_quan_ly_muon_events(self):
        self.ui_muon.btnMuon.clicked.connect(self.handle_muon_sach); self.ui_muon.btnTimKiem.clicked.connect(self.handle_tim_kiem_muon)
        completer = QCompleter(dich_vu_muon_sach.lay_tat_ca_ten_sach())
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui_muon.txtTenSach.setCompleter(completer)

    def load_data_muon(self, data=None):
        if data is None: data = dich_vu_muon_sach.lay_danh_sach_muon()
        self.ui_muon.tableMuon.setRowCount(0)
        for r, row_d in enumerate(data):
            self.ui_muon.tableMuon.insertRow(r)
            for c, val in enumerate(row_d): self.ui_muon.tableMuon.setItem(r, c, QtWidgets.QTableWidgetItem(str(val)))

    def handle_muon_sach(self):
        res, msg = dich_vu_muon_sach.cho_muon_sach(self.ui_muon.txtMaSV.text().strip(), self.ui_muon.txtHoTen.text().strip(), self.ui_muon.txtTenSach.text().strip(), int(self.ui_muon.txtSoLuong.text() or 0), self.ui_muon.txtNgayTra.date().toString("yyyy-MM-dd"))
        if res: self.load_data_muon(); self.cap_nhat_du_lieu_trang_chu()

    def handle_tim_kiem_muon(self): self.load_data_muon(dich_vu_muon_sach.tim_kiem_tong_hop(self.ui_muon.txtTimKiem.text().strip()))

    # ----------------------------------------------------------------
    # CHUYỂN TRANG VÀ SIDEBAR
    # ----------------------------------------------------------------
    def connect_sidebar_buttons(self):
        self.button_map = {
            self.ui.btnTrangChu: 0, self.ui.btnSach: 1, self.ui.btnMuonSach: 2,
            self.ui.btnTraSach: 3, self.ui.btnNhapHang: 4, self.ui.btnNCC: 5,
            self.ui.btnNhanVien: 6, self.ui.btnThongKe: 7, self.ui.btnTaiKhoan: 8
        }
        for btn, index in self.button_map.items():
            if btn: btn.clicked.connect(lambda checked, i=index: self.switch_page(i))

    def switch_page(self, index):
        self.ui.StackedWidget.setCurrentIndex(index)
        if index == 0: self.cap_nhat_du_lieu_trang_chu()
        elif index == 1: self.load_data_sach()
        elif index == 2: self.load_data_muon()
        elif index == 3: self.load_data_tra()
        elif index == 4: self.refresh_nhap_hang_suggestions()
        elif index == 5: self.load_data_ncc()
        elif index == 6: self.load_data_nv()
        elif index == 7: self.load_data_thong_ke()

# ================================================================
# CHƯƠNG TRÌNH CHÍNH
# ================================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    login_win = LoginWindow()
    main_win = LibraryManager()
    login_win.login_success.connect(lambda user_info: main_win.show())
    login_win.show()
    sys.exit(app.exec())