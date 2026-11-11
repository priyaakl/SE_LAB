def parse_collection(text):
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    if text.count(':') != 1:
        raise ValueError("Input must contain exactly one colon")

    material, kg = text.split(':')

    material = material.strip()
    kg = kg.strip()

    if not material:
        raise ValueError("Material cannot be empty")

    if not kg:
        raise ValueError("Weight cannot be empty")

    try:
        weight = float(kg)
    except ValueError:
        raise ValueError("Weight must be a valid number")

    return material.title(), weight


def weight_average(weights_csv):
    if not isinstance(weights_csv, str):
        raise ValueError("Input must be a string")

    if not weights_csv.strip():
        raise ValueError("Weight list cannot be empty")

    try:
        values = [int(r.strip()) for r in weights_csv.split(',')]
    except ValueError:
        raise ValueError("All weights must be valid integers")

    if not values:
        raise ValueError("Weight list cannot be empty")

    return sum(values) // len(values)


def net_points(text):
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    if text.count('|') != 1:
        raise ValueError("Input must contain exactly one |")

    points, penalty = text.split('|')

    points = points.strip()
    penalty = penalty.strip()

    if not points or not penalty:
        raise ValueError("Points and penalty cannot be empty")

    try:
        points = float(points)
        penalty = float(penalty)
    except ValueError:
        raise ValueError("Points and penalty must be valid numbers")

    return max(points * 2 - penalty, 0)


def main():
    print("==== Running parse_collection ====")
    user_input = input("Enter material:weight in kg (e.g. paper:12): ")
    try:
        result = parse_collection(user_input)
        print("Material and Weight:", result)
    except ValueError as e:
        print("Invalid input:", e)

    print("\n==== Running weight_average ====")
    user_input = input("Enter weights in kg as CSV (e.g. 5,12,20): ")
    try:
        result = weight_average(user_input)
        print("Average Weight:", result)
    except ValueError as e:
        print("Invalid input:", e)

    print("\n==== Running net_points ====")
    user_input = input("Enter points|penalty (e.g. 80|10): ")
    try:
        result = net_points(user_input)
        print("Net Points:", result)
    except ValueError as e:
        print("Invalid input:", e)


if __name__ == "__main__":
    main()
