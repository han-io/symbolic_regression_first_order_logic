from pyscript import document
from sr_fol.__main__ import best_expression
from sr_fol.Assignment import Assignment, RandomAssignment
from sr_fol.Expression import Not, Or, And, Nand, Xor, Implies, Converse
#from warnings import simplefilter
#simplefilter(action='ignore', category=FutureWarning)
from pandas import DataFrame

""" TODO 
-while running show best expression sofar and colour the fulfilled assignments
-in tree view preferred
-on hover on assignment colour the outputs red for False and green for True
-docstring _pyscript.py
"""


def prepare_table_cell(row, col, selected=None, allow_none=True):
    none_option = f'<option value="None" {'selected' if selected is None else ''}>None</option>' if allow_none else ''
    cell = f'''<td><select id="r{row}c{col}">{none_option}
                     <option value="True" {'selected' if selected is True else ''}>True</option>
                     <option value="False" {'selected' if selected is False else ''}>False</option>
                   </select></td>'''
    return cell


def prepare_table():
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


def find_expression(event):
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
                                                                  binary_operators=tuple(options_binary),
                                                                  unary_operators=tuple(options_unary),
                                                                  verbose=True)


def change_number(event):
    document.querySelector("#input-table").innerHTML = prepare_table()


document.querySelector("#input-table").innerHTML = prepare_table()
