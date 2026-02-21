# EduGenie: Google Gemini Powered Learning Assistant 

EduGenie is a personal AI learning assistant built with Python Flask and Groq AI (LLaMA 3.3 70B). It helps students study smarter with features like smart Q&A, quiz generation, answer validation, flashcards, summarization, translation, and voice support.

## Features
Smart Q&A: Ask academic questions and receive structured AI answers
Concept Explainer:	Understand topics with definitions, analogies, and key points
Quiz Generator:	Generate MCQs with adjustable difficulty
Test Yourself:	Submit answers and receive score, grade, and feedback
Flashcards:	Interactive flip cards with shuffle and tracking
Summarizer:	Convert content into structured bullet-point summaries
Translate and Simplify:	Translate to multiple languages or simplify explanations

## Voice Features
- Voice input for answering questions
- Text-to-speech for responses and feedback
- Automatic reading of score and grade after test submission

  
## Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Backend  | Python, Flask, Flask-CORS          |
| AI Model | Groq API - LLaMA 3.3 70B Versatile |
| Frontend | HTML5, CSS3, JavaScript            |
| Voice    | Web Speech API                     |


## Get API Key
Go to https://console.groq.com  
Create an account and generate an API key.

## Project Structure

```
EduGenie/
│
├── app.py
├── requirements.txt
├── .env
│
├── static/
│   └── style.css
│
└── templates/
    ├── index.html
    ├── ask.html
    ├── explain.html
    ├── quiz.html
    ├── test.html
    ├── flashcards.html
    ├── summary.html
    └── translate.html
```

