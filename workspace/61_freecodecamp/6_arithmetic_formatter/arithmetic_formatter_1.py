# feecodecamp arithmetic formatter
#
def arithmetic_arranger(problems, show_answers=False):
    # print(type(problems))
    # if(len(problems) > 6):
    #     problems = 'Error: Too many problems.'
    # else:
    all_first_horizontal_line = []
    all_second_horizontal_line = []
    for problem in problems:
        split_problem = problem.split()
        arithmatic_operator = split_problem[1]
        first_param = split_problem[0]
        second_param = split_problem[2]
        first_param_length = (2 + len(second_param)) - len(first_param)
        # print(first_param_length)
        # print(' '.join(space_list))
        # print(f"{' '.join(space_list)}{first_param}")
        # print(f'{arithmatic_operator} {second_param}')
        # print('-----')
        # print()
        # all_first_horizontal_line = f"{all_first_horizontal_line}{' '.join(space_list)}{first_param}    "
        # all_second_horizontal_line = f'{all_second_horizontal_line}{arithmatic_operator} {second_param}    '

        second_space_list = len(first_param) - len(second_param)
        space_list = []
        for i in range(second_space_list):
            space_list.append('')
        all_second_horizontal_line.append(f"{arithmatic_operator} {' '.join(space_list)}{second_param}")

        # all_first_horizontal_line.append(first_param)

        first_space_list = []
        for i in range(first_param_length):
            if i > 0:
                first_space_list.append('')

        xs = list(range(first_param_length))
        print(xs)
        # if len(first_space_list) > 0:
        all_first_horizontal_line.append(f"{''.join(first_space_list)}{first_param}")
        # else:
            # all_first_horizontal_line.append(f"{first_param}")

        # print(first_param)
    # print(all_first_horizontal_line)
    # print(all_second_horizontal_line)
    all_first_horizontal_line_str = ''
    for fkey in all_first_horizontal_line:
        all_first_horizontal_line_str += fkey + '    '

    all_second_horizontal_line_str = ''
    for skey in all_second_horizontal_line:
        all_second_horizontal_line_str += skey + '    '

    print(all_first_horizontal_line_str)
    print(all_second_horizontal_line_str)

    return problems

print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49"])}')
