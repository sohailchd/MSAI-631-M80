# Simple Traditional Chatbot - MSAI-631 Project

A rule-based chatbot implementation using Microsoft Bot Framework, built for educational purposes to demonstrate traditional (non-LLM) conversational AI approaches.

## Project Overview

This chatbot demonstrates traditional AI conversation techniques including:
- Rule-based response generation
- Pattern matching for natural language
- Command processing
- Input validation and error handling
- Extensible architecture for AI service integration

## Setup Instructions

### 1. Create Anaconda Environment

First, create a new Anaconda environment with Python 3.8.2 as specified in the project requirements:

```bash
conda create --name MSAI631_MBF python==3.8.2
```

Activate the environment:

```bash
conda activate MSAI631_MBF
```

### 2. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

If you encounter issues with the cffi package, run:

```bash
pip -vvv install --upgrade --force-reinstall cffi
```

### 3. Download Bot Framework Emulator

Download and install the Bot Framework Emulator for testing:
- Go to: https://github.com/microsoft/BotFramework-Emulator/releases
- Download the version for your operating system
- Install the emulator

## Running the Bot

1. Start the bot application:

```bash
python app.py
```

You should see output similar to:
```
Starting Simple Traditional Chatbot...
Server will run on http://localhost:3978
Bot endpoint: http://localhost:3978/api/messages
Use Bot Framework Emulator to connect and test
```

2. Open Bot Framework Emulator

3. Click "Open Bot" and enter the endpoint URL:
```
http://localhost:3978/api/messages
```

4. Click "Connect" (leave App ID and Password empty for local development)

## Bot Capabilities

### Commands
- `/help` - Show available commands
- `/capabilities` - List bot features
- `/reverse [text]` - Reverse any text
- `/time` - Get current date and time
- `/joke` - Hear a programming joke
- `/calculate [num1] [op] [num2]` - Simple calculator

### Natural Language
- Greetings: "hello", "hi", "hey" 
- Farewells: "bye", "goodbye", "farewell"
- Questions: Any message ending with "?"
- Default: Echo and reverse any other text

### Example Interactions

```
User: Hello!
Bot: Hello! I'm a simple traditional chatbot. Type /help to see what I can do.

User: /reverse Hello World
Bot: Reversed: dlroW olleH

User: /calculate 15 + 25
Bot: 15.0 + 25.0 = 40.0

User: What's your name?
Bot: I'm a Simple Traditional Chatbot built for MSAI-631.

User: Random text
Bot: You said: Random text. Reversed: txet modnaR
```

## Project Structure

```
project-root/
├── app.py              # Main bot application
├── requirements.txt    # Python dependencies  
├── README.md          # This file
└── screenshots/       # Documentation screenshots
```

## Technical Details

### Architecture
- **Framework**: Microsoft Bot Framework 4.x
- **Language**: Python 3.8.2
- **Web Server**: aiohttp
- **Pattern**: ActivityHandler-based bot

### Key Features
- Rule-based message processing
- Command pattern implementation
- Pattern matching for natural language
- Error handling for malformed input
- Extensible command system
- Bot Framework Emulator compatible

### Error Handling
The bot gracefully handles:
- Empty or null messages
- Unknown commands
- Malformed calculator input
- Network errors
- Invalid JSON requests

## Testing Scenarios

1. **Basic Commands**: Test all slash commands
2. **Natural Language**: Try greetings, questions, farewells
3. **Error Cases**: Send empty messages, invalid commands
4. **Calculator**: Test math operations including edge cases
5. **Default Behavior**: Send random text to see reversal

## Extension Possibilities

This bot provides a foundation for:
- Azure Cognitive Services integration
- LUIS (Language Understanding) integration
- Database connectivity for persistent conversations
- Multi-channel deployment (Teams, Slack, etc.)
- Advanced state management
- Rich media responses

## Troubleshooting

### Common Issues

1. **Port 3978 already in use**
   - Kill any existing processes using the port
   - Or change the port in app.py

2. **Bot Framework Emulator connection fails**
   - Ensure the bot is running first
   - Check the endpoint URL includes `/api/messages`
   - Verify no firewall blocking localhost:3978

3. **Dependency installation errors**
   - Ensure using Python 3.8.2 specifically
   - Try the cffi reinstall command above
   - Consider using conda install for problematic packages

4. **Bot not responding**
   - Check console for error messages
   - Verify JSON formatting in requests
   - Test the /health endpoint first

### Debugging

- Check console output for detailed error messages
- Use the /health endpoint to verify bot is running
- Test basic connectivity before complex interactions

## Development Notes

This implementation follows the Microsoft Bot Framework patterns while maintaining simplicity for educational purposes. The code is well-commented and structured for easy modification and extension.

## Academic Context

Built for MSAI-631 - Artificial Intelligence for Human-Computer Interaction course, demonstrating traditional chatbot development approaches before the LLM era.