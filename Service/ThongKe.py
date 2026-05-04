import pyodbc

from Database.database import db_manager



class DichVuThongKe:

    def __init__(self):

        # Sử dụng db_manager chung của hệ thống

        self.quan_ly_db = db_manager



    def lay_data_bieu_do_cot(self, tu_ngay, den_ngay):

        """

        Lấy Top 10 sách được mượn nhiều nhất trong khoảng thời gian từ tu_ngay đến den_ngay.

        Dựa trên cột NgayMuon trong bảng PhieuMuon.

        """

        ket_noi = self.quan_ly_db.get_connection()

        if not ket_noi:

            return []

        try:

            con_tro = ket_noi.cursor()

            # SQL Server: Lọc theo NgayMuon nằm trong khoảng tu_ngay và den_ngay

            query = """

                SELECT TOP 10 s.TenSach, SUM(ctpm.SoLuongMuon) as TongMuon

                FROM Sach s

                JOIN ChiTietPhieuMuon ctpm ON s.MaSach = ctpm.MaSach

                JOIN PhieuMuon pm ON ctpm.MaPhieuMuon = pm.MaPhieuMuon

                WHERE pm.NgayMuon BETWEEN ? AND ?

                GROUP BY s.TenSach

                ORDER BY TongMuon DESC

            """

            con_tro.execute(query, (tu_ngay, den_ngay))

            return con_tro.fetchall()

        except Exception as e:

            print(f"Lỗi truy vấn dữ liệu biểu đồ cột: {e}")

            return []

        finally:

            ket_noi.close()



    def lay_data_bieu_do_tron(self, tu_ngay, den_ngay):

        """

        Lấy thống kê số lượng phiếu trả Đúng hạn và Trễ hạn trong khoảng từ tu_ngay đến den_ngay.

        Dựa trên cột NgayTra trong bảng PhieuTra.

        """

        ket_noi = self.quan_ly_db.get_connection()

        if not ket_noi:

            return {"DungHen": 0, "TreHan": 0}

        try:

            con_tro = ket_noi.cursor()

            # SQL Server: Lọc theo NgayTra nằm trong khoảng tu_ngay và den_ngay

            query = """

                SELECT

                    SUM(CASE WHEN SoNgayTre = 0 THEN 1 ELSE 0 END) AS DungHen,

                    SUM(CASE WHEN SoNgayTre > 0 THEN 1 ELSE 0 END) AS TreHan

                FROM PhieuTra

                WHERE NgayTra BETWEEN ? AND ?

            """

            con_tro.execute(query, (tu_ngay, den_ngay))

            row = con_tro.fetchone()

           

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