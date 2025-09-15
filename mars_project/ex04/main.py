import os
import sys
import time
import decrypto


def main():
    dc = decrypto.Decrypt()
    passwd = dc.do_brutforce()
    print(f"pass word is {passwd}")
    dc.save_password()


if __name__ == "__main__":
    main()
