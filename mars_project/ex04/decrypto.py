import os
import zipfile
import time
from datetime import datetime
import zlib


class Decrypt:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.passwd_seed = b"abcdefghijklmnopqrstuvwxyz0123456789"
        self.found_passwd = ""
        self.passwd_len = 6
        self.start_time = time.time()
        self.show_info_per_count = 100000
        self.counter = 0
        self.max_try_count = len(self.passwd_seed) ** self.passwd_len

    def get_passwd(self, *args) -> str:
        return "".join(self.passwd_seed[int(x)] for x in args)

    def get_elapsed(self) -> str:
        now = time.time()
        elapsed = now - self.start_time
        return f"{elapsed:.3f} 초 경과"

    def print_info(self):
        if self.counter % self.show_info_per_count == 0:
            print(
                f'시작 시간 {datetime.fromtimestamp(self.start_time).strftime("%Y-%m-%d %H:%M:%S")} 시도횟수 {self.counter} 경과시간 {self.get_elapsed()} 퍼센티지 {(self.counter / self.max_try_count) * 100 : .3f}%'
            )

    def pick_member(self, zf: zipfile.ZipFile):
        for info in zf.infolist():
            if not info.is_dir():
                return info
        raise ValueError("Error : ther is no file in zip!")

    def save_password(self):
        saved_path = os.path.join(self.base_path, "passwd.txt")
        try:
            with open(saved_path, "w", encoding="utf-8") as f:
                f.write(self.found_passwd)
        except Exception as e:
            print(f"error : {e}")

    def do_brutforce(self) -> str:
        zip_file_path = os.path.join(self.base_path, "emergency_storage_key.zip")
        with zipfile.ZipFile(zip_file_path, "r") as zf:
            member = self.pick_member(zf)
            seed = self.passwd_seed
            a36 = len(seed)
            for i0 in range(a36):
                c0 = seed[i0]
                for i1 in range(a36):
                    c1 = seed[i1]
                    for i2 in range(a36):
                        c2 = seed[i2]
                        for i3 in range(a36):
                            c3 = seed[i3]
                            for i4 in range(a36):
                                c4 = seed[i4]
                                for i5 in range(a36):
                                    c5 = seed[i5]
                                    passwd_bytes = bytes((c0, c1, c2, c3, c4, c5))
                                    # print(passwd_bytes.decode("utf-8"))
                                    try:
                                        self.counter += 1
                                        with zf.open(
                                            member,
                                            "r",
                                            pwd=passwd_bytes,
                                        ) as f:
                                            byte = f.read(1)
                                            self.print_info()
                                            self.found_passwd = passwd_bytes.decode(
                                                "utf-8"
                                            )
                                            return self.found_passwd
                                    except (
                                        RuntimeError,
                                        zipfile.BadZipFile,
                                        zipfile.LargeZipFile,
                                        zlib.error,
                                    ):
                                        self.print_info()
                                        continue
        return "can't found passwd"
