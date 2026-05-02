import pyodbc
from Database.database import db_manager

class DichVuThongKe:
    def __init__(self):
        # Sử dụng db_manager chung của hệ thống
        self.quan_ly_db = db_manager

    def lay_data_bieu_do_cot(self):
        """
        Lấy Top 10 sách được mượn nhiều nhất.
        Kết nối: Sach -> ChiTietPhieuMuon.
        """
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi: 
            return []
        try:
            con_tro = ket_noi.cursor()
            # SQL Server: Lấy Top 10 sách dựa trên tổng lượng mượn
            query = """
                SELECT TOP 10 s.TenSach, SUM(ctpm.SoLuongMuon) as TongMuon
                FROM Sach s
                JOIN ChiTietPhieuMuon ctpm ON s.MaSach = ctpm.MaSach
                GROUP BY s.TenSach
                ORDER BY TongMuon DESC
            """
            con_tro.execute(query)
            # Trả về list các tuple: [('Sách A', 15), ('Sách B', 12),...]
            return con_tro.fetchall()
        except Exception as e:
            print(f"Lỗi truy vấn dữ liệu biểu đồ cột: {e}")
            return []
        finally:
            ket_noi.close()

    def lay_data_bieu_do_tron(self):
        """
        Lấy thống kê số lượng phiếu trả Đúng hạn và Trễ hạn.
        Dựa vào cột SoNgayTre trong bảng PhieuTra.
        """
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return {"DungHen": 0, "TreHan": 0}
        try:
            con_tro = ket_noi.cursor()
            # Đếm số dòng đúng hạn (SoNgayTre = 0) và trễ (> 0)
            query = """
                SELECT 
                    SUM(CASE WHEN SoNgayTre = 0 THEN 1 ELSE 0 END) AS DungHen,
                    SUM(CASE WHEN SoNgayTre > 0 THEN 1 ELSE 0 END) AS TreHan
                FROM PhieuTra
            """
            con_tro.execute(query)
            row = con_tro.fetchone()
            
            # Xử lý trường hợp database chưa có dữ liệu (trả về 0 thay vì None)
            return {
                "DungHen": row[0] if row and row[0] else 0,
                "TreHan": row[1] if row and row[1] else 0
            }
        except Exception as e:
            print(f"Lỗi truy vấn dữ liệu biểu đồ tròn: {e}")
            return {"DungHen": 0, "TreHan": 0}
        finally:
            ket_noi.close()

# Khởi tạo instance để các file khác (như main.py) có thể import và dùng ngay
dich_vu_tk = DichVuThongKe()