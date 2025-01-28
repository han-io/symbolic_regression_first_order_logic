from pyscript import document
from sr_fol.__main__ import best_expression
from sr_fol.Assignment import Assignment, RandomAssignment
from sr_fol.Expression import Not, Or, And, Nand, Xor, Implies, Converse
from pandas import DataFrame


def prepare_table_cell(row: int, col: int, allow_none: bool = True) -> str:
    """
    Return a html table cell with an input field.

    :return: html table cell
    """
    none_option = f'<option value="None">None</option>' if allow_none else ''
    cell = f'''<td><select id="r{row}c{col}">{none_option}
                     <option value="True">True</option>
                     <option value="False">False</option>
                   </select></td>'''
    return cell


def prepare_table() -> str:
    """
    Return a html table with input fields in the cells for input of the assignment matrix.

    :return: html table
    """
    rows = int(document.querySelector("#number-of-variables").value) + 1
    columns = int(document.querySelector("#number-of-assignments").value)
    table = '<table id="input-table">'
    for row in range(rows):
        table += f'<tr><th>{f'v<sub>{str(row+1)}</sub>' if row < rows-1 else 'e'}</th>'
        table += ''.join([prepare_table_cell(row, column, allow_none=row < rows-1) for column in range(columns)])
    table += '<tr><th></th>'
    table += ''.join([f'<th>a<sub>{str(column+1)}</sub></th>' for column in range(columns)])
    table += '</tr></table>'
    return table


def find_expression(_) -> None:
    """ Read options and the input table and start the search for an adequate expression. """
    rows = int(document.querySelector("#number-of-variables").value) + 1
    columns = int(document.querySelector("#number-of-assignments").value)
    options_unary = []
    if document.querySelector('#not').checked:
        options_unary.append(Not)
    options_binary = []
    if document.querySelector("#or").checked:
        options_binary.append(Or)
    if document.querySelector("#and").checked:
        options_binary.append(And)
    if document.querySelector("#nand").checked:
        options_binary.append(Nand)
    if document.querySelector("#xor").checked:
        options_binary.append(Xor)
    if document.querySelector("#implies").checked:
        options_binary.append(Implies)
    if document.querySelector("#converse").checked:
        options_binary.append(Converse)

    data = []
    for row in range(rows):
        data_row = []
        for col in range(columns):
            cell_value = document.querySelector(f'#r{row}c{col}').value
            if cell_value == 'True':
                data_row.append(True)
            elif cell_value == 'False':
                data_row.append(False)
            else:
                data_row.append(None)
        data.append(data_row)

    assignment = Assignment(DataFrame(data))
    assignment.clean()
    document.querySelector("#output").innerText = best_expression(assignment.matrix,
                                                                  populations=10,
                                                                  population_size=10,
                                                                  maxdepth=5,
                                                                  binary_operators=tuple(options_binary),
                                                                  unary_operators=tuple(options_unary),
                                                                  verbose=True)


def change_number(_) -> None:
    """ Allow different number of variables and assignments. """
    document.querySelector("#input-table").innerHTML = prepare_table()


document.querySelector("#input-table").innerHTML = prepare_table()
