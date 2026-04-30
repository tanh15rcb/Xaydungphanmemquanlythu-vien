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

    # --- PHẦN SỬA LỖI HIỂN THỊ TRANG CHỦ ---
    def cap_nhat_du_lieu_trang_chu(self):
        # 1. Cập nhật các con số thống kê
        tk = dich_vu_trang_chu.lay_thong_ke_tong_hop()
        if tk:
            try:
                self.ui.lbl_val_tong_sach.setText(f"{tk['tong_sach']:,}")
                self.ui.lbl_val_dang_muon.setText(f"{tk['dang_muon']:,}")
                self.ui.lbl_val_qua_han.setText(f"{tk['qua_han']:,}")
            except AttributeError: pass

        # 2. Cập nhật bảng "Danh sách mượn mới nhất" (Sửa lỗi không hiển thị)
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
    # QUẢN LÝ TRẢ SÁCH
    # ----------------------------------------------------------------
    def connect_quan_ly_tra_events(self):
        self.ui_tra.dateTra.setDate(QtCore.QDate.currentDate())
        self.ui_tra.btnTinh.clicked.connect(self.handle_tinh_tien_phat)
        self.ui_tra.btnTra.clicked.connect(self.handle_xac_nhan_tra)
        self.ui_tra.dateTra.dateChanged.connect(self.handle_tinh_so_ngay_tre)
        self.ui_tra.txtMaSV.editingFinished.connect(self.update_tra_sach_completer)

    def update_tra_sach_completer(self):
        ma_sv = self.ui_tra.txtMaSV.text().strip()
        if not ma_sv:
            self.ui_tra.txtSach.setCompleter(None)
            return
        self.du_lieu_muon_chua_tra = dich_vu_tra_sach.lay_danh_sach_chua_tra(ma_sv)
        ten_sach_list = list(set([row[3] for row in self.du_lieu_muon_chua_tra]))
        completer = QCompleter(ten_sach_list)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.activated[str].connect(self.fill_thong_tin_muon)
        self.ui_tra.txtSach.setCompleter(completer)

    def fill_thong_tin_muon(self, ten_sach):
        for row in self.du_lieu_muon_chua_tra:
            if row[3] == ten_sach:
                self.ui_tra.txtTenSV.setText(str(row[2]))
                self.ui_tra.dateMuon.setDate(QtCore.QDate.fromString(str(row[4]), "yyyy-MM-dd"))
                self.ui_tra.dateHanTra.setDate(QtCore.QDate.fromString(str(row[5]), "yyyy-MM-dd"))
                self.ui_tra.formContainer.setProperty("current_phieu_muon_id", row[0])
                self.handle_tinh_so_ngay_tre()
                break

    def handle_tinh_so_ngay_tre(self):
        han_tra = self.ui_tra.dateHanTra.date()
        ngay_tra_thuc_te = self.ui_tra.dateTra.date()
        days_diff = han_tra.daysTo(ngay_tra_thuc_te)
        so_tre = days_diff if days_diff > 0 else 0
        self.ui_tra.txtTre.setText(str(so_tre))
        self.handle_tinh_tien_phat()

    def handle_tinh_tien_phat(self):
        try:
            so_ngay_tre = int(self.ui_tra.txtTre.text() or 0)
            muc_phat_ngay = 2000 
            if hasattr(self.ui_tra, 'txtPhatNgay') and self.ui_tra.txtPhatNgay.text():
                try: muc_phat_ngay = int(self.ui_tra.txtPhatNgay.text())
                except: pass
            tong_phat = so_ngay_tre * muc_phat_ngay
            self.ui_tra.txtTongPhat.setText(f"{tong_phat}")
            self.ui_tra.formContainer.setProperty("raw_tien_phat", tong_phat)
        except:
            self.ui_tra.txtTongPhat.setText("0")

    def handle_xac_nhan_tra(self):
        ma_pm = self.ui_tra.formContainer.property("current_phieu_muon_id")
        if not ma_pm:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Mã SV và chọn Sách!")
            return
        ngay_tra = self.ui_tra.dateTra.date().toString("yyyy-MM-dd")
        so_tre = int(self.ui_tra.txtTre.text() or 0)
        tien = self.ui_tra.formContainer.property("raw_tien_phat") or 0
        res, msg = dich_vu_tra_sach.xac_nhan_tra_sach(ma_pm, ngay_tra, so_tre, tien)
        if res:
            QtWidgets.QMessageBox.information(self, "Thành công", msg)
            self.load_data_tra()
            self.ui_tra.txtMaSV.clear()
            self.ui_tra.txtTenSV.clear()
            self.ui_tra.txtSach.clear()
            self.ui_tra.txtTre.setText("0")
            self.ui_tra.txtTongPhat.setText("0")
            self.cap_nhat_du_lieu_trang_chu()
        else:
            QtWidgets.QMessageBox.critical(self, "Lỗi", msg)

    def load_data_tra(self):
        data = dich_vu_tra_sach.lay_lich_su_tra_sach()
        if hasattr(self.ui_tra, 'tableMuonTra'):
            self.ui_tra.tableMuonTra.setRowCount(0)
            for row_idx, row_data in enumerate(data):
                self.ui_tra.tableMuonTra.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.ui_tra.tableMuonTra.setItem(row_idx, col_idx, item)

    # ----------------------------------------------------------------
    # CÁC PHẦN KHÁC (GIỮ NGUYÊN)
    # ----------------------------------------------------------------
    def connect_quan_ly_sach_events(self):
        self.ui_sach.btnThem.clicked.connect(self.handle_them_sach)
        self.ui_sach.btnSua.clicked.connect(self.handle_sua_sach)
        self.ui_sach.btnXoa.clicked.connect(self.handle_xoa_sach)
        self.ui_sach.btnTimKiem.clicked.connect(self.handle_tim_kiem_sach)
        self.ui_sach.tableSach.itemClicked.connect(self.handle_table_sach_click)

    def load_data_sach(self, data=None):
        if data is None: data = dich_vu_quan_ly_sach.lay_tat_ca_sach()
        self.ui_sach.tableSach.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.ui_sach.tableSach.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ui_sach.tableSach.setItem(row_idx, col_idx, item)

    def handle_table_sach_click(self, item):
        row = item.row()
        self.ui_sach.txtTenSach.setText(self.ui_sach.tableSach.item(row, 1).text())
        self.ui_sach.txtTacGia.setText(self.ui_sach.tableSach.item(row, 2).text())
        self.ui_sach.txtTheLoai.setText(self.ui_sach.tableSach.item(row, 3).text())
        self.ui_sach.txtSoLuong.setText(self.ui_sach.tableSach.item(row, 4).text())
        self.ui_sach.txtNXB.setText(self.ui_sach.tableSach.item(row, 5).text())
        self.ui_sach.txtNamXB.setText(self.ui_sach.tableSach.item(row, 6).text())
        self.ui_sach.formContainer.setProperty("current_id", self.ui_sach.tableSach.item(row, 0).text())

    def handle_them_sach(self):
        res, msg = dich_vu_quan_ly_sach.them_sach(
            self.ui_sach.txtTenSach.text().strip(), self.ui_sach.txtTacGia.text().strip(),
            self.ui_sach.txtTheLoai.text().strip(), self.ui_sach.txtNXB.text().strip(), 
            int(self.ui_sach.txtNamXB.text() or 0)
        )
        QtWidgets.QMessageBox.information(self, "Thông báo", msg)
        if res: self.load_data_sach()

    def handle_sua_sach(self):
        ma_sach = self.ui_sach.formContainer.property("current_id")
        if not ma_sach: return
        res, msg = dich_vu_quan_ly_sach.sua_sach(
            ma_sach, self.ui_sach.txtTenSach.text().strip(), self.ui_sach.txtTacGia.text().strip(),
            self.ui_sach.txtTheLoai.text().strip(), int(self.ui_sach.txtSoLuong.text() or 0),
            self.ui_sach.txtNXB.text().strip(), int(self.ui_sach.txtNamXB.text() or 0)
        )
        QtWidgets.QMessageBox.information(self, "Thông báo", msg)
        if res: self.load_data_sach()

    def handle_xoa_sach(self):
        ma_sach = self.ui_sach.formContainer.property("current_id")
        if not ma_sach: return
        confirm = QtWidgets.QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa?", 
                 QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            res, msg = dich_vu_quan_ly_sach.xoa_sach(ma_sach)
            QtWidgets.QMessageBox.information(self, "Thông báo", msg)
            if res: self.load_data_sach()

    def handle_tim_kiem_sach(self):
        tu_khoa = self.ui_sach.txtTimKiem.text().strip()
        ket_qua = dich_vu_quan_ly_sach.tim_kiem_sach(tu_khoa)
        self.load_data_sach(ket_qua)

    def connect_quan_ly_muon_events(self):
        self.ui_muon.btnMuon.clicked.connect(self.handle_muon_sach)
        self.ui_muon.btnTimKiem.clicked.connect(self.handle_tim_kiem_muon)
        self.update_book_completer()

    def update_book_completer(self):
        danh_sach_ten = dich_vu_muon_sach.lay_tat_ca_ten_sach()
        completer = QCompleter(danh_sach_ten)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.ui_muon.txtTenSach.setCompleter(completer)

    def load_data_muon(self, data=None):
        if data is None: data = dich_vu_muon_sach.lay_danh_sach_muon()
        self.ui_muon.tableMuon.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.ui_muon.tableMuon.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.ui_muon.tableMuon.setItem(row_idx, col_idx, item)

    def handle_muon_sach(self):
        ma_sv = self.ui_muon.txtMaSV.text().strip()
        ho_ten = self.ui_muon.txtHoTen.text().strip()
        ten_sach = self.ui_muon.txtTenSach.text().strip()
        so_luong = self.ui_muon.txtSoLuong.text().strip()
        han_tra = self.ui_muon.txtNgayTra.date().toString("yyyy-MM-dd")
        res, msg = dich_vu_muon_sach.cho_muon_sach(ma_sv, ho_ten, ten_sach, int(so_luong or 0), han_tra)
        if res:
            QtWidgets.QMessageBox.information(self, "Thành công", msg)
            self.load_data_muon()
            self.cap_nhat_du_lieu_trang_chu()
        else:
            QtWidgets.QMessageBox.critical(self, "Lỗi", msg)

    def handle_tim_kiem_muon(self):
        tu_khoa = self.ui_muon.txtTimKiem.text().strip()
        ket_qua = dich_vu_muon_sach.tim_kiem_tong_hop(tu_khoa)
        self.load_data_muon(ket_qua)

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
        elif index == 3: 
            self.load_data_tra()
            self.ui_tra.dateTra.setDate(QtCore.QDate.currentDate())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    login_win = LoginWindow()
    main_win = LibraryManager()
    login_win.login_success.connect(lambda user_info: main_win.show())
    login_win.show()
    sys.exit(app.exec())