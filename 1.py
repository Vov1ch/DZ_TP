while True:
    print("\n--- КАЛЬКУЛЯТОР-ШАГОМЕТР ---")
    
    distance = float(input("Введите расстояние (в км): "))
    time = float(input("Введите время ходьбы (в часах): "))
    gender = input("Введите пол (м/ж): ").lower()
    
    # Средняя скорость
    speed = distance / time
    
    # Перевод расстояния в метры
    distance_m = distance * 1000
    
    # Длина шага
    if gender == "м":
        step_length = 0.8
    elif gender == "ж":
        step_length = 0.5
    else:
        print("Некорректный ввод пола!")
        continue
    
    # Количество шагов
    steps = distance_m / step_length
    
    # Оценка состояния здоровья
    if 2 <= speed <= 3:
        health = "побольше ходи!!!"
    elif 4 <= speed <= 5:
        health = "продолжай в том же духе!"
    elif 6 <= speed <= 10:
        health = "а ты герой!"
    else:
        health = "скорость вне диапазона оценки"
    
    print("\n--- РЕЗУЛЬТАТЫ ---")
    print(f"Средняя скорость: {speed:.2f} км/ч")
    print(f"Количество шагов: {int(steps)}")
    print(f"Состояние здоровья: {health}")
    
    repeat = input("\nХотите выполнить расчёт ещё раз? (да/нет): ").lower()
    if repeat != "да":
        break
