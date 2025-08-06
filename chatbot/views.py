import json
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import ChatSession, ChatMessage
import openai
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def home(request):
    """Main chat interface"""
    return render(request, 'chatbot/home.html')

@csrf_exempt
@require_http_methods(["POST"])
def chat(request):
    """Handle chat messages"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        session_id = data.get('session_id', '')
        model_choice = data.get('model_choice', 'openai')
        
        # Create or get session
        if not session_id:
            session_id = str(uuid.uuid4())
            session = ChatSession.objects.create(
                session_id=session_id,
                model_choice=model_choice
            )
        else:
            session, created = ChatSession.objects.get_or_create(
                session_id=session_id,
                defaults={'model_choice': model_choice}
            )
        
        # Get AI response based on model choice
        if model_choice == 'openai':
            response = get_openai_response(message)
        else:
            response = get_google_response(message)
        
        # Save messages
        ChatMessage.objects.create(
            session=session,
            message=message,
            response=response,
            is_user_message=True
        )
        
        ChatMessage.objects.create(
            session=session,
            message=message,
            response=response,
            is_user_message=False
        )
        
        return JsonResponse({
            'response': response,
            'session_id': session_id,
            'success': True
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'success': False
        }, status=500)

def get_openai_response(message):
    """Get response from OpenAI"""
    try:
        # You'll need to set OPENAI_API_KEY in environment variables
        api_key = os.environ.get('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY')
        print(f"DEBUG: API Key loaded: {api_key[:20] if api_key else 'NOT_FOUND'}...")
        if not api_key:
            return "Sorry, OpenAI API key is not configured. Please set the OPENAI_API_KEY environment variable."
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Zoal AI, a helpful assistant with knowledge about Sudanese and African culture. Respond in a friendly and informative way."},
                {"role": "user", "content": message}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        print(f"DEBUG: OpenAI error: {error_msg}")
        return f"Sorry, I'm having trouble connecting to OpenAI. Please check your API key. Error: {error_msg}"

def get_google_response(message):
    """Get response from Google Gemini"""
    try:
        # You'll need to set GOOGLE_API_KEY in environment variables
        api_key = os.environ.get('GOOGLE_API_KEY') or os.getenv('GOOGLE_API_KEY')
        print(f"DEBUG: Google API Key loaded: {api_key[:20] if api_key else 'NOT_FOUND'}...")
        if not api_key:
            return "Sorry, Google API key is not configured. Please set the GOOGLE_API_KEY environment variable."
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            f"You are Zoal AI, a helpful assistant with knowledge about Sudanese and African culture. Respond in a friendly and informative way. User message: {message}"
        )
        return response.text
    except Exception as e:
        return f"Sorry, I'm having trouble connecting to Google AI. Please check your API key. Error: {str(e)}"

@csrf_exempt
@require_http_methods(["POST"])
def get_chat_history(request):
    """Get chat history for a session"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id', '')
        
        if session_id:
            session = ChatSession.objects.get(session_id=session_id)
            messages = session.messages.all()
            
            history = []
            for msg in messages:
                history.append({
                    'message': msg.message,
                    'response': msg.response,
                    'timestamp': msg.timestamp.isoformat(),
                    'is_user_message': msg.is_user_message
                })
            
            return JsonResponse({
                'history': history,
                'success': True
            })
        else:
            return JsonResponse({
                'history': [],
                'success': True
            })
            
    except ChatSession.DoesNotExist:
        return JsonResponse({
            'history': [],
            'success': True
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'success': False
        }, status=500)
