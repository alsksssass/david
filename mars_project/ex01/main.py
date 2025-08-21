import csv
import json


def log_print_reverse_timestamp(logs):
    for log in reversed(logs):
        print(log)


def parse_log_file(file_path):
    parsed_data = []
    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                parsed_data.append(row)
        return parsed_data[1:]  # Skip the header row
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
    return []


def parse_contain_word_log(log, *args):
    print_logs = []
    for row in log:
        if any(arg.lower() in row[2].lower() for arg in args):
            print_logs.append(row)
    if print_logs:
        for log in print_logs:
            print(log)
    else:
        print("No matching logs found.")


if __name__ == "__main__":
    log_file_path = "mission_computer_main.log"
    parsed_logs = parse_log_file(log_file_path)
    print("Parsed Logs:")
    for log in parsed_logs:
        print(log)
    print("\nSorted Logs:")
    sorted_logs = sorted(
        parsed_logs, key=lambda x: x[0], reverse=True
    )  # Sort by timestamp (first column) in descending order
    for log in sorted_logs:
        print(log)

    print("\nDictionary of Logs:")
    log_dict = {
        log[0]: log[1:] for log in sorted_logs
    }  # Use the first column as the key
    for key, value in log_dict.items():
        print(f"{key}: {value}")

    print("\nsaving json file")
    # Save the dictionary to a JSON file
    try:
        with open("logs.json", "w") as json_file:
            json.dump(log_dict, json_file, indent=4)  # log_dict는 저장할 딕셔너리
        print("Logs successfully saved to logs.json")
    except FileNotFoundError:
        print("Error: The specified file path was not found.")
    except PermissionError:
        print("Error: Permission denied. Unable to write to the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("\nPrinting logs in reverse order:")
    log_print_reverse_timestamp(sorted_logs)

    print("\nPrinting logs containing specific words:")
    parse_contain_word_log(
        sorted_logs, "explosion", "leak", "Oxygen", "high temperature"
    )

    keywords = input("\nPrinting logs containing 'What you want':")
    parse_contain_word_log(sorted_logs, keywords)
