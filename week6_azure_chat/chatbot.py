"""
AI-Integrated Chatbot with Azure Cognitive Services
MSAI-631 - AI for Human-Computer Interaction

This chatbot integrates Azure AI Language Services for sentiment analysis
and entity recognition, extending the traditional chatbot from Topic 5.

Author: Basar Chowdhury
Date: Oct 5
Course: MSAI-631
Project: AI Service Integration
"""

import os
import logging
from datetime import datetime
from aiohttp import web
from aiohttp.web import Request, Response
from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount, Activity
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Config:
    """
    Configuration class for bot and Azure AI services
    Retrieves sensitive credentials from environment variables
    """
    # Bot configuration
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    
    # Azure AI Language Service configuration
    # These should be set as environment variables for security
    AI_SERVICE_ENDPOINT = os.environ.get(
        "MicrosoftAIServiceEndpoint",
        "YOUR_ENDPOINT_HERE"
    )
    AI_SERVICE_KEY = os.environ.get(
        "MicrosoftAPIKey",
        "MS_AZURE_API_KEY"
    )
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        if cls.AI_SERVICE_ENDPOINT == "YOUR_ENDPOINT_HERE":
            logger.warning("Azure AI Service endpoint not configured!")
            logger.warning("Set environment variable: MicrosoftAIServiceEndpoint")
            return False
        
        if cls.AI_SERVICE_KEY == "YOUR_KEY_HERE":
            logger.warning("Azure AI Service key not configured!")
            logger.warning("Set environment variable: MicrosoftAPIKey")
            return False
        
        return True

class AIIntegratedBot(ActivityHandler):
    """
    Enhanced chatbot with Azure AI Language Services integration
    Provides sentiment analysis and intelligent response generation
    """
    
    def __init__(self, text_analytics_client=None):
        super().__init__()
        logger.info("Initializing AI-Integrated Chatbot")
        
        # Store Azure AI client
        self.text_analytics_client = text_analytics_client
        self.ai_enabled = text_analytics_client is not None
        
        if self.ai_enabled:
            logger.info("Azure AI Services enabled")
        else:
            logger.warning("Azure AI Services not available - running in basic mode")
        
        # Bot capabilities
        self.capabilities = [
            "Sentiment analysis of your messages",
            "Entity recognition and extraction",
            "Intelligent response generation",
            "Command processing",
            "Conversation context awareness",
            "Help and capability information"
        ]
        
        # Response templates based on sentiment
        self.sentiment_responses = {
            "positive": [
                "I'm glad you're feeling positive! How can I help you further?",
                "Your positive energy is wonderful! What would you like to discuss?",
                "It's great to sense your enthusiasm! What can I do for you?",
                "I appreciate your positive outlook! How may I assist you?"
            ],
            "negative": [
                "I sense you might be frustrated. Let me try to help you better.",
                "I understand this might be challenging. How can I assist you?",
                "I'm here to help. Let's see what we can do to improve things.",
                "I want to make this better for you. What specifically can I help with?"
            ],
            "neutral": [
                "I understand. How can I help you today?",
                "Got it. What would you like to know?",
                "Understood. What can I do for you?",
                "I'm here to help. What do you need?"
            ],
            "mixed": [
                "I sense mixed feelings in your message. Let me help clarify things.",
                "I understand this is complex. How can I best assist you?",
                "I see there are different aspects to consider. What's most important to you?"
            ]
        }
        
        # Conversation history for context
        self.conversation_history = {}
        
        logger.info("Bot initialization complete")

    async def on_message_activity(self, turn_context: TurnContext):
        """Handle incoming message with AI sentiment analysis"""
        user_message = turn_context.activity.text
        user_id = turn_context.activity.from_property.id
        
        if not user_message or not user_message.strip():
            response = "I didn't receive any text. Please type something!"
            await turn_context.send_activity(MessageFactory.text(response))
            return
        
        user_message = user_message.strip()
        logger.info(f"Received message from {user_id}: {user_message}")
        
        # Store conversation history
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            'timestamp': datetime.now(),
            'message': user_message
        })
        
        # Process message with AI analysis if available
        if self.ai_enabled:
            response_text = await self.process_with_ai(user_message, turn_context)
        else:
            response_text = self.process_basic(user_message)
        
        # Send response
        await turn_context.send_activity(MessageFactory.text(response_text))

    async def process_with_ai(self, message: str, turn_context: TurnContext):
        """Process message using Azure AI services"""
        try:
            # Perform sentiment analysis
            sentiment_result = await self.analyze_sentiment(message)
            
            # Perform entity recognition
            entities = await self.recognize_entities(message)
            
            # Check for commands first
            if message.startswith('/'):
                return self.handle_command(message, sentiment_result, entities)
            
            # Generate intelligent response based on AI analysis
            return self.generate_ai_response(message, sentiment_result, entities)
            
        except Exception as e:
            logger.error(f"Error in AI processing: {e}")
            return f"I processed your message but encountered an issue with AI analysis. Here's what you said: {message}"

    async def analyze_sentiment(self, text: str):
        """Analyze sentiment using Azure AI Language Service"""
        try:
            documents = [text]
            response = self.text_analytics_client.analyze_sentiment(
                documents=documents,
                show_opinion_mining=True
            )[0]
            
            sentiment_info = {
                'sentiment': response.sentiment,
                'confidence_scores': {
                    'positive': response.confidence_scores.positive,
                    'neutral': response.confidence_scores.neutral,
                    'negative': response.confidence_scores.negative
                },
                'sentences': []
            }
            
            # Analyze individual sentences
            for sentence in response.sentences:
                sentiment_info['sentences'].append({
                    'text': sentence.text,
                    'sentiment': sentence.sentiment,
                    'confidence_scores': {
                        'positive': sentence.confidence_scores.positive,
                        'neutral': sentence.confidence_scores.neutral,
                        'negative': sentence.confidence_scores.negative
                    }
                })
            
            logger.info(f"Sentiment analysis: {response.sentiment}")
            return sentiment_info
            
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return None

    async def recognize_entities(self, text: str):
        """Recognize entities using Azure AI Language Service"""
        try:
            documents = [text]
            response = self.text_analytics_client.recognize_entities(
                documents=documents
            )[0]
            
            entities = []
            for entity in response.entities:
                entities.append({
                    'text': entity.text,
                    'category': entity.category,
                    'subcategory': entity.subcategory,
                    'confidence_score': entity.confidence_score
                })
            
            if entities:
                logger.info(f"Recognized {len(entities)} entities")
            
            return entities
            
        except Exception as e:
            logger.error(f"Entity recognition error: {e}")
            return []

    def generate_ai_response(self, message: str, sentiment_result: dict, entities: list):
        """Generate intelligent response based on AI analysis"""
        import random
        
        response_parts = []
        
        # Add sentiment-aware greeting
        if sentiment_result:
            sentiment = sentiment_result['sentiment']
            confidence = sentiment_result['confidence_scores']
            
            # Select appropriate response based on sentiment
            if sentiment in self.sentiment_responses:
                greeting = random.choice(self.sentiment_responses[sentiment])
                response_parts.append(greeting)
            
            # Add sentiment details
            response_parts.append(
                f"\n\nSentiment Analysis: {sentiment.upper()} "
                f"(confidence: {confidence[sentiment]:.2%})"
            )
        
        # Add entity information if found
        if entities:
            response_parts.append(f"\n\nI detected {len(entities)} key entities in your message:")
            for entity in entities[:5]:  # Show top 5 entities
                response_parts.append(
                    f"  - {entity['text']}: {entity['category']}"
                )
        
        # Add helpful suggestion
        response_parts.append(
            "\n\nType /help to see what else I can do, or continue our conversation!"
        )
        
        return "".join(response_parts)

    def handle_command(self, message: str, sentiment_result: dict, entities: list):
        """Handle bot commands"""
        parts = message.split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command == '/help':
            return self.show_help()
        
        elif command == '/capabilities':
            return self.show_capabilities()
        
        elif command == '/analyze':
            if args:
                if sentiment_result:
                    return self.detailed_analysis(args, sentiment_result, entities)
                else:
                    return "AI analysis not available. Please configure Azure AI services."
            else:
                return "Usage: /analyze [your text]\nExample: /analyze I love this chatbot!"
        
        elif command == '/history':
            return self.show_history()
        
        elif command == '/clear':
            return "Conversation history cleared. Let's start fresh!"
        
        else:
            return f"Unknown command: {command}\nType /help for available commands."

    def detailed_analysis(self, text: str, sentiment_result: dict, entities: list):
        """Provide detailed AI analysis of text"""
        analysis = ["DETAILED AI ANALYSIS"]
        analysis.append("=" * 50)
        
        # Sentiment breakdown
        if sentiment_result:
            analysis.append(f"\nOverall Sentiment: {sentiment_result['sentiment'].upper()}")
            analysis.append("\nConfidence Scores:")
            for sent_type, score in sentiment_result['confidence_scores'].items():
                analysis.append(f"  {sent_type.capitalize()}: {score:.2%}")
            
            # Sentence-level analysis
            if sentiment_result['sentences']:
                analysis.append("\nSentence-by-Sentence Analysis:")
                for i, sentence in enumerate(sentiment_result['sentences'], 1):
                    analysis.append(
                        f"  {i}. \"{sentence['text']}\" - {sentence['sentiment']}"
                    )
        
        # Entity analysis
        if entities:
            analysis.append(f"\nEntities Detected: {len(entities)}")
            for entity in entities:
                analysis.append(
                    f"  - {entity['text']}: {entity['category']} "
                    f"(confidence: {entity['confidence_score']:.2%})"
                )
        else:
            analysis.append("\nNo entities detected in the text.")
        
        return "\n".join(analysis)

    def show_help(self):
        """Display help information"""
        help_text = """
AI-INTEGRATED CHATBOT HELP

Available Commands:
  /help - Show this help message
  /capabilities - List bot capabilities
  /analyze [text] - Get detailed AI analysis of text
  /history - View recent conversation
  /clear - Clear conversation history

Features:
  - Real-time sentiment analysis
  - Entity recognition and extraction  
  - Context-aware responses
  - Multi-turn conversation support

How to Use:
  - Type normally for conversation with sentiment analysis
  - Use commands (starting with /) for specific functions
  - Ask questions or share thoughts naturally

Example Interactions:
  - "I'm really excited about this project!"
  - "/analyze This is the best chatbot ever!"
  - "Can you help me understand sentiment analysis?"
        """
        return help_text.strip()

    def show_capabilities(self):
        """Display bot capabilities"""
        capabilities_text = "BOT CAPABILITIES:\n\n"
        for i, capability in enumerate(self.capabilities, 1):
            capabilities_text += f"{i}. {capability}\n"
        
        capabilities_text += "\nPowered by Azure AI Language Services"
        if not self.ai_enabled:
            capabilities_text += "\n\nNote: AI features currently unavailable"
        
        return capabilities_text

    def show_history(self):
        """Show conversation history"""
        return "Conversation history feature coming soon!"

    def process_basic(self, message: str):
        """Basic processing when AI is not available"""
        if message.startswith('/'):
            return self.handle_command(message, None, [])
        
        return (
            f"I received your message: \"{message}\"\n\n"
            f"Note: AI analysis not available. Please configure Azure AI services.\n"
            f"Type /help for available commands."
        )

    async def on_members_added_activity(self, members_added: list, turn_context: TurnContext):
        """Greet new members"""
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                welcome_text = """
Welcome to the AI-Integrated Chatbot!

I use Azure AI Language Services to analyze sentiment and understand your messages better.

Type /help to get started, or just start chatting naturally!
                """.strip()
                await turn_context.send_activity(MessageFactory.text(welcome_text))


def create_text_analytics_client():
    """Create Azure Text Analytics client"""
    try:
        endpoint = Config.AI_SERVICE_ENDPOINT
        key = Config.AI_SERVICE_KEY
        
        if endpoint == "YOUR_ENDPOINT_HERE" or key == "YOUR_KEY_HERE":
            logger.warning("Azure AI credentials not configured")
            return None
        
        credential = AzureKeyCredential(key)
        client = TextAnalyticsClient(
            endpoint=endpoint,
            credential=credential
        )
        
        logger.info(f"Text Analytics client created for endpoint: {endpoint}")
        return client
        
    except Exception as e:
        logger.error(f"Failed to create Text Analytics client: {e}")
        return None


# Initialize bot and client
text_analytics_client = create_text_analytics_client()
BOT = AIIntegratedBot(text_analytics_client)


async def messages(req: Request) -> Response:
    """Handle incoming messages"""
    try:
        body = await req.json()
        activity = Activity().deserialize(body)
        
        if activity.type == "message" and activity.text:
            response_text = BOT.process_basic(activity.text) if not BOT.ai_enabled else "Processing..."
            
            # Create mock turn context for processing
            class MockTurnContext:
                def __init__(self, activity):
                    self.activity = activity
                    self.responses = []
                
                async def send_activity(self, message):
                    self.responses.append(message.text)
            
            mock_context = MockTurnContext(activity)
            await BOT.on_message_activity(mock_context)
            
            response_text = mock_context.responses[0] if mock_context.responses else "Error processing message"
            
        elif activity.type == "conversationUpdate" and activity.members_added:
            response_text = "Welcome to the AI-Integrated Chatbot! Type /help to get started."
        else:
            response_text = "I can only process text messages right now."
        
        response_data = {
            "type": "message",
            "text": response_text,
            "from": {
                "id": "bot",
                "name": "AI-Integrated Bot"
            }
        }
        
        return web.json_response(response_data)
        
    except Exception as e:
        logger.error(f"Error in messages handler: {e}")
        return web.Response(text="Error processing message", status=500)


async def health_check(req: Request) -> Response:
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "bot": "AI-Integrated Chatbot",
        "ai_enabled": BOT.ai_enabled,
        "timestamp": datetime.now().isoformat()
    }
    return web.json_response(health_status)


async def root_handler(req: Request) -> Response:
    """Root endpoint"""
    return web.Response(
        text=(
            "AI-Integrated Chatbot is running!\n"
            f"AI Services: {'Enabled' if BOT.ai_enabled else 'Disabled'}\n"
            "Connect with Bot Framework Emulator at: http://localhost:3978/api/messages"
        ),
        content_type="text/plain"
    )


# Create web application
app = web.Application()
app.router.add_post("/api/messages", messages)
app.router.add_get("/health", health_check)
app.router.add_get("/", root_handler)


if __name__ == "__main__":
    print("="*60)
    print("AI-INTEGRATED CHATBOT STARTING")
    print("="*60)
    print(f"Server: http://localhost:3978")
    print(f"Bot endpoint: http://localhost:3978/api/messages")
    print(f"Health check: http://localhost:3978/health")
    print(f"AI Services: {'Enabled' if Config.validate_config() else 'Disabled - Configure environment variables'}")
    print("="*60)
    print("\nEnvironment Variables Needed:")
    print("  SET MicrosoftAIServiceEndpoint=<your_endpoint>")
    print("  SET MicrosoftAPIKey=<your_key>")
    print("\nPress Ctrl+C to stop")
    print("="*60)
    
    web.run_app(app, host="localhost", port=3978)