def calculate_statistics(numbers):
    """Calculate statistics for a list of numbers.
    
    Args:
        numbers: List of numeric values.
    
    Returns:
        Tuple of (average, maximum, minimum) or None if list is empty.
    """
    if not numbers:
        return None
    total = 0
    count = 0
    maximum = numbers[0]
    
    for num in numbers:
        total += num
        count += 1
        if num > maximum:  # Track maximum value during iteration
            maximum = num
    
    average = total / count
    minimum = min(numbers)
    positive = total > 0  # Check if sum is positive
    
    stats = {"average": average, "max": maximum}  # Store selected statistics
    
    if average == maximum:  # All numbers are equal
        print("Equal")
    
    return average, maximum, minimum

    
result = calculate_statistics([1, 2, 3, 4, 5])