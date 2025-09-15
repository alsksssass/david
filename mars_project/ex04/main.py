import david.mars_project.ex04.door_hacking as door_hacking


def main():
    dc = door_hacking.Decrypt()
    passwd = dc.unlock_zip()
    print(f"pass word is {passwd}")
    dc.save_password()


if __name__ == "__main__":
    main()
