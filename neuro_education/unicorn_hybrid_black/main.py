from multiprocessing import Process
import os
import unicorn_connect as up
""" 
p1 = Process(target=calculate_squares, args=(first_half,))
p2 = Process(target=calculate_squares, args=(second_half,))

p1.start()
p2.start() """

def unicorn_process(device_number=0):
    unicorn_tec = up.unicorn_device("subject1")
    unicorn_tec.get_port_id(device_number)
    unicorn_tec.unicorn_connect()
    unicorn_tec.unicorn_stream()
    unicorn_tec.unicorn_disconnect()

def ui_process():
    pass

if __name__ == '__main__':
    p1 = Process(target=unicorn_process, args=())
    p2 = Process(target=ui_process, args=())

    p1.start()
    p2.start()

    p1.join()
    p2.join()

