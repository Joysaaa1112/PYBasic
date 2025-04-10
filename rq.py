import threading
from time import sleep


def task(name, number, letter):
    print(f"{name} 线程开始")
    count = 0
    while count < number:
        sleep(1)
        print(f"{name} 正在运行")
        count += 1
    print(f"{name} 线程结束")


if __name__ == '__main__':
    threading1 = threading.Thread(target=task, args=("线程1", 5, "A"))
    threading2 = threading.Thread(target=task, args=("线程2", 5, "B"))

    threading1.start()
    threading2.start()

    threading1.join()  # 等待线程1结束
    threading2.join()  # 等待线程2结束
