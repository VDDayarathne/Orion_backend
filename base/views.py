from django.shortcuts import render
import requests
import json
import base64  # Import base64 for encoding image bytes
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

GEMINI_API_KEY = 'AIzaSyAHQnfMDZUcZ-C1ZZpSEAb4kNgvgrLL1rU'  # Replace with your actual Gemini API key

def enhance_prompt_with_gemini(user_prompt, task_objective, task_description):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=' + GEMINI_API_KEY

    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'contents': [{
            'parts': [{
                'text': f"{task_objective}. {task_description}. {user_prompt}"
            }]
        }]
    }

    response = requests.post(url, headers=headers, json=data)

    # Debugging: Print the full response
    print("Response status code:", response.status_code)
    print("Response content:", response.content)

    if response.ok:
        gemini_response = response.json()
        # Check if 'candidates' is in the response and contains data
        if 'candidates' in gemini_response and len(gemini_response['candidates']) > 0:
            if 'content' in gemini_response['candidates'][0] and 'parts' in gemini_response['candidates'][0]['content']:
                enhanced_prompt = gemini_response['candidates'][0]['content']['parts'][0]['text']
                return enhanced_prompt
            else:
                error_message = "Invalid structure in 'candidates'"
                raise KeyError(f"Expected key 'parts' not found in response. Error: {error_message}")
        else:
            error_message = gemini_response.get('error', {}).get('message', 'Invalid response structure')
            raise KeyError(f"Expected key 'candidates' not found in response. Error: {error_message}")
    else:
        error_response = response.json()
        print("Error response:", error_response)
        raise Exception(f"Error from Gemini API: {error_response}")

def generate_images(prompt):
    url = 'https://clipdrop-api.co/text-to-image/v1'

    headers = {
        'x-api-key': '2aee5f564dfe39b501d82dab39633b21cb9848429dee77527c8c32839dc73fc92b3ca56641de83b28696bb98f49e79c7'
    }

    # Sending a POST request with the prompt
    response = requests.post(url, files={'prompt': (None, prompt, 'text/plain')}, headers=headers)

    if response.ok:
        # If the request was successful, return the image content as base64 encoded string
        return base64.b64encode(response.content).decode('utf-8')  # Convert bytes to base64 string
    else:
        response.raise_for_status()


# Define levels, tasks with objectives and descriptions, and challenges
LEVELS = {
    1: {
        'tasks': [
            {
                'description': "Describe a serene beach scene.",
                'objective': "Task 1 Objective: Capture the tranquility and beauty of a peaceful beach setting."
            },
            {
                'description': "Create a futuristic city skyline.",
                'objective': "Task 2 Objective: Imagine and design a city skyline from the future with technological advancements."
            },
            {
                'description': "Illustrate a fantasy forest.",
                'objective': "Task 3 Objective: Depict a magical forest filled with mythical creatures and vibrant colors."
            },
            {
                'description': "Generate an underwater world.",
                'objective': "Task 4 Objective: Create a vibrant and mysterious underwater ecosystem filled with marine life."
            },
            {
                'description': "Design a cozy cabin in winter.",
                'objective': "Task 5 Objective: Capture the warmth and charm of a secluded cabin surrounded by snow."
            }
        ],
        'challenge': "Challenge: Combine elements from all tasks into one cohesive image."
    },
    2: {
        'tasks': [
            {
                'description': "Depict a bustling marketplace.",
                'objective': "Task 1 Objective: Illustrate the lively atmosphere and diversity of a busy marketplace."
            },
            {
                'description': "Visualize a historical event.",
                'objective': "Task 2 Objective: Recreate an iconic moment in history, emphasizing key details and emotions."
            },
            {
                'description': "Create an alien landscape.",
                'objective': "Task 3 Objective: Imagine a strange and otherworldly landscape with alien flora and fauna."
            },
            {
                'description': "Illustrate a character from mythology.",
                'objective': "Task 4 Objective: Bring to life a character from ancient mythology, focusing on their iconic traits."
            },
            {
                'description': "Generate a scene from your favorite book.",
                'objective': "Task 5 Objective: Visualize a memorable scene from your favorite novel, capturing its essence."
            }
        ],
        'challenge': "Challenge: Create an image that tells a story using elements from all tasks."
    },
    3: {
        'tasks': [
            {
                'description': "Design an abstract piece based on emotions.",
                'objective': "Task 1 Objective: Create an abstract work of art that evokes strong emotions through shapes and colors."
            },
            {
                'description': "Illustrate a dreamlike scenario.",
                'objective': "Task 2 Objective: Depict a surreal, dreamlike scene filled with impossible landscapes and elements."
            },
            {
                'description': "Create a portrait of an imaginary creature.",
                'objective': "Task 3 Objective: Design a unique and imaginative creature, focusing on its features and personality."
            },
            {
                'description': "Generate a surreal landscape.",
                'objective': "Task 4 Objective: Create a landscape that challenges reality, blending the real with the surreal."
            },
            {
                'description': "Depict a scene inspired by music.",
                'objective': "Task 5 Objective: Visualize a scene that reflects the rhythm, mood, and energy of a musical piece."
            }
        ],
        'challenge': "Challenge: Synthesize all tasks into a single surreal artwork."
    }
}

@csrf_exempt
def home(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            level_number = data.get('level', None)
            task_number = data.get('task', None)
            user_prompt = data.get('prompt', None)

            if level_number is None or task_number is None or user_prompt is None:
                return JsonResponse({'error': 'Level, task number, and prompt are required.'}, status=400)

            # Validate level and task number
            if level_number not in LEVELS or task_number < 1 or task_number > len(LEVELS[level_number]['tasks']):
                return JsonResponse({'error': 'Invalid level or task number.'}, status=400)

            # Get task description and objective for the selected level and task
            task_info = LEVELS[level_number]['tasks'][task_number - 1]
            task_description = task_info['description']
            task_objective = task_info['objective']

            # Enhance the user prompt using Gemini, with both task description and objective
            enhanced_prompt = enhance_prompt_with_gemini(user_prompt, task_objective, task_description)

            # Generate images using the enhanced prompt
            image_data = generate_images(enhanced_prompt)

            if image_data:
                response_data = {
                    'images': [image_data],  # Wrap in list for future scalability
                    'current_task_description': task_description,
                    'enhanced_prompt': enhanced_prompt,
                    'next_task': task_number + 1 if task_number < len(LEVELS[level_number]['tasks']) else None,
                    'challenge': LEVELS[level_number]['challenge'] if task_number == len(LEVELS[level_number]['tasks']) else None
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Failed to generate images'}, status=500)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON input: {str(e)}'}, status=400)

    return render(request, 'index.html', {'levels': LEVELS})  # Pass levels to the template
