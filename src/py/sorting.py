"""Python implementations of common sorting algorithms."""
from random import randint
from typing import List, Optional

# Type allias for list of ints.
IntArray = List[int]


def insertion_sort(array: IntArray) -> IntArray:
    """Sort and return unsorted input using the insertion sort algorithm
    params:
        array: a list of integers.
    returns:
        mutated version of array with values in non-decreasing order.
    runtime:
        O(n^2) by standard analysis because in worst case both loops execute n times,
        but python list indexing is also O(n), so actually O(n^3) because of the "array[j]"
        calls in the inner loop. This implementation detail will be ignored in subsequent
        analyses.
    """
    n = len(array)
    for i in range(1, n):
        value = array[i]
        j = i
        while j > 0 and array[j-1] > value:
            # Going leftwards through sorted array array[:i],
            # shift elements one index right until proper place for value
            # is found. Then save value at that index.
            array[j] = array[j-1]
            j -= 1
        array[j] = value
    return array


def merge_sort(array: IntArray) -> IntArray:
    """Sort and return unsorted input using the merge sort algorithm
    params:
        array: a list of integers.
    returns:
        new array with values of imput in non-decreasing order.
    runtime:
        - Each recursive call takes T(n/2)
        - merging takes O(n)
        - base case: O(1)
        - Recurence Relation: T(n) = { 2T(n/2) + n if n > 1
                                     { O(1)        if n = 1
        - By master theorem, runtime is O(nlog(n))
    """
    n = len(array)
    if n <= 1:
        # empty list and singleton already sorted.
        return array
    split_point = n//2
    # recurse and sort the left and right halves.
    left_list = merge_sort(array[:split_point])
    right_list = merge_sort(array[split_point:])
    sorted_list = []

    left = 0
    right = 0
    # merge the lists as follows:
    #  0. Create pointers to 0th elements of each list.
    #  1. Pick the smaller of the pointed at elements.
    #  2. Append that to sorted list.
    #  3. Move pointer to selected element to next element.
    for _ in range(n):
        if left == len(left_list):
            sorted_list.append(right_list[right])
            right += 1
        elif right == len(right_list):
            sorted_list.append(left_list[left])
            left += 1
        elif left_list[left] < right_list[right]:
            sorted_list.append(left_list[left])
            left += 1
        else:
            sorted_list.append(right_list[right])
            right += 1
    return sorted_list


def heap_sort(array: IntArray) -> IntArray:
    """Sort and return unsorted input using the heap sort algorithm

    params:
        array: an unsorted list of integers.
    returns:
        mutated version of array with values in non-decreasing order.
    runtime:
        O(nlogn): max_heapify runs n times and has a runtime of O(log(n)),
        dominating O(n) term from build_max_heap
    """
    def _max_heapify(heap: IntArray, i) -> IntArray:
        """Insert integer at index'i' into the given "heap".
        params:
            heap: an array sorted such that the left and right
                subtrees of index i are max heaps.
            i: integer to be the root of the new heap.
        returns:
            mutated version of heap having i added in the right
            possition.
        runtime:
            Starts at index n, then n/2, ... n/2^i -> log(n)
        """
        left = 2 * i
        right = 2 * i + 1
        # Compare i to its children and find the largest one.
        largest = i
        if left < len(heap) and heap[left] > heap[i]:
            largest = left
        if right < len(heap) and heap[right] > heap[largest]:
            largest = right
        # if i not largest, swap with largest child and recurse.
        if largest != i:
            heap[i], heap[largest] = heap[largest], heap[i]
            return _max_heapify(heap, largest)
        return heap

    def _build_max_heap(array: IntArray) -> IntArray:
        """Sort array into a max heap.

        params:
            array: unsorted array of integers.
        returns:
            mutated version of array fitting following constraints.
               1. "Parent" node is at ⌊i/2⌋ if i != 0, else no parent.
                2. Left child is at index i*2
                3. Right child is at index i*2 +1
                4. For all i, array[Parent(i)] >= array(i)
        runtime:
            O(n), by math too complicated to fit in a docstring.
            Source: CLRS, page 159.
        """
        n = len(array)
        for i in range(n//2 + 1, -1, -1):
            array = _max_heapify(array, i)
        return array

    n = len(array)
    # make into a heap, with largest value at index 0
    _build_max_heap(array)
    for i in range(n-1, -1, -1):
        # For each i from 0 to n, move the largest element
        # to index i and re-heapify. Then, array[:i] is a
        # max heap, so iterate and do the same until entire list
        # is sorted.
        array[0], array[i] = array[i], array[0]
        old_array = array.copy()
        array = _max_heapify(array[:i], 0) + old_array[i:]
    return array


def quick_sort(
        array: IntArray,
        start: Optional[int] = None,
        end: Optional[int] = None
) -> IntArray:
    """Sort and return unsorted input using a randomized implementation of
    the quicksort algorithm.

    params:
        array: an unsorted list of integers.
        start: starting index of portion to be sorted.
        end: ending index of portion to be sorted.
    returns:
        mutated version of array with values in non-decreasing order.
    runtime:
        Worst Case:
            Partition is unbalanced, and we have one n-1 element
            subproblem and one 0 element subproblem (i.e. array is sorted)
            Then, recurence is:
                T(n) = O(1) (constant time to just return)                          if n <= 1
                T(n) = O(large subproblemn) + O(empty subproblem) + O(partitioning) else.
            So
                T(n) = T(n-1) + O(n)     if n > 1
                T(n) = O(1)              else
             This forms an arithmatic sequence
             T(n) = O(n) + O(n-1) + O(n-2) ... + O(1) = O(n^2)

        Expected Time:
            The running time of quicksort is the sum of
                1. The total number of calls to partiiton and the constant amount
                    of associated work. There will be at most n calls to partition,
                    in the case that i increases by one each time.

                2. The total number of times the inner for loop executes,
                    equal to the number of times the comparison "if array[j] <= x:"
                    is executed (calls this X)
            Thus, expected runtime is O(n + E[X])

            It is not difficult to calculate (with calculations too length for a docstring)
            that with the pivot randomly chosen each time, the value of E[X] is O(nlog(n))

            Thus, expected runtime is O(n + nlog(n)) = O(nlog(n))
    """
    def _partition(array: IntArray, start: int, end: int) -> int:
        """Arrange array around some pivot i such that for all j:

            array[i] > array[j] if i > j
            array[i] > array[j] if i < j

        Then return pivot i.

        params:
            array: an unsorted list of integers.
            start: starting index of portion to be partitioned.
            end: ending index of portion to be partitioned.
        returns:
            pivot i, as described above
        runtime:
            O(end-start), since have to iterate over that range
            and perform constant time operations.

        """
        # Swap end and some random element in the array
        # so the value of x is always random.
        rand = randint(start, end)
        array[rand], array[end] = array[end], array[rand]
        x = array[end]
        i = start - 1
        for j in range(start, end):
            # If jth element is less than final value
            # increase pivot by one and swap j and pivot.
            if array[j] <= x:
                i += 1
                array[i], array[j] = array[j], array[i]
        i += 1
        array[i], array[end] = array[end], array[i]
        return i

    # On initial call, set start and end.
    if start is None:
        start = 0
    if end is None:
        end = len(array) - 1

    # Implicit base case: start not less than end, do nothing since array is singleton
    if start < end:
        pivot = _partition(array, start, end)
        quick_sort(array, start, pivot - 1)
        quick_sort(array, pivot + 1, end)
    return array


def counting_sort(input_array: IntArray) -> IntArray:
    """Sort and return unsorted input using the counting sort algorithm

    params:
        array: an unsorted list of integers.
    returns:
        a new array with integers of input sorted in non-decreasing order.
    runtime:
        O(n + K), where k is largest element in input minus the smallest.
        It takes O(K) time to allocate empty array of length K to write to,
        and O(n) time to find what the value of K is. All other operations
        are either O(n) or O(k), so total is still O(n + k)
    """
    if len(input_array) == 0:
        return []

    # Need to shift array over by magnitute of
    # smallest value if negative element present.
    shift = abs(min(min(input_array), 0))
    K = max(input_array) + shift

    N = len(input_array)
    # Need to acount for 0-indexing.
    temp_array = [0 for _ in range(K + 1)]
    output_array = [0 for _ in range(N)]

    for i in range(0, N):
        # set temp_array[i] to the number of elements of value i
        temp_array[input_array[i] + shift] += 1
    for j in range(1, K + 1):
        # now set temp_array[j] to number of elements of value <= i
        temp_array[j] += temp_array[j-1]
    for k in range(N - 1, -1, -1):
        # For each element in input array, place in position
        # where there are k elements smaller than it.
        # In case of duplicates, decriment count so next element
        # is same value.
        element = input_array[k]
        output_array[temp_array[element + shift]-1] = element
        temp_array[element + shift] -= 1
    return output_array
