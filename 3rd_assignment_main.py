#########################################################################
# Date: 2018/10/02
# file name: 3rd_assignment_main.py
# Purpose: this code has been generated for the 4 wheel drive body
# moving object to perform the project with line detector
# this code is used for the student only
#########################################################################

from car import Car
import time
import TCS34725.TCS34725_RGB as rgb


class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)
        # PID configure
        self.Kp = 9
        self.Ki = 0
        self.Kd = 0
        self.last_error = 0
        self.error_sum = 0

    def drive_parking(self):
        self.car.drive_parking()

    def get_error(self):
        rgb.calculate_color_temperature(1,2,3)
        sensor = self.car.line_detector.read_digital()
        cnt, error = 0, 0
        for i in range(0, 5):
            if sensor[i] == 1:
                error += (i - 2)
                cnt += 1
        if cnt != 0:
            error /= cnt
        error = error ** 2
        return error, cnt

    def get_pid(self, error):
        self.error_sum += error
        p_term = self.Kp * error
        i_tern = self.Ki * self.error_sum * 0.001
        d_term = self.Kd * (error - self.last_error)
        self.last_error = error
        return p_term + i_tern + d_term

    def car_startup(self):
        pass

    def turn_left_90(self, speed):
        while True:
            error, cnt = self.get_error()
            if cnt != 0 and -1 < error < 1:
                return
            self.car.accelerator.go_backward(speed)
            self.car.steering.turn(130)

    def car_startup(self):
        speed = 60
        while True:
            error, cnt = self.get_error()
            if self.last_error <= -1.5 and cnt == 0:
                self.turn_left_90(speed)
            angle = self.get_pid(error)
            self.car.steering.turn(angle + 90)
            if 0<= self.car.distance_detector.get_distance() <=20:
                break

    # =======================================================================
    # 3RD_ASSIGNMENT_CODE
    # Complete the code to perform Third Assignment
    # =======================================================================
    # def car_startup(self):
    #     start_time = time.time()
    #     speed = 60
    #     self.car.accelerator.go_forward(speed)
    #     time_cnt = 0
    #     prev_time = time.time()
    #     error_sum = 0
    #     while True:
    #         time_cnt += 1
    #         error, cnt = self.get_error()
    #         if cnt != 0:
    #             error /= cnt
    #         if cnt == 0 and last_error < -1:
    #             self.turn_left_90(speed)
    #         cur_time = (time.time() - prev_time)
    #         error_sum += cur_time * error
    #         direction = self.get_pid(error)
    #         print("error: %1d, last_error: %1d, delta: %1.7f, kp: %3d, ki: %3.5f, kd: %3.5f" % (
    #             error, last_error, cur_time, Kp * error, Ki * (error * cur_time), Kd * (error - last_error)))
    #         last_error = error if cnt != 0 else last_error
    #         prev_time = time.time()
    #         self.car.steering.turn(direction + 90)
    #         self.car.accelerator.go_forward(speed)
    #         dist = self.car.distance_detector.get_distance()
    #         print("cnt: %1d, error: %1d, direction: %3d, dist: %3.0f, time: %1.5f, speed: %3d\n" % (
    #             cnt, error, direction, dist, cur_time, speed))
    #         # print("cnt:",cnt,",error:", error, ",direction:",direction,"dist:",dist,",delta:",cur_time,"speed:", speed)
    #         if 0 <= dist <= 20:
    #             break
    #             # pass
    #     # self.car.accelerator.go_backward(40)
    #     # sleep(0.2)
    #     print(time.time() - start_time)
    #     self.car.drive_parking()


if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()
