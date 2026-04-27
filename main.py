import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
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

# --- IMPORT SERVICE ĐĂNG NHẬP ---
from Service.DangNhap import dich_vu_dang_nhap

# ================================================================
# LỚP ĐĂNG NHẬP (Đã cập nhật dùng Service Database)
# ================================================================
class LoginWindow(QtWidgets.QWidget):
    login_success = QtCore.pyqtSignal(dict) # Gửi kèm thông tin user khi đăng nhập thành công

    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginForm()
        self.ui.setupUi(self)

        # Đổ bóng để làm nổi bật form đăng nhập
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.ui.container.setGraphicsEffect(shadow)

        self.ui.btnLogin.clicked.connect(self.handle_login)
        self.ui.btnClose.clicked.connect(QtWidgets.QApplication.quit)
        self.ui.txtPass.returnPressed.connect(self.handle_login)

    def handle_login(self):
        # Lấy dữ liệu từ giao diện
        tai_khoan = self.ui.txtUser.text().strip()
        mat_khau = self.ui.txtPass.text().strip()

        if not tai_khoan or not mat_khau:
            QtWidgets.QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ tài khoản và mật khẩu!")
            return

        # Gọi Service để kiểm tra trong Database SQL Server
        ket_qua_dang_nhap = dich_vu_dang_nhap.thuc_hien_dang_nhap(tai_khoan, mat_khau)

        if ket_qua_dang_nhap["ket_qua"] == "thanh_cong":
            # Nếu thành công, gửi dữ liệu user và đóng cửa sổ login
            self.login_success.emit(ket_qua_dang_nhap["thong_tin"])
            self.close()
        else:
            # Hiển thị lỗi cụ thể từ Service (Sai thông tin hoặc Lỗi kết nối)
            QtWidgets.QMessageBox.warning(self, "Lỗi đăng nhập", ket_qua_dang_nhap["noi_dung"])

# ================================================================
# LỚP QUẢN LÝ CHÍNH (Giữ nguyên các hàm chức năng)
# ================================================================
class LibraryManager(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainFrame()
        self.ui.setupUi(self)
        self.setWindowTitle("Hệ Thống Quản Lý Thư Viện Pro")

        # --- 1. KHỞI TẠO CÁC TRANG CON ---
        self.init_sub_pages()

        # --- 2. KẾT NỐI SIDEBAR ---
        self.connect_sidebar_buttons()

        # Mặc định Trang Chủ
        self.ui.StackedWidget.setCurrentIndex(0)

    def _embed_page(self, ui_class, index):
        """Hàm nhúng UI con vào StackedWidget"""
        temp_window = QtWidgets.QMainWindow()
        ui_instance = ui_class()
        ui_instance.setupUi(temp_window)
        if hasattr(ui_instance, 'sidebar'):
            ui_instance.sidebar.hide()
        self.ui.StackedWidget.insertWidget(index, ui_instance.centralwidget)
        return ui_instance

    def init_sub_pages(self):
        """Khởi tạo tất cả các trang theo đúng thứ tự Index"""
        self.ui_sach = self._embed_page(Ui_QuanLySach, 1)
        self.ui_muon = self._embed_page(Ui_QuanLyMuon, 2)
        self.ui_tra = self._embed_page(Ui_QuanLyTraSach, 3)
        self.ui_nhap = self._embed_page(Ui_NhapHang, 4)
        self.ui_ncc = self._embed_page(Ui_NhaCungCap, 5)
        self.ui_nv = self._embed_page(Ui_QuanLyNhanVien, 6)
        
        # Trang Thống kê và Biểu đồ
        self.ui_thongke = self._embed_page(Ui_ThongKe, 7)
        self.ui_thongke.btnXemBaoCao.clicked.connect(self.update_charts)
        self.update_charts() # Vẽ biểu đồ lần đầu

        self.ui_taikhoan = self._embed_page(Ui_TaiKhoan, 8)

    # --- CÁC HÀM XỬ LÝ BIỂU ĐỒ ---
    def get_test_data(self, criteria):
        if "mượn nhiều nhất" in criteria.lower():
            bar_data = {"Dế Mèn": 150, "Số Đỏ": 90, "Lão Hạc": 110, "Tắt Đèn": 200}
            pie_data = {"Đúng hạn": 85, "Trễ hạn": 15}
            titles = ("Sách Mượn Nhiều Nhất", "Tỉ lệ hoàn trả")
        else:
            bar_data = {"Tháng 1": 5, "Tháng 2": 15, "Tháng 3": 8, "Tháng 4": 12}
            pie_data = {"Sách tốt": 92, "Sách hỏng": 8}
            titles = ("Thống kê trả trễ", "Tình trạng kho")
        return bar_data, pie_data, titles

    def update_charts(self):
        self.clear_layout(self.ui_thongke.barVLayout)
        self.clear_layout(self.ui_thongke.pieVLayout)

        criteria = self.ui_thongke.cbLoaiThongKe.currentText()
        bar_data, pie_data, titles = self.get_test_data(criteria)

        fig_bar = Figure(figsize=(5, 4), tight_layout=True)
        ax_bar = fig_bar.add_subplot(111)
        ax_bar.bar(bar_data.keys(), bar_data.values(), color='#3498db')
        ax_bar.set_title(titles[0])
        self.ui_thongke.barVLayout.addWidget(FigureCanvas(fig_bar))

        fig_pie = Figure(figsize=(5, 4), tight_layout=True)
        ax_pie = fig_pie.add_subplot(111)
        ax_pie.pie(pie_data.values(), labels=pie_data.keys(), autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'])
        ax_pie.set_title(titles[1])
        self.ui_thongke.pieVLayout.addWidget(FigureCanvas(fig_pie))

    def clear_layout(self, layout):
        while layout.count() > 0:
            item = layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    # --- KẾT NỐI SIDEBAR ---
    def connect_sidebar_buttons(self):
        self.button_map = {
            self.ui.btnTrangChu: 0,
            self.ui.btnSach: 1,
            self.ui.btnMuonSach: 2,
            self.ui.btnTraSach: 3,
            self.ui.btnNhapHang: 4,
            self.ui.btnNCC: 5,
            self.ui.btnNhanVien: 6,
            self.ui.btnThongKe: 7,
            self.ui.btnTaiKhoan: 8
        }
        for btn, index in self.button_map.items():
            if btn: btn.clicked.connect(lambda checked, i=index: self.switch_page(i))

        if hasattr(self.ui, 'btnLogout'):
            self.ui.btnLogout.clicked.connect(self.close)

    def switch_page(self, index):
        self.ui.StackedWidget.setCurrentIndex(index)

# ================================================================
# CHƯƠNG TRÌNH CHÍNH
# ================================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QtGui.QFont("Segoe UI", 10))

    login_win = LoginWindow()
    main_win = LibraryManager()

    # Kết nối: Đăng nhập OK -> Hiện Main
    # Nhận thêm dữ liệu người dùng (nếu cần hiển thị tên lên trang chủ)
    login_win.login_success.connect(lambda user_info: main_win.show())

    login_win.show()
    sys.exit(app.exec())