import pyodbc
from Database.database import db_manager

class QuanLyGopYService:
    def __init__(self):
        self.quan_ly_db = db_manager

    def lay_danh_sach_gop_y(self):
        """Lấy toàn bộ danh sách góp ý để Admin xem"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return []

        try:
            con_tro = ket_noi.cursor()
            query = "SELECT MaGopY, NoiDung, ThoiGian FROM GopY ORDER BY ThoiGian DESC"
            con_tro.execute(query)
            return con_tro.fetchall()
        except Exception as e:
            print(f"Lỗi lấy danh sách góp ý: {str(e)}")
            return []
        finally:
            ket_noi.close()

dich_vu_quan_ly_gop_y = QuanLyGopYService()