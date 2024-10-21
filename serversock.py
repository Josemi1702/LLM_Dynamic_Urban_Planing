import asyncio
import websockets
import json
from openai import OpenAI    

def change_house(client, housing_data, profile):
    prompt = (f"""
    You are a person living in Cambridge, Boston. From this list of economic profiles: ['<$30000','$30000 - $44999','$45000 - $59999','$60000 - $99999','$100000 - $124999','$125000 - $149999','$150000 - $199999','>$200000'] you are an economic profile of {profile}. Today, you are facing a significant life decision: whether to move to a new house or stay in your current home. This is a choice that could impact your lifestyle, finances, and well-being.

    Given the following characteristics of the houses (all of them are marks between -1 and 1), you should consider whether you prefer to move or not: {housing_data}. But YOUR DECISSION MUST BE THE FINAL LINE OF ANSWER

    Before you make your decision, consider the following and think step by step:

    1. **Who you are**: Think about your background, financial stability, personal values, and lifestyle. You’ve lived your life within the bounds of your economic profile: {profile}. Reflect on how important factors like stability, financial security, and personal comfort are to you. What have you learned from your experiences about the trade-offs between cost, quality of life, and proximity to things you love? What does your gut tell you about moving?

    2. **What matters most to you** (remember all variables are marks, the higher the mark is, the better it is): 
    - **Affordability**: Reflect on how much the cost of housing affects your overall quality of life. **A higher mark in cost means the house is more affordable (lower cost)**, and **a lower mark means it is more expensive**. Think about your long-term financial goals and whether this move aligns with them.
    - **Diversity**: How much does the social and cultural diversity of a neighborhood impact your sense of belonging? Do you thrive in diverse environments, or do you prefer familiarity?
    - **Preferred Location**: Which location is your preferred.
    - How much does time affect your daily life? Reflect on how important it is for you to minimize commuting. **A higher mark in travel time means shorter travel time** (better), while **a lower mark means longer travel time** (worse).

    3. **Analyze the two housing options**: 
    - **New House**: Think carefully about this option. It may offer different benefits and challenges. Is the cost manageable within your budget? Does the neighborhood feel like a place where you could thrive? Consider the travel time to your daily activities—will it add more stress to your routine, or free up time for things you care about?
    - **Current House**: Think about your current home. Does it still meet your needs, or have you outgrown it? Does staying here offer you the stability and security you desire, or are there frustrations you’ve been ignoring? Think about how comfortable you feel in your current neighborhood and how much time you spend commuting.

    4. **Emotional and practical reflection**:
    - Take a moment to reflect on the **emotional weight** of this decision. Moving can be stressful, exciting, or both. Consider the potential emotional strain of leaving behind what’s familiar versus the thrill of a fresh start.
    - **Practically speaking**, think about how this move aligns with your goals and values. Are you prepared to take on new challenges, or is staying in your comfort zone the wiser choice for now?

    5. **Make your decision**: Now that you’ve taken the time to reflect on your priorities, emotions, and practical considerations, it’s time to decide. 
    - If you feel that moving to the new house would enhance your quality of life, return `0`.
    - If you believe that staying in your current home is the better decision, return `1`.

    YOU MUST give your decision in the following format: `####value####`.

    Take your time and make the best choice for your life.
    """
    )
    final_answer_int=-1

    while not (final_answer_int==0 or final_answer_int==1):
        answer = client.chat.completions.create(
                model="local-model",
                messages=[
                    {"role": "system", "content": "You are a human being who makes decisions about whether or not to move to another house."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
            )
        response=answer.choices[0].message.content

        if "####" in response:
            start_index = response.index("####") + len("####")
            end_index = response.rindex("####")
            final_answer = response[start_index:end_index].strip()
        else:
                final_answer_int = -1

        try:
            final_answer_int=int(final_answer)
        
        except Exception:
            final_answer_int=-1
      

        with open("change_house.txt", "a") as f:
            f.write(f"Desarrollo del LLM:\n {response}\n")
            f.write(f"Final answer: {final_answer_int} \n-------------------------------------------------\n")
    
    return final_answer



def evaluate_main_trip(client, transport_data, profile):
    prompt = (f"""
    You are a resident of Cambridge, Boston. From this list of economic profiles: ['<$30000','$30000 - $44999','$45000 - $59999','$60000 - $99999','$100000 - $124999','$125000 - $149999','$150000 - $199999','>$200000'] you are an economic profile of {profile}. You are now faced with a decision on which mode of transport to use for commuting to your main activities.

    Given the following characteristics of the transports (all of them are marks between -1 and 1), you should consider which you prefer to use: {transport_data}. But YOUR DECISSION MUST BE THE FINAL LINE OF ANSWER

    You will evaluate the available transport options based on the following factors (remember all variables are marks, the higher the mark is, the better it is):
    1. **Affordability**: How much does each transport mode cost, and how does it fit with your budget and financial priorities? Remember a higher mark means a good price for you. **A higher mark in cost means the house is more affordable (lower cost)**, and **a lower mark means it is more expensive**.
    2. **Diversity**: How does the diversity of the area or route affect your experience or comfort level with using this transport?
    3. **Preference for Zones**: How well does the transport route match your preferred areas or paths of travel?
    4. **Travel Time**: How long will it take to reach your destination using each transport option? **A higher mark in travel time means shorter travel time** (better), while **a lower mark means longer travel time** (worse).

    Before you make your decision, take a deep breath and consider the following:
    1. **Self-Reflection**: Think about your personal situation, background, and financial profile. How important are the cost, the diversity of the route, your preferred zones, and the time it takes to commute? Reflect on your priorities as someone with your specific economic profile.

    2. **Transport Analysis**: Review the characteristics of the transport options. Compare each one in terms of cost, diversity, alignment with your preferred zones, and travel time. Consider which one aligns best with your personal needs and priorities.

    3. **Final Decision**: Based on your reflection and analysis, select the best transport option. If you choose the first option, return `0`, if the second, return `1`, and so on for each option.

    Your RESPONSE MUST be formatted like this: `####value####`.

    Take your time and make the best choice for your life.

    """
    )
    final_answer_int=-1
   
    while not (final_answer_int>=0 and final_answer_int<6):
        answer = client.chat.completions.create(
                model="local-model",
                messages=[
                    {"role": "system", "content": "You are a human being who makes decisions about which transport prefers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
            )
        response=answer.choices[0].message.content

        if "####" in response:
            start_index = response.index("####") + len("####")
            end_index = response.rindex("####")
            final_answer = response[start_index:end_index].strip()
        else:
                final_answer_int = -1


        try:
            final_answer_int=int(final_answer)
        
        except Exception:
            final_answer_int=-1
       


        with open("transport.txt", "a") as f:
            f.write(f"Desarrollo del LLM:\n {response}\n")
            f.write(f"Final answer: {final_answer_int} \n-------------------------------------------------\n")
    
    return final_answer

# Función del servidor WebSocket
async def housing(websocket, path):

    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
    
    while True:
        data = await websocket.recv()
        data = json.loads(data)


        # Extraemos los campos del JSON
        function = data.get("function")
        profile = data.get("profile")
        transports= data.get("transport_op")
        data = data.get("data")
        

        if function == 'change_house': 

            list1, list2 = data
            json_data = {
                "New House": {
                    "Affordability Mark": list1[0],
                    "Diversity Mark": list1[1],
                    "Preferred Location Mark": list1[2],
                    "Travel time optimization Mark": list1[3]
                },
                "Current House": {
                    "Affordability Mark": list2[0],
                    "Diversity Mark": list2[1],
                    "Preferred Location Mark": list2[2],
                    "Travel time optimization Mark": list2[3]
                }
            }
        
            json_string = json.dumps(json_data)
            llm_result = change_house(client, json_string, profile)
            await websocket.send(llm_result)

        elif function== 'evaluate_main_trip':
            json_data = {"Transport_Candidates": []}
            
            i=0

            for  candidate in data:

                json_data["Transport_Candidates"].append({
                    "Transport": ""+transports[i]+"(OPTION "+ str(i) +")",
                    "Cost Mark": candidate[0],
                    "Diversity Mark": candidate[1],
                    "Preference Zone Path Mark": candidate[2],
                    "Travel Time Mark": candidate[3]
                })
                i+=1
            
            json_string = json.dumps(json_data)
            llm_result = evaluate_main_trip(client, json_string, profile)
            await websocket.send(llm_result)


start_server = websockets.serve(housing, "localhost", 8765)

# Ejecutar el servidor indefinidamente
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
