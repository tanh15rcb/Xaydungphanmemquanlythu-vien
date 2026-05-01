import pyodbc
from Database.database import db_manager

class DichVuNhapHang:
    def __init__(self):
        # Sử dụng db_manager đã cấu hình kết nối localhost\SQLEXPRESS
        self.quan_ly_db = db_manager

    def lay_danh_sach_ncc(self):
        """Lấy danh sách tên nhà cung cấp để hiển thị lên ComboBox."""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi: return []
        try:
            con_tro = ket_noi.cursor()
            con_tro.execute("SELECT TenNCC FROM NhaCungCap")
            return [dong[0] for dong in con_tro.fetchall()]
        except:
            return []
        finally:
            ket_noi.close()

    def lay_danh_sach_ten_sach(self):
        """Lấy danh sách tên sách đã tồn tại để gợi ý (AutoComplete)."""
        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi: return []
        try:
            con_tro = ket_noi.cursor()
            con_tro.execute("SELECT TenSach FROM Sach")
            return [dong[0] for dong in con_tro.fetchall()]
        except:
            return []
        finally:
            ket_noi.close()

    def xac_nhan_nhap_kho(self, ten_ncc, danh_sach_hang):
        """
        Xử lý nghiệp vụ nhập hàng vào database.
        danh_sach_hang: List các dict [{'ten_sach':..., 'so_luong':..., 'gia_nhap':...}]
        """
        if not ten_ncc or ten_ncc == "-- Chọn Nhà Cung Cấp --":
            return {"ket_qua": "loi", "noi_dung": "Vui lòng chọn nhà cung cấp!"}
        
        if not danh_sach_hang:
            return {"ket_qua": "loi", "noi_dung": "Danh sách hàng nhập trống!"}

        ket_noi = self.quan_ly_db.get_connection()
        if not ket_noi:
            return {"ket_qua": "loi", "noi_dung": "Không thể kết nối đến SQL Server"}

        try:
            con_tro = ket_noi.cursor()
            
            # 1. Tìm MaNCC từ tên đã chọn
            con_tro.execute("SELECT MaNCC FROM NhaCungCap WHERE TenNCC = ?", (ten_ncc,))
            dong_ncc = con_tro.fetchone()
            if not dong_ncc:
                return {"ket_qua": "loi", "noi_dung": "Nhà cung cấp không tồn tại"}
            ma_ncc = dong_ncc[0]

            # 2. Tạo phiếu nhập mới (Dùng OUTPUT để lấy ID vừa tạo)
            truy_van_phieu = "INSERT INTO PhieuNhap (MaNCC, NgayNhap) OUTPUT INSERTED.MaPhieuNhap VALUES (?, GETDATE())"
            con_tro.execute(truy_van_phieu, (ma_ncc,))
            ma_phieu = con_tro.fetchone()[0]

            # 3. Duyệt danh sách hàng để lưu chi tiết
            for hang in danh_sach_hang:
                # Tìm MaSach theo tên
                con_tro.execute("SELECT MaSach FROM Sach WHERE TenSach = ?", (hang['ten_sach'],))
                dong_sach = con_tro.fetchone()
                
                if dong_sach:
                    ma_sach = dong_sach[0]
                else:
                    # Nếu sách mới hoàn toàn, thêm vào bảng Sach trước (các thông tin khác để NULL hoặc mặc định)
                    truy_van_sach_moi = "INSERT INTO Sach (TenSach, SoLuong) OUTPUT INSERTED.MaSach VALUES (?, 0)"
                    con_tro.execute(truy_van_sach_moi, (hang['ten_sach'],))
                    ma_sach = con_tro.fetchone()[0]

                # Lưu ChiTietPhieuNhap (Trigger trg_CongSachNhap trong SQL sẽ tự cộng tồn kho)
                truy_van_ctpn = """
                    INSERT INTO ChiTietPhieuNhap (MaPhieuNhap, MaSach, SoLuongNhap, GiaNhap)
                    VALUES (?, ?, ?, ?)
                """
                con_tro.execute(truy_van_ctpn, (ma_phieu, ma_sach, hang['so_luong'], hang['gia_nhap']))

            ket_noi.commit()
            return {
                "ket_qua": "thanh_cong", 
                "noi_dung": f"Đã nhập kho thành công! Mã phiếu: {ma_phieu}",
                "ma_phieu": ma_phieu
            }

        except Exception as e:
            ket_noi.rollback()
            return {"ket_qua": "loi_he_thong", "noi_dung": f"Lỗi hệ thống: {str(e)}"}
        finally:
            ket_noi.close()

# Khởi tạo đối tượng để sử dụng
dich_vu_nhap_hang = DichVuNhapHang()