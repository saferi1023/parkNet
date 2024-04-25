from dotenv import load_dotenv
import openai
import os
import time
import json

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("VP_ASSIST_KEY")


def check_status(run_id,thread_id):
    run = openai.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )
    return run.status

def send_message_and_get_response(prompt):

    thread = openai.beta.threads.create()
    thread_id = thread.id

    openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    ) 

    run_id = run.id

    while True:
        status = check_status(run_id, thread_id)
        print("...",status)
        if status == "completed":
            break
        time.sleep(2)

    response = openai.beta.threads.messages.list(thread_id=thread_id)
    return response.data[0].content[0].text.value

def main():
    # Read Text file and send the data
    with open('simple_input.json', 'r') as file:
    # Read the contents of the file into a Python dictionary
        data = json.load(file)
        json_string = json.dumps(data, indent=4)

    # sample_input = "Name: George, Age: 45, Number of people: 4, Travel Dates: 4th May to 6th May, Destination: Grand Canyon, Enthusiasm Level: 3."
    whole_response = send_message_and_get_response(json_string)

    print(whole_response)
    with open('itinerary.txt', 'w') as file:
        file.write(whole_response)


if __name__ == "__main__":
    main()