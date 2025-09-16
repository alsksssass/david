import os
import zipfile
import time
from datetime import datetime
import zlib
from multiprocessing import Process, Event
import mmap


class Decrypt:
    def __init__(self):
        self.cpu_cores = os.cpu_count() or 6
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.passwd_seed = b"abcdefghijklmnopqrstuvwxyz0123456789"
        self.base = len(self.passwd_seed)
        self.found_passwd = ""
        self.passwd_len = 6
        self.start_time = time.time()
        self.show_info_per_count = 100000
        self.counter = 0
        self.max_try_count = self.base**self.passwd_len

    def range_for_worker(self, worker_id, num_workers) -> tuple[int, int]:
        base = self.max_try_count // num_workers
        extra = self.max_try_count % num_workers
        if worker_id < extra:
            start = worker_id * (base + 1)
            end = start + (base + 1)
        else:
            start = extra * (base + 1) + (worker_id - extra) * base
            end = start + base
        return start, end

    def get_passwd(self, idx) -> bytes:
        out = bytearray(self.passwd_len)
        for pos in range(self.passwd_len - 1, -1, -1):
            idx, left = divmod(idx, self.base)
            out[pos] = self.passwd_seed[left]
        return bytes(out)

    def get_elapsed(self) -> str:
        now = time.time()
        elapsed = now - self.start_time
        return f"{elapsed:.3f} 초 경과"

    def print_info(self, count, max_try):
        if count % self.show_info_per_count == 0:
            print(
                f'시작 시간 {datetime.fromtimestamp(self.start_time).strftime("%Y-%m-%d %H:%M:%S")} 시도횟수 {count} 경과시간 {self.get_elapsed()} 퍼센티지 {(count / max_try) * 100 : .3f}%'
            )

    def pick_member(self, zf: zipfile.ZipFile):
        for info in zf.infolist():
            if not info.is_dir():
                return info
        raise ValueError("Error : ther is no file in zip!")

    def save_password(self, password):
        saved_path = os.path.join(self.base_path, "password.txt")
        try:
            with open(saved_path, "w", encoding="utf-8") as f:
                f.write(password)
        except Exception as e:
            print(f"error : {e}")

    def unlock_zip(self, idx, total, event) -> str:
        zip_file_path = os.path.join(self.base_path, "emergency_storage_key.zip")
        start, end = self.range_for_worker(idx, total)
        max_try = end - start
        with open(zip_file_path, "rb") as mf:
            with mmap.mmap(mf.fileno(), length=0, access=mmap.ACCESS_READ) as mm:
                with zipfile.ZipFile(mm, "r") as zf:
                    member = self.pick_member(zf)
                    for i in range(start, end):
                        if event.is_set():
                            print("비밀번호 발견되어 종료됨")
                            break
                        passwd = self.get_passwd(i)
                        # print(f"process No . {idx} pssword = {passwd.decode(encoding='utf-8')}")
                        try:
                            self.counter += 1
                            with zf.open(
                                member,
                                "r",
                                pwd=passwd,
                            ) as f:
                                byte = f.read(1)
                                self.print_info(i - start, max_try)
                                password = passwd.decode(encoding="utf-8")
                                self.save_password(password)
                                print(f"password founded ! : {password}")
                                event.set()
                                return passwd
                        except (
                            RuntimeError,
                            zipfile.BadZipFile,
                            zipfile.LargeZipFile,
                            zlib.error,
                        ):
                            self.print_info(i - start, max_try)
                            continue
        return "can't found passwd"

    def multi_processing(self):
        event = Event()
        process = [
            Process(
                target=self.unlock_zip,
                args=(
                    i,
                    self.cpu_cores,
                    event,
                ),
            )
            for i in range(self.cpu_cores)
        ]

        for p in process:
            p.start()
        for p in process:
            p.join()
        for p in process:
            if p.is_alive():
                p.terminate()
                p.join()
