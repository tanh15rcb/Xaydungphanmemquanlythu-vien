import pyodbc
from Database.database import db_manager

class DichVuNhaCungCap:
    def __init__(self):
        # Sử dụng db_manager đã cấu hình kết nối localhost\SQLEXPRESS
        self.quan_ly_db = db_manager

    def lay_tat_ca_ncc(self):
        """Lấy toàn bộ danh sách nhà cung cấp để hiển thị lên bảng."""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return []
        try:
            con_tro = ket_noi.cursor()
            # Lấy đúng 5 cột theo cấu trúc bảng tableNCC đã thiết kế trong UI
            truy_van = "SELECT MaNCC, TenNCC, DiaChi, DienThoai, Email FROM NhaCungCap"
            con_tro.execute(truy_van)
            return con_tro.fetchall()
        except:
            return []
        finally:
            ket_noi.close()

    def them_ncc(self, ten, dia_chi, sdt, email):
        """Thực hiện thêm mới nhà cung cấp."""
        if not ten:
            return {"ket_qua": "loi", "noi_dung": "Tên nhà cung cấp không được để trống!"}

        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return {"ket_qua": "loi", "noi_dung": "Không thể kết nối đến SQL Server"}

        try:
            con_tro = ket_noi.cursor()
            truy_van = """
                INSERT INTO NhaCungCap (TenNCC, DiaChi, DienThoai, Email)
                VALUES (?, ?, ?, ?)
            """
            con_tro.execute(truy_van, (ten, dia_chi, sdt, email))
            ket_noi.commit()
            return {"ket_qua": "thanh_cong", "noi_dung": "Đã thêm nhà cung cấp mới thành công!"}
        except Exception as e:
            return {"ket_qua": "loi_he_thong", "noi_dung": f"Lỗi hệ thống: {str(e)}"}
        finally:
            ket_noi.close()

    def sua_ncc(self, ma_ncc, ten, dia_chi, sdt, email):
        """Cập nhật thông tin nhà cung cấp hiện có."""
        if not ma_ncc:
            return {"ket_qua": "loi", "noi_dung": "Không tìm thấy mã đối tác cần sửa!"}

        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return {"ket_qua": "loi", "noi_dung": "Không thể kết nối đến SQL Server"}

        try:
            con_tro = ket_noi.cursor()
            truy_van = """
                UPDATE NhaCungCap 
                SET TenNCC = ?, DiaChi = ?, DienThoai = ?, Email = ?
                WHERE MaNCC = ?
            """
            con_tro.execute(truy_van, (ten, dia_chi, sdt, email, ma_ncc))
            ket_noi.commit()
            return {"ket_qua": "thanh_cong", "noi_dung": "Cập nhật thông tin đối tác thành công!"}
        except Exception as e:
            return {"ket_qua": "loi_he_thong", "noi_dung": f"Lỗi hệ thống: {str(e)}"}
        finally:
            ket_noi.close()

    def xoa_ncc(self, ma_ncc):
        """Xóa nhà cung cấp khỏi hệ thống."""
        if not ma_ncc:
            return {"ket_qua": "loi", "noi_dung": "Vui lòng chọn đối tác cần xóa!"}

        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return {"ket_qua": "loi", "noi_dung": "Không thể kết nối đến SQL Server"}

        try:
            con_tro = ket_noi.cursor()
            
            # Kiểm tra xem NCC đã có phiếu nhập hàng chưa trước khi xóa
            con_tro.execute("SELECT COUNT(*) FROM PhieuNhap WHERE MaNCC = ?", (ma_ncc,))
            if con_tro.fetchone()[0] > 0:
                return {"ket_qua": "loi", "noi_dung": "Không thể xóa! Nhà cung cấp này đang có dữ liệu nhập hàng liên kết."}

            con_tro.execute("DELETE FROM NhaCungCap WHERE MaNCC = ?", (ma_ncc,))
            ket_noi.commit()
            return {"ket_qua": "thanh_cong", "noi_dung": "Đã xóa nhà cung cấp thành công!"}
        except Exception as e:
            return {"ket_qua": "loi_he_thong", "noi_dung": f"Lỗi hệ thống: {str(e)}"}
        finally:
            ket_noi.close()

# Khởi tạo đối tượng để sử dụng
dich_vu_ncc = DichVuNhaCungCap()