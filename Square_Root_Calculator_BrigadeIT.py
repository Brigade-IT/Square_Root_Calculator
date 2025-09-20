import cmath
from decimal import Decimal, getcontext


# Функция для вывода текста пользователю и получения его ответа на выбранном языке
def prompt(lang, ru_text, en_text):
    return input(ru_text if lang == '1' else en_text)


# Функция для вывода текста (print) на выбранном языке
def show(lang, ru_text, en_text):
    print(ru_text if lang == '1' else en_text)


# Функция для проверки и ввода числа
# type_root == '1' → арифметический корень (только float ≥ 0)
# type_root == '2' → алгебраический корень (поддержка комплексных чисел)
def input_number(user_input, lang, type_root):
    if type_root == '1':
        while True:
            # заменяем запятую и пробелы для удобства
            user_input = user_input.replace(',', '.').replace(' ', '')
            try:
                user_input = float(user_input)
                # Проверка на отрицательное число
                if user_input < 0:
                    user_input = prompt(lang,
                                        'Число должно быть больше или равно нулю\nВведите число для извлечения корня: ',
                                        'The number must be greater than or equal to zero\nEnter a number to extract the root: ')

                    continue
                return user_input
            except:
                user_input = prompt(lang, 'Ошибка, вы ввели не число\nВведите число для извлечения корня: ',
                                    'Error, you entered an invalid number\nEnter a number to extract the root: ')
                user_input = user_input.replace(',', '.')
    else:
        while True:
            # Поддержка комплексных чисел (замена i → j для Python)
            user_input = user_input.replace('i', 'j').replace(',', '.').replace(' ', '')
            try:
                return complex(user_input)
            except:
                user_input = prompt(lang, 'Ошибка, вы ввели не число\nВведите число для извлечения корня: ',
                                    'Error, you entered an invalid number\nEnter a number to extract the root: ')


# Функция для форматирования комплексных чисел с заданной точностью
def format_complex(z, accuracy):
    real = z.real
    imag = z.imag
    if imag == 0:
        return f"{real:.{accuracy}f}"
    elif real == 0:
        return f"{imag:.{accuracy}f}i"
    else:
        sign = '+' if imag > 0 else '-'
        return f"{real:.{accuracy}f}{sign}{abs(imag):.{accuracy}f}i"


# Главное меню программы
def menu(lang):
    value = prompt(lang, '1 - Вычисление корней\n2 - Поменять язык\n3 - Закрыть программу\nВведите число: ',
                   '1 - Calculating roots\n2 - Change language\n3 - Close the program\nEnter the number: ')
    return get_valid_choice(value, ['1', '2', '3'], lang)


# Функция возвращает два квадратных корня числа
def sqrt_roots(z: complex):
    root = cmath.sqrt(z)
    return [root, -root]


# Проверка, что введённое значение входит в список допустимых
def get_valid_choice(user_input, sample, lang):
    if user_input not in sample:
        while user_input not in sample:
            # Если список допустимых значений небольшой — выводим их
            if len(sample) < 20:
                print('Ошибка, введите одно из этих чисел: ', end='') if lang == '1' \
                    else print('Error, please enter one of these numbers: ', end='')
                for i in sample:
                    print(f'{i}, ', end='') if i != sample[-1] else print(i)
            else:
                # Если список большой — выводим только сообщение об ошибке
                show(lang, 'Ошибка, число введено неверно', 'Error, the number entered is incorrect')
            # Запрашиваем повторный ввод
            user_input = prompt(lang, 'Введите число: ', 'Enter the number: ')
    return user_input


# Определение языка интерфейса
def identify_language():
    lang = input('1 - Русский\n2 - English\nВыберите язык \\ Select language: ')
    while lang != '1' and lang != '2':
        lang = input('Ошибка, нужно ввести 1 или 2 \\ Error, please enter 1 or 2: ')
    show(lang, 'Привет! Это программа для извлечения квадратных корней.',
         'Hello! This is a program for extracting square roots.')
    return lang


# Выбор типа корня: арифметический или алгебраический
def choose_type_root(lang):
    type_root = prompt(lang, '1 - арифметический\n2 - алгебраический\nВведите число: ',
                       '1 - arithmetic\n2 - algebraic\nEnter the number: ')
    return get_valid_choice(type_root, ['1', '2'], lang)


# Выбор точности вычислений
def choose_accuracy(lang, type_root):
    if type_root == '2':
        accuracy = prompt(lang, 'Введите количество чисел после запятой (не больше 15)\nВведите число: ',
                          'Enter the number of digits after the decimal point (up to 15)\nEnter the number: ')
        accuracy = int(get_valid_choice(accuracy, [str(i) for i in range(0, 16)], lang))
    else:
        accuracy = prompt(lang, 'Введите количество чисел после запятой (не больше 5 000)\nВведите число: ',
                          'Enter the number of digits after the decimal point (up to 5 000)\nEnter the number: ')
        accuracy = int(get_valid_choice(accuracy, [str(i) for i in range(0, 5001)], lang))
        # Добавляем запас точности для Decimal
        getcontext().prec = accuracy + 10
    return accuracy


# Запрос числа для вычисления корня
def choose_number(lang, type_root):
    number = prompt(lang, 'Введите число для извлечения корня: ', 'Enter a number to extract the root: ')
    number = input_number(number, lang, type_root)
    return number


# Основная функция программы
def program(lang):
    type_root = choose_type_root(lang)
    accuracy = choose_accuracy(lang, type_root)
    number = choose_number(lang, type_root)

    if number == 0:
        # Отдельный случай для 0
        number = 0
        show(lang, f'Результат: {number:.{accuracy}f}', f'Result: {number:.{accuracy}f}')
    elif type_root == '1':
        # Арифметический корень через Decimal
        number = Decimal(number)
        result = number.sqrt()
        show(lang, f'Результат: {format(result, f".{accuracy}f")}',
             f'Result: {format(result, f".{accuracy}f")}')
    else:
        # Алгебраический корень (возвращаются два значения)
        result1, result2 = sqrt_roots(number)
        result1, result2 = format_complex(result1, accuracy), format_complex(result2, accuracy)
        show(lang, f'Результаты: {result1}, {result2}', f'Results: {result1}, {result2}')


# Запуск программы
language = identify_language()

# Цикл главного меню
while True:
    window = menu(language)
    if window == '1':
        program(language)
    elif window == '2':
        language = identify_language()
    else:
        break
