from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sort', methods=['POST'])
def sort():
    data = request.get_json()
    array = data['array']
    algorithm = data['algorithm']
    sorted_array, steps, duration = sort_array(array, algorithm)
    return jsonify({'sorted_array': sorted_array, 'steps': steps, 'duration': duration})


def sort_array(array, algorithm):
    start_time = time.perf_counter()
    if algorithm == 'insertion':
        sorted_array, steps = insertion_sort(array)
    elif algorithm == 'bubble':
        sorted_array, steps = bubble_sort(array)
    elif algorithm == 'selection':
        sorted_array, steps = selection_sort(array)
    elif algorithm == 'merge':
        sorted_array, steps = merge_sort(array)
    elif algorithm == 'quick':
        sorted_array, steps = quick_sort(array)
    elif algorithm == 'heap':
        sorted_array, steps = heap_sort(array)
    elif algorithm == 'shell':
        sorted_array, steps = shell_sort(array)
    elif algorithm == 'counting':
        sorted_array, steps = counting_sort(array)
    elif algorithm == 'radix':
        sorted_array, steps = radix_sort(array)
    else:
        return array, [], 0
    end_time = time.perf_counter()
    duration = end_time - start_time
    return sorted_array, steps, duration

# Other sorting functions remain the same


def insertion_sort(array):
    steps = []
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            steps.append((array.copy(), j + 1))
            j -= 1
        array[j + 1] = key
        steps.append((array.copy(), j + 1))
    return array, steps


def bubble_sort(array):
    steps = []
    n = len(array)
    for i in range(n):
        for j in range(0, n-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                steps.append((array.copy(), j + 1))
    return array, steps


def selection_sort(array):
    steps = []
    for i in range(len(array)):
        min_idx = i
        for j in range(i+1, len(array)):
            if array[min_idx] > array[j]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
        steps.append((array.copy(), i))
    return array, steps


def merge_sort(array):
    steps = []
    _merge_sort(array, 0, len(array) - 1, steps)
    return array, steps


def _merge_sort(array, left, right, steps):
    if left < right:
        mid = (left + right) // 2
        _merge_sort(array, left, mid, steps)
        _merge_sort(array, mid + 1, right, steps)
        merge(array, left, mid, right, steps)


def merge(array, left, mid, right, steps):
    left_copy = array[left:mid + 1]
    right_copy = array[mid + 1:right + 1]
    left_copy_index = 0
    right_copy_index = 0
    sorted_index = left
    while left_copy_index < len(left_copy) and right_copy_index < len(right_copy):
        if left_copy[left_copy_index] <= right_copy[right_copy_index]:
            array[sorted_index] = left_copy[left_copy_index]
            left_copy_index += 1
        else:
            array[sorted_index] = right_copy[right_copy_index]
            right_copy_index += 1
        steps.append((array.copy(), sorted_index))
        sorted_index += 1
    while left_copy_index < len(left_copy):
        array[sorted_index] = left_copy[left_copy_index]
        steps.append((array.copy(), sorted_index))
        left_copy_index += 1
        sorted_index += 1
    while right_copy_index < len(right_copy):
        array[sorted_index] = right_copy[right_copy_index]
        steps.append((array.copy(), sorted_index))
        right_copy_index += 1
        sorted_index += 1


def quick_sort(array):
    steps = []
    _quick_sort(array, 0, len(array) - 1, steps)
    return array, steps


def _quick_sort(array, low, high, steps):
    if low < high:
        pi = partition(array, low, high, steps)
        _quick_sort(array, low, pi - 1, steps)
        _quick_sort(array, pi + 1, high, steps)


def partition(array, low, high, steps):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] <= pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
            steps.append((array.copy(), j))
    array[i + 1], array[high] = array[high], array[i + 1]
    steps.append((array.copy(), i + 1))
    return i + 1


def heap_sort(array):
    steps = []
    n = len(array)
    for i in range(n // 2 - 1, -1, -1):
        heapify(array, n, i, steps)
    for i in range(n - 1, 0, -1):
        array[i], array[0] = array[0], array[i]
        steps.append((array.copy(), i))
        heapify(array, i, 0, steps)
    return array, steps


def heapify(array, n, i, steps):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and array[i] < array[left]:
        largest = left
    if right < n and array[largest] < array[right]:
        largest = right
    if largest != i:
        array[i], array[largest] = array[largest], array[i]
        steps.append((array.copy(), i))
        heapify(array, n, largest, steps)


def shell_sort(array):
    steps = []
    n = len(array)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = array[i]
            j = i
            while j >= gap and array[j - gap] > temp:
                array[j] = array[j - gap]
                steps.append((array.copy(), j))
                j -= gap
            array[j] = temp
            steps.append((array.copy(), j))
        gap //= 2
    return array, steps


def counting_sort(array):
    steps = []
    max_val = max(array)
    m = max_val + 1
    count = [0] * m
    for a in array:
        count[a] += 1
    i = 0
    for a in range(m):
        for c in range(count[a]):
            array[i] = a
            steps.append((array.copy(), i))
            i += 1
    return array, steps


def radix_sort(array):
    steps = []
    max_val = max(array)
    exp = 1
    while max_val // exp > 0:
        _counting_sort_for_radix(array, exp, steps)
        exp *= 10
    return array, steps


def _counting_sort_for_radix(array, exp, steps):
    n = len(array)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        index = array[i] // exp
        count[index % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    i = n - 1
    while i >= 0:
        index = array[i] // exp
        output[count[index % 10] - 1] = array[i]
        count[index % 10] -= 1
        i -= 1
    for i in range(n):
        array[i] = output[i]
        steps.append((array.copy(), i))


if __name__ == '__main__':
    app.run(debug=True)
