import math


def dist(p1, p2):
    p1 = p1.split(' ')
    p2 = p2.split(' ')
    return math.sqrt((float(p2[0]) - float(p1[0])) ** 2 + (float(p2[1]) - float(p1[1])) ** 2)


def add_cord(input_string):
    string_to_work = input_string[10:]
    string_to_work = string_to_work[::-1]
    string_to_work = string_to_work[2:]
    string_to_work = string_to_work[::-1]

    temp_var = string_to_work.split(', ')

    ans_mas = [temp_var[0]]

    data = string_to_work.split(', ')
    to_add = 100 - len(data) + 2

    data = data[:2]
    total_dist = dist(data[0], data[1])

    dist_to_add = total_dist / to_add
    for i in range(to_add - 1):
        a = data[0].split(' ')
        b = data[1].split(' ')

        ac = dist_to_add * (i + 1)
        cb = total_dist - ac

        k = ac / cb

        ax = float(a[0])
        ay = float(a[1])

        bx = float(b[0])
        by = float(b[1])

        x1 = (ax + k * bx) / (1 + k)
        y1 = (ay + k * by) / (1 + k)
        temp_string = str(x1) + " " + str(y1)
        ans_mas.append(temp_string)

    for i in range(1, len(temp_var)):
        ans_mas.append(temp_var[i])

    final_answer = []
    for i in range(len(ans_mas)):
        temp_data = ans_mas[i].split(' ')
        final_answer.append(float(temp_data[0]))
        final_answer.append(float(temp_data[1]))
    return final_answer
