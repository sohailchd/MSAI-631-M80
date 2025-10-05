# AI-Integrated Chatbot with Azure Cognitive Services

**Course**: MSAI-631 - Artificial Intelligence for Human-Computer Interaction  
**Project**: AI Service Integration  
**Institution**: University of the Cumberlands

## Project Overview

This project extends a traditional rule-based chatbot with Microsoft Azure AI Language Services, specifically implementing sentiment analysis and entity recognition capabilities. The bot can detect user emotions in real-time and generate contextually appropriate responses based on sentiment analysis results.

### Origin

This project builds upon the simple echo bot developed in Topic 5 (Week 5). The original bot provided basic message echoing functionality, which has been significantly enhanced with AI capabilities to create an intelligent conversational agent.

## Features

- **Real-time Sentiment Analysis**: Analyzes user messages to detect positive, negative, neutral, or mixed sentiment
- **Entity Recognition**: Identifies and categorizes named entities (people, locations, organizations, etc.)
- **Sentiment-Aware Responses**: Generates contextually appropriate responses based on detected sentiment
- **Opinion Mining**: Analyzes specific aspects mentioned in user messages
- **Command Processing**: Supports slash commands for specific functionality
- **Conversation History**: Tracks user interactions for context awareness
- **Graceful Degradation**: Functions in basic mode when AI services unavailable
- **Comprehensive Error Handling**: Provides informative error messages
- **Bot Framework Emulator Compatible**: Easy local testing and debugging

## Technologies Used

- **Python 3.8.2**: Programming language
- **Microsoft Bot Framework**: Conversational AI platform
- **Azure AI Language Services**: Sentiment analysis and entity recognition
- **aiohttp**: Asynchronous web framework
- **Bot Framework Emulator**: Local testing tool

## Prerequisites

- Python 3.8.2 (use Anaconda for environment management)
- Microsoft Azure account (free tier available)
- Bot Framework Emulator (for local testing)
- Azure AI Language Service provisioned

## Installation

### 1. Clone the Repository

```bash
git clone [your-repository-url]
cd ai-integrated-chatbot
```

### 2. Create Anaconda Environment

```bash
conda create --name MSAI631_AI_Bot python==3.8.2
conda activate MSAI631_AI_Bot
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Azure Credentials

Set environment variables with your Azure AI Service credentials:

**Windows:**
```cmd
SET MicrosoftAIServiceEndpoint=https://your-service.cognitiveservices.azure.com/
SET MicrosoftAPIKey=your_actual_key_here
```

**Mac/Linux:**
```bash
export MicrosoftAIServiceEndpoint=https://your-service.cognitiveservices.azure.com/
export MicrosoftAPIKey=your_actual_key_here
```

**Alternative**: Add to system environment variables for persistence

## Azure Setup

### Create Free Azure Account

1. Navigate to https://azure.microsoft.com/en-us/free
2. Click "Start free" and sign in with Microsoft account
3. Complete account setup (requires credit card for verification, but won't be charged for free tier)

### Provision Azure AI Language Service

1. Log in to Azure Portal (https://portal.azure.com)
2. Search for "sentiment" in the search bar
3. Select "Language service" from Azure AI Services
4. Click "Create language" button
5. Configure service:
   - **Subscription**: Your Azure subscription
   - **Resource Group**: Create new or use existing
   - **Region**: Choose closest region
   - **Name**: Unique service name
   - **Pricing Tier**: Free F0 (5,000 text records/month)
6. Review and create
7. After deployment, navigate to resource → "Keys and Endpoints"
8. Copy Endpoint URL and Key 1

### Free Tier Limits

- **Text Analytics**: 5,000 text records per month
- **Transactions**: 20 transactions per minute
- Perfect for development and testing

## Running the Bot

### Start the Bot

```bash
python app.py
```

Expected output:
```
============================================================
AI-INTEGRATED CHATBOT STARTING
============================================================
Server: http://localhost:3978
Bot endpoint: http://localhost:3978/api/messages
Health check: http://localhost:3978/health
AI Services: Enabled
============================================================
```

### Connect with Bot Framework Emulator

1. Download Bot Framework Emulator from https://github.com/microsoft/BotFramework-Emulator/releases
2. Open emulator
3. Click "Open Bot"
4. Enter bot URL: `http://localhost:3978/api/messages`
5. Leave App ID and Password empty (for local development)
6. Click "Connect"

## Usage Examples

### Basic Conversation
```
User: I'm really excited about this AI project!
Bot: I'm glad you're feeling positive! How can I help you further?

Sentiment Analysis: POSITIVE (confidence: 99.2%)
```

### Commands

**Help Command:**
```
User: /help
Bot: [Displays complete help information with available commands]
```

**Capabilities:**
```
User: /capabilities
Bot: [Lists all bot capabilities]
```

**Detailed Analysis:**
```
User: /analyze Microsoft Azure is amazing!
Bot: [Provides detailed sentiment and entity analysis]
```

### Sentiment Detection Examples

**Positive:**
- "This is fantastic and I love it!"
- "Great job on the implementation!"

**Negative:**
- "This is frustrating and doesn't work."
- "I'm disappointed with the results."

**Neutral:**
- "Can you explain sentiment analysis?"
- "What are the features?"

**Mixed:**
- "I love the concept but hate the setup process."
- "The bot is great but the documentation needs work."

## Project Structure

```
ai-integrated-chatbot/
├── app.py                    # Main application file
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
└── config.py                # Configuration (if separated)
```

## API Endpoints

- **POST** `/api/messages` - Main bot messaging endpoint
- **GET** `/health` - Health check endpoint
- **GET** `/` - Root endpoint with bot status

## Configuration

### Config Class

The `Config` class manages bot and Azure AI service configuration:

```python
class Config:
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    AI_SERVICE_ENDPOINT = os.environ.get("MicrosoftAIServiceEndpoint", "")
    AI_SERVICE_KEY = os.environ.get("MicrosoftAPIKey", "")
```

### Security Best Practices

- Never commit API keys to version control
- Use environment variables for sensitive credentials
- Rotate keys regularly using Azure portal
- Use Azure Key Vault for production deployments
- Enable Azure Active Directory authentication for production

## Error Handling

The bot implements comprehensive error handling:

1. **Configuration Validation**: Checks credentials at startup
2. **Client Initialization**: Validates Azure AI client creation
3. **Graceful Degradation**: Operates in basic mode if AI unavailable
4. **Exception Handling**: Catches and logs all exceptions
5. **User-Friendly Messages**: Provides helpful error messages

## Development Notes

### Code Organization

- **AIIntegratedBot**: Main bot class extending ActivityHandler
- **Config**: Configuration management with environment variables
- **create_text_analytics_client()**: Azure AI client initialization
- **analyze_sentiment()**: Sentiment analysis implementation
- **recognize_entities()**: Entity recognition implementation
- **generate_ai_response()**: Intelligent response generation

### Key Design Decisions

1. **Asynchronous Architecture**: All I/O operations use async/await
2. **Environment Variables**: Secure credential management
3. **Template-Based Responses**: Varied, natural responses
4. **Fallback Mechanism**: Basic functionality when AI unavailable
5. **Comprehensive Logging**: Detailed logs for debugging

## Testing

### Manual Testing Checklist

- [ ] Positive sentiment detection
- [ ] Negative sentiment detection  
- [ ] Neutral sentiment detection
- [ ] Mixed sentiment detection
- [ ] Entity recognition
- [ ] Command processing
- [ ] Error handling
- [ ] Health endpoint

### Test Messages

```python
test_messages = [
    "I absolutely love this project!",
    "This is terrible and frustrating.",
    "Can you help me understand sentiment analysis?",
    "Microsoft Azure provides excellent AI services.",
    "/help",
    "/analyze This is a test message.",
    ""  # Empty message test
]
```

## Troubleshooting

### Bot Won't Start

**Problem**: "Azure AI credentials not configured"  
**Solution**: Ensure environment variables are set correctly

**Problem**: "Port 3978 already in use"  
**Solution**: Kill existing process or change port in code

### AI Services Not Working

**Problem**: "Authentication failed"  
**Solution**: Verify endpoint URL and API key are correct

**Problem**: "Quota exceeded"  
**Solution**: Check Azure portal for usage limits

### Bot Framework Emulator Connection Issues

**Problem**: "Unable to connect"  
**Solution**: 
- Ensure bot is running
- Verify endpoint URL includes `/api/messages`
- Check firewall settings

## Future Enhancements

Potential improvements for future iterations:

1. **Multi-turn Conversation**: Implement conversation state management
2. **Intent Recognition**: Integrate LUIS for natural language understanding
3. **Multilingual Support**: Add language detection and translation
4. **Rich Cards**: Implement adaptive cards for visual responses
5. **Conversation Analytics**: Track and analyze conversation patterns
6. **Custom Entity Recognition**: Train models for domain-specific entities
7. **Deployment**: Deploy to Azure App Service for production use
8. **Authentication**: Add user authentication and personalization

## Resources

### Documentation
- [Microsoft Bot Framework](https://dev.botframework.com/)
- [Azure AI Language](https://azure.microsoft.com/en-us/products/ai-services/ai-language/)
- [Bot Framework Emulator](https://github.com/microsoft/BotFramework-Emulator)
- [Azure Text Analytics API](https://learn.microsoft.com/en-us/azure/ai-services/language-service/)

### Tutorials
- [Bot Framework Python Quickstart](https://learn.microsoft.com/en-us/azure/bot-service/python/bot-builder-python-quickstart)
- [Text Analytics with Python](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-textanalytics-readme)

## License

This project is created for educational purposes as part of MSAI-631 coursework at University of the Cumberlands.

## Author Details

- Author: Basar Chowdhury
- Date: Oct 5
- Course: MSAI-631
- Project: AI Service Integration

## Acknowledgments

- Course materials and instructions provided by Alan L. Dennis
- Microsoft Azure for free tier AI services
- Microsoft Bot Framework team for excellent documentation
- University of the Cumberlands MSAI program

---

**Note**: This README provides comprehensive documentation for the AI-integrated chatbot project. For detailed technical report and analysis, refer to the project report document.