from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp
from datetime import datetime
from IPython.display import clear_output
import time
def prompt_gen_builder():

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
    # Read history from the file
    with open('history.txt', 'r') as file:
        history = file.read()

    # Get the current date in the format "dd/mm/yyyy"
    today = datetime.now().strftime("%d/%m/%Y")
    today_day = datetime.now().strftime("%A")
    
    prompt = f"""[INST] <<SYS>> You are an individual dedicated to expanding our understanding of the world and pushing the boundaries of human knowledge.
For the task specified below, outline a set of instructions to successfully achieve it.
You are an accademic which cares about being precise about what you say and about knowledge.<</SYS>>

Topic examples
{history}
{today} - {today_day} -"""
    
    return prompt
    
def build_thought_prompt(topic="", last_thought=""):

    if topic == "": return None

    
    
    prompt = f"""[INST] <<SYS>> You are an individual dedicated to expanding our understanding of the world and pushing the boundaries of human knowledge.
For the task specified below, outline a set of instructions to successfully achieve it.
You are an accademic which cares about being precise about what you say and about knowledge.<</SYS>>
Think about the given topic, a previous thought is also provided, use it to dive deeper into the subject.

Topic: {topic}

Last thought: {last_thought}

Thought: """

    return prompt


def generate_thoughts(topic="", iterations=3, delay=3, model=""):
    """
    Generates thoughts based on a given topic, iteratively refining them.

    This function generates thoughts in a loop, each time refining the thought based on the output of the previous iteration. 
    After each iteration, except the last, the function waits for a specified delay and then clears the output. 
    This is useful for iterative refinement processes where only the final output is desired.

    Parameters:
    topic (str): The topic based on which thoughts are to be generated.
    iterations (int, optional): The number of iterations for refining the thought. Defaults to 3.
    delay (int, optional): The time delay (in seconds) before clearing the output in each iteration. Defaults to 3 seconds.

    Returns:
    str: The final refined thought after all iterations.
    """
    if topic == "": return None
    if model == "": return None

    thought = ""
    for i in range(iterations):
        print(thought + "\n\n")  # Print the current state of thought
        think_prompt = build_thought_prompt(topic, thought)  # Build the prompt
        thought = model(think_prompt, stop=["\n\n"])  # Generate the new thought

        if i < iterations - 1:  # Delay and clear the output except in the last iteration
            time.sleep(delay)  # Wait for specified seconds
            clear_output(wait=True)  # Clear the current output

    return thought

# Example usage:
# final_thought = generate_thoughts("environment")



