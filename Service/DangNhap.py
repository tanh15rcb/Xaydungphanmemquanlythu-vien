import pyodbc
from Database.database import db_manager

class DichVuDangNhap:
    def __init__(self):
        # Sử dụng db_manager đã cấu hình kết nối localhost\SQLEXPRESS
        self.quan_ly_db = db_manager

    def thuc_hien_dang_nhap(self, tai_khoan, mat_khau):
        """
        Kiểm tra thông tin đăng nhập từ cơ sở dữ liệu (Dành cho Thủ thư/Admin).
        """
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return {"ket_qua": "loi", "noi_dung": "Không thể kết nối đến SQL Server"}

        try:
            con_tro = ket_noi.cursor()
            truy_van = """
                SELECT u.TenDangNhap, u.Role, u.MaNhanVien, n.TenNhanVien
                FROM Users u
                LEFT JOIN NhanVien n ON u.MaNhanVien = n.MaNhanVien
                WHERE u.TenDangNhap = ? AND u.MatKhau = ?
            """
            con_tro.execute(truy_van, (tai_khoan, mat_khau))
            dong_du_lieu = con_tro.fetchone()
            
            if dong_du_lieu:
                return {
                    "ket_qua": "thanh_cong",
                    "thong_tin": {
                        "ten_dang_nhap": dong_du_lieu[0],
                        "vai_tro": dong_du_lieu[1],
                        "ma_nv": dong_du_lieu[2],
                        "ten_nv": dong_du_lieu[3]
                    }
                }
            else:
                return {"ket_qua": "sai_thong_tin", "noi_dung": "Tên đăng nhập hoặc mật khẩu không đúng"}

        except Exception as e:
            return {"ket_qua": "loi_he_thong", "noi_dung": f"Lỗi truy vấn: {str(e)}"}
        finally:
            if ket_noi:
                ket_noi.close()

    # --- HÀM MỚI: ĐĂNG NHẬP NHANH CHO SINH VIÊN ---
    def dang_nhap_nhanh_sinh_vien(self):
        """
        Cho phép vào thẳng hệ thống với quyền Sinh viên mà không cần tài khoản/mật khẩu.
        Giữ nguyên cấu trúc trả về để đồng bộ với hàm trên.
        """
        return {
            "ket_qua": "thanh_cong",
            "thong_tin": {
                "ten_dang_nhap": "Guest",
                "vai_tro": "SinhVien", # Dùng vai trò này để điều hướng giao diện
                "ma_nv": None,
                "ten_nv": "Khách (Sinh viên)"
            }
        }

# Khởi tạo đối tượng để sử dụng
dich_vu_dang_nhap = DichVuDangNhap()