def quick_sort(arr):
    def partition(low, high):
        pivot = arr[high]
        i = low
        for j in range(low, high):
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[high] = arr[high], arr[i]
        return i

    def quicksort(low, high):
        if low >= high:
            return
        pivot_index = partition(low, high)
        quicksort(low, pivot_index - 1)
        quicksort(pivot_index + 1, high)

    quicksort(0, len(arr) - 1)
    return arr