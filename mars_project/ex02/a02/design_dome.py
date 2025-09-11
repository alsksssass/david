import math
import os


def sphere_area(diameter: float, meterial: str, thickness: float = 1.0):
    meterial_value = {"glass": 2.4, "aluminum": 2.7, "carbon_steel": 7.85}
    if diameter <= 0:
        raise ValueError("invaid value at radius!!")
    if meterial not in meterial_value:
        raise ValueError("not support meterial!!")
    gravity_mars = 9.8 * 0.38
    r = diameter / 2
    area = 2 * math.pi * r**2
    thickness_m = thickness / 100

    volume = area * thickness_m
    struct_weight = volume * meterial_value.get(meterial)
    struct_weight_mars = struct_weight * gravity_mars
    print(f"area = {volume:3f} weight = {struct_weight_mars}")


def main():
    while True:
        try:
            print(
                "돔구조물 설계 프로그램입니다. 해당하는 입력값을 입력해 주세요, 종료는 exit"
            )
            r = input("지름(Folat)을 입력하세요 : ")
            if r == "exit":
                os._exit(0)
            r = float(r)
            meterial = str(input("재질(str)을 입력하세요 : "))
            sphere_area(r, meterial)
        except ValueError as e:
            print(f"error : invalid input value!! {e}")
        except Exception as e:
            print(f"error : {e}")


if __name__ == "__main__":
    main()
