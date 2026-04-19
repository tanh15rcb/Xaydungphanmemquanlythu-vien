class ThuThu:
    def __init__(self,
                 ma_thu_thu=None,
                 ho_ten="",
                 gioi_tinh="",
                 ngay_sinh="",
                 so_dien_thoai="",
                 email="",
                 dia_chi="",
                 chuc_vu="Thu thu",
                 luong=0.0):
        
        self.ma_thu_thu = ma_thu_thu
        self.ho_ten = ho_ten
        self.gioi_tinh = gioi_tinh
        self.ngay_sinh = ngay_sinh
        self.so_dien_thoai = so_dien_thoai
        self.email = email
        self.dia_chi = dia_chi
        self.chuc_vu = chuc_vu
        self.luong = luong

    # Hiển thị thông tin
    def __str__(self):
        return f"{self.ho_ten} - {self.chuc_vu}"

    # Convert object -> dict
    def to_dict(self):
        return {
            "ma_thu_thu": self.ma_thu_thu,
            "ho_ten": self.ho_ten,
            "gioi_tinh": self.gioi_tinh,
            "ngay_sinh": self.ngay_sinh,
            "so_dien_thoai": self.so_dien_thoai,
            "email": self.email,
            "dia_chi": self.dia_chi,
            "chuc_vu": self.chuc_vu,
            "luong": self.luong
        }

    # Tạo object từ dict
    @staticmethod
    def from_dict(data):
        return ThuThu(
            ma_thu_thu=data.get("ma_thu_thu"),
            ho_ten=data.get("ho_ten"),
            gioi_tinh=data.get("gioi_tinh"),
            ngay_sinh=data.get("ngay_sinh"),
            so_dien_thoai=data.get("so_dien_thoai"),
            email=data.get("email"),
            dia_chi=data.get("dia_chi"),
            chuc_vu=data.get("chuc_vu"),
            luong=data.get("luong")
        )