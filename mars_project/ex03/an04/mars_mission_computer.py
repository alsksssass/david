import MissionComputer
import threading
import multiprocessing

is_multiprocess = True

# is_multiprocess = False


def main():
    runComputer = MissionComputer.MissonComputer()
    worker = [
        runComputer.get_sensor_data,
        runComputer.get_misson_computer_info,
        runComputer.get_mission_computer_load,
    ]

    if is_multiprocess:
        process_lock = multiprocessing.Lock()
        process = [
            multiprocessing.Process(
                target=worker[i],
                args=(process_lock,),
            )
            for i in range(3)
        ]
        try:
            for p in process:
                p.daemon = True
                p.start()
            for p in process:
                p.join()
        except KeyboardInterrupt:
            print("\ncomputer shutdown")
            for p in process:
                if p.is_alive():
                    p.terminate()
                p.join()
        except Exception as e:
            print(f"error : {e}")
    else:
        thread_lock = threading.Lock()
        thread_event = threading.Event()
        threads = [
            threading.Thread(
                target=worker[i],
                args=(thread_lock, thread_event),
            )
            for i in range(3)
        ]
        try:
            for t in threads:
                t.daemon = True
                t.start()
            for t in threads:
                t.join()
        except KeyboardInterrupt:
            print("\ncomputer shutdown")
            thread_event.set()
            for t in threads:
                t.join()
        except Exception as e:
            print(f"error : {e}")


if __name__ == "__main__":
    main()
