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
**verbose:** output more info to sdtout

### python package
```python
from pandas import DataFrame
from symbolic_regession_first_order_logic import best_expression

data = {'v_1':[True, True, False, False], 
        'v_2':[True, False, True, False],
        'e'  :[True, False, True, True]}
df = DataFrame.from_dict(data)

best_expression(df)
```
#### with options
```python
...
best_expression(input_df, 
                populations=31, 
                population_size=27, 
                maxdepth=10, 
                niterations=100, 
                verbose=False)
```
### console
Use --input_df argument to point to pickled DataFrame
```bash
python .\symbolic_regression_first_order_logic.py --input_df a.pkl
```
#### with options
```bash
python .\symbolic_regression_first_order_logic.py --input_df a.pkl --populations 31 --population_size 27 --maxdepth 10 --niteration 100 --verbose
```