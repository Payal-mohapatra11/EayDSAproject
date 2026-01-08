from groq import Groq
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

client = Groq(api_key=settings.GROQ_API_KEY)

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question', '')
        
        response = client.chat.completions.create(model="llama-3.1-8b-instant",messages=[ { 
            "role": "system",
            "content": (
                "You are an expert EasyDSA Tutor." 
                "Only answer Data Structures and Algorithms related questions."
                "Explain step-by-step solutions with examles where application is necessary."
                "Always include time and space complexity in your answers."
                "Give code snippets in Java,C++ or Python if the question requires coding and give the step by step explanation for the code."
            )
        },
             {
              "role":"user",
              "content": question
          }                                                                      
        ],
          
          temperature=0.6
          
          )
        answer = response.choices[0].message.content
        return JsonResponse({"answer": answer})
    
    return JsonResponse({"error":"Invalid request method."},status=400)
        