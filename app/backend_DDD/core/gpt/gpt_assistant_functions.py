from app.backend_DDD.core.gpt.gpt_public_assistant_functions import Assistant, Thread , Run , ToolCalls , client 
from app.backend_DDD.core.gpt import helper_variables as helper
from app.backend_DDD.core.gpt.gpt_tool_functions import GptToolFunctions
from app.backend_DDD.core.gpt import gpt_id as id

class GptAssistant:
    def __init__(self):
        self.run = Run(client=client)
        self.thread = Thread(client=client)
        self.tool_calls = ToolCalls()
        self.asist = Assistant(client=client)
        pass

    def process_public_query(self, query):
        
        #== Create a message ==#
        message = self.thread.create_message(helper.public_thread_id, 'user', query)
        #== Run our Assitant ==#
        run = client.beta.threads.runs.create(
            thread_id=helper.public_thread_id,
            assistant_id=helper.public_assistant_id,
        )

        #== Run ==#
        response_gpt  = run.wait_for_run_completion(client=client, thread_id=helper.public_thread_id, run_id=run.id)


        response = response_gpt  # Replace with actual GPT processing
        return response
    

    def run_type_one(self, query: str):
        # Create a run
        # See if any funciton tool needs to be called
        # Pass function tool response
        # return response


        #== Cancel old runs if any ==#
        self.run.cancel_old_runs(thread_id=helper.public_thread_id)
        print('Cancelled old runs')

        #== Create a message in thread ==#
        query_message = self.thread.create_message(helper.public_thread_id, 'user', query)

        #== Create a run in that thread ==#
        query_run = self.run.create_run(assistant_id=id.lums_public_assitant_id, thread_id=id.lums_public_thread_id, parallel_functions=True)

        #== Handle tool calls ==#
        query_tool_calls = self.run.wait_and_get_required_function(thread_id=id.lums_public_thread_id, run_id=query_run.id)

        if query_tool_calls:
            query_tool_call_outputs = self.tool_calls.call_tool_actions(tool_calls=query_tool_calls)

            self.tool_calls.submit_tool_outputs_to_run(client=client, thread_id=id.lums_public_thread_id, run_id=query_run.id, tool_outputs=query_tool_call_outputs)

        #== Wait for run completion ==#
        response = self.run.wait_for_run_completion(thread_id=id.lums_public_thread_id, run_id=query_run.id)

        return response

        
