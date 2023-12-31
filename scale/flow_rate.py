import time
from statistics import mean
from scale_class import Scale

if __name__ == '__main__':

    scale = Scale(pd_sck_pin=2, dout_pin=3)

    # window size for moving average (number of data points)
    window = 15

    # frequency of flow rate measurement (seconds)
    freq = 5

    start_time = time.time()
    data = [scale.read_weight() for _ in range(window)]
    start_weight = mean(data)
    time.sleep(5)
    while True:
        try:
            reading = scale.read_weight()
            data.append(reading)
            avg_weight = mean(data)
            data.pop(0)
            if time.time() - start_time >= freq:
                flow_rate = ((start_weight - avg_weight)/freq)*60
                print(f'Flow rate: {flow_rate} mL/min, Volume: {reading} mL')
                #print(flow_rate)

                start_time = time.time()
                start_weight = avg_weight
            
            time.sleep(0.1) # wait 0.1 seconds between weight measurements

        except (KeyboardInterrupt, SystemExit):
            scale.stop()

