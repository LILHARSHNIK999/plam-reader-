import os
import base64
from flask import Flask, render_template, request, redirect, url_for, flash, session
import google.generativeai as genai
from werkzeug.utils import secure_filename
import secrets
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from .env file if it exists
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set the API key directly for Google Gemini
GEMINI_API_KEY = "AIzaSyClrhH15h-x1_hVMpicFR28ZtDQGrhClCg"

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Set the model directly
GEMINI_MODEL = "gemini-1.5-pro"  # This is Google's model that supports vision

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_palm_image(image_path):
    try:
        # Load the image using PIL
        image = Image.open(image_path)
        
        # Check if API key is valid
        if not GEMINI_API_KEY or GEMINI_API_KEY == 'YOUR_GEMINI_API_KEY':
            return "Error: Google Gemini API key is not set. Please configure your API key."
        
        try:
            # Initialize the Gemini model
            model = genai.GenerativeModel(GEMINI_MODEL)
            
            # Create the prompt
            prompt = """
            You are an expert palm reader. Analyze the palm image provided and give a detailed reading covering 
            the major lines (heart, head, life, fate), mounts, and any special markings. 
            Provide insights about personality, career, relationships, and potential future based on palmistry principles.
            """
            
            # Generate content with the image
            response = model.generate_content([prompt, image])
            
            # Extract and return the palm reading
            return response.text
            
        except Exception as e:
            error_message = str(e)
            if "API key" in error_message.lower():
                return "Error: Invalid Google Gemini API key. Please check your API key configuration."
            elif "model" in error_message.lower():
                return f"Error: The model '{GEMINI_MODEL}' may not be available. Please check your model configuration."
            elif "quota" in error_message.lower() or "limit" in error_message.lower():
                return "Error: Your Google Gemini account has exceeded its quota or doesn't have sufficient credits. Please check your billing details."
            else:
                return f"Error analyzing palm image with Gemini: {error_message}"
                
    except Exception as e:
        return f"Error reading or processing image file: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'palm_image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['palm_image']
        
        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Analyze the palm image
            reading = analyze_palm_image(file_path)
            
            # Store the reading and image path in session
            session['reading'] = reading
            session['image_path'] = file_path
            
            return redirect(url_for('result'))
        else:
            flash('Allowed file types are png, jpg, jpeg')
            return redirect(request.url)
    
    return render_template('index.html')

@app.route('/result')
def result():
    reading = session.get('reading', 'No reading available')
    image_path = session.get('image_path', None)
    
    # Get just the filename for display
    image_filename = os.path.basename(image_path) if image_path else None
    
    return render_template('result.html', reading=reading, image_filename=image_filename)

if __name__ == '__main__':
    # Check if Gemini API key is set to a valid value
    if not GEMINI_API_KEY or GEMINI_API_KEY == 'YOUR_GEMINI_API_KEY':
        print("\n" + "="*80)
        print("WARNING: Valid GEMINI_API_KEY not found!")
        print("The application will start but palm reading functionality will not work.")
        print("\nTo fix this issue:")
        print("1. Edit the palm.py file")
        print("2. Replace 'YOUR_GEMINI_API_KEY' with your actual Google Gemini API key")
        print("3. Restart the application")
        print("="*80 + "\n")
    else:
        print(f"Using Google Gemini model: {GEMINI_MODEL}")
        print("Application is ready! Access it at http://127.0.0.1:5000")
    
    # Start the Flask application
    app.run(debug=True, port=5001)  # Using a different port to avoid conflicts