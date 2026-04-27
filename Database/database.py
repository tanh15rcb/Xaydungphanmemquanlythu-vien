import pyodbc

class DatabaseConnection:
    def __init__(self):
        # Cập nhật Server Name chính xác từ hình ảnh của bạn
        self.server = 'localhost\\SQLEXPRESS' 
        self.database = 'QuanLyThuVien'
        # Driver phổ biến nhất hiện nay
        self.driver = '{ODBC Driver 17 for SQL Server}'
        
    def get_connection(self):
        """Thiết lập kết nối sử dụng Windows Authentication"""
        conn_str = (
            f'DRIVER={self.driver};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'Trusted_Connection=yes;' # Tương ứng với Windows Authentication
        )
        
        try:
            conn = pyodbc.connect(conn_str)
            print("Kết nối SQL Server thành công!")
            return conn
        except pyodbc.Error as e:
            # Nếu Driver 17 chưa cài, thử dùng Driver cũ có sẵn trong Windows
            try:
                print("Đang thử lại với Driver SQL Server mặc định...")
                conn_str_alt = conn_str.replace(self.driver, '{SQL Server}')
                return pyodbc.connect(conn_str_alt)
            except:
                print(f"Lỗi kết nối: {e}")
                return None

# Khởi tạo đối tượng dùng chung cho các Service
db_manager = DatabaseConnection()