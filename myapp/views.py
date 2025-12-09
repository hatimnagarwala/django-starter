from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Django Starter</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                color: white;
            }
            .container {
                text-align: center;
                background: rgba(255, 255, 255, 0.1);
                padding: 50px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            h1 {
                font-size: 3em;
                margin: 0;
                animation: fadeIn 1s ease-in;
            }
            p {
                font-size: 1.5em;
                margin-top: 20px;
            }
            .badge {
                display: inline-block;
                background: rgba(255, 255, 255, 0.2);
                padding: 10px 20px;
                border-radius: 25px;
                margin: 10px;
                font-size: 0.9em;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Django Starter App</h1>
            <p>Successfully deployed on Azure Container Apps! ☁️</p>
            <div>
                <span class="badge">✅ Django 5.2.9</span>
                <span class="badge">🐳 Docker</span>
                <span class="badge">☁️ Azure</span>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
