def arithmetic_arranger(problems, show_answers=False):
    if (len(problems) > 5):
        return 'Error: Too many problems.'

    first_list = []
    second_list = []
    horizontal_line_list = []
    total_list = []

    for problem in problems:
        # print(problem)
        split_problem = problem.split()
        arithmatic_operator = split_problem[1]
        first_param = split_problem[0]
        second_param = split_problem[2]

        if not first_param.isdigit() or not second_param.isdigit():
            return "Error: Numbers must only contain digits."
            break

        if len(first_param) > 4 or len(second_param) > 4:
            return "Error: Numbers cannot be more than four digits."
            break

        if not arithmatic_operator == '+' and not arithmatic_operator == '-':
            return "Error: Operator must be '+' or '-'."
            break

        if arithmatic_operator == '-':
            total_list.append(int(first_param) - int(second_param))
        else:
            total_list.append(int(first_param) + int(second_param))


        second_space_length = len(first_param) - len(second_param)
        space_list = []
        for i in range(second_space_length):
            space_list.append('')

        if second_space_length < 0:
            second_value = f'{arithmatic_operator} {second_param}'
            second_value_length = len(second_value)
            second_list.append(second_value)
        else:
            second_value = f"{arithmatic_operator}{' '.join(space_list)} {second_param}"
            second_value_length = len(second_value)
            second_list.append(second_value)
        horizontal_line_list.append('-' * second_value_length)
        first_space_length = second_value_length - len(first_param)

        first_space_list = []
        for i in range(first_space_length):
            first_space_list.append('')
        # print(first_param_length)
        # first_list.append(split_problem[0])
        if first_space_length < 0:
            first_value = str(first_param)
            # first_value_length = len(first_value)
            first_list.append(first_value)
        else:
            first_value = str(' '.join(first_space_list) + ' ' + str(first_param))
            # first_value_length = len(first_value)
            first_list.append(first_value)


    first_list_str = ''
    for fvalue in first_list:
        first_list_str += fvalue + '    '

    second_list_str = ''
    for svalue in second_list:
        second_list_str += svalue + '    '

    total_list_str = ''
    for tvalue in horizontal_line_list:
        total_list_str += tvalue + '    '

    total_str = ''

    if show_answers:
        for i, tovalue in enumerate(total_list):
            second_list_length = len(second_list[i])
            # print(second_list_length)
            tovalue_str = f'{tovalue}'
            total_space = " " * (second_list_length - len(tovalue_str))
            # total_str += f"{' '.join(first_space_list)} {first_param}"
            total_str += f"{total_space}{tovalue}    "

    problems = f"{first_list_str}\n{second_list_str}\n{total_list_str}"
    # if show_answers:
        # problems += f'\n{total_str}
    # print(problems)
    # print(second_list_str)
    # print(total_list_str)
    # print(total_str)
    return problems

# print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49", "123 + 49", "123 + 49"])}')
# print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49", "123 + 49"],True)}')

print(f'\n{arithmetic_arranger(["3801 - 2", "123 + 49"], True)}')

# print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49", "123 + 49", "123 + 49"])}')
# print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49", "123 + 49"],True)}')
