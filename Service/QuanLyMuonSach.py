import pyodbc
from Database.database import db_manager
from datetime import datetime

class DichVuMuonSach:
    def __init__(self):
        self.quan_ly_db = db_manager

    def lay_danh_sach_muon(self):
        """Lấy danh sách mượn bằng cách JOIN bảng PhieuMuon và ChiTietPhieuMuon"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi: return []
        try:
            con_tro = ket_noi.cursor()
            # Sửa lại truy vấn JOIN để lấy dữ liệu từ cấu trúc bảng mới
            truy_van = """
                SELECT pm.MaSinhVien, pm.TenSinhVien, s.TenSach, ct.SoLuongMuon, pm.NgayMuon, pm.HanTra 
                FROM PhieuMuon pm
                JOIN ChiTietPhieuMuon ct ON pm.MaPhieuMuon = ct.MaPhieuMuon
                JOIN Sach s ON ct.MaSach = s.MaSach
                ORDER BY pm.NgayMuon DESC
            """
            con_tro.execute(truy_van)
            return con_tro.fetchall()
        except Exception as e:
            print(f"Lỗi lấy danh sách mượn: {e}")
            return []
        finally:
            ket_noi.close()

    def lay_tat_ca_ten_sach(self):
        """Lấy danh sách tên sách để phục vụ QCompleter"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi: return []
        try:
            con_tro = ket_noi.cursor()
            con_tro.execute("SELECT TenSach FROM Sach WHERE SoLuong > 0")
            return [row[0] for row in con_tro.fetchall()]
        except Exception as e:
            print(f"Lỗi lấy tên sách: {e}")
            return []
        finally:
            ket_noi.close()

    def cho_muon_sach(self, ma_sv, ho_ten, ten_sach, so_luong, han_tra):
        """Thực hiện lưu phiếu mượn vào 2 bảng và trừ số lượng (thông qua Trigger)"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi: return False, "Lỗi kết nối DB"
        try:
            con_tro = ket_noi.cursor()
            
            # 1. Tìm MaSach dựa trên TenSach
            con_tro.execute("SELECT MaSach FROM Sach WHERE TenSach = ?", (ten_sach,))
            result = con_tro.fetchone()
            if not result:
                return False, "Sách không tồn tại trong hệ thống!"
            ma_sach = result[0]

            # 2. Thêm vào bảng PhieuMuon (Khớp cột: MaSinhVien, TenSinhVien)
            # MaNhanVien tạm thời để 1 (Admin) theo dữ liệu mẫu của bạn
            truy_van_muon = """
                INSERT INTO PhieuMuon (MaSinhVien, TenSinhVien, MaNhanVien, NgayMuon, HanTra)
                OUTPUT INSERTED.MaPhieuMuon
                VALUES (?, ?, 1, GETDATE(), ?)
            """
            con_tro.execute(truy_van_muon, (ma_sv, ho_ten, han_tra))
            ma_phieu_vua_tao = con_tro.fetchone()[0]
            
            # 3. Thêm vào bảng ChiTietPhieuMuon (Khớp cột: SoLuongMuon)
            # Lưu ý: Trigger trg_KiemTraSoLuongSach trong SQL của bạn sẽ tự trừ số lượng ở bảng Sach
            truy_van_chi_tiet = """
                INSERT INTO ChiTietPhieuMuon (MaPhieuMuon, MaSach, SoLuongMuon)
                VALUES (?, ?, ?)
            """
            con_tro.execute(truy_van_chi_tiet, (ma_phieu_vua_tao, ma_sach, so_luong))

            ket_noi.commit()
            return True, "Cho mượn sách thành công!"
        except Exception as e:
            ket_noi.rollback()
            # Xử lý lỗi từ Trigger (ví dụ: Không đủ số lượng sách)
            error_msg = str(e)
            if "Không đủ số lượng sách" in error_msg:
                return False, "Lỗi: Không đủ số lượng sách trong kho!"
            return False, f"Lỗi: {error_msg}"
        finally:
            ket_noi.close()

    def tim_kiem_tong_hop(self, tu_khoa):
        """Tìm kiếm kết hợp trên cấu trúc bảng mới"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi: return []
        try:
            con_tro = ket_noi.cursor()
            truy_van = """
                SELECT pm.MaSinhVien, pm.TenSinhVien, s.TenSach, ct.SoLuongMuon, pm.NgayMuon, pm.HanTra 
                FROM PhieuMuon pm
                JOIN ChiTietPhieuMuon ct ON pm.MaPhieuMuon = ct.MaPhieuMuon
                JOIN Sach s ON ct.MaSach = s.MaSach
                WHERE pm.MaSinhVien LIKE ? OR pm.TenSinhVien LIKE ? OR s.TenSach LIKE ?
            """
            pattern = f"%{tu_khoa}%"
            con_tro.execute(truy_van, (pattern, pattern, pattern))
            return con_tro.fetchall()
        except Exception as e:
            print(f"Lỗi tìm kiếm: {e}")
            return []
        finally:
            ket_noi.close()

dich_vu_muon_sach = DichVuMuonSach()