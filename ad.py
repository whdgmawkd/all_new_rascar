#########################################################################
# Date: 2018/10/02
# file name: 3rd_assignment_main.py
# Purpose: this code has been generated for the 4 wheel drive body
# moving object to perform the project with line detector
# this code is used for the student only
#########################################################################

from car import Car
import RPi.GPIO as GPIO
import TCS34725.TCS34725_RGB as rgb
import time
import keyboard
from multiprocessing import Process


class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(8,GPIO.OUT)
        self.p=GPIO.PWM(8,100)
        
    def dist_warn(self):
        buzz_time =0
        sleep_time=0
        while True:
            t = time.time()
            dist = self.car.distance_detector.get_distance()
            if 0 < dist <= 30 and sleep_time <= 0:
                if dist < 10:
                    self.p.start(5)
                    self.p.ChangeFrequency(530)
                    continue
                buzz_time = 0.1
                sleep_time = dist*0.005
#                 print("warn",dist)
                
            if buzz_time > (time.time() - t):
                buzz_time -= (time.time() - t)
                self.p.start(5)
                self.p.ChangeFrequency(530)
            else:
                sleep_time -= (time.time() - t)
                self.p.stop()
            
        
    def warn(self, dist):
        if 0 < dist < 10:
            self.p.start(5)
            self.p.ChangeFrequency(530)
        else:
            self.p.start(5)
            self.p.ChangeFrequency(530)
            time.sleep(dist * 0.004)
            self.p.stop()
            time.sleep(dist * 0.004 * 5)
        
    def car_startup(self):
        last = 0
        self.started=True
        distWarn = Process(target=self.dist_warn)
        distWarn.start()
        while(True):
            speed=30
#             print(keyboard.is_pressed('a'), keyboard.is_pressed('s'),keyboard.is_pressed('d'),keyboard.is_pressed('w'))
            if keyboard.is_pressed('space'):
                if distWarn.is_alive():
                    distWarn.terminate()
                self.p.start(5)
                self.p.ChangeFrequency(400)
            else:
                self.p.stop()
                if not distWarn.is_alive():
                    distWarn = Process(target=self.dist_warn)
                    distWarn.start()
            if keyboard.is_pressed('shift'):
                speed=100
            if keyboard.is_pressed('w'):
                self.car.accelerator.go_forward(speed)
            elif keyboard.is_pressed('s'):
                self.car.accelerator.go_backward(speed)
            else:
                self.car.accelerator.go_forward(0)
            if keyboard.is_pressed('a'):
                self.car.steering.turn(90-45)
                last=-1
            elif keyboard.is_pressed('d'):
                self.car.steering.turn(90+32)
                last=1
            else:
                if last==1:
                    self.car.steering.turn(90-7)
                elif last==-1:
                    self.car.steering.turn(90+3)
                else:
                    self.car.steering.turn(90)
            raw = self.car.color_getter.get_raw_data()
#             print(*raw)
            if raw[0] > 200 and raw[0] > (raw[1] + raw[2]) * 0.7:
                print("maybe red?")
                print(*raw)
#             print(rawData)
#             print(*list(rawData)[:3])
#             print(rgb.calculate_color_temperature(*list(rawData)[:3]))
#             print(rgb.calculate_lux(*list(rawData)[:3]))
        p.stop()
            
    def drive_parking(self):
        self.car.drive_parking()

if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()
    except Exception as e:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        print(e)
        myCar.drive_parking()
    else:
        myCar.drive_parking()


