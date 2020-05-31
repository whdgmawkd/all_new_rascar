from car import Car
import time
from multiprocessing import Process
import RPi.GPIO as GPIO

class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)
        self.detect_cnt = 0
        self.time = time.time()
        self.enabled=True
        self.endline_cnt=0
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(8,GPIO.OUT)
        self.buzz = GPIO.PWM(8,100)
        self.distWarn=Process(target=self.dist_warn)
        
    def sing(self):
        tone = [329,311,329,311,329,246,293,261,220,146,174,220,246,174,233,246,261]
        term = [350,350,350,350,350,400,400,400,1000,350,400,400,1000,400,400,400,1000]
        self.buzz.start(5)
        for i in range(len(tone)):
            self.buzz.ChangeFrequency(tone[i]*1.5)
            time.sleep(term[i] / 1400)
        self.buzz.stop()
    
    def dist_warn(self):
        buzz_time =0
        sleep_time=0
        while True:
            t = time.time()
            dist = self.car.distance_detector.get_distance()
            print(dist)
            self.buzz.start(5)
            if 0 < dist <= 10:
                self.buzz.ChangeFrequency(530)
            elif 0 < dist <= 30:
                self.buzz.ChangeFrequency(530)
                time.sleep(0.05)
                self.buzz.stop()
                time.sleep(dist * 0.004)
            else:
                self.buzz.ChangeFrequency(1)

            '''
            time.sleep(dist * 0.02)
            if 0 < dist <= 10:
                sleep_time = 0
            elif 10 < dist <= 30 and sleep_time <= 0:
                sleep_time = dist/100
            self.buzz.start(5)
            self.buzz.ChangeFrequency(530)
            time.sleep(0.1)
            sleep_time -= (time.time() - t)
            if sleep_time <= 0:
                self.buzz.stop()
            '''

    def drive_parking(self):
        self.car.drive_parking()
    
    def get_direction(self,sensor):
        direction = 0
        if sensor[0]:
            direction = -35
        elif sensor[1]:
            direction = -17
        elif sensor[2]:
            direction = 0
        elif sensor[3]:
            direction = 17
        elif sensor[4]:
            direction = 35
        return direction
    
    def track(self,speed):
        dist_cnt=0
        sign_flag = False
        while True:
            sensor = self.car.line_detector.read_digital()
            direction = self.get_direction(sensor)
            if sensor == [1,1,1,1,1]:
                return True
#                 sign_flag = False
#                 self.enabled = True
#                 direction = 0
#                 self.endline_cnt+=1
#             if sensor == [1,1,1,1,1] and self.detect_cnt >= 4 and self.endline_cnt >= 2:
#                 return False
            if sensor == [0,0,0,0,0]:
                self.car.steering.turn(90+35)
                self.car.accelerator.go_backward(speed)
                while self.car.line_detector.read_digital() == [0,0,0,0,0] or self.car.line_detector.read_digital() == [1,0,0,0,0]:
                    pass
            self.car.steering.turn(90+direction)
            self.car.accelerator.go_forward(speed)
            
            raw = self.car.color_getter.get_raw_data()
            print(raw)
            r,g,b = raw[0]//4, raw[1]//4, raw[2]//4
            r,g,b = r**2,g**2,b**2
            fac = max(r,g,b)
            r,g,b = r/fac,g/fac,b/fac
            r,g,b = r*255,g*255,b*255
            print(r,g,b)
            print("\x1b[48;2;%d;%d;%dm \x1b[0m" % (r,g,b))
            if r > 230 and r > (g + b) * 0.7 and not sign_flag: # red light
                sign_flag = True
                print("red")
                self.car.accelerator.go_forward(0)
                time.sleep(3)
#                 self.distWarn.terminate()
#                 time.sleep(1)
#                 self.sing()
            dist = self.car.distance_detector.get_distance()
            print(dist)
            if 0 < dist < 10:
                self.car.accelerator.go_forward(0)
                time.sleep(1)
                self.distWarn.terminate()
                time.sleep(1)
                self.car.accelerator.go_backward(speed-10)
                p=Process(target=self.sing)
                p.start()
                while self.car.distance_detector.get_distance() < 30:
                    sensor = self.car.line_detector.read_digital()
                    direction = self.get_direction(sensor)
                    self.car.steering.turn(90 + (-1 * direction))
                p.terminate()
                self.car.accelerator.go_forward(speed)
                time.sleep(0.4)
                return False

    def detect(self,speed):
        self.detect_cnt += 1
        sleeptime = 1/speed * 20
        self.car.steering.turn(90-35)
        time.sleep(sleeptime)
        self.car.steering.turn(90)
        while self.car.line_detector.read_digital() == [0,0,0,0,0]:
            pass
        print("mid line detected")
        self.car.steering.turn(90+35)
        time.sleep(sleeptime)
        while self.car.line_detector.read_digital() == [0,0,0,0,0]:
            pass
        print("main line detected")

    def car_startup(self):
        self.distWarn = Process(target=self.dist_warn)
        self.distWarn.start()
        speed = 35
        while True:
            if self.track(speed):
                return
            self.detect(speed)
            self.endline_cnt = 0
            if self.detect_cnt == 1 or self.detect_cnt == 4:
                self.enabled = False

if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()
    except Exception as e:
#         when the Ctrl+C key has been pressed,
#         the moving object will be stopped
        print(e)
        myCar.drive_parking()
    else:
        myCar.drive_parking()
