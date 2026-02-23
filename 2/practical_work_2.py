import json
import random
from datetime import datetime
from pathlib import Path


DATA_FILE = Path("meals_history.json")


PRODUCT_NAMES = {
    "молочное": ["молоко", "кефир", "творог", "йогурт", "сыр"],
    "сладкое": ["шоколад", "печенье", "вафли", "зефир", "мед"],
    "овощи": ["огурец", "помидор", "морковь", "брокколи", "перец"],
    "фрукты": ["яблоко", "банан", "апельсин", "груша", "киви"],
    "мясо": ["курица", "говядина", "индейка", "свинина", "телятина"],
}


RANGES = {
    "молочное": {"calories": (45, 360), "proteins": (2, 25), "fats": (0, 30), "carbs": (2, 20)},
    "сладкое": {"calories": (250, 600), "proteins": (1, 10), "fats": (1, 35), "carbs": (40, 90)},
    "овощи": {"calories": (15, 90), "proteins": (1, 5), "fats": (0, 2), "carbs": (2, 15)},
    "фрукты": {"calories": (30, 120), "proteins": (0, 3), "fats": (0, 1), "carbs": (6, 30)},
    "мясо": {"calories": (100, 350), "proteins": (15, 35), "fats": (2, 30), "carbs": (0, 2)},
}


def generate_products(seed=42):
    random.seed(seed)
    products = []
    product_id = 1
    for category, names in PRODUCT_NAMES.items():
        for name in names:
            limits = RANGES[category]
            product = {
                "id": product_id,
                "name": name,
                "category": category,
                "calories": random.randint(*limits["calories"]),
                "proteins": round(random.uniform(*limits["proteins"]), 1),
                "fats": round(random.uniform(*limits["fats"]), 1),
                "carbs": round(random.uniform(*limits["carbs"]), 1),
            }
            products.append(product)
            product_id += 1
    return products


def print_products(products):
    print("\nСписок продуктов (на 100 г):")
    for p in products:
        print(
            f"{p['id']:>2}. {p['name']:<10} | {p['category']:<9} | "
            f"ккал: {p['calories']:<4} | Б: {p['proteins']:<5} Ж: {p['fats']:<5} У: {p['carbs']:<5}"
        )


def choose_numeric_parameter():
    params = {"1": "calories", "2": "proteins", "3": "fats", "4": "carbs"}
    print("\nВыберите параметр:")
    print("1 - калорийность")
    print("2 - белки")
    print("3 - жиры")
    print("4 - углеводы")
    selected = input("Ваш выбор: ").strip()
    return params.get(selected)


def filter_products(products):
    parameter = choose_numeric_parameter()
    if not parameter:
        print("Неверный выбор параметра.")
        return
    try:
        limit = float(input("Введите максимальное значение: ").strip())
    except ValueError:
        print("Некорректное число.")
        return

    filtered = list(filter(lambda product: product[parameter] <= limit, products))
    if not filtered:
        print("Подходящих продуктов не найдено.")
        return

    print("\nПодходящие продукты:")
    print_products(filtered)


def sort_products(products):
    parameter = choose_numeric_parameter()
    if not parameter:
        print("Неверный выбор параметра.")
        return products
    reverse_choice = input("Сортировать по убыванию? (д/н): ").strip().lower()
    reverse = reverse_choice == "д"
    return sorted(products, key=lambda product: product[parameter], reverse=reverse)


def calculate_totals(chosen_items):
    totals = {"calories": 0.0, "proteins": 0.0, "fats": 0.0, "carbs": 0.0}
    for item in chosen_items:
        grams_multiplier = item["grams"] / 100
        totals["calories"] += item["product"]["calories"] * grams_multiplier
        totals["proteins"] += item["product"]["proteins"] * grams_multiplier
        totals["fats"] += item["product"]["fats"] * grams_multiplier
        totals["carbs"] += item["product"]["carbs"] * grams_multiplier
    return {key: round(value, 1) for key, value in totals.items()}


def load_history():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_history(history):
    DATA_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


def add_meal(products):
    meal_name = input("\nНазвание приема пищи (например, Обед): ").strip()
    if not meal_name:
        print("Название не может быть пустым.")
        return

    sorted_products = sort_products(products)
    print_products(sorted_products)
    by_id = {product["id"]: product for product in products}
    chosen = []

    print("\nДобавьте продукты в прием пищи.")
    print("Введите ID продукта и граммы. Для завершения оставьте ID пустым.")

    while True:
        raw_id = input("ID продукта: ").strip()
        if raw_id == "":
            break
        if not raw_id.isdigit() or int(raw_id) not in by_id:
            print("Такого ID нет.")
            continue
        try:
            grams = float(input("Граммы: ").strip())
        except ValueError:
            print("Некорректные граммы.")
            continue
        if grams <= 0:
            print("Граммы должны быть больше 0.")
            continue
        chosen.append({"product": by_id[int(raw_id)], "grams": grams})

    if not chosen:
        print("Прием пищи не добавлен: список пуст.")
        return

    totals = calculate_totals(chosen)
    print(f"\n{meal_name}")
    for item in chosen:
        print(f"- {item['product']['name']} {item['grams']} г")
    print(f"Суммарная калорийность: {totals['calories']} ккал")
    print(f"Белки: {totals['proteins']} г")
    print(f"Жиры: {totals['fats']} г")
    print(f"Углеводы: {totals['carbs']} г")

    history = load_history()
    history.append(
        {
            "meal_name": meal_name,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": [
                {
                    "name": item["product"]["name"],
                    "category": item["product"]["category"],
                    "grams": item["grams"],
                }
                for item in chosen
            ],
            "totals": totals,
        }
    )
    save_history(history)
    print(f"Прием пищи сохранен в {DATA_FILE}.")


def show_history():
    history = load_history()
    if not history:
        print("\nИстория приемов пищи пуста.")
        return

    print("\nИстория приемов пищи:")
    for idx, meal in enumerate(history, start=1):
        print(f"\n{idx}. {meal['meal_name']} ({meal['created_at']})")
        for item in meal["items"]:
            print(f"- {item['name']} ({item['category']}): {item['grams']} г")
        print(
            f"Итого -> ккал: {meal['totals']['calories']}, "
            f"Б: {meal['totals']['proteins']}, Ж: {meal['totals']['fats']}, У: {meal['totals']['carbs']}"
        )


def main():
    products = generate_products()
    actions = {
        "1": lambda: print_products(products),
        "2": lambda: filter_products(products),
        "3": lambda: add_meal(products),
        "4": show_history,
    }

    while True:
        print("\nМеню:")
        print("1 - Показать все продукты")
        print("2 - Фильтр продуктов по параметру")
        print("3 - Добавить прием пищи")
        print("4 - Показать историю приемов пищи")
        print("0 - Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "0":
            print("Работа завершена.")
            break

        action = actions.get(choice)
        if not action:
            print("Неверный пункт меню.")
            continue
        action()


if __name__ == "__main__":
    main()
