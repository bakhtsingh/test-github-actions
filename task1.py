import os
import sys

def task1(environment):
    print("Task1 Completed")
    return "successful"

def task2(environment):
    print("Task2 Completed")
    return "successful"

def task3(environment):
    task1(environment)
    task2(environment)
    print("Task3 Completed")
    return "successful"

def run_all_functions(environment):
    functions_list = [task1,task2,task3]
    out = {}
    for func in functions_list:
        out[func.__name__] = func(environment)
        if "successful" not in out[func.__name__].lower():
            print("Intentionally creating an error to stop execution\
     of all other testcases when one testcase fails")
            print(2/0)
    print(f'out = {out}')

def run_individual_function(selected_function, environment):
    function_mapping = {
        "task1": task1,
        "task2": task2,
        "run all tasks": task3
    }
    selected_function = selected_function.lower()
    if selected_function in function_mapping:
        out = {selected_function: function_mapping[selected_function](environment)}
        print(f'out = {out}')
    else:
        print("Invalid function name")

def main():
    selected_function = os.environ.get('SELECTED_FUNCTION', 'run all tasks')
    print(f'Selected Function: {selected_function}')
    environment = os.environ.get('ENVIRONMENT', 'PROD')
    print(f'Selected Environment: {environment}')
    if selected_function.lower() == "run all tasks":
        run_all_functions(environment)
    else:
        run_individual_function(selected_function, environment)

if __name__ == "__main__":
    main()
