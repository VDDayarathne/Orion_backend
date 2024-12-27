from django.shortcuts import render
import requests
import json
import base64
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import google.generativeai as genai

GEMINI_API_KEY = 'AIzaSyCNHr7tntpyPrHDf1z2QVjMrkNH4Z8WqpA'
CLIPDROP_API_KEY = '2aee5f564dfe39b501d82dab39633b21cb9848429dee77527c8c32839dc73fc92b3ca56641de83b28696bb98f49e79c7'  # Replace with your actual ClipDrop API key
IMAGEN_API_KEY = 'AIzaSyDlwTMLPIyV7q1mOP23YtlS1bu1nxZ7_1Y'  # Replace with your Imagen API key
STABILITY_AI_API_KEY = 'sk-Ezo9a98HEdeSzopjxgQrAiLVFMWLiQYcn3iJrrPKkgR8T0m7'

# Configure Imagen API
genai.configure(api_key=IMAGEN_API_KEY)
imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")

# Function to enhance the prompt using Gemini API (working correctly)
def enhance_prompt_with_gemini(user_prompt, task_objective, task_description):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}'
    headers = {'Content-Type': 'application/json'}
    data = {
        'contents': [{
            'parts': [{
                'text': f"{task_objective}. {task_description}. {user_prompt}"
            }]
        }]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.ok:
        gemini_response = response.json()
        try:
            enhanced_prompt = gemini_response['candidates'][0]['content']['parts'][0]['text']
            return enhanced_prompt
        except (KeyError, IndexError):
            raise KeyError("Unexpected response structure from Gemini API.")
    else:
        error_response = response.json()
        raise Exception(f"Error from Gemini API: {error_response}")

# Function to generate images with selected service
def generate_images(service, prompt):
    try:
        if service == 'clipdrop':
            url = 'https://clipdrop-api.co/text-to-image/v1'
            headers = {
                'x-api-key': CLIPDROP_API_KEY
            }

            response = requests.post(url,
                files={
                    'prompt': (None, prompt, 'text/plain')
                },
                headers=headers
            )

            # Log the response for debugging
            print(f"ClipDrop Response: {response.status_code} - {response.text}")

            if response.ok:
                # The content contains the bytes of the returned image
                return base64.b64encode(response.content).decode('utf-8')
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

        elif service == 'limewire':
            url = "https://api.limewire.com/api/image/generation"
            headers = {
                "Content-Type": "application/json",
                "X-Api-Version": "v1",
                "Accept": "application/json",
                "Authorization": "Bearer lmwr_sk_59hmu2ZtUE_UE5bduJldDbXK77hlYPTes3SGbIkOfXQZ6ZTT"
            }
            payload = {
                "prompt": prompt,
                "aspect_ratio": "1:1"
            }

            response = requests.post(url, json=payload, headers=headers)

            # Log the response for debugging
            print(f"LimeWire Response: {response.status_code} - {response.text}")

            if response.ok:
                return base64.b64encode(response.content).decode('utf-8')
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

        elif service == 'imagen3':
            result = imagen.generate_images(
                prompt=prompt,
                number_of_images=1,  # Generate one image for this example
                safety_filter_level="block_only_high",
                person_generation="allow_adult",
                aspect_ratio="3:4",
                negative_prompt=""
            )

            # Assuming the API returns images as PIL objects
            images = []
            for image in result.images:
                image_base64 = base64.b64encode(image._pil_image.tobytes()).decode('utf-8')
                images.append(image_base64)

            return images[0] if images else None

        elif service == 'stability_ai':
            url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
            headers = {
                "authorization": f"Bearer {STABILITY_AI_API_KEY}",
                "accept": "image/*"
            }
            data = {
                "prompt": prompt,
                "output_format": "jpeg"
            }

            response = requests.post(url, headers=headers, data=data, files={"none": ""})
            print(f"Stability AI Response: {response.status_code}")

            if response.status_code == 200:
                return base64.b64encode(response.content).decode("utf-8")
            else:
                error_message = response.json() if response.headers.get("Content-Type") == "application/json" else response.text
                print(f"Error: {response.status_code} - {error_message}")
                return None

        else:
            return None

    except requests.RequestException as e:
        print(f"RequestException occurred: {str(e)}")
        raise e

    except Exception as e:
        print(f"Unexpected exception: {str(e)}")
        raise e

# Define levels, tasks with objectives and descriptions, and challenges
LEVELS = {
    1: {
        'tasks': [
            {
                'task_number': 1,
                'description': "In the heart of the Acropolis of Code, an ancient Oracle has awakened, foretelling a coming storm that threatens the harmony between man and machine. Queen Sophia, wise and just, has summoned the most skilled promptsmiths to her court. As a Promptian, your first task is to craft a simple yet powerful prompt that can guide the Oracle to reveal more about this impending danger. The prompt must be clear and precise, as the Oracle's response will shape the kingdom's next steps.",
                'objective': "Create a prompt that will ask the Oracle to describe the nature of the threat posed by the Silencers and suggest ways to safeguard the kingdom. Keep it concise, ensuring the Oracle understands and responds with valuable insights."
            },
            {
                'task_number': 2,
                'description': "Create a futuristic city skyline.",
                'objective': "Imagine and design a city skyline from the future with technological advancements."
            },
            {
                'task_number': 3,
                'description': "Illustrate a fantasy forest.",
                'objective': "Depict a magical forest filled with mythical creatures and vibrant colors."
            },
            {
                'task_number': 4,
                'description': "Generate an underwater world.",
                'objective': "Create a vibrant and mysterious underwater ecosystem filled with marine life."
            },
            {
                'task_number': 5,
                'description': "Design a cozy cabin in winter.",
                'objective': "Capture the warmth and charm of a secluded cabin surrounded by snow."
            }
        ],
        'challenge': "Combine elements from all tasks into one cohesive image."
    },
    2: {
        'tasks': [
            {
                'task_number': 1,
                'description': "Depict a bustling marketplace.",
                'objective': "Illustrate the lively atmosphere and diversity of a busy marketplace."
            },
            {
                'task_number': 2,
                'description': "Visualize a historical event.",
                'objective': "Recreate an iconic moment in history, emphasizing key details and emotions."
            },
            {
                'task_number': 3,
                'description': "Create an alien landscape.",
                'objective': "Imagine a strange and otherworldly landscape with alien flora and fauna."
            },
            {
                'task_number': 4,
                'description': "Illustrate a character from mythology.",
                'objective': "Bring to life a character from ancient mythology, focusing on their iconic traits."
            },
            {
                'task_number': 5,
                'description': "Generate a scene from your favorite book.",
                'objective': "Visualize a memorable scene from your favorite novel, capturing its essence."
            }
        ],
        'challenge': "Create an image that tells a story using elements from all tasks."
    },
    3: {
        'tasks': [
            {
                'task_number': 1,
                'description': "Design an abstract piece based on emotions.",
                'objective': "Create an abstract work of art that evokes strong emotions through shapes and colors."
            },
            {
                'task_number': 2,
                'description': "Illustrate a dreamlike scenario.",
                'objective': "Depict a surreal, dreamlike scene filled with impossible landscapes and elements."
            },
            {
                'task_number': 3,
                'description': "Create a portrait of an imaginary creature.",
                'objective': "Design a unique and imaginative creature, focusing on its features and personality."
            },
            {
                'task_number': 4,
                'description': "Generate a surreal landscape.",
                'objective': "Create a landscape that challenges reality, blending the real with the surreal."
            },
            {
                'task_number': 5,
                'description': "Depict a scene inspired by music.",
                'objective': "Visualize a scene that reflects the rhythm, mood, and energy of a musical piece."
            }
        ],
        'challenge': "Synthesize all tasks into a single surreal artwork."
    }
}

@csrf_exempt
def make_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            level_number = data.get('level', None)
            task_number = data.get('task', None)
            user_prompt = data.get('prompt', None)
            service = data.get('service', 'clipdrop')

            # Validate input data
            if level_number is None or task_number is None or user_prompt is None:
                return JsonResponse({'error': 'Level, task number, and prompt are required.'}, status=400)

            # Validate level
            if level_number not in LEVELS:
                return JsonResponse({'error': 'Invalid level number.'}, status=400)

            # Validate task number
            tasks_for_level = LEVELS[level_number].get('tasks', [])
            if task_number <= 0 or task_number > len(tasks_for_level):
                return JsonResponse({'error': 'Invalid task number for the selected level.'}, status=400)

            # Get task description and objective for the selected task
            selected_task = tasks_for_level[task_number - 1]
            task_description = selected_task['description']
            task_objective = selected_task['objective']

            # Enhance the user prompt using Gemini (Assumed to be working correctly)
            enhanced_prompt = enhance_prompt_with_gemini(user_prompt, task_objective, task_description)

            # Debugging for enhanced prompt construction
            print(f"Enhanced Prompt for Task {task_number} in Level {level_number}: {enhanced_prompt}")

            # Generate images using the selected service
            image_data = generate_images(service, enhanced_prompt)

            if image_data:
                response_data = {
                    'images': [image_data],
                    'current_task_number': task_number,
                    'current_task_description': task_description,
                    'enhanced_prompt': enhanced_prompt,
                    'next_task_number': task_number + 1 if task_number < len(tasks_for_level) else None,
                    'challenge': LEVELS[level_number]['challenge']
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': f"Failed to generate image for {service}. Please check the API response."}, status=500)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON input: {str(e)}'}, status=400)

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'index.html', {'levels': LEVELS})