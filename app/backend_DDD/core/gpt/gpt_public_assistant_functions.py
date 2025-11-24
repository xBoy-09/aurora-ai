import time
import json
import openai
import os
import logging
from datetime import datetime
from app.backend_DDD.core.gpt.helper_variables import *
from app.backend_DDD.core.gpt.gpt_tool_functions import GptToolFunctions
from dotenv import load_dotenv, find_dotenv

# load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(api_key+"12")
client = openai.OpenAI(api_key=api_key)

model = "gpt-4o-mini"


class Assistant:
    def __init__(self, client: openai.OpenAI):
        self.client = client

    def create_assistant(self, name: str, instructions, model: str):
        return self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model,
        )

    def get_assistant(self, assistant_id: str):
        return self.client.beta.assistants.retrieve(
            assistant_id=assistant_id,
        )
    
    def get_file_name(self, file_id: str) -> str:
        return self.client.files.retrieve(file_id=file_id).filename

    def update_assistant(self, assistant_id: str, instruction=None, tools=None):
        kwargs = {'assistant_id': assistant_id}
        if instruction is not None:
            kwargs['instructions'] = instruction
        if tools is not None:
            kwargs['tools'] = tools

        return self.client.beta.assistants.update(**kwargs)

    def add_function_tool(self, assistant_id: str, function_to_add: dict):
        assistant = self.get_assistant(assistant_id)
        functions = assistant.tools
        functions.append(function_to_add)
        return self.update_assistant(assistant_id, tools=functions)

    def modify_function_tool(self, assistant_id: str, function_to_modify: str, new_function: dict):
        assistant = self.get_assistant(assistant_id)
        functions = assistant.tools
        functions = [new_function if function.function.name == function_to_modify else function for function in functions]
        return self.update_assistant(assistant_id, tools=functions)

    def get_tool_functions(self, assistant_id: str):
        return self.get_assistant(assistant_id).tools

    def retrieve_function_names(self, assistant_id: str):
        return [tool.function.name for tool in self.get_tool_functions(assistant_id)]


class Thread:
    def __init__(self, client: openai.OpenAI):
        self.client = client

    def create_thread(self):
        return self.client.beta.threads.create()

    def create_message(self, thread_id: str, role: str, content: str):
        return self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=content,
        )

    def retrieve_thread(self, thread_id: str):
        return self.client.beta.threads.retrieve(thread_id=thread_id)
    
    def get_thread_messages(self, thread_id: str):
        return self.client.beta.threads.messages.list(thread_id=thread_id)
    
    def delete_thread(self, thread_id: str):
        return self.client.beta.threads.delete(thread_id=thread_id)


class Run:
    def __init__(self, client: openai.OpenAI):
        self.client = client

    def create_run(self, thread_id: str, assistant_id: str, response_format=None, instructions=None, parallel_functions=True):
        kwargs = {'thread_id': thread_id, 'assistant_id': assistant_id, 'parallel_tool_calls': parallel_functions}
        if instructions is not None:
            kwargs['instructions'] = instructions

        return self.client.beta.threads.runs.create(**kwargs)

    def cancel_old_runs(self, thread_id: str):
        runs = self.client.beta.threads.runs.list(thread_id=thread_id)
        for run in runs.data:
            if run.status in ['requires_action', 'in_progress']:
                print(f'Cancelling run with id {run.id}, status: {run.status}')
                self.client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run.id)

    def cancel_run(self, thread_id: str, run_id: str):
        return self.client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)

    def wait_and_get_required_function(self, thread_id: str, run_id: str, sleep_interval=2):
        while True:
            try:
                run = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
                print("Waiting for run to retrieve function...", run.status)
                if run.status == 'incomplete':
                    print(f'Run incomplete : {run.incomplete_details}')
                    return None
                if run.status == 'failed':
                    print('Run failed with error:', run.last_error)
                    return None
                if run.required_action:
                    print(f'Run requires action. \n {run.required_action} \nRetrieving tool calls...')
                    return run.required_action.submit_tool_outputs.tool_calls
                elif run.status == 'completed':
                    return None
            except Exception as e:
                logging.error(f"An error occurred while retrieving the run: {e}")
                break
            time.sleep(sleep_interval)

    def wait_for_run_completion(self, thread_id: str, run_id: str, sleep_interval=2):
        while True:
            try:
                run = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
                print(f"Waiting for run {run.id} to complete...", run.status)
                if run.status == 'requires_action':
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls
                    tool_outputs = ToolCalls.call_tool_actions(tool_calls)
                    ToolCalls.submit_tool_outputs_to_run(tool_outputs, self.client, thread_id, run_id)

                if run.completed_at:
                    elapsed_time = run.completed_at - run.created_at
                    formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                    print(f"Run completed in {formatted_time}")
                    messages = self.client.beta.threads.messages.list(thread_id=thread_id)
                    last_message = messages.data[0]
                    response = last_message.content[0]
                    return response
            except Exception as e:
                logging.error(f"An error occurred while retrieving the run: {e}")
                break
            # time.sleep(sleep_interval)


class ToolCalls:
    @staticmethod
    def call_tool_actions(tool_calls: list):
        tool_outputs = []
        if not tool_calls:
            return tool_outputs
        for tool in tool_calls:
            arguments = json.loads(tool.function.arguments)
            response = GptToolFunctions.available_function_map[tool.function.name](**arguments)
            tool_output = {
                "tool_call_id": tool.id,
                "output": response
            }
            tool_outputs.append(tool_output)
        return tool_outputs

    @staticmethod
    def submit_tool_outputs_to_run(tool_outputs, client: openai.OpenAI, thread_id: str, run_id: str):
        try:
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id, 
                run_id=run_id, 
                tool_outputs=tool_outputs,
            )
            print('Tool outputs submitted successfully. Run status:', run.status)
        except Exception as e:
            logging.error(f"An error occurred while submitting tool outputs: {e}")

