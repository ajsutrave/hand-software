from __future__ import print_function
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
imoprt tkinter as tk
import threading


class RemoteFingerServo(AngularServo):
    def __init__(self, gpio, pin_factory, finger,
                 min_angle=0, max_angle=100, inverted=False):
        super(RemoteFingerServo,self).__init__(gpio,
                                               pin_factory=pin_factory,
                                               min_angle=min_angle,
                                               max_angle=max_angle)
        self.finger=finger
        self.inverted=inverted
    def set_angle(self, val, debug=False):
        if debug: print(self.finger, "servo angle: ", self.angle, "val:", int(val))
        self.angle = int(val)

class HandGUI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.pin_factory=PiGPIOFactory(host='192.168.1.216')
        self.start()
    def callback(self):
        self.root.quit()
        for servo in self.servos:
            print("detatching servo for", servo.finger)
            servo.detach()
    def run(self):
        self.servos = [
            RemoteFingerServo(18, pin_factory=self.pin_factory, finger='pinky',),
            RemoteFingerServo(17, pin_factory=self.pin_factory, finger='middle', inverted=True),
        ]
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        label = tk.Label(self.root, text=self.__class__.__name__)
        label.pack()
        for servo in self.servos:
            scale = tk.Scale(orient='horizontal',
                             to_=servo.min_angle, from_=servo.max_angle,
                             command=servo.set_angle, label= servo.finger)
            scale.set(servo.angle)
            scale.pack()
        self.root.mainloop()

if __name__ == "__main__":
    gui = HandGUI()
    print("Here")
