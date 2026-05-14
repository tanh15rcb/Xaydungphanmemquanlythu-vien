import pyodbc
from Database.database import db_manager

class XemSachService:
    def __init__(self):
        # Sử dụng db_manager đồng bộ với các service khác
        self.quan_ly_db = db_manager

    def tim_kiem_sach(self, tu_khoa=""):
        """Truy vấn danh sách sách (7 cột) dựa trên từ khóa"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return []

        try:
            con_tro = ket_noi.cursor()
            # Truy vấn lấy 7 cột: Ma, Ten, TacGia, TheLoai, SoLuong, NXB, NamXB
            query = """
                SELECT MaSach, TenSach, TacGia, TheLoai, SoLuong, NhaXuatBan, NamXuatBan 
                FROM Sach 
                WHERE TenSach LIKE ? OR TacGia LIKE ? OR TheLoai LIKE ?
            """
            search_val = f"%{tu_khoa}%"
            con_tro.execute(query, (search_val, search_val, search_val))
            data = con_tro.fetchall()
            return data
        except Exception as e:
            print(f"Lỗi truy vấn tìm kiếm sách: {str(e)}")
            return []
        finally:
            ket_noi.close()

    def gui_gop_y(self, noi_dung):
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi: return False
        try:
            con_tro = ket_noi.cursor()
            con_tro.execute("INSERT INTO GopY (NoiDung) VALUES (?)", (noi_dung,))
            ket_noi.commit()
            return True
        except Exception as e:
            print(f"Lỗi: {e}")
            return False
        finally:
            ket_noi.close()

# Khởi tạo đối tượng để dùng chung trong toàn ứng dụng
dich_vu_xem_sach = XemSachService()