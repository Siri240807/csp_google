#!/usr/bin/env python3
"""
Web interface for the AI Customer Issue Analyzer + Auto-Resolution Agent.
"""

import os
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
from orchestrator import SupportOrchestrator
import asyncio
import threading

# Load environment variables
load_dotenv()

app = Flask(__name__)
orchestrator = SupportOrchestrator()

# HTML template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Customer Support Agent</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #10b981;
            --dark: #1e293b;
            --light: #f8fafc;
            --gray: #94a3b8;
            --glass-bg: rgba(255, 255, 255, 0.15);
            --glass-border: rgba(255, 255, 255, 0.2);
            --glass-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #4f46e5, #7c3aed, #ec4899);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            min-height: 100vh;
            padding: 20px;
            color: var(--light);
        }
        
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            padding: 40px 20px;
            animation: fadeInDown 0.8s ease;
        }
        
        h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        
        .subtitle {
            font-size: 1.2rem;
            font-weight: 300;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 20px;
            border: 1px solid var(--glass-border);
            box-shadow: var(--glass-shadow);
            padding: 30px;
            margin-bottom: 30px;
            animation: fadeInUp 0.8s ease;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(31, 38, 135, 0.25);
        }
        
        .input-section {
            margin-bottom: 30px;
        }
        
        textarea {
            width: 100%;
            height: 180px;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid var(--glass-border);
            background: rgba(255, 255, 255, 0.1);
            color: var(--light);
            font-family: 'Poppins', sans-serif;
            font-size: 1rem;
            resize: vertical;
            transition: all 0.3s ease;
        }
        
        textarea:focus {
            outline: none;
            border-color: var(--primary);
            background: rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3);
        }
        
        textarea::placeholder {
            color: rgba(255, 255, 255, 0.6);
        }
        
        .button-group {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        
        button {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 15px;
            font-family: 'Poppins', sans-serif;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
            flex: 1;
            min-width: 150px;
        }
        
        button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 25px rgba(99, 102, 241, 0.6);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .secondary-btn {
            background: rgba(255, 255, 255, 0.15);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        
        .secondary-btn:hover {
            background: rgba(255, 255, 255, 0.25);
            box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 30px;
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: var(--primary);
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .response {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            margin-top: 20px;
            animation: fadeIn 0.5s ease;
        }
        
        .response-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .response-title {
            font-size: 1.5rem;
            font-weight: 600;
        }
        
        .response-meta {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .meta-item {
            background: rgba(99, 102, 241, 0.2);
            padding: 8px 15px;
            border-radius: 50px;
            font-size: 0.9rem;
        }
        
        .solution-content {
            line-height: 1.6;
            background: rgba(0, 0, 0, 0.1);
            padding: 20px;
            border-radius: 15px;
            white-space: pre-wrap;
        }
        
        .solution-content strong {
            color: var(--secondary);
        }
        
        .solution-content h3 {
            color: var(--secondary);
            margin: 20px 0 10px;
        }
        
        .solution-content ul, .solution-content ol {
            padding-left: 20px;
            margin: 10px 0;
        }
        
        .solution-content li {
            margin-bottom: 8px;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .examples {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .example-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .example-card:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-3px);
        }
        
        .example-title {
            font-weight: 600;
            margin-bottom: 10px;
            color: var(--secondary);
        }
        
        .example-text {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        footer {
            text-align: center;
            padding: 30px 0;
            opacity: 0.7;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 2rem;
            }
            
            .glass-card {
                padding: 20px;
            }
            
            .button-group {
                flex-direction: column;
            }
            
            button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>AI Customer Support Agent</h1>
            <p class="subtitle">Enterprise-grade multi-agent system powered by Google Gemini for intelligent customer issue resolution</p>
        </header>
        
        <main>
            <div class="glass-card">
                <div class="input-section">
                    <textarea id="customerMessage" placeholder="Enter customer message here... For example: 'I ordered product XYZ last week but haven't received it yet. My order ID is ORD-12345.'"></textarea>
                    
                    <div class="button-group">
                        <button type="submit" id="submitBtn">Generate AI Response</button>
                        <button type="button" class="secondary-btn" id="clearBtn">Clear</button>
                    </div>
                </div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Processing your request with AI...</p>
                </div>
                
                <div id="responseArea"></div>
            </div>
            
            <div class="glass-card">
                <h2 style="margin-bottom: 20px;">Example Messages</h2>
                <div class="examples">
                    <div class="example-card" data-example="I ordered product XYZ last week but haven't received it yet. My order ID is ORD-12345.">
                        <div class="example-title">📦 Shipping Issue</div>
                        <div class="example-text">Customer hasn't received their order</div>
                    </div>
                    <div class="example-card" data-example="There's a bug in your mobile app. It crashes every time I try to login.">
                        <div class="example-title">🐛 Technical Support</div>
                        <div class="example-text">App crashing issue with login</div>
                    </div>
                    <div class="example-card" data-example="I'd like to return the item I purchased because it's not what I expected.">
                        <div class="example-title">↩️ Return Request</div>
                        <div class="example-text">Customer wants to return a product</div>
                    </div>
                </div>
            </div>
        </main>
        
        <footer>
            <p>AI Customer Issue Analyzer + Auto-Resolution Agent • Powered by Google Gemini</p>
        </footer>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const form = document.getElementById('supportForm');
            const submitBtn = document.getElementById('submitBtn');
            const clearBtn = document.getElementById('clearBtn');
            const messageInput = document.getElementById('customerMessage');
            const loading = document.getElementById('loading');
            const responseArea = document.getElementById('responseArea');
            
            // Example cards click handler
            document.querySelectorAll('.example-card').forEach(card => {
                card.addEventListener('click', function() {
                    messageInput.value = this.getAttribute('data-example');
                    messageInput.focus();
                });
            });
            
            // Submit handler
            submitBtn.addEventListener('click', async function(e) {
                e.preventDefault();
                
                const message = messageInput.value;
                
                if (!message.trim()) {
                    alert('Please enter a customer message');
                    return;
                }
                
                loading.style.display = 'block';
                responseArea.innerHTML = '';
                
                try {
                    const response = await fetch('/api/process', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    });
                    
                    const data = await response.json();
                    loading.style.display = 'none';
                    
                    if (response.ok) {
                        responseArea.innerHTML = `
                            <div class="response">
                                <div class="response-header">
                                    <div class="response-title">AI Generated Response</div>
                                    <div class="response-meta">
                                        <div class="meta-item">Category: ${data.category}</div>
                                        <div class="meta-item">Confidence: ${(data.confidence * 100).toFixed(1)}%</div>
                                        <div class="meta-item">Session: ${data.session_id.substring(0, 8)}...</div>
                                    </div>
                                </div>
                                <div class="solution-content">${data.solution}</div>
                            </div>
                        `;
                    } else {
                        responseArea.innerHTML = `
                            <div class="response" style="background: rgba(239, 68, 68, 0.1);">
                                <div class="response-header">
                                    <div class="response-title">Error</div>
                                </div>
                                <div class="solution-content">
                                    <p>${data.error || 'An error occurred processing your request'}</p>
                                </div>
                            </div>
                        `;
                    }
                } catch (error) {
                    loading.style.display = 'none';
                    responseArea.innerHTML = `
                        <div class="response" style="background: rgba(239, 68, 68, 0.1);">
                            <div class="response-header">
                                <div class="response-title">Connection Error</div>
                            </div>
                            <div class="solution-content">
                                <p>Failed to connect to the server: ${error.message}</p>
                            </div>
                        </div>
                    `;
                }
            });
            
            // Clear handler
            clearBtn.addEventListener('click', function() {
                messageInput.value = '';
                responseArea.innerHTML = '';
                messageInput.focus();
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Serve the main web page."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/process', methods=['POST'])
def process_message():
    """API endpoint to process customer messages."""
    try:
        data = request.get_json()
        customer_message = data.get('message', '')
        
        if not customer_message:
            return jsonify({'error': 'No message provided'}), 400
            
        # Run the async function in a separate thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(orchestrator.process_customer_message(customer_message))
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)