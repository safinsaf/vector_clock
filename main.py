from multiprocessing import Process, Pipe

def calc_recv_timestamp(recv_time_stamp, counter):
    #Take max of recieved and current value for each process
    result = [0 for i in range(len(counter))]
    for i in range(len(counter)):
        result[i] = max(recv_time_stamp[i], counter[i])
    return result

def event(pid, counter):
    # Increase counter of current pid
    counter[pid] += 1
    return counter

def send_message(pipe, pid, counter):
    # Increase counter of current pid and send counter
    counter[pid] += 1
    pipe.send(('Empty shell', counter))
    return counter

def recv_message(pipe, pid, counter):
    # increase counter of current pid, receive counter from other
    # process and call function to recalculate counter
    counter[pid] += 1
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    return counter

def process_one(pipe12):
    pid = 0
    counter = [0,0,0]
    counter = send_message(pipe12, pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)

    print("Process",str(pid), ":", counter)

def process_two(pipe21, pipe23):
    pid = 1
    counter = [0,0,0]
    counter = recv_message(pipe21, pid, counter)
    counter = recv_message(pipe21, pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = recv_message(pipe23, pid, counter)
    counter = event(pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = send_message(pipe23, pid, counter)
    counter = send_message(pipe23, pid, counter)

    print("Process", str(pid), ":", counter)

def process_three(pipe32):
    pid = 2
    counter = [0,0,0]
    counter = send_message(pipe32, pid, counter)
    counter = recv_message(pipe32, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe32, pid, counter)

    print("Process", str(pid), ":", counter)

if __name__ == '__main__':
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    process1 = Process(target=process_one,
                       args=(oneandtwo,))
    process2 = Process(target=process_two,
                       args=(twoandone, twoandthree))
    process3 = Process(target=process_three,
                       args=(threeandtwo,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()