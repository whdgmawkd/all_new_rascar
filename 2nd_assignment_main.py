#########################################################################
# Date: 2018/10/02
# file name: 1st_assignment_main.py
# Purpose: this code has been generated for the 4 wheels drive body
# moving object to perform the project with ultra sensor
# this code is used for the student only
#########################################################################

from car import Car
import time


class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)

    def drive_parking(self):
        self.car.drive_parking()

    def car_startup(self):
        start_time = time.time()
        speed = 90
        self.car.accelerator.go_forward(speed)
        time_cnt=0
        last_error=0
        prev_time = time.time()
        while(True):
            time_cnt+=1
            sensor = self.car.line_detector.read_digital()
            print(sensor)
            cnt=0
            error = 0
            for i in range(0,5):
                if sensor[i] == 1:
                    error+=(i-2)
                    cnt+=1 
            if cnt!=0:
                error/=cnt
            Kp=10
            Ki=10
            Kd=10
            cur_time = (prev_time - time.time())
            direction = Kp*error + Ki*(error*cur_time) + Kd*(error - last_error)
            print("error: %1d, last_error: %1d, delta: %1.7f, kp: %3d, ki: %3.5f, kd: %3.5f"%(error,last_error,cur_time,Kp*error,Ki*(error*cur_time),Kd*(error - last_error)))
            last_error = error if cnt!=0 else last_error
            prev_time = time.time()
            speed = 90 - (50 if cnt==0 else 0)
            self.car.steering.turn(direction + 90)
            self.car.accelerator.go_forward(speed)
            dist=self.car.distance_detector.get_distance()
            print("cnt: %1d, error: %1d, direction: %3d, dist: %3.0f, time: %1.5f, speed: %3d\n"%(cnt,error,direction,dist,cur_time,speed))
            # print("cnt:",cnt,",error:", error, ",direction:",direction,"dist:",dist,",delta:",cur_time,"speed:", speed)
            if 0<=dist<=20 or cnt==5:
                break
                # pass
        #self.car.accelerator.go_backward(40)
        #sleep(0.2)
        print(time.time() - start_time)
        self.car.drive_parking()

if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()

    except:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()
