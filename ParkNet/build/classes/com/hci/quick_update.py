from dotenv import load_dotenv
from datetime import datetime
import openai
import os
import time
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("VP_ASSIST3_KEY")

current_date = datetime.now().strftime("%B %d, %Y")

def get_day_events():

    in_section = False

    itinerary_path = "itinerary.txt"
    relevant_text = ""
    # Read the file
    with open(itinerary_path, "r") as file:
        for line in file:
            # Check if the line starts with "####"
            if line.startswith("####"):
                # Extract the date from the line
                date_part = line.split(":")[1].split("–")[0].strip()
                # Check if the extracted date matches the current date
                if date_part == current_date:
                    in_section = True
                    relevant_text = line  # Start capturing text with the line itself
                else:
                    # If we were capturing and encounter another "####", stop capturing
                    if in_section:
                        break
            elif in_section:
                # If we are in the relevant section, keep appending lines
                relevant_text += line

    return relevant_text


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
    partial_itinerary = get_day_events()

    print(partial_itinerary)
    print("______________________________________")

    # sample_input = "Name: George, Age: 45, Number of people: 4, Travel Dates: 4th May to 6th May, Destination: Grand Canyon, Enthusiasm Level: 3."
    if partial_itinerary == "":
        print("Keep patience! The adventure is yet to begin!!!")
        with open('quick_update.txt', 'w') as file:
            file.write("Keep patience! The adventure is yet to begin!!!")
    else: 
        whole_response = send_message_and_get_response(partial_itinerary)

        print(whole_response)
        with open('quick_update.txt', 'w') as file:
            file.write(whole_response)


if __name__ == "__main__":
    main()