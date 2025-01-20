# symbolic_regression_first_order_logic

This repository implements symbolic regression for first-order logic.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/han-io/symbolic_regression_first_order_logic
```

2. Install libraries:

```bash
pip install requirements.txt
```

## Usage

### options
**populations:** number of populations used in the genetic algorithm  
**population_size:** number of individual expressions per population  
**maxdepth:** maximum depth of the expressions in the populations  
**niterations:** number of generations of mutation and crossover  
**binary_operators:** only use these binary operators  
**unary_operators:** only use these unary operators  
**verbose:** output more info to sdtout

### python package
```python
from pandas import DataFrame
from symbolic_regression_first_order_logic.src.sr_fol import best_expression, Not, Or, And, Nand, Xor, Implies, Converse

data = {'v_1':[True, True, False, False], 
        'v_2':[True, False, True, False],
        'e'  :[True, False, True, True]}
df = DataFrame.from_dict(data)

best_expression(df)  # This returns a logical expression
```
#### with options
```python
...
best_expression(input_df, 
                populations=31, 
                population_size=27, 
                maxdepth=10, 
                niterations=100,
                binary_operators=(Or, And, Nand, Xor, Implies, Converse),
                unary_operators=(Not,),
                verbose=False)
```
### console
Use --input_df argument to point to pickled DataFrame
```bash
cd .\symbolic_regression_first_order_logic\src\
python -m sr_fol --input_df_path input.pkl
```
#### with options
```bash
...
python -m sr_fol --input_df input.pkl --populations 31 --population_size 27 --maxdepth 10 --niteration 100 --binary_operators all_or_and_nand_xor_implies_converse --unary_operators all_not --verbose
```
