from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
import tkinter
from time import sleep

pin_factory = PiGPIOFactory(host='192.168.1.216')
servo = AngularServo(18, pin_factory=pin_factory,
                     min_angle=0, max_angle=100)

servo.max()
sleep(5)

def set_servo_angle(val):
    print( "Servo angle: ", servo.angle, "Val:", val)
    servo.angle = int(val)

root = tkinter.Tk()

scale = tkinter.Scale(orient='horizontal',
                      from_=servo.min_angle, to=servo.max_angle,
                      command=set_servo_angle)
scale.pack()
root.mainloop()
