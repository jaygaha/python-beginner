# feecodecamp arithmetic formatter

def arithmetic_arranger(problems, show_answers=False):
    if (len(problems) > 5):
        return 'Error: Too many problems.'

    first_list = []
    second_list = []
    horizontal_line_list = []
    total_list = []

    for problem in problems:
        # Split the problem into its parts
        split_problem = problem.split()
        arithmatic_operator = split_problem[1]
        first_param = split_problem[0]
        second_param = split_problem[2]

        # Check if operator is valid
        if not arithmatic_operator == '+' and not arithmatic_operator == '-':
            return "Error: Operator must be '+' or '-'."
            break

        # Check if the first param is a number
        if not first_param.isdigit() or not second_param.isdigit():
            return "Error: Numbers must only contain digits."
            break

        # check if first or second param is more than 4 digits
        if len(first_param) > 4 or len(second_param) > 4:
            return "Error: Numbers cannot be more than four digits."
            break

        # There should be a single space between the operator and the longest of the two operands, the operator will be on the same line as the second operand,
        # both operands will be in the same order as provided (the first will be the top one and the second will be the bottom).
        param_max_width = max(len(first_param), len(second_param)) + 2

        # format the first param
        first_list.append(first_param.rjust(param_max_width)) # right justify the first param
        # format the second param
        second_list.append(f"{arithmatic_operator} {second_param.rjust(param_max_width - 2)}") # right justify the second perator and the second param

        # format the dashes
        horizontal_line_list.append('-' * param_max_width)

        if show_answers:
            total_value = ''
            if arithmatic_operator == '-':
                total_value = int(first_param) - int(second_param)
            else:
                total_value = int(first_param) + int(second_param)
            total_list.append(str(total_value).rjust(param_max_width))

    # Join the lines into a single string
    result = '    '.join(first_list) + '\n' + '    '.join(second_list) + '\n' + '    '.join(horizontal_line_list)

    if show_answers:
        result += '\n' + '    '.join(total_list)

    return result

print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49", "123 + 49", "123 + 49"])}')
print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49", "123 + 49"],True)}')
print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49", "123 * 49"],True)}')
print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49", "12o3 + 49i"],True)}')
print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49", "12300 + 49"],True)}')

print(f'\n{arithmetic_arranger(["3801 - 2", "123 + 49"])}')

# print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49", "123 + 49", "123 + 49"])}')
# print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49", "123 + 49"],True)}')
