import sys


def handle_interrupt(signal, frame, processes: dict) -> None:
    print("\n")
    for name, process in processes.items():
        print(f"Terminating {name} server...", end="\t")
        process.kill()
        if process.poll() is None:
            print("done!")
        else:
            print("FAILED!")
    sys.exit()
