def get_user_input():
    """Get and validate weight and height from the user."""
    try:
        weight = float(input("Enter your weight in kg: "))
        height = float(input("Enter your height (e.g., 5.7): "))

        # Validate weight
        if weight <= 0:
            print("Error: Weight must be greater than zero.")
            return None, None

        # Validate height
        if height <= 0:
            print("Error: Height must be greater than zero.")
            return None, None

        # Convert input such as 5.7 into 5 feet 7 inches
        feet = int(height)
        inches = round((height - feet) * 10)

        # Validate feet
        if feet < 3 or feet > 8:
            print("Error: Height must be between 3 and 8 feet.")
            return None, None

        # Validate inches
        if inches < 0 or inches > 11:
            print("Error: Inches must be between 0 and 11.")
            return None, None

        return weight, (feet, inches)

    except ValueError:
        print("Error: Please enter valid numbers.")
        return None, None


def convert_height_to_meters(feet, inches):
    """Convert feet and inches to meters."""
    total_inches = (feet * 12) + inches
    height_meters = total_inches * 0.0254

    return height_meters


def calculate_bmi(weight, height_meters):
    """Calculate BMI."""
    bmi = weight / (height_meters ** 2)

    return bmi


def get_bmi_category(bmi):
    """Return the BMI category."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def display_result(weight, feet, inches, height_meters, bmi, category):
    """Display the BMI result."""
    print("\n===== BMI RESULT =====")
    print(f"Weight: {weight:.2f} kg")
    print(f"Height: {feet} ft {inches} in")
    print(f"Height in meters: {height_meters:.2f} m")
    print(f"BMI: {bmi:.2f}")
    print(f"Category: {category}")


def main():
    """Run the BMI calculator."""
    print("===== BMI CALCULATOR =====")

    weight, height = get_user_input()

    if weight is None:
        return

    feet, inches = height

    height_meters = convert_height_to_meters(feet, inches)

    bmi = calculate_bmi(weight, height_meters)

    category = get_bmi_category(bmi)

    display_result(
        weight,
        feet,
        inches,
        height_meters,
        bmi,
        category
    )


if __name__ == "__main__":
    main()