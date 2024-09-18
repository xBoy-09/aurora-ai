from app.backend_DDD.core.gpt import gpt_public_assistant_functions as gpt
from app.backend_DDD.core.gpt import helper_variables as helper
from app.backend_DDD.core.gpt.gpt_tool_functions import GptToolFunctions

class GptAssistant:
    def __init__(self):
        # Initialize the GPT assistant
        pass

    def process_public_query(self, query):
        
        #== Create a message ==#
        message = gpt.create_msg(gpt.client, helper.public_thread_id, 'user', query)
        #== Run our Assitant ==#
        run = gpt.client.beta.threads.runs.create(
            thread_id=helper.public_thread_id,
            assistant_id=helper.public_assistant_id,
        )


        # === Run ===
        response_gpt  = gpt.wait_for_run_completion(client=gpt.client, thread_id=helper.public_thread_id, run_id=run.id)


        response = response_gpt  # Replace with actual GPT processing
        return response
    

    def run_type_one(query: str):
        # Fetch instructions from GPT
        # Use instruction to create new run
        # get query response


        #== Make a run in instruction thread ==#
        instruction_run = gpt.create_run(gpt.client, helper.lums_instruction_thread_id, helper.lums_instruction_assitant_id, query)

        #== Get function tool call ==#
        instruction_tool_calls = gpt.wait_and_get_required_function(gpt.client, helper.public_instruction_thread_id, instruction_run.id)
        
        #== Get response instructions from those tool functions ==#
        #== Cancel that run ==#
        
        #== Create a message in query thread ==#
        #== Create a run in query thread with fetched instruction ==#
        #== See if tool function call ==#
        #== get tool function output ==#
        #== execute run wioth tool function output ==#
        #== return response ==#
        pass
