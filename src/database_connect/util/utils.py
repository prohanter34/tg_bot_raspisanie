def dowTransform(numbOfDay):
    dayOfDow = {0: "Воскресенье", 1: "Понедельник", 2: "Вторник", 3: "Среда", 4: "Четверг", 5: "Пятница", 6: "Суббота", 7: "Воскресенье"}
    return dayOfDow[numbOfDay]


def create_timetable(array):
    output_str = "\n--------------------------------------------------"
    for i in array:
        id, day, subject, room, time, teacher = i
        output_str += '\n{}  {}  {}\n  {}\n'.format(subject, room, time, teacher)
    if array == []:
        output_str += "\nВ этот день у вас 0 пар!"
    return output_str


def create_timetable_of_week(array):
    output_str = ""
    counter = 1
    for i in array:
        dayOfWeek = dowTransform(counter)
        output_str += dayOfWeek
        output_str += create_timetable(i)
        output_str += "\n\n"
        counter += 1
    return output_str


def typeOfWeek(numbOfWeek):
    if numbOfWeek % 2 == 0:
        return "Чётная"
    else:
        return "Нечётная"