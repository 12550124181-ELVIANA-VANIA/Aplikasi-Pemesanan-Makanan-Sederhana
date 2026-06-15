from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum


# =========================
# ENUM
# =========================

class StatusPesanan(Enum):
    MENUNGGU = "Menunggu"
    DIPROSES = "Diproses"
    SELESAI = "Selesai"


class StatusPembayaran(Enum):
    BELUM_BAYAR = "Belum Bayar"
    LUNAS = "Lunas"


# =========================
# MIXIN
# =========================

class LoggingMixin:
    def logActivity(self, msg):
        print(f"[LOG] {msg}")


class TimestampMixin:
    def __init__(self):
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()


# =========================
# USER (ABC)
# =========================

class User(ABC):
    def __init__(self, idUser, username, password):
        self.idUser = idUser
        self.username = username
        self.password = password

    def login(self):
        print(f"\n{self.username} berhasil login")
        return True

    def logout(self):
        print(f"{self.username} berhasil logout")


# =========================
# PELANGGAN
# =========================

class Pelanggan(User):
    def __init__(self, idUser, username, password,
                 noHp, alamat):

        super().__init__(
            idUser,
            username,
            password
        )

        self.noHp = noHp
        self.alamat = alamat

    def buatPesanan(self):
        return Pesanan()


# =========================
# MEMBER
# =========================

class Member(Pelanggan):
    def __init__(self,
                 idUser,
                 username,
                 password,
                 noHp,
                 alamat,
                 poin=0):

        super().__init__(
            idUser,
            username,
            password,
            noHp,
            alamat
        )

        self.poin = poin

    def tambahPoin(self, nilai):
        self.poin += nilai


# =========================
# MENU
# =========================

class Menu:
    def __init__(self,
                 idMenu,
                 nama,
                 harga,
                 deskripsi,
                 stok):

        self.idMenu = idMenu
        self.nama = nama
        self.harga = harga
        self.deskripsi = deskripsi
        self.stok = stok

    def kurangiStok(self, qty):
        self.stok -= qty

    def tambahStok(self, qty):
        self.stok += qty


# =========================
# ITEM KERANJANG
# =========================

class ItemKeranjang:
    def __init__(self, menu, qty):
        self.menu = menu
        self.qty = qty
        self.subtotal = self.hitungSubtotal()

    def hitungSubtotal(self):
        return self.menu.harga * self.qty


# =========================
# KERANJANG
# =========================

class Keranjang:
    def __init__(self, idKeranjang):
        self.idKeranjang = idKeranjang
        self.tanggal = datetime.now()
        self.daftarItem = []

    def tambah(self, menu, qty):
        item = ItemKeranjang(menu, qty)
        self.daftarItem.append(item)

    def hitungTotal(self):
        total = 0

        for item in self.daftarItem:
            total += item.subtotal

        return total


# =========================
# DETAIL PESANAN
# =========================

class DetailPesanan:
    def __init__(self, menu, qty):
        self.menu = menu
        self.qty = qty
        self.subtotal = self.hitungSubtotal()

    def hitungSubtotal(self):
        return self.menu.harga * self.qty


# =========================
# PESANAN
# =========================

class Pesanan(LoggingMixin, TimestampMixin):

    jumlahPesanan = 0

    def __init__(self):
        TimestampMixin.__init__(self)

        Pesanan.jumlahPesanan += 1

        self.idPesanan = f"PSN{Pesanan.jumlahPesanan:03d}"
        self.tanggal = datetime.now()
        self.status = StatusPesanan.MENUNGGU
        self.total = 0
        self.detailPesanan = []

    def tambahItem(self, menu, qty):

        detail = DetailPesanan(menu, qty)

        self.detailPesanan.append(detail)

        self.total = self.hitungTotal()

        self.logActivity(
            f"Menambahkan {qty} x {menu.nama}"
        )

    def hitungTotal(self):

        total = 0

        for item in self.detailPesanan:
            total += item.subtotal

        return total

    def ubahStatus(self, status):
        self.status = status

    # Operator Overloading

    def __str__(self):
        return (
            f"Pesanan {self.idPesanan} | "
            f"Total = Rp{self.total}"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.total == other.total

    def __lt__(self, other):
        return self.total < other.total

    def __add__(self, other):
        return self.total + other.total

    def __len__(self):
        return len(self.detailPesanan)


# =========================
# PEMBAYARAN (ABC)
# =========================

class Pembayaran(ABC):

    def __init__(self, total):
        self.total = total
        self.status = StatusPembayaran.BELUM_BAYAR

    @abstractmethod
    def pay(self):
        pass


# =========================
# CASH
# =========================

class Cash(Pembayaran):

    def __init__(self, total, uangDiterima):
        super().__init__(total)

        self.uangDiterima = uangDiterima
        self.kembalian = 0

    def pay(self):

        if self.uangDiterima >= self.total:

            self.kembalian = (
                self.uangDiterima - self.total
            )

            self.status = StatusPembayaran.LUNAS

            return True

        return False


# =========================
# TRANSFER
# =========================

class Transfer(Pembayaran):

    def __init__(self,
                 total,
                 bank,
                 noRekening):

        super().__init__(total)

        self.bank = bank
        self.noRekening = noRekening

    def pay(self):
        self.status = StatusPembayaran.LUNAS
        return True


# =========================
# PROGRAM UTAMA
# =========================

if __name__ == "__main__":

    print("=" * 40)
    print("SISTEM PEMESANAN MAKANAN")
    print("=" * 40)

    # LOGIN

    idUser = input("ID User       : ")
    username = input("Username      : ")
    password = input("Password      : ")
    noHp = input("No HP         : ")
    alamat = input("Alamat        : ")

    member = Member(
        idUser,
        username,
        password,
        noHp,
        alamat
    )

    member.login()

    # MENU

    menu1 = Menu(
        "M001",
        "Nasi Goreng",
        20000,
        "Nasi Goreng Spesial",
        20
    )

    menu2 = Menu(
        "M002",
        "Mie Goreng",
        18000,
        "Mie Goreng Pedas",
        15
    )

    menu3 = Menu(
        "M003",
        "Es Teh",
        5000,
        "Minuman Dingin",
        30
    )

    pesanan = member.buatPesanan()

    while True:

        print("\n===== DAFTAR MENU =====")
        print("1. Nasi Goreng  - Rp20.000")
        print("2. Mie Goreng   - Rp18.000")
        print("3. Es Teh       - Rp5.000")
        print("0. Selesai")

        pilihan = input("Pilih menu : ")

        if pilihan == "0":
            break

        qty = int(input("Jumlah : "))

        if pilihan == "1":
            pesanan.tambahItem(menu1, qty)

        elif pilihan == "2":
            pesanan.tambahItem(menu2, qty)

        elif pilihan == "3":
            pesanan.tambahItem(menu3, qty)

        else:
            print("Menu tidak tersedia")

    print("\n" + "=" * 30)
    print("DETAIL PESANAN")
    print("=" * 30)

    print("ID Pesanan :", pesanan.idPesanan)
    print(
        "Tanggal    :",
        pesanan.tanggal.strftime("%d-%m-%Y %H:%M:%S")
    )

    for item in pesanan.detailPesanan:

        print(
            f"{item.menu.nama} x {item.qty}"
            f" = Rp{item.subtotal}"
        )

    print("-" * 30)
    print("Total Bayar :", pesanan.total)

    print("\nOperator Overloading")
    print(pesanan)
    print("Jumlah item :", len(pesanan))

    print("\nMetode Pembayaran")
    print("1. Cash")
    print("2. Transfer")

    metode = input("Pilih : ")

    if metode == "1":

        uang = int(
            input("Masukkan uang pembayaran : ")
        )

        pembayaran = Cash(
            pesanan.total,
            uang
        )

        if pembayaran.pay():

            print("Pembayaran berhasil")
            print(
                "Kembalian :",
                pembayaran.kembalian
            )

        else:
            print("Uang tidak cukup")

    elif metode == "2":

        bank = input("Nama Bank : ")
        rekening = input("No Rekening : ")

        pembayaran = Transfer(
            pesanan.total,
            bank,
            rekening
        )

        pembayaran.pay()

        print("Transfer berhasil")
        print(
            "Status :",
            pembayaran.status.value
        )

    pesanan.ubahStatus(
        StatusPesanan.SELESAI
    )

    print(
        "\nStatus Pesanan :",
        pesanan.status.value
    )

    member.logout()