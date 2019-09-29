"""Python implementations of common sorting algorithms."""
from typing import List


def insertion_sort(array: List[int]) -> List[int]:
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


def merge_sort(array: List[int]) -> List[int]:
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


def heap_sort(array: List[int]) -> List[int]:
    """Sort and return unsorted input using the heap sort algorithm

    params:
        array: an unsorted list of integers.
    returns:
        mutated version of array with values in non-decreasing order.
    runtime:
        O(nlogn): max_heapify runs n times and has a runtime of O(log(n)),
        dominating O(n) term from build_max_heap
    """
    def _max_heapify(heap: List[int], i) -> List[int]:
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

    def _build_max_heap(array: List[int]) -> List[int]:
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
