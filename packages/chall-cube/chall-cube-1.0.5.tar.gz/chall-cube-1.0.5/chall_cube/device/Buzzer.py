from time import sleep
import RPi.GPIO as GPIO
from threading import Thread


class Buzzer:

    def __init__(self, pin):
        self.__pin = pin
        GPIO.setup(pin, GPIO.OUT)

    def low(self):
        GPIO.output(self.__pin, GPIO.LOW)

    def high(self):
        GPIO.output(self.__pin, GPIO.HIGH)

    def beep(self):
        self.high()
        sleep(0.5)
        self.low()

    def hz(self, hz, time):
        gap = 0.00001
        t = 0.0
        periode = 1.0 / hz
        
        while t < time:
            self.high()
            sleep(gap)
            self.low()
            sleep(periode - gap)
            t = t + periode

    def hz_async(self, hz, time):
        def async():
            self.hz(hz, time)

        Thread(target=async, daemon=True).start()
