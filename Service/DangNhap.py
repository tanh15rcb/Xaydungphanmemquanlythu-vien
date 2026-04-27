import pyodbc
from Database.database import db_manager

class DichVuDangNhap:
    def __init__(self):
        # Sử dụng db_manager đã cấu hình kết nối localhost\SQLEXPRESS
        self.quan_ly_db = db_manager

    def thuc_hien_dang_nhap(self, tai_khoan, mat_khau):
        """
        Kiểm tra thông tin đăng nhập từ cơ sở dữ liệu QuanLyThuVien.
        Trả về: Kết quả kiểm tra và thông tin nhân viên nếu thành công.
        """
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return {"ket_qua": "loi", "noi_dung": "Không thể kết nối đến SQL Server"}

        try:
            con_tro = ket_noi.cursor()
            
            # Câu truy vấn kết hợp bảng Users và NhanVien
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
            ket_noi.close()

# Khởi tạo đối tượng để sử dụng
dich_vu_dang_nhap = DichVuDangNhap()