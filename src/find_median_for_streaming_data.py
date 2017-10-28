import heapq
import math

class running_medium:

    def __init__(self):
        # min heap to store higher half elements( right side of the median)
        self.min_heap_right = []
        # max heap to store lower half elements( left side of the median)
        self.max_heap_left = []


    def heappeak(self,heap):
        top = heapq.heappop(heap)
        heapq.heappush(heap,top)
        return top

    def negate(self, num):
        return -num

    def calc_running_median(self, num, median = 0):
        """
        :param num: Incoming new streaming number
        :return: new medium number at this point of time
         At any time we try to make heaps balanced and
            their sizes differ by atmost 1. If heaps are
            balanced,then we declare median as average of
            min_heap_right.top() and max_heap_left.top()
            If heaps are unbalanced,then median is defined
            as the top element of heap of larger size  */

        """

        #  left side heap has more elements
        if len(self.max_heap_left) > len(self.min_heap_right):
            if num < median:
                heapq.heappush(self.min_heap_right, self.negate(heapq.heappop(self.max_heap_left)))
                heapq.heappush(self.max_heap_left, self.negate(num))
            else:
                heapq.heappush(self.min_heap_right, num)
            newmedian = int(math.ceil( (self.negate(self.heappeak(self.max_heap_left)) + self.heappeak(self.min_heap_right))/2.0))

        # both heaps are balanced
        elif len(self.max_heap_left) == len(self.min_heap_right):
            if num < median:
                heapq.heappush(self.max_heap_left,self.negate(num))
                newmedian = self.negate(self.heappeak(self.max_heap_left))
            else:
                heapq.heappush(self.min_heap_right, num)
                newmedian = self.heappeak(self.min_heap_right)

        # right side heap has more elements
        else:
            if num > median:
                heapq.heappush(self.max_heap_left, self.negate(heapq.heappop(self.min_heap_right)))
                heapq.heappush(self.min_heap_right, num)
            else:
                heapq.heappush(self.max_heap_left, self.negate(num))
            newmedian = int(math.ceil((self.heappeak(self.min_heap_right) + self.negate(self.heappeak(self.max_heap_left)))/2.0))

        return newmedian

"""
# driver program to test
a = [5, 15, 10, 20, 3, 100, 200, 300, 50, 15]
b = [250,333]

C00177436|30004|384|1|384
C00384818|02895|250|1|250
C00177436|30750|230|1|230
C00177436|04105|384|1|384
C00384818|02895|292|2|583
C00177436|04105|384|2|768

r = running_medium()
median = 0
for each in b:
    print "new median = "
    newmedian =   r.calc_running_median(each, median)
    print newmedian
    median = newmedian
    print r.max_heap_left
    print r.min_heap_right
"""

