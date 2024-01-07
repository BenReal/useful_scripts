import multiprocessing

def get_cpu_cores():
    return multiprocessing.cpu_count()

if __name__ == "__main__":
    cores = get_cpu_cores()
    print(f"The computer has {cores} CPU cores.")
