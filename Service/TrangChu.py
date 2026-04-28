import pyodbc
from Database.database import db_manager

class DichVuTrangChu:
    def __init__(self):
        # Sử dụng db_manager đã cấu hình kết nối localhost\SQLEXPRESS
        self.quan_ly_db = db_manager

    def lay_thong_ke_tong_hop(self):
        """
        Lấy số liệu cho các thẻ thống kê: Tổng sách, Đang mượn, Quá hạn.
        """
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return None

        try:
            con_tro = ket_noi.cursor()
            
            # 1. Tổng số lượng sách (từ cột SoLuong bảng Sach)
            con_tro.execute("SELECT SUM(SoLuong) FROM Sach")
            tong_sach = con_tro.fetchone()[0] or 0

            # 2. Sách đang mượn (Số lượng trong CT mượn mà chưa có trong phiếu trả)
            query_dang_muon = """
                SELECT SUM(ct.SoLuongMuon) 
                FROM ChiTietPhieuMuon ct
                WHERE ct.MaPhieuMuon NOT IN (SELECT MaPhieuMuon FROM PhieuTra)
            """
            con_tro.execute(query_dang_muon)
            dang_muon = con_tro.fetchone()[0] or 0

            # 3. Sách quá hạn (Phiếu mượn có HanTra < hiện tại và chưa trả)
            query_qua_han = """
                SELECT COUNT(DISTINCT MaPhieuMuon) 
                FROM PhieuMuon 
                WHERE HanTra < GETDATE() 
                AND MaPhieuMuon NOT IN (SELECT MaPhieuMuon FROM PhieuTra)
            """
            con_tro.execute(query_qua_han)
            qua_han = con_tro.fetchone()[0] or 0

            return {
                "tong_sach": tong_sach,
                "dang_muon": dang_muon,
                "qua_han": qua_han
            }
        except Exception as e:
            print(f"Lỗi truy vấn thống kê: {str(e)}")
            return None
        finally:
            ket_noi.close()

    def lay_danh_sach_muon_moi(self):
        """
        Lấy dữ liệu cho bảng tableMuonSach (ID, Mã phiếu mượn, Mã sách, Số lượng).
        """
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return []

        try:
            con_tro = ket_noi.cursor()
            
            # Lấy thông tin từ bảng ChiTietPhieuMuon
            # MaCTPM (ID), MaPhieuMuon, MaSach, SoLuongMuon
            truy_van = """
                SELECT TOP 50 MaCTPM, MaPhieuMuon, MaSach, SoLuongMuon 
                FROM ChiTietPhieuMuon 
                ORDER BY MaCTPM DESC
            """
            
            con_tro.execute(truy_van)
            danh_sach = con_tro.fetchall()
            return danh_sach

        except Exception as e:
            print(f"Lỗi truy vấn danh sách mượn: {str(e)}")
            return []
        finally:
            ket_noi.close()

# Khởi tạo đối tượng để sử dụng
dich_vu_trang_chu = DichVuTrangChu()