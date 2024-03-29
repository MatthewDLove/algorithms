import pytest  # type: ignore

from random import randint

from sorting import counting_sort, heap_sort, insertion_sort, merge_sort, quick_sort


ALGORITHMS = [counting_sort, heap_sort, insertion_sort, merge_sort, quick_sort]


class TestDeterministic:
    @pytest.mark.parametrize('sorting_algo', ALGORITHMS)
    @pytest.mark.parametrize(
        'unsorted_array, sorted_array',
        [
            ([], []),
            ([1, 2, 3], [1, 2, 3]),
            ([2, 3, 0, 1], [0, 1, 2, 3]),
            ([100, 5, -16, 85, -7, 7, 1], [-16, -7, 1, 5, 7, 85, 100]),
        ]
    )
    def test_unsorted_lists(self, sorting_algo, unsorted_array, sorted_array):
        assert sorting_algo(unsorted_array) == sorted_array


class TestProbabilistic:
    """Putting a lot of faith in python's correctness, tests long psudo-randomly generated
    lists against python's built in sort function (using the "TimSort" algorithm)
    """
    @pytest.mark.parametrize('N', [10, 1000, 10000])
    @pytest.mark.parametrize('sorting_algo', ALGORITHMS)
    def test_random_list(self, N, sorting_algo):
        array = [randint(-N, N) for _ in range(N)]
        expected = array[:]
        expected.sort()
        assert sorting_algo(array) == expected
