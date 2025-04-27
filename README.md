# Palm Reader AI

A web application that uses OpenAI's GPT-4 Vision API to analyze palm images and provide palm readings.

## Features

- Upload palm images in JPG, JPEG, or PNG format
- Get detailed palm readings based on palmistry principles
- View your palm image alongside the reading
- Simple and intuitive user interface

## Requirements

- Python 3.6+
- Flask
- OpenAI API key

## Installation

1. Clone this repository or download the source code.

2. Install the required dependencies:
   ```
   pip install flask openai python-dotenv werkzeug
   ```

3. Set up your OpenAI API key:
   - Edit the `.env` file in the project root directory
   - Replace the placeholder with your actual OpenAI API key: 
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```
   - Optionally, you can specify a different model by uncommenting and setting:
     ```
     OPENAI_MODEL=gpt-4-vision-preview
     ```

## Usage

1. Run the application:
   ```
   python palm.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`

3. Upload a clear image of your palm
   - Make sure the image is well-lit and shows the palm lines clearly
   - Supported formats: JPG, JPEG, PNG

4. View your palm reading results

## Troubleshooting

If you encounter any issues:

1. **API Key Error**: Make sure your OpenAI API key is correctly set in the `.env` file
   - The key should be valid and have access to the GPT-4 Vision model
   - The application will show a warning if the API key is not set or is using the default placeholder

2. **Model Access**: Ensure your OpenAI account has access to the GPT-4 Vision model
   - If you don't have access, you may need to join a waitlist or upgrade your account

3. **Image Upload Issues**: 
   - Check that your image is in a supported format (JPG, JPEG, PNG)
   - Ensure the image file is not corrupted
   - Try using a different image if problems persist

## Important Notes

- This application requires an OpenAI API key with access to the GPT-4 Vision model
- Palm readings are for entertainment purposes only
- The quality of the reading depends on the clarity of the uploaded palm image

## Directory Structure

```
palm/
├── palm.py              # Main application file
├── .env                 # Environment variables (API key)
├── static/              # Static files
│   └── uploads/         # Uploaded palm images
└── templates/           # HTML templates
    ├── index.html       # Upload page
    └── result.html      # Results page
```

## License

This project is open source and available under the MIT License.