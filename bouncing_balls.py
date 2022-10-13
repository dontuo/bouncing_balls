import utime
import urandom
from machine import Pin, I2C, ADC
import ssd1306
class BouncingBalls:
    def __init__(self):
        self.coordinateballs = []
        self.coordinateballs2 = []
        self.vectorballx = []
        self.vectorbally = []
        self.vectx = 0
        self.vecty = 0
        self.amount = 4
        self.vector = 0
        self.width = 64
        self.height = 48
        self.a = 0
        
        i2c = I2C(sda=Pin(4), scl=Pin(5))
        self.display = ssd1306.SSD1306_I2C(64, 48, i2c)
        
        self.x1 = 0
        self.y1 = 0
        self.meter = 5
    def take_random(self):
        for i in range(0, self.amount):
            self.coordinateballs.append([self._randint(10, 50),self._randint(5, 25)])

        for i in range(0, self.amount):
            vectx = self._randint(1, 3)
            vecty = self._randint(1, 3)
            stan = self._randint(0,1)
            if stan:
                vectx = self._randint(1, 2) * -1
                vecty = self._randint(1, 2) * -1
                stan = 0
            self.vectorballx.append(vectx)
            self.vectorbally.append(vecty)
    
    def main_loop(self):
        self.take_random()
        while True:
            self.display.fill(0)
            self._draw_lines()
            self._draw_balls()
            #utime.sleep(0.3)
            self.display.show()
    def _draw_balls(self):
        for i in self.coordinateballs:
            self.x = i[0]
            self.y = i[1]
            
            
            if self.x + 3>= self.width - 1: self.vectorballx[self.vector] = -self.vectorballx[self.vector]
            elif self.x <= 2: self.vectorballx[self.vector] *= -1
            if self.y >= self.height - 4: self.vectorbally[self.vector] = -self.vectorbally[self.vector]
            elif self.y + 3 <= 4: self.vectorbally[self.vector] *= -1
            
            self.x += self.vectorballx[self.vector]
            self.y += self.vectorbally[self.vector]
            self.coordinateballs2.append([self.x, self.y])
            for b in self.coordinateballs2:
                x = b[0]
                y = b[1]
                
                self.display.line(self.x + 1, self.y + 1, x + 1, y + 1,1) 
            
            self.display.fill_rect(self.x, self.y, 3, 3, 1)
            #self.display.show()
            #utime.sleep(0.3)
            self.a += 1
            self.vector += 1
            
        self.a = 0
        self.vector = 0
        self.coordinateballs = self.coordinateballs2
        self.coordinateballs2 = []
        
    def _find_dist_from_xy(self, zx, zy, x1, y1):
        x2 = zx - x1
        y2 = zy - y1
        self.display.fill(0)
        if x2 < 0: x2 *= -1
        elif y2 < 0: y2 *= -1
        if x2 <= self.meter and y2 <= self.meter: return True
    
    def _randint(self, min, max):
        span = max - min + 1
        div = 0x3fffffff // span
        offset = urandom.getrandbits(30) // div
        val = min + offset
        return val
    def _draw_lines(self):
        self.display.line(0, 0, 64, 0, 1)
        self.display.line(0, 0, 0, 48, 1)
        self.display.line(63, 0, 63, 48, 1)
        self.display.line(63, 47, 1, 47, 1)

BouncingBalls().main_loop()
