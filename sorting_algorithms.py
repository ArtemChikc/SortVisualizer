# this is a collection of sorting algorithms

# you can add your own here by adding a function
# that will accept a list of numbers as input, and it should use the "yield" method


import random



def quicksort_gen(arr):
    stack = [(0, len(arr)-1)]
    while stack:
        low, high = stack.pop()
        if low>=high:
            continue
        pivot = arr[high]
        i = low
        for j in range(low, high):
            if arr[j]<pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                yield
        arr[i], arr[high] = arr[high], arr[i]
        yield
        stack.append((low, i-1))
        stack.append((i+1, high))


def beton_sort_gen(arr):
    while not all(arr[i]<=arr[i+1] for i in range(len(arr)-1)):
        for i in range(len(arr)-1):
            if arr[i]>arr[i+1]:
                start = i-1
                break
        for i in range(start, len(arr)):
            for j in range(len(arr)-1, i, -1):
                if arr[i] > arr[j]:
                    arr[i], arr[j] = arr[j], arr[i]
                    yield


def bubble_sort_gen(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j]>arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                yield


def selection_sort_gen(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j]<arr[min_idx]:
                min_idx = j
                yield
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield


def insertion_sort_gen(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j>=0 and key<arr[j]:
            arr[j+1] = arr[j]
            j -= 1
            yield
        arr[j+1] = key
        yield


def merge_sort_gen(arr):
    def merge(arr, l, m, r):
        n1 = m-l+1
        n2 = r-m
        L = [0]*n1
        R = [0]*n2
        for i in range(n1):
            L[i] = arr[l+i]
        for j in range(n2):
            R[j] = arr[m+1+j]
        i = j = 0
        k = l
        while i<n1 and j<n2:
            if L[i]<=R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            yield
        while i<n1:
            arr[k] = L[i]
            i += 1
            k += 1
            yield
        while j<n2:
            arr[k] = R[j]
            j += 1
            k += 1
            yield

    def merge_sort(arr, l, r):
        if l<r:
            m = (l+r)//2
            yield from merge_sort(arr, l, m)
            yield from merge_sort(arr, m+1, r)
            yield from merge(arr, l, m, r)

    yield from merge_sort(arr, 0, len(arr)-1)


def heap_sort_gen(arr):
    def heapify(arr, n, i):
        largest = i
        l = 2*i+1
        r = 2*i+2
        if l<n and arr[i]<arr[l]:
            largest = l
        if r<n and arr[largest]<arr[r]:
            largest = r
        if largest!=i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield
            yield from heapify(arr, n, largest)

    n = len(arr)
    for i in range(n//2-1, -1, -1):
        yield from heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield
        yield from heapify(arr, i, 0)


def shell_sort_gen(arr):
    n = len(arr)
    gap = n//2
    while gap>0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j>=gap and arr[j-gap]>temp:
                arr[j] = arr[j-gap]
                j -= gap
                yield
            arr[j] = temp
            yield
        gap //= 2


def counting_sort_gen(arr):
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val-min_val+1
    count = [0]*range_val
    output = [0]*len(arr)
    
    for i in range(len(arr)):
        count[arr[i]-min_val] += 1
        yield
    
    for i in range(1, len(count)):
        count[i] += count[i-1]
        yield
    
    for i in range(len(arr)-1, -1, -1):
        output[count[arr[i]-min_val]-1] = arr[i]
        count[arr[i]-min_val] -= 1
        yield
    
    for i in range(len(arr)):
        arr[i] = output[i]
        yield


def radix_sort_gen(arr):
    def counting_sort(arr, exp):
        n = len(arr)
        output = [0]*n
        count = [0]*10
        
        for i in range(n):
            index = arr[i]//exp
            count[index%10] += 1
            yield
        
        for i in range(1, 10):
            count[i] += count[i-1]
            yield
        
        i = n-1
        while i>=0:
            index = arr[i]//exp
            output[count[index%10] - 1] = arr[i]
            count[index%10] -= 1
            i -= 1
            yield
        
        for i in range(n):
            arr[i] = output[i]
            yield

    max_val = max(arr)
    exp = 1
    while max_val//exp>0:
        yield from counting_sort(arr, exp)
        exp *= 10


def cocktail_sort_gen(arr):
    n = len(arr)
    swapped = True
    start = 0
    end = n-1
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i]>arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = True
                yield
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end-1, start-1, -1):
            if arr[i]>arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = True
                yield
        start += 1


def bogo_sort_gen(arr):
    while not all(arr[i]<=arr[i+1] for i in range(len(arr)-1)):
        random.shuffle(arr)
        yield


def gnome_sort_gen(arr):
    i = 0
    while i<len(arr):
        if i==0 or arr[i]>=arr[i-1]:
            i += 1
        else:
            arr[i], arr[i-1] = arr[i-1], arr[i]
            i -= 1
            yield



SORT_ALGORITHMS = {
    "Quick Sort": quicksort_gen,
    "Bubble Sort": bubble_sort_gen,
    "Selection Sort": selection_sort_gen,
    "Insertion Sort": insertion_sort_gen,
    "Merge Sort": merge_sort_gen,
    "Heap Sort": heap_sort_gen,
    "Shell Sort": shell_sort_gen,
    "Counting Sort": counting_sort_gen,
    "Radix Sort": radix_sort_gen,
    "Cocktail Sort": cocktail_sort_gen,
    "Bogo Sort": bogo_sort_gen,
    "Gnome Sort": gnome_sort_gen,
    "Beton Sort": beton_sort_gen # this is my algorithm)
}