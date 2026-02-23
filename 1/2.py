import math

print("\n--- КАЛЬКУЛЯТОР РЕМОНТА ---")

perimeter = float(input("Введите периметр комнаты (в м): "))
height = float(input("Введите высоту потолка (в м): "))
repair_type = input("Введите вид ремонта (обои/краска): ").lower()

# Площадь стен
wall_area = perimeter * height

if repair_type == "обои":
    roll_length = float(input("Введите длину рулона (в м): "))
    roll_width = float(input("Введите ширину рулона (в м): "))
    roll_price = float(input("Введите стоимость одного рулона: "))
    
    roll_area = roll_length * roll_width
    rolls_needed = math.ceil(wall_area / roll_area)
    total_cost = rolls_needed * roll_price
    
    print("\n--- РЕЗУЛЬТАТ ---")
    print(f"Площадь стен: {wall_area:.2f} м²")
    print(f"Необходимое количество рулонов: {rolls_needed}")
    print(f"Общая стоимость: {total_cost:.2f} руб.")

elif repair_type == "краска":
    paint_consumption = float(input("Введите расход краски (л на 1 м²): "))
    paint_price = float(input("Введите стоимость 1 литра краски: "))
    
    liters_needed = math.ceil(wall_area * paint_consumption)
    total_cost = liters_needed * paint_price
    
    print("\n--- РЕЗУЛЬТАТ ---")
    print(f"Площадь стен: {wall_area:.2f} м²")
    print(f"Необходимое количество краски: {liters_needed} л")
    print(f"Общая стоимость: {total_cost:.2f} руб.")

else:
    print("Некорректный вид ремонта!")
