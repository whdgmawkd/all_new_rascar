#########################################################################
# Date: 2018/10/02
# file name: 3rd_assignment_main.py
# Purpose: this code has been generated for the 4 wheel drive body
# moving object to perform the project with line detector
# this code is used for the student only
#########################################################################

from car import Car
import time


class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)
        self.detect_cnt = 0
        self.time = time.time()
        self.enabled=True
        self.endline_cnt=0
        
    def get_dist(self):
        total=0
        for i in range(3):
            total += self.car.distance_detector.get_distance()
        return total/5

    def drive_parking(self):
        self.car.drive_parking()

    def track(self,speed):
        dist_cnt=0
        while True:
            sensor = self.car.line_detector.read_digital()
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
            if sensor == [1,1,1,1,1]:
                self.enabled = True
                direction = 0;
                self.endline_cnt+=1
            if sensor == [1,1,1,1,1] and self.detect_cnt >= 4 and self.endline_cnt >= 2:
                return True
            if sensor == [0,0,0,0,0]:
                self.car.steering.turn(90+35)
                self.car.accelerator.go_backward(speed)
                while self.car.line_detector.read_digital() == [0,0,0,0,0] or self.car.line_detector.read_digital() == [1,0,0,0,0]:
                    pass
            self.car.steering.turn(90+direction)
            self.car.accelerator.go_forward(speed)
            dist = self.get_dist()
            print(dist)
            if 0<dist<30:
                dist_cnt+=1
            else:
                dist_cnt=0
            if dist_cnt >= 7:
                if self.enabled:
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
        speed = 35
        while True:
            if self.track(speed):
                return
            self.detect(speed)
            self.endline_cnt = 0
            if self.detect_cnt == 2 or self.detect_cnt == 4:
                self.enabled = False

if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()
    except:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()
    else:
        myCar.drive_parking()
