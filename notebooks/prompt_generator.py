from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp

def prompt_gen_builder(task):

    """Constructs a custom prompt for a digital agent, aimed at generating Python code based on a given task description.

    This function creates a structured prompt that guides a digital agent to understand and respond to a specific task related to Python programming. 
    The prompt includes an instructional section and examples of input-output pairs, demonstrating the desired behavior 
    in generating Python code from a task description.
    
    Parameters:
    task (str): A description of the task for which Python code needs to be generated. 
    This description should be clear and concise, outlining the specific functionality required.
    
    Returns:
    str: A complete prompt that includes instructions and examples tailored to the given task. 
    This prompt can be used to guide a digital agent in generating appropriate Python code based on the task description.
    """
    
    prompt = f"""[INST] <<SYS>> You are an individual dedicated to expanding our understanding of the world and pushing the boundaries of human knowledge.
For the task specified below, outline a set of instructions to successfully achieve it.
Based on the task given, the goal is to correctly write a prompt form to generate an answer from an digital agent. 
The structure should consist of an example section with input : output pairs to show the correct behaviour.<</SYS>>

Task: Given a 'Description' of a python function, write the code.
Examples

Example Input: 
Description: A function which takes two numbers and multiplies them.
Example Output: def multiply(a,b):
    return a*b
    
Example Input: 
Description: A Python function to calculate the factorial of a number.
Example Output: def factorial(n):
    return 1 if n == 0 else n * factorial(n-1)

Task: {task}
Examples
Example Input:"""
    return prompt

def gen_task_example(model="", task=""):
    
    """Generates an example input and output for a specified task using a given model.

    This function is designed to assist in constructing examples for language model prompts. 
    It first checks if the provided task and model strings are empty, and if not, it builds a prompt using the 'prompt_gen_builder' function. 
    The model is then used to generate an input example based on this prompt. 
    The function further prompts the model to generate a corresponding output example, thus creating a complete input-output pair for the specified task.
    
    Parameters:
    model (str): The name or identifier of the language model to be used for generating examples.
    task (str): A description of the task for which examples are to be generated.
    
    Returns:
    tuple: A tuple containing two elements; 
    the first is the generated input example, and the second is the corresponding output example. 
    If either the task or model is not specified (empty string), the function returns None.
    """
    # Check if input string is empty
    if task == "": return None
    if model == "": return None

    # Given a task, we want to build a prompt which shows the LLM how prompts are built
    prompt = prompt_gen_builder(task)
    # Call the model. Given this prompt, we want to generate an input example
    input_example_response = model(prompt, stop=["Example Input:", "Example Output:"])
    # Add the response to the prompt and add the Output string to ellicit the output of the example.
    prompt_with_input = prompt + input_example_response + "\nExample Output: "
    # Call the model. Given this prompt, we want to generate an output example
    output_example_response = model(prompt_with_input, stop=["Input Example:", "Example Output:"])

    return input_example_response, output_example_response


def task_and_examples_to_prompt(task="", examples=""):

    """Constructs a structured prompt for a digital agent, integrating a specified task and its associated examples.
    
    This function creates a detailed prompt designed to guide a digital agent in understanding and responding to a specific programming-related task. 
    The prompt includes an instructional section along with a series of input-output pairs as examples. 
    It begins by validating the input parameters, returning None if either 'task' or 'examples' is an empty string. 
    The function then constructs the prompt, incorporating the given task and examples into the format expected by the digital agent.
    
    Parameters:
    task (str): A description of the task for which the prompt is being created.
    examples (list of tuples): A list where each tuple contains two elements - an example input (str) and its corresponding output (str). 
    These examples illustrate the expected behavior for the given task.
    
    Returns:
    str: A fully constructed prompt that includes the task description and formatted examples. 
    This prompt can be used to elicit appropriate responses from a digital agent based on the specified task and examples. 
    If either 'task' or 'examples' is an empty string, the function returns None.
    """
    # Check if inputs are valid
    if task == "": return None
    if examples == "": return None

    prompt = f"""[INST] <<SYS>> You are an individual dedicated to expanding our understanding of the world and pushing the boundaries of human knowledge.
For the task specified below, outline a set of instructions to successfully achieve it.
Based on the task given, the goal is to correctly write a prompt form to generate an answer from an digital agent. 
The structure should consist of an example section with input : output pairs to show the correct behaviour.<</SYS>>

Task: {task}
Examples
"""
    for example in examples:
        prompt = prompt + f"Example Input: {example[0]}\nExample Output:{example[1]}\n"

    prompt += "Example Input: "
    return prompt


def autogen_prompt(task="", model="", example_num=3):
    """
    Automatically generates a structured prompt for a specified task, using a given model to create example input-output pairs.

    This function facilitates the automatic generation of prompts for a language model. 
    It first validates the provided 'task', 'model', and 'example_num' parameters. 
    If the task or model is an empty string, or if the number of examples requested is less than 1, the function returns None. 
    The function then generates a specified number of example input-output pairs using the 'gen_task_example' function. 
    These examples are compiled into a list, which is then used to create a full prompt that includes the task description and the generated examples.

    Parameters:
    task (str): The task description to be included in the prompt.
    model (str): The model used to generate example inputs and outputs.
    example_num (int): The number of examples to generate for the prompt.

    Returns:
    str: A string containing the constructed prompt, which includes the task description and the generated examples. 
    If 'task', 'model' is empty, or 'example_num' is less than 1, the function returns None.
    """
    

    # Input checks
    if task == "": return None
    if model=="": return None
    if example_num < 1: return None

    # For each example we want ..
    examples = []
    while len(examples) != example_num:
        example_input, example_output = gen_task_example(model=model, task=task)

        # Check if the bi-grams are not in both the input and the output
        if "Example Input:" not in example_input and "Example Output:" not in example_output and \
           "Example Input:" not in example_output and "Example Output:" not in example_input:
            examples.append([example_input, example_output])
    
    # Once we have our examples, compose the prompt
    return task_and_examples_to_prompt(task, examples)



def main():
    
    return None




    

if __name__ == "__main__":
    main()



























