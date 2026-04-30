from Database.database import db_manager

class DichVuTraSach:
    def __init__(self):
        self.quan_ly_db = db_manager

    def lay_danh_sach_chua_tra(self, ma_sv=None):
        """Lấy sách chưa trả. Nếu có ma_sv thì chỉ lấy sách của SV đó."""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi: return []
        try:
            con_tro = ket_noi.cursor()
            # Câu truy vấn lọc các phiếu mượn chưa nằm trong phiếu trả
            truy_van = """
                SELECT pm.MaPhieuMuon, pm.MaSinhVien, pm.TenSinhVien, s.TenSach, 
                       pm.NgayMuon, pm.HanTra, s.MaSach
                FROM PhieuMuon pm
                JOIN ChiTietPhieuMuon ctp ON pm.MaPhieuMuon = ctp.MaPhieuMuon
                JOIN Sach s ON ctp.MaSach = s.MaSach
                WHERE pm.MaPhieuMuon NOT IN (SELECT MaPhieuMuon FROM PhieuTra)
            """
            
            if ma_sv:
                truy_van += " AND pm.MaSinhVien = ?"
                con_tro.execute(truy_van, (ma_sv,))
            else:
                con_tro.execute(truy_van)
                
            return con_tro.fetchall()
        except Exception as e:
            print(f"Lỗi SQL: {e}")
            return []
        finally:
            ket_noi.close()

    def xac_nhan_tra_sach(self, ma_phieu_muon, ngay_tra, so_ngay_tre, tien_phat):
        """Lưu vào bảng PhieuTra (Trigger trg_CongSachKhiTra sẽ tự động chạy)"""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi: return False, "Lỗi kết nối"
        try:
            con_tro = ket_noi.cursor()
            # Lưu ý: Database của bạn có trigger tự tính tiền phạt, 
            # nhưng truyền từ UI xuống để minh bạch cũng không sao.
            truy_van = "INSERT INTO PhieuTra (MaPhieuMuon, NgayTra, SoNgayTre, TienPhat) VALUES (?, ?, ?, ?)"
            con_tro.execute(truy_van, (ma_phieu_muon, ngay_tra, so_ngay_tre, tien_phat))
            ket_noi.commit()
            return True, "Trả sách thành công! Kho đã cập nhật."
        except Exception as e:
            return False, f"Lỗi: {str(e)}"
        finally:
            ket_noi.close()

    def lay_lich_su_tra_sach(self):
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi: return []
        try:
            con_tro = ket_noi.cursor()
            truy_van = """
                SELECT pt.MaPhieuTra, pm.MaSinhVien, pm.TenSinhVien, s.TenSach, 
                       pm.NgayMuon, pt.NgayTra, pt.SoNgayTre, pt.TienPhat
                FROM PhieuTra pt
                JOIN PhieuMuon pm ON pt.MaPhieuMuon = pm.MaPhieuMuon
                JOIN ChiTietPhieuMuon ctp ON pm.MaPhieuMuon = ctp.MaPhieuMuon
                JOIN Sach s ON ctp.MaSach = s.MaSach
                ORDER BY pt.MaPhieuTra DESC
            """
            con_tro.execute(truy_van)
            return con_tro.fetchall()
        finally:
            ket_noi.close()

dich_vu_tra_sach = DichVuTraSach()