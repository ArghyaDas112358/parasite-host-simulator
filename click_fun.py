import pyautogui
import time

from fractions import Fraction as Fr
def bernoulli2():
    A, m = [], 0
    while True:
        A.append(Fr(1, m+1))
        for j in range(m, 0, -1):
          A[j-1] = j*(A[j-1] - A[j])
        yield A[0] # (which is Bm)
        m += 1
 
bn2 = [ix for ix in zip(range(15), bernoulli2())]
bn2 = [(i, b) for i,b in bn2 if b]
width = max(len(str(b.numerator)) for i,b in bn2)

time.sleep(5)  

for i,b in bn2:
    pyautogui.write('B(%2i) = %*i/%i' % (i, width, b.numerator, b.denominator))
    pyautogui.keyDown("Enter")

'''
B( 0) =    1/1
B( 1) =    1/2
B( 2) =    1/6
B( 4) =   -1/30
B( 6) =    1/42
B( 8) =   -1/30
B(10) =    5/66
B(12) = -691/2730
B(14) =    7/6

'''

