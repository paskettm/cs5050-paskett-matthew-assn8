import random
import time
import numpy as np
import cmath
import matplotlib.pyplot as plt


# Main FFT function
# Based off of the Cooley and Tukey exploitation of the discrete Fourier Transform
# Works based on symmetry in the function to exploit the fact that you can split even and odd parts of the function.
# With the exploitation it becomes O(nlogn + n) but the final +n falls off.
# Source: https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm
def FFT(x:[], N:int):
    if N <= 1:
        return x

    else:
        listEven = FFT(x[::2], int(N/2))
        listOdd = FFT(x[1::2], int(N/2))

        ans = [0 for i in range(N)]

        for k in range(int(N/2)):
            ans[k] = listEven[k] + cmath.exp(-2j*cmath.pi*k/N)*listOdd[k]
            ans[k+int(N/2)] = listEven[k] - cmath.exp(-2j*cmath.pi*k/N)*listOdd[k]
        return ans


# Adds to the end of the string to make it a square length
def square(x):
    power = 0
    while 2**power < len(x):
        power += 1
    if len(x) == 2**power:
        return x

    squareX = [0 for i in range(2**power)]
    for i in range(len(x)):
        squareX[i] = x[i]
    return squareX


# Beginning FFT function
def beginFFT(x):
    squareX = square(x)
    ans = FFT(squareX, len(squareX))
    return ans


# Prints the output to a file instead of just the screen
def printToFile(pow: int, npFFT, stFFT):
    file = open('dataCache.txt', 'a')
    file.write(f"size:    \t2^{pow}\n")
    file.write(f"n:       \t{npFFT}\n")
    file.write(f"time(ns):\t{stFFT}\n\n")
    file.close()


def graph(powers:[], studentTimes:[], numpyTimes:[]):
    plt.scatter(powers, studentTimes, color='red', label='My FFT times')
    plt.scatter(powers, numpyTimes, color='blue', label='numpy FFT times')

    plt.yscale('log')
    plt.xlabel('Size (power of 2)')
    plt.ylabel('Time (ns)')
    plt.title('FFT Solve Time')
    plt.xlim([0, 25])
    plt.ylim([10**6, 10**12])

    # Showing the graph
    plt.legend()
    plt.show()


if __name__ == '__main__':
    pows = []
    timeNumpy = []
    timeMyFFT = []

    largestPow = 20

    for pow in range(largestPow + 1):
        print(f'Length of 2^{pow}')

        FFTthis = [random.randint(0, 50) for i in range(2**pow)]

        start = time.time_ns()
        beginFFT(FFTthis)
        end = time.time_ns()
        deltaMyFFT = end - start

        start = time.time_ns()
        np.fft.fft(FFTthis)
        end = time.time_ns()
        deltaNP = end - start

        printToFile(pow, deltaNP, deltaMyFFT)
        pows.append(pow)
        timeNumpy.append(deltaNP)
        timeMyFFT.append(deltaMyFFT)

    print(f"timeNumpy = {timeNumpy}\ntimeMyFFT = {timeMyFFT}\n")
    graph(pows, timeMyFFT, timeNumpy)
