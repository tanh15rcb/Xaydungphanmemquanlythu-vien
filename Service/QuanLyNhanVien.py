import pyodbc
from Database.database import db_manager

class DichVuNhanVien:
    def __init__(self):
        self.quan_ly_db = db_manager

    def lay_tat_ca_nv(self):
        """Lấy danh sách nhân viên hiển thị lên bảng."""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi: 
            return []
        try:
            con_tro = ket_noi.cursor()
            # Sử dụng đúng tên cột theo Database: MaNhanVien, TenNhanVien
            query = """
                SELECT MaNhanVien, TenNhanVien, GioiTinh, DienThoai, Email, DiaChi 
                FROM NhanVien
            """
            con_tro.execute(query)
            return con_tro.fetchall()
        except Exception as e:
            print(f"Lỗi lấy danh sách nhân viên: {e}")
            return []
        finally:
            ket_noi.close()

    def them_nv(self, ten, gioi_tinh, sdt, email, dia_chi):
        """Thêm nhân viên mới."""
        if not ten or not sdt:
            return {"ket_qua": "loi", "noi_dung": "Tên và Số điện thoại không được để trống!"}
        
        ket_noi = self.quan_ly_db.get_connection()
        try:
            con_tro = ket_noi.cursor()
            query = """
                INSERT INTO NhanVien (TenNhanVien, GioiTinh, DienThoai, Email, DiaChi)
                VALUES (?, ?, ?, ?, ?)
            """
            con_tro.execute(query, (ten, gioi_tinh, sdt, email, dia_chi))
            ket_noi.commit()
            return {"ket_qua": "thanh_cong", "noi_dung": "Thêm nhân viên thành công!"}
        except Exception as e:
            return {"ket_qua": "loi", "noi_dung": f"Lỗi: {str(e)}"}
        finally:
            ket_noi.close()

    def sua_nv(self, ma_nv, ten, gioi_tinh, sdt, email, dia_chi):
        """Cập nhật thông tin nhân viên dựa trên MaNhanVien."""
        if not ma_nv: 
            return {"ket_qua": "loi", "noi_dung": "Vui lòng chọn nhân viên cần sửa!"}
        
        ket_noi = self.quan_ly_db.get_connection()
        try:
            con_tro = ket_noi.cursor()
            query = """
                UPDATE NhanVien 
                SET TenNhanVien=?, GioiTinh=?, DienThoai=?, Email=?, DiaChi=?
                WHERE MaNhanVien=?
            """
            con_tro.execute(query, (ten, gioi_tinh, sdt, email, dia_chi, ma_nv))
            ket_noi.commit()
            return {"ket_qua": "thanh_cong", "noi_dung": "Cập nhật thông tin thành công!"}
        except Exception as e:
            return {"ket_qua": "loi", "noi_dung": f"Lỗi: {str(e)}"}
        finally:
            ket_noi.close()

    def xoa_nv(self, ma_nv):
        """Xóa nhân viên và xử lý ràng buộc khóa ngoại."""
        ket_noi = self.quan_ly_db.get_connection()
        try:
            con_tro = ket_noi.cursor()
            
            # Kiểm tra xem nhân viên có tài khoản (Users) hoặc đang đứng tên phiếu mượn không
            # Hệ thống SQL Server sẽ tự báo lỗi nếu có ràng buộc Foreign Key (FK)
            query = "DELETE FROM NhanVien WHERE MaNhanVien=?"
            con_tro.execute(query, (ma_nv,))
            
            ket_noi.commit()
            return {"ket_qua": "thanh_cong", "noi_dung": "Đã xóa nhân viên khỏi hệ thống!"}
        except Exception as e:
            # Thông báo này hiện ra nếu MaNhanVien đang được dùng ở bảng Users hoặc PhieuMuon
            return {"ket_qua": "loi", "noi_dung": "Không thể xóa: Nhân viên này đang có dữ liệu liên kết (Tài khoản/Phiếu mượn)!"}
        finally:
            ket_noi.close()

    def tim_kiem_nv(self, tu_khoa):
        """
        Tìm kiếm đa thành phần: 
        Tìm theo Tên, Số điện thoại, Email hoặc Địa chỉ.
        """
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi: 
            return []
        try:
            con_tro = ket_noi.cursor()
            # Tìm kiếm không phân biệt hoa thường với LIKE và dấu %
            query = """
                SELECT MaNhanVien, TenNhanVien, GioiTinh, DienThoai, Email, DiaChi 
                FROM NhanVien 
                WHERE TenNhanVien LIKE ? 
                   OR DienThoai LIKE ? 
                   OR Email LIKE ? 
                   OR DiaChi LIKE ?
            """
            search_param = f"%{tu_khoa}%"
            con_tro.execute(query, (search_param, search_param, search_param, search_param))
            return con_tro.fetchall()
        except Exception as e:
            print(f"Lỗi tìm kiếm: {e}")
            return []
        finally:
            ket_noi.close()

# Khởi tạo đối tượng dịch vụ dùng chung
dich_vu_nv = DichVuNhanVien()