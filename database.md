/* =========================================
   TẠO DATABASE
========================================= */

CREATE DATABASE QuanLyThuVien
GO

USE QuanLyThuVien
GO


/* =========================================
   BẢNG SÁCH
========================================= */

CREATE TABLE Sach
(
    MaSach INT IDENTITY(1,1) PRIMARY KEY,

    TenSach NVARCHAR(200) NOT NULL,

    TheLoai NVARCHAR(100),

    TacGia NVARCHAR(150),

    NhaXuatBan NVARCHAR(150),

    NamXuatBan INT,

    SoLuong INT DEFAULT 0
)
GO


/* =========================================
   BẢNG NHÀ CUNG CẤP
========================================= */

CREATE TABLE NhaCungCap
(
    MaNCC INT IDENTITY(1,1) PRIMARY KEY,

    TenNCC NVARCHAR(200) NOT NULL,

    DiaChi NVARCHAR(200),

    DienThoai VARCHAR(15),

    Email VARCHAR(100)
)
GO


/* =========================================
   BẢNG NHÂN VIÊN
========================================= */

CREATE TABLE NhanVien
(
    MaNhanVien INT IDENTITY(1,1) PRIMARY KEY,

    TenNhanVien NVARCHAR(150) NOT NULL,

    GioiTinh NVARCHAR(10),

    DienThoai VARCHAR(15),

    Email VARCHAR(100),

    DiaChi NVARCHAR(200)
)
GO


/* =========================================
   BẢNG USERS (ĐĂNG NHẬP)
========================================= */

CREATE TABLE Users
(
    MaUser INT IDENTITY(1,1) PRIMARY KEY,

    TenDangNhap VARCHAR(50) UNIQUE NOT NULL,

    MatKhau VARCHAR(100) NOT NULL,

    Role VARCHAR(20) NOT NULL,

    MaNhanVien INT,

    FOREIGN KEY (MaNhanVien)
    REFERENCES NhanVien(MaNhanVien)
)
GO


/* Chỉ cho phép Admin hoặc NhanVien */

ALTER TABLE Users
ADD CONSTRAINT chk_Role
CHECK (Role IN ('Admin', 'NhanVien'))
GO


/* =========================================
   BẢNG PHIẾU NHẬP
========================================= */

CREATE TABLE PhieuNhap
(
    MaPhieuNhap INT IDENTITY(1,1) PRIMARY KEY,

    MaNCC INT,

    NgayNhap DATE DEFAULT GETDATE(),

    FOREIGN KEY (MaNCC)
    REFERENCES NhaCungCap(MaNCC)
)
GO


/* =========================================
   CHI TIẾT PHIẾU NHẬP
========================================= */

CREATE TABLE ChiTietPhieuNhap
(
    MaCTPN INT IDENTITY(1,1) PRIMARY KEY,

    MaPhieuNhap INT,

    MaSach INT,

    SoLuongNhap INT,

    GiaNhap DECIMAL(10,2),

    FOREIGN KEY (MaPhieuNhap)
    REFERENCES PhieuNhap(MaPhieuNhap),

    FOREIGN KEY (MaSach)
    REFERENCES Sach(MaSach)
)
GO


/* =========================================
   PHIẾU MƯỢN
========================================= */

CREATE TABLE PhieuMuon
(
    MaPhieuMuon INT IDENTITY(1,1) PRIMARY KEY,

    MaSinhVien VARCHAR(20) NOT NULL,

    TenSinhVien NVARCHAR(150),

    MaNhanVien INT,

    NgayMuon DATE DEFAULT GETDATE(),

    HanTra DATE,

    FOREIGN KEY (MaNhanVien)
    REFERENCES NhanVien(MaNhanVien)
)
GO


/* =========================================
   CHI TIẾT PHIẾU MƯỢN
========================================= */

CREATE TABLE ChiTietPhieuMuon
(
    MaCTPM INT IDENTITY(1,1) PRIMARY KEY,

    MaPhieuMuon INT,

    MaSach INT,

    SoLuongMuon INT,

    FOREIGN KEY (MaPhieuMuon)
    REFERENCES PhieuMuon(MaPhieuMuon),

    FOREIGN KEY (MaSach)
    REFERENCES Sach(MaSach)
)
GO


/* =========================================
   PHIẾU TRẢ
========================================= */

CREATE TABLE PhieuTra
(
    MaPhieuTra INT IDENTITY(1,1) PRIMARY KEY,

    MaPhieuMuon INT,

    NgayTra DATE DEFAULT GETDATE(),

    SoNgayTre INT DEFAULT 0,

    TienPhat DECIMAL(10,2) DEFAULT 0,

    FOREIGN KEY (MaPhieuMuon)
    REFERENCES PhieuMuon(MaPhieuMuon)
)
GO


/* =========================================
   TRIGGER TĂNG SÁCH KHI NHẬP
========================================= */

CREATE TRIGGER trg_CongSachNhap
ON ChiTietPhieuNhap
AFTER INSERT
AS
BEGIN
    UPDATE Sach
    SET SoLuong = SoLuong + i.SoLuongNhap
    FROM Sach s
    JOIN inserted i
    ON s.MaSach = i.MaSach
END
GO


/* =========================================
   ⚠️ KHÔNG CHO MƯỢN KHI HẾT SÁCH
========================================= */

CREATE TRIGGER trg_KiemTraSoLuongSach
ON ChiTietPhieuMuon
INSTEAD OF INSERT
AS
BEGIN

    IF EXISTS
    (
        SELECT *
        FROM inserted i
        JOIN Sach s
        ON i.MaSach = s.MaSach
        WHERE s.SoLuong < i.SoLuongMuon
    )
    BEGIN
        PRINT N'Không đủ số lượng sách để mượn!'
        RETURN
    END

    INSERT INTO ChiTietPhieuMuon
    (
        MaPhieuMuon,
        MaSach,
        SoLuongMuon
    )
    SELECT
        MaPhieuMuon,
        MaSach,
        SoLuongMuon
    FROM inserted


    UPDATE Sach
    SET SoLuong = SoLuong - i.SoLuongMuon
    FROM Sach s
    JOIN inserted i
    ON s.MaSach = i.MaSach

END
GO


/* =========================================
   CỘNG SÁCH KHI TRẢ
========================================= */

CREATE TRIGGER trg_CongSachKhiTra
ON PhieuTra
AFTER INSERT
AS
BEGIN
    UPDATE Sach
    SET SoLuong = SoLuong + ctp.SoLuongMuon
    FROM Sach s
    JOIN ChiTietPhieuMuon ctp
        ON s.MaSach = ctp.MaSach
    JOIN inserted i
        ON ctp.MaPhieuMuon = i.MaPhieuMuon
END
GO


/* =========================================
   TÍNH TIỀN PHẠT TRẢ MUỘN
   2000đ / ngày
========================================= */

CREATE TRIGGER trg_TinhTienPhat
ON PhieuTra
AFTER INSERT
AS
BEGIN

    UPDATE pt
    SET 
        SoNgayTre =
            CASE
                WHEN DATEDIFF(DAY, pm.HanTra, pt.NgayTra) > 0
                THEN DATEDIFF(DAY, pm.HanTra, pt.NgayTra)
                ELSE 0
            END,

        TienPhat =
            CASE
                WHEN DATEDIFF(DAY, pm.HanTra, pt.NgayTra) > 0
                THEN DATEDIFF(DAY, pm.HanTra, pt.NgayTra) * 2000
                ELSE 0
            END

    FROM PhieuTra pt
    JOIN inserted i
        ON pt.MaPhieuTra = i.MaPhieuTra
    JOIN PhieuMuon pm
        ON pt.MaPhieuMuon = pm.MaPhieuMuon

END
GO


/* =========================================
   DỮ LIỆU MẪU
========================================= */

INSERT INTO Sach
(
TenSach,
TheLoai,
TacGia,
NhaXuatBan,
NamXuatBan,
SoLuong
)
VALUES
(
N'Lập trình Python',
N'Công nghệ thông tin',
N'Nguyễn Văn A',
N'NXB Giáo Dục',
2023,
10
)


INSERT INTO NhanVien
(
TenNhanVien,
GioiTinh,
DienThoai,
Email,
DiaChi
)
VALUES
(
N'Nguyễn Văn Nam',
N'Nam',
'0123456789',
'nam@gmail.com',
N'Hà Nội'
)


INSERT INTO Users
(
TenDangNhap,
MatKhau,
Role,
MaNhanVien
)
VALUES
(
'admin',
'123',
'Admin',
'1'
)
GO

/* =========================================
   BẢNG GÓP Ý (ẨN DANH)
========================================= */

CREATE TABLE GopY
(
    MaGopY INT IDENTITY(1,1) PRIMARY KEY, -- ID tự tăng
    
    NoiDung NVARCHAR(MAX) NOT NULL,        -- Nội dung góp ý
    
    ThoiGian DATETIME DEFAULT GETDATE()    -- Tự động ghi lại ngày giờ gửi
)
GO

/* =========================================
   DỮ LIỆU MẪU
========================================= */

INSERT INTO GopY (NoiDung)
VALUES 
(N'Giao diện rất dễ sử dụng.'),
(N'Thư viện nên bổ sung thêm sách ngoại văn.'),
(N'Hệ thống phản hồi rất nhanh.')
GO