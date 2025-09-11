import os
import csv
import pprint
import csv_paser_manager


def main():
    try:
        csv_manager = csv_paser_manager.Csv_manager()

        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_dir_path = os.path.join(base_dir, "mars_base")
        csv_file_path = os.path.join(csv_dir_path, "Mars_Base_Inventory_List.csv")
        csv_save_path = os.path.join(csv_dir_path, "Mars_Base_Inventory_danger.csv")
        pprint.pprint("-----------csv 파일을 읽어서 화면에 출력 -------------")
        csv_manager.set_csv(csv_file_path, "r", True)
        # pprint.pprint(csv_manager.csv_data)

        pprint.pprint("------------csv 파일을 , 로 파싱하여 출력한다----------")
        pprint.pprint(csv_manager.get_csv_list())

        pprint.pprint("--------인화성 지수가 0.7 이상인 항목만 출력한다----------")
        filter_result = csv_manager.get_csv_filter("Flammability", 0.7, ">=")
        pprint.pprint(filter_result)
        # pprint.pprint(csv_manager.get_csv_filter("Strength", "Weak"))

        pprint.pprint("--------인화성 지수가 0.7 이상의 데이터 파일로 저장----------")
        with open(csv_save_path, "w", newline="", encoding="utf-8") as save_file:
            file = csv.writer(save_file)
            file.writerow(csv_manager.get_csv_header())
            file.writerows(filter_result)
        pprint.pprint("--------파일 저장 완료 ----------")

    except Exception as e:
        print(e)


def sort_by_flammabliity(data, index):
    return float(data[-1]) >= index


if __name__ == "__main__":
    main()
