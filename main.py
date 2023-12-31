from  task1 import task1
from  task2 import task2
from  task3 import task3

def run_all_functions():
    functions_list = [task1,task2,task3]
    out = {}
    for func in functions_list:
        out[func.__name__] = func()
    print(f'out = {out}')

def run_individual_function(selected_function):
    function_mapping = {
        "task1": task1,
        "task2": task2,
        "task3": task3,
        "run all tasks": run_all_functions
    }

    selected_function = selected_function.lower()
    if selected_function in function_mapping:
        out = {selected_function: function_mapping[selected_function]()}
        print(f'out = {out}')
    else:
        print("Invalid function name")

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        run_all_functions()
    elif len(sys.argv) == 2:
        run_individual_function(sys.argv[1])
    else:
        print("Usage: python main_script.py [function_name]")
