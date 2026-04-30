import pyodbc
from Database.database import db_manager

class DichVuQuanLySach:
    def __init__(self):
        # Sử dụng db_manager đã cấu hình kết nối localhost\SQLEXPRESS
        self.quan_ly_db = db_manager

    def lay_tat_ca_sach(self):
        """Lấy danh sách toàn bộ sách để hiển thị lên bảng"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return []
        try:
            con_tro = ket_noi.cursor()
            # Truy vấn theo đúng cấu trúc bảng mới
            truy_van = "SELECT MaSach, TenSach, TacGia, TheLoai, SoLuong, NhaXuatBan, NamXuatBan FROM Sach ORDER BY MaSach DESC"
            con_tro.execute(truy_van)
            return con_tro.fetchall()
        except Exception as e:
            print(f"Lỗi lấy danh sách sách: {str(e)}")
            return []
        finally:
            ket_noi.close()

    def them_sach(self, ten_sach, tac_gia, the_loai, nxb, nam_xb):
        """Thêm một cuốn sách mới với số lượng mặc định ban đầu là 0"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return False, "Không thể kết nối cơ sở dữ liệu"
        try:
            con_tro = ket_noi.cursor()
            # Bỏ cột SoLuong khỏi câu lệnh INSERT để Database tự dùng DEFAULT 0
            # Hoặc truyền trực tiếp giá trị 0 vào SQL
            truy_van = """
                INSERT INTO Sach (TenSach, TacGia, TheLoai, SoLuong, NhaXuatBan, NamXuatBan) 
                VALUES (?, ?, ?, 0, ?, ?)
            """
            con_tro.execute(truy_van, (ten_sach, tac_gia, the_loai, nxb, nam_xb))
            ket_noi.commit()
            return True, "Thêm sách thành công! (Số lượng mặc định: 0)"
        except Exception as e:
            return False, f"Lỗi khi thêm: {str(e)}"
        finally:
            ket_noi.close()

    def sua_sach(self, ma_sach, ten_sach, tac_gia, the_loai, so_luong, nxb, nam_xb):
        """Cập nhật thông tin sách dựa trên mã sách"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return False, "Không thể kết nối cơ sở dữ liệu"
        try:
            con_tro = ket_noi.cursor()
            truy_van = """
                UPDATE Sach 
                SET TenSach = ?, TacGia = ?, TheLoai = ?, SoLuong = ?, NhaXuatBan = ?, NamXuatBan = ?
                WHERE MaSach = ?
            """
            con_tro.execute(truy_van, (ten_sach, tac_gia, the_loai, so_luong, nxb, nam_xb, ma_sach))
            ket_noi.commit()
            return True, "Cập nhật thông tin thành công!"
        except Exception as e:
            return False, f"Lỗi khi sửa: {str(e)}"
        finally:
            ket_noi.close()

    def xoa_sach(self, ma_sach):
        """Xóa sách khỏi database"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return False, "Không thể kết nối cơ sở dữ liệu"
        try:
            con_tro = ket_noi.cursor()
            truy_van = "DELETE FROM Sach WHERE MaSach = ?"
            con_tro.execute(truy_van, (ma_sach,))
            ket_noi.commit()
            return True, "Xóa sách thành công!"
        except pyodbc.IntegrityError:
            return False, "Không thể xóa sách này vì đang có dữ liệu mượn/trả liên quan."
        except Exception as e:
            return False, f"Lỗi khi xóa: {str(e)}"
        finally:
            ket_noi.close()

    def tim_kiem_sach(self, tu_khoa):
        """Tìm kiếm thông minh: tìm theo tên, tác giả, thể loại, NXB, năm XB hoặc mã sách"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return []
        try:
            con_tro = ket_noi.cursor()
            # Tìm kiếm trên tất cả các trường dữ liệu quan trọng
            truy_van = """
                SELECT MaSach, TenSach, TacGia, TheLoai, SoLuong, NhaXuatBan, NamXuatBan 
                FROM Sach 
                WHERE CAST(MaSach AS NVARCHAR) LIKE ? 
                   OR TenSach LIKE ? 
                   OR TacGia LIKE ? 
                   OR TheLoai LIKE ? 
                   OR NhaXuatBan LIKE ? 
                   OR CAST(NamXuatBan AS NVARCHAR) LIKE ?
            """
            pattern = f"%{tu_khoa}%"
            # Truyền tham số cho tất cả dấu ? trong câu lệnh trên
            con_tro.execute(truy_van, (pattern, pattern, pattern, pattern, pattern, pattern))
            return con_tro.fetchall()
        except Exception as e:
            print(f"Lỗi tìm kiếm sách: {str(e)}")
            return []
        finally:
            ket_noi.close()

# Khởi tạo đối tượng
dich_vu_quan_ly_sach = DichVuQuanLySach()