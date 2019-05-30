import LightController as LightController

# COLOR TEMPERATURES
COLD = 0
NORMAL = 1
WARM = 2

#BRIGTHNESS = 0 - 254
while True:
    x = input()
    LightController.setLights(int(x),0)




