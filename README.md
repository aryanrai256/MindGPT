# MindCare: Psychology and Psychiatry Chatbot

![MindCare Logo](https://img.icons8.com/color/96/000000/mental-health.png)

**MindCare** is an advanced AI chatbot specialized in psychology and psychiatry, designed to provide empathetic support, evidence-based coping strategies, and mental health information. Built from scratch in Python, MindCare offers a safe, non-judgmental space for users to explore their feelings and learn about mental health.

## ⚠️ Important Ethical Notice

**MindCare is NOT a substitute for professional mental health care.** This chatbot provides informational support and coping strategies only. If you are experiencing a mental health crisis or need professional help, please contact a licensed mental health professional or a crisis hotline immediately.

## Features

### 🧠 Psychology Knowledge Base
- **Mental Health Conditions**: Comprehensive information about depression, anxiety, stress, and more
- **Symptoms and Treatment**: Evidence-based information about mental health conditions
- **When to Seek Help**: Clear guidance on when professional help is needed

### 🛠️ Coping Strategies
- **Emotional Strategies**: Journaling, emotion labeling, self-compassion
- **Physical Strategies**: Progressive muscle relaxation, diaphragmatic breathing, grounding techniques
- **Cognitive Strategies**: Cognitive restructuring, thought records, worry time
- **Behavioral Strategies**: Behavioral activation, exposure therapy, problem-solving

### 💡 Therapy Techniques
- **Cognitive Behavioral Therapy (CBT)**: Thought challenging, cognitive distortions
- **Acceptance and Commitment Therapy (ACT)**: Mindfulness, values clarification
- **Dialectical Behavior Therapy (DBT)**: Distress tolerance, emotion regulation, interpersonal effectiveness
- **Mindfulness-Based Therapies**: MBSR, MBCT, meditation practices

### 🚨 Crisis Support
- **Crisis Detection**: Automatically identifies potential crisis situations
- **Emergency Resources**: Provides immediate crisis hotline information
- **Safety First**: Prioritizes user safety with appropriate responses

### 📊 Emotion Tracking
- **Emotion Detection**: Identifies user emotions from text input
- **Emotion History**: Tracks emotional state throughout conversation
- **Personalized Responses**: Tailors responses based on detected emotions

### 🌍 Global Resources
- **International Hotlines**: Crisis resources for multiple countries
- **Online Therapy**: Platforms for professional help
- **Self-Help Resources**: Websites and tools for mental health
- **Recommended Apps**: Mobile applications for mental wellness

## Installation

### Prerequisites
- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

### Quick Start

```bash
# Clone the repository or download the files
git clone https://github.com/your-repo/mindcare.git
cd mindcare

# Run the chatbot
python main.py
```

### Development Setup

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest test_chatbot.py -v

# Run with code formatting and linting
black main.py test_chatbot.py
flake8 main.py test_chatbot.py
```

## Usage

### Starting a Conversation

```bash
python main.py
```

The chatbot will greet you and ask how you're feeling. You can:
- Share your emotions and thoughts
- Ask questions about mental health
- Request coping strategies
- Learn about therapy techniques
- Get crisis resources

### Example Conversations

**User**: "I'm feeling really anxious today"

**MindCare**: "That sounds really anxiety-provoking. Would it help to talk through what's making you feel this way?"

---

**User**: "What is depression?"

**MindCare**: 
```
**Depression**

A mood disorder causing persistent feelings of sadness and loss of interest.

**Common symptoms include:**
- Persistent sad, anxious, or empty mood
- Feelings of hopelessness or pessimism
- Loss of interest or pleasure in hobbies and activities
- Decreased energy or fatigue
- Difficulty concentrating, remembering, or making decisions

**Treatment options may include:**
- Psychotherapy (talk therapy)
- Medications (antidepressants)
- Lifestyle changes (exercise, diet, sleep)
- Social support
- Mindfulness and meditation

**When to seek professional help:**
- Symptoms persist for more than 2 weeks
- Symptoms interfere with daily life
- Having thoughts of self-harm or suicide
- Difficulty functioning at work or home

Would you like more information about depression or help with coping strategies?
```

---

**User**: "How can I cope with stress?"

**MindCare**: 
```
**Coping with Stress**

Here are some strategies that might help:

1. Break tasks into smaller, manageable steps
2. Prioritize what's most important and let go of the rest
3. Practice time management and set realistic deadlines
4. Take regular breaks, even if just for a few deep breaths
5. Engage in physical activity to release tension
6. Practice mindfulness or meditation
7. Talk to someone about what's stressing you
8. Make time for activities you enjoy

Would you like to explore any of these strategies in more detail?
```

### Commands

| Command | Description |
|---------|-------------|
| `quit`, `exit`, `bye` | End the conversation |
| `What is [condition]?` | Get information about a mental health condition |
| `How can I cope with [emotion]?` | Get coping strategies for a specific emotion |
| `Tell me about [therapy]` | Learn about therapy techniques (CBT, ACT, DBT, etc.) |
| `I need help` | Get crisis resources and support information |
| `Save conversation` | Save the current conversation to a file |

## Architecture

### Core Components

```
MindCare Chatbot
├── Psychology Knowledge Base
│   ├── Mental Health Conditions
│   ├── Symptoms and Treatment
│   └── When to Seek Help
├── Coping Strategies
│   ├── Emotional Strategies
│   ├── Physical Strategies
│   ├── Cognitive Strategies
│   └── Behavioral Strategies
├── Therapy Techniques
│   ├── CBT
│   ├── ACT
│   ├── DBT
│   └── Mindfulness-Based
├── Crisis Support
│   ├── Crisis Detection
│   ├── Emergency Responses
│   └── Resource Directory
├── Emotion Tracking
│   ├── Emotion Detection
│   ├── Emotion History
│   └── Personalized Responses
└── Conversation Management
    ├── Conversation History
    ├── User Preferences
    └── Session Management
```

### Key Classes

- **`PsychologyChatbot`**: Main chatbot class with all functionality
- **`Emotion`**: Enum for emotion categories
- **`CrisisLevel`**: Enum for crisis assessment levels

### Key Methods

- `detect_emotion(text)`: Detects emotion from user input
- `assess_crisis_level(text)`: Assesses if user is in crisis
- `handle_crisis(user_input)`: Handles crisis situations appropriately
- `process_input(user_input)`: Processes user input and generates responses
- `get_crisis_resources(location)`: Provides crisis resources for specific locations
- `save_conversation(filename)`: Saves conversation history to file
- `load_conversation(filename)`: Loads conversation history from file

## Testing

The chatbot includes a comprehensive test suite that covers:

- Emotion detection
- Crisis level assessment
- Input processing
- Response generation
- Conversation management
- File I/O operations
- Edge cases and error handling

### Running Tests

```bash
# Run all tests
python -m pytest test_chatbot.py -v

# Run specific test class
python -m pytest test_chatbot.py::TestPsychologyChatbot -v

# Run with coverage
python -m pytest test_chatbot.py --cov=main --cov-report=term
```

## Customization

### Adding New Knowledge

To add information about a new mental health condition:

```python
# In the _load_knowledge_base method
knowledge_base = {
    # ... existing conditions ...
    "new_condition": {
        "description": "Description of the condition",
        "symptoms": ["Symptom 1", "Symptom 2", "Symptom 3"],
        "treatment": ["Treatment 1", "Treatment 2"],
        "when_to_seek_help": ["Reason 1", "Reason 2"]
    }
}
```

### Adding New Coping Strategies

To add a new coping strategy:

```python
# In the _load_coping_strategies method
coping_strategies = {
    # ... existing categories ...
    "new_category": [
        {
            "name": "Strategy Name",
            "description": "Description of the strategy",
            "steps": ["Step 1", "Step 2", "Step 3"]
        }
    ]
}
```

### Adding New Therapy Techniques

To add a new therapy technique:

```python
# In the _load_therapy_techniques method
therapy_techniques = {
    # ... existing techniques ...
    "new_therapy": {
        "name": "Therapy Name",
        "description": "Description of the therapy",
        "key_concepts": ["Concept 1", "Concept 2"],
        "skills": [
            {"name": "Skill Name", "steps": ["Step 1", "Step 2"]}
        ]
    }
}
```

## Crisis Resources

### International
- **International Association for Suicide Prevention**: [https://www.iasp.info/resources/Crisis_Centres/](https://www.iasp.info/resources/Crisis_Centres/)
- **Befrienders Worldwide**: [https://www.befrienders.org/](https://www.befrienders.org/)

### United States
- **988 Suicide & Crisis Lifeline**: Call or text 988
- **Crisis Text Line**: Text HOME to 741741
- **National Domestic Violence Hotline**: 1-800-799-SAFE (7233)
- **SAMHSA National Helpline**: 1-800-662-HELP (4357)

### United Kingdom
- **Samaritans**: 116 123
- **Mind Infoline**: 0300 123 3393
- **Campaign Against Living Miserably (CALM)**: 0800 58 58 58

### Canada
- **Talk Suicide Canada**: 1-833-456-4566
- **Crisis Services Canada**: 1-833-456-4566

### Australia
- **Lifeline**: 13 11 14
- **Beyond Blue**: 1300 22 4636

## Online Therapy Platforms

- **BetterHelp**: [https://www.betterhelp.com/](https://www.betterhelp.com/) - Online counseling with licensed therapists
- **Talkspace**: [https://www.talkspace.com/](https://www.talkspace.com/) - Online therapy platform
- **7 Cups**: [https://www.7cups.com/](https://www.7cups.com/) - Free emotional support and online therapy
- **Woebot**: [https://woebothealth.com/](https://woebothealth.com/) - AI chatbot for mental health (evidence-based)

## Recommended Apps

- **Headspace** (iOS/Android): Meditation and mindfulness app
- **Calm** (iOS/Android): Meditation, sleep stories, and relaxation
- **Sanvello** (iOS/Android): CBT-based mood tracking and tools
- **What's Up** (iOS/Android): CBT and ACT tools for anxiety and depression
- **Finch** (iOS/Android): Self-care pet app for emotional support

## Self-Help Resources

- **MoodTools**: [https://www.moodtools.org/](https://www.moodtools.org/) - Free tools for depression and anxiety
- **Psychology Today**: [https://www.psychologytoday.com/](https://www.psychologytoday.com/) - Therapist directory and mental health articles
- **National Institute of Mental Health**: [https://www.nimh.nih.gov/](https://www.nimh.nih.gov/) - Mental health information and resources
- **Mind**: [https://www.mind.org.uk/](https://www.mind.org.uk/) - UK mental health charity with resources

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Contribution Guidelines

- All code must pass existing tests
- New features must include appropriate tests
- Follow PEP 8 style guidelines
- Keep commits atomic and well-described
- Include documentation for new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by evidence-based psychological practices
- Built with care and attention to mental health best practices
- Special thanks to all mental health professionals who dedicate their lives to helping others

## Disclaimer

**IMPORTANT**: This chatbot is for informational and educational purposes only. It is NOT a substitute for professional mental health care, diagnosis, or treatment. Always consult with a licensed mental health professional for any mental health concerns.

If you are in crisis or experiencing thoughts of self-harm or suicide, please contact a crisis hotline or emergency services immediately.

---

**You are not alone. Help is available. Your mental health matters.**
