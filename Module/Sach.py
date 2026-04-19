class Sach:
    def __init__(self, 
                 ma_sach=None, 
                 ten_sach="", 
                 tac_gia="", 
                 the_loai="", 
                 so_luong=0, 
                 gia=0.0,
                 nam_xuat_ban="",
                 nha_xuat_ban="",
                 anh_bia=""):
        
        self.ma_sach = ma_sach
        self.ten_sach = ten_sach
        self.tac_gia = tac_gia
        self.the_loai = the_loai
        self.so_luong = so_luong
        self.gia = gia
        self.nam_xuat_ban = nam_xuat_ban
        self.nha_xuat_ban = nha_xuat_ban
        self.anh_bia = anh_bia   # đường dẫn ảnh

    # Hiển thị thông tin
    def __str__(self):
        return f"{self.ten_sach} - {self.tac_gia}"

    # Chuyển object -> dict (lưu DB)
    def to_dict(self):
        return {
            "ma_sach": self.ma_sach,
            "ten_sach": self.ten_sach,
            "tac_gia": self.tac_gia,
            "the_loai": self.the_loai,
            "so_luong": self.so_luong,
            "gia": self.gia,
            "nam_xuat_ban": self.nam_xuat_ban,
            "nha_xuat_ban": self.nha_xuat_ban,
            "anh_bia": self.anh_bia
        }

    # Tạo object từ dict (lấy từ DB)
    @staticmethod
    def from_dict(data):
        return Sach(
            ma_sach=data.get("ma_sach"),
            ten_sach=data.get("ten_sach"),
            tac_gia=data.get("tac_gia"),
            the_loai=data.get("the_loai"),
            so_luong=data.get("so_luong"),
            gia=data.get("gia"),
            nam_xuat_ban=data.get("nam_xuat_ban"),
            nha_xuat_ban=data.get("nha_xuat_ban"),
            anh_bia=data.get("anh_bia")
        )