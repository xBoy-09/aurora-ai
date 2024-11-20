from app.backend_DDD.core.gpt.gpt_public_assistant_functions import Assistant, Thread , Run , ToolCalls , client 
from app.backend_DDD.core.gpt import helper_variables as helper
from app.backend_DDD.core.gpt.gpt_tool_functions import GptToolFunctions
from app.backend_DDD.core.gpt import gpt_id as id
from app.backend_DDD.core.database.database_api_queries import DatabaseManager as db_man


class GptAssistant:
    def __init__(self):
        self.run = Run(client=client)
        self.thread = Thread(client=client)
        self.tool_calls = ToolCalls()
        self.asist = Assistant(client=client)
        pass


    def get_thread_messages(self, thread_id):
        messages = self.thread.get_thread_messages(thread_id=thread_id).model_dump()
        messages_data  = messages["data"]

        for i in range(len(messages_data)):
            message_data = messages_data[i]
            if message_data['role'] == 'assistant':
                annotations = message_data['content'][0]['text']['annotations']
                for j in range (len(annotations)):
                    file_id = annotations[j]['file_citation']['file_id']
                    file_name = self.asist.get_file_name(file_id=file_id)
                    messages_data[i]['content'][0]['text']['annotations'][j]['file_citation']['file_name'] = file_name



        msg_list = []
        length = len(messages_data)
        temp = 0
        while temp+1 < length:
            user_message = messages_data[temp+1]
            assistant_message = messages_data[temp]
            if user_message["role"] == "user" and assistant_message["role"] == "assistant":
                if user_message["incomplete_details"] == None and assistant_message["incomplete_details"] == None:
                    msg_list.append({
                        "user": messages_data[temp+1]["content"],
                        "assistant": messages_data[temp]["content"]
                    })
                temp += 2
            else:
                temp += 1

        
        return {
            "messages": msg_list,
            "last_id": messages["last_id"],
            "has_more": messages["has_more"]
        }


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
    

    def run_type_one(self, query: str, thread_id: str) -> str:
        # Create a run
        # See if any funciton tool needs to be called
        # Pass function tool response
        # return response


        #== Cancel old runs if any ==#
        self.run.cancel_old_runs(thread_id=thread_id)
        print('Cancelled old runs')

        #== Create a message in thread ==#
        query_message = self.thread.create_message(thread_id, 'user', query)

        #== Create a run in that thread ==#
        query_run = self.run.create_run(assistant_id=id.lums_public_assitant_id, thread_id=thread_id, parallel_functions=True)

        # #== Handle tool calls ==#
        # query_tool_calls = self.run.wait_and_get_required_function(thread_id=thread_id, run_id=query_run.id)

        # if query_tool_calls:
        #     query_tool_call_outputs = self.tool_calls.call_tool_actions(tool_calls=query_tool_calls)

        #     self.tool_calls.submit_tool_outputs_to_run(client=client, thread_id=thread_id, run_id=query_run.id, tool_outputs=query_tool_call_outputs)

        #== Wait for run completion ==#
        response = self.run.wait_for_run_completion(thread_id=thread_id, run_id=query_run.id)
        
        annotations = response.text.annotations

        for i in range(len(annotations)):
            file_id = annotations[i].file_citation.file_id
            file_name = self.asist.get_file_name(file_id=file_id)
            response.text.annotations[i].file_citation.file_name = file_name
            
        return response
    
    

    

    def run_get_thread_name(self, query: str, db_man: db_man) -> str:
        # Get assistant id
        assistant_id =  db_man.get_assistant_id_by_name(assistant_name='Thread-Name')

        # Create a thread
        thread = self.thread.create_thread()

        # Create a message in thread
        message = self.thread.create_message(thread_id=thread.id, role='user', content=query)

        # Create a run in that thread
        run = self.run.create_run(thread_id=thread.id, assistant_id=assistant_id, parallel_functions=True)

        # Handle response
        response = self.run.wait_for_run_completion(thread_id=thread.id, run_id=run.id)

        self.thread.delete_thread(thread_id=thread.id)

        return response.text.value
    
    def get_thread_id(self, user_id: str) -> str:
        thread = self.thread.create_thread()
        return thread.id
    



        
