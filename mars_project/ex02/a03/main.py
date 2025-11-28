import numpy as np
import os
import csv


def main():
    files = [
        "mars_base_main_parts-001.csv",
        "mars_base_main_parts-002.csv",
        "mars_base_main_parts-003.csv",
    ]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_dir = os.path.join(base_dir, "mars_base")
    total_arry = []
    for file in files:
        try:
            file_path = os.path.join(csv_dir, file)
            arry = np.loadtxt(
                file_path, delimiter=",", dtype="U100", encoding="utf-8-sig"
            )
            total_arry.append(np.array(arry))
            print("22")
        except FileNotFoundError:
            print(f"{file} is not exit!!")
            os._exit(1)
        except Exception as e:
            print(f"error : {e}")
            os._exit(1)
    print(total_arry)

    headers = total_arry[0][0]
    goods = [name[0] for name in total_arry[0][1:]]
    print(goods)
    arry1 = [row[1] for row in total_arry[0][1:]]
    arry2 = [row[1] for row in total_arry[1][1:]]
    arry3 = [row[1] for row in total_arry[2][1:]]
    stack_arry = np.column_stack([arry1, arry2, arry3])
    csv_ndarray = np.zeros(len(goods), dtype=[("goods", "U20"), ("value", ("i4", 3))])
    csv_ndarray["goods"] = goods
    csv_ndarray["value"] = stack_arry
    print("ndarray 생성")
    print(csv_ndarray)
    print("parts 기준으로 평균값 50 이상찾기")
    save_data = []
    for data in csv_ndarray:
        if np.mean(data[1]) >= 50:
            save_data.append([str(data[0]), data[1].tolist()])

    print(save_data)

    print("csv 로 50 이상값 저장")
    try:
        with open("parts_to_work_on.csv", "w", newline="", encoding="utf-8") as file:
            csv_file = csv.writer(file)
            csv_file.writerow(headers)
            for parts, values in save_data:
                csv_file.writerow([parts] + values)
    except Exception as e:
        print(f"error : {e}")


if __name__ == "__main__":

    main()
