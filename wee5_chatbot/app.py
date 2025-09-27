"""
Simple Traditional Chatbot using Microsoft Bot Framework
MSAI-631 - AI for Human-Computer Interaction

Clean implementation following Bot Framework patterns
"""

import logging
from datetime import datetime
from aiohttp import web
from aiohttp.web import Request, Response
from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount, Activity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleTraditionalBot(ActivityHandler):
    """
    Simple Traditional Chatbot that extends basic EchoBot functionality
    """
    
    def __init__(self):
        super().__init__()
        logger.info("SimpleTraditionalBot initialized")
        
        # Bot capabilities
        self.capabilities = [
            "Echo and reverse your messages",
            "Process simple commands",
            "Provide help information",
            "Handle greetings and farewells", 
            "Perform basic calculations",
            "Tell simple jokes",
            "Show current time"
        ]
        
        # Simple jokes
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the robot go on a diet? It had a byte problem!",
            "What do you call a chatbot that sings? A vocal bot!"
        ]
        self.joke_index = 0

    async def on_message_activity(self, turn_context: TurnContext):
        """Handle incoming message activity"""
        user_message = turn_context.activity.text
        
        if not user_message:
            response_text = "I didn't receive any text. Please type something!"
            await turn_context.send_activity(MessageFactory.text(response_text))
            return
        
        user_message = user_message.strip()
        logger.info(f"Received message: {user_message}")
        
        # Process the message
        response_text = self.process_message(user_message)
        
        # Send response
        await turn_context.send_activity(MessageFactory.text(response_text))

    def process_message(self, message: str) -> str:
        """Process incoming message and return appropriate response"""
        message_lower = message.lower()
        
        # Command processing
        if message.startswith('/'):
            return self.handle_command(message)
        
        # Greeting patterns
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I'm a simple traditional chatbot. Type /help to see what I can do."
        
        # Farewell patterns  
        if any(farewell in message_lower for farewell in ['bye', 'goodbye', 'see you', 'farewell']):
            return "Goodbye! Thanks for chatting with me. Come back anytime!"
        
        # Help requests
        if 'help' in message_lower or 'what can you do' in message_lower:
            return self.show_help()
        
        # Capabilities inquiry
        if 'capabilities' in message_lower or 'features' in message_lower:
            return self.show_capabilities()
        
        # Question handling
        if message.endswith('?'):
            return self.handle_question(message)
        
        # Default behavior - Enhanced echo with reversal
        return self.handle_default_echo(message)

    def handle_command(self, message: str) -> str:
        """Handle slash commands"""
        parts = message.split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command == '/help':
            return self.show_help()
        elif command == '/capabilities':
            return self.show_capabilities()
        elif command == '/reverse':
            if args:
                return f"Reversed: {args[::-1]}"
            else:
                return "Usage: /reverse [text to reverse]"
        elif command == '/time':
            return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        elif command == '/joke':
            joke = self.jokes[self.joke_index]
            self.joke_index = (self.joke_index + 1) % len(self.jokes)
            return f"Here's a joke: {joke}"
        elif command == '/calculate':
            return self.simple_calculator(args)
        else:
            return f"Unknown command: {command}. Type /help for available commands."

    def simple_calculator(self, expression: str) -> str:
        """Perform simple calculations"""
        if not expression:
            return "Usage: /calculate [num1] [operator] [num2]. Example: /calculate 5 + 3"
        
        try:
            parts = expression.split()
            if len(parts) != 3:
                return "Please use format: number operator number"
            
            num1 = float(parts[0])
            operator = parts[1]
            num2 = float(parts[2])
            
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    return "Error: Cannot divide by zero"
                result = num1 / num2
            else:
                return f"Unknown operator: {operator}. Use +, -, *, or /"
            
            return f"{num1} {operator} {num2} = {result}"
            
        except ValueError:
            return "Error: Please use valid numbers"
        except Exception as e:
            return f"Calculation error: {str(e)}"

    def handle_question(self, message: str) -> str:
        """Handle questions"""
        message_lower = message.lower()
        
        if 'name' in message_lower:
            return "I'm a Simple Traditional Chatbot built for MSAI-631."
        elif 'time' in message_lower:
            return f"The current time is {datetime.now().strftime('%H:%M:%S')}"
        elif 'date' in message_lower:
            return f"Today's date is {datetime.now().strftime('%Y-%m-%d')}"
        elif 'how are you' in message_lower:
            return "I'm functioning well! All systems operational. How are you?"
        else:
            return f"That's an interesting question. Here it is reversed: {message[::-1]}"

    def handle_default_echo(self, message: str) -> str:
        """Default handler - Enhanced echo with reversal"""
        reversed_message = message[::-1]
        return f"You said: {message}. Reversed: {reversed_message}"

    def show_help(self) -> str:
        """Show available commands"""
        return """Available commands:
/help - Show this help message
/capabilities - List bot capabilities
/reverse [text] - Reverse the provided text
/time - Show current time
/joke - Tell a joke
/calculate [num1] [op] [num2] - Simple calculator

You can also:
- Say hello for a greeting
- Say goodbye for farewell
- Ask questions ending with ?
- Type anything to see it echoed and reversed"""

    def show_capabilities(self) -> str:
        """Show bot capabilities"""
        capabilities_text = "My capabilities include:\n"
        for i, capability in enumerate(self.capabilities, 1):
            capabilities_text += f"{i}. {capability}\n"
        capabilities_text += "\nI can handle malformed questions and provide helpful responses."
        return capabilities_text

    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):
        """Greet new members"""
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                welcome_text = "Welcome! I'm a Simple Traditional Chatbot. Type /help to get started."
                await turn_context.send_activity(MessageFactory.text(welcome_text))


# Create bot instance
BOT = SimpleTraditionalBot()

async def messages(req: Request) -> Response:
    """Main message handler endpoint"""
    try:
        body = await req.json()
        activity = Activity().deserialize(body)
        
        # Simple response for different activity types
        if activity.type == "message" and activity.text:
            response_text = BOT.process_message(activity.text)
        elif activity.type == "conversationUpdate" and activity.members_added:
            response_text = "Welcome! I'm a Simple Traditional Chatbot. Type /help to get started."
        else:
            response_text = "I can only process text messages right now."
        
        # Create response
        response_data = {
            "type": "message",
            "text": response_text,
            "from": {
                "id": "bot",
                "name": "SimpleTraditionalBot"
            }
        }
        
        return web.json_response(response_data)
        
    except Exception as e:
        logger.error(f"Error in messages handler: {e}")
        return web.Response(text="Error processing message", status=500)

async def health_check(req: Request) -> Response:
    """Health check endpoint"""
    return web.json_response({"status": "healthy", "bot": "SimpleTraditionalBot"})

async def root_handler(req: Request) -> Response:
    """Root endpoint"""
    return web.Response(
        text="Simple Traditional Chatbot is running!\nConnect with Bot Framework Emulator at: http://localhost:3978/api/messages",
        content_type="text/plain"
    )

# Create web application
app = web.Application()

# Add routes
app.router.add_post("/api/messages", messages)
app.router.add_get("/health", health_check)
app.router.add_get("/", root_handler)

if __name__ == "__main__":
    try:
        print("Starting Simple Traditional Chatbot...")
        print("Server will run on http://localhost:3978")
        print("Bot endpoint: http://localhost:3978/api/messages")
        print("Use Bot Framework Emulator to connect and test")
        print("Press Ctrl+C to stop")
        
        # Run the application
        web.run_app(app, host="localhost", port=3978)
        
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Error starting bot: {e}")
        logger.error(f"Startup error: {e}")