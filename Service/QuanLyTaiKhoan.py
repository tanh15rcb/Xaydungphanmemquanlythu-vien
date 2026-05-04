import pyodbc
from Database.database import db_manager

class DichVuTaiKhoan:
    def __init__(self):
        # Sử dụng db_manager đã cấu hình kết nối localhost\SQLEXPRESS
        self.quan_ly_db = db_manager

    def lay_tat_ca_tai_khoan(self):
        """Lấy danh sách tất cả tài khoản từ database"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return []
        try:
            con_tro = ket_noi.cursor()
            # Lấy thông tin tài khoản (có thể join với NhanVien nếu muốn hiện tên NV)
            truy_van = "SELECT MaUser, TenDangNhap, MatKhau, Role, MaNhanVien FROM Users"
            con_tro.execute(truy_van)
            return con_tro.fetchall()
        except Exception as e:
            print(f"Lỗi lấy dữ liệu tài khoản: {str(e)}")
            return []
        finally:
            ket_noi.close()

    def them_tai_khoan(self, ten_dn, mat_khau, vai_tro, ma_nv):
        """Thêm tài khoản mới vào hệ thống"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return False, "Không thể kết nối cơ sở dữ liệu"
        try:
            con_tro = ket_noi.cursor()
            truy_van = "INSERT INTO Users (TenDangNhap, MatKhau, Role, MaNhanVien) VALUES (?, ?, ?, ?)"
            con_tro.execute(truy_van, (ten_dn, mat_khau, vai_tro, ma_nv))
            ket_noi.commit()
            return True, "Thêm tài khoản thành công!"
        except Exception as e:
            return False, f"Lỗi SQL: {str(e)}"
        finally:
            ket_noi.close()

    def sua_tai_khoan(self, ma_user, ten_dn, mat_khau, vai_tro, ma_nv):
        """Cập nhật thông tin tài khoản hiện có"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return False, "Không thể kết nối cơ sở dữ liệu"
        try:
            con_tro = ket_noi.cursor()
            truy_van = """
                UPDATE Users 
                SET TenDangNhap = ?, MatKhau = ?, Role = ?, MaNhanVien = ? 
                WHERE MaUser = ?
            """
            con_tro.execute(truy_van, (ten_dn, mat_khau, vai_tro, ma_nv, ma_user))
            ket_noi.commit()
            return True, "Cập nhật tài khoản thành công!"
        except Exception as e:
            return False, f"Lỗi SQL: {str(e)}"
        finally:
            ket_noi.close()

    def xoa_tai_khoan(self, ma_user):
        """Xóa tài khoản khỏi hệ thống"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return False, "Không thể kết nối cơ sở dữ liệu"
        try:
            con_tro = ket_noi.cursor()
            truy_van = "DELETE FROM Users WHERE MaUser = ?"
            con_tro.execute(truy_van, (ma_user,))
            ket_noi.commit()
            return True, "Xóa tài khoản thành công!"
        except Exception as e:
            return False, f"Lỗi SQL: {str(e)}"
        finally:
            ket_noi.close()

# Khởi tạo đối tượng để sử dụng trong main.py
dich_vu_tai_khoan = DichVuTaiKhoan()