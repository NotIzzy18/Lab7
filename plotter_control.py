from machine import Pin, PWM
import time

s1=PWM(Pin(0), freq = 50) # shoulder
s2=PWM(Pin(1), freq = 50) # elbow
s3=PWM(Pin(2), freq = 50) # wrist

def translate(angle:float) -> int:
    MIN=1638
    MAX=8192
    DEG=(MAX-MIN)/180
    angle=max(0,min(180,angle))
    return int(angle*DEG+MIN)

def move(servo:PWM,deg:float) -> None:
    servo.duty_u16(translate(deg))

def execute(gcodearray:list) -> None:
    n=0 # index number
    for i in gcodearray:
        if i=="M18":
            print("Read stop code.")
            SystemExit()
        elif i=="M5":
            time.sleep_ms(500)
            move(s3,0) # UP
        elif i=="M3":
            move(s3,30) # DOWN
            time.sleep_ms(500)
        elif i=="G1":
            move(s1, float(gcodearray[n+1][1:])) # pass the element after G1, minus the first character
            print(gcodearray[n+1][1:])
            move(s2, float(gcodearray[n+2][1:])) # pass the one after that
            print(gcodearray[n+2][1:])
        elif i[0]=="S" or i[0]=="E": # Ignore degrees themselves
            pass
        else:
            print(f"Parsing error: Unknown command \"{i}\".")
        n+=1

with open(r"circle.gcode") as f: # Change this path so that quotes match file name
    file=f.read()

execute(file.split())