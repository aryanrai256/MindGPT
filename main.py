#!/usr/bin/env python3
"""
MindCare: Psychology and Psychiatry Chatbot
A supportive AI companion for mental health awareness and coping strategies.

IMPORTANT: This chatbot provides informational support only. It is NOT a substitute
for professional mental health care. Always consult with a licensed mental health
professional for diagnosis and treatment.
"""

import re
import random
import json
import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import textwrap


class Emotion(Enum):
    """Emotion categories for tracking user state"""
    HAPPY = "happy"
    SAD = "sad"
    ANXIOUS = "anxious"
    ANGRY = "angry"
    CALM = "calm"
    CONFUSED = "confused"
    STRESSED = "stressed"
    LONELY = "lonely"
    HOPEFUL = "hopeful"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"


class CrisisLevel(Enum):
    """Crisis assessment levels"""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    EMERGENCY = 4


class PsychologyChatbot:
    """
    A psychology-focused chatbot that provides empathetic support,
    evidence-based coping strategies, and mental health information.
    """
    
    def __init__(self, name: str = "MindCare"):
        self.name = name
        self.conversation_history = []
        self.user_emotions = []
        self.current_emotion = Emotion.NEUTRAL
        self.crisis_level = CrisisLevel.NONE
        self.session_start = datetime.datetime.now()
        self.user_name = None
        
        # Load knowledge bases
        self.knowledge_base = self._load_knowledge_base()
        self.coping_strategies = self._load_coping_strategies()
        self.therapy_techniques = self._load_therapy_techniques()
        self.resources = self._load_resources()
        self.crisis_keywords = self._load_crisis_keywords()
        
        # Conversation patterns
        self.greetings = [
            "Hello! I'm {}, your mental health companion.",
            "Hi there! I'm {} here to support you.",
            "Welcome! I'm {} - let's talk about how you're feeling."
        ]
        self.goodbyes = [
            "Take care of yourself. Remember, you're not alone.",
            "I'm here whenever you need to talk. Stay strong.",
            "Be kind to yourself. Reach out anytime. Take care."
        ]
        
    def _load_knowledge_base(self) -> Dict:
        """Load psychology knowledge base"""
        return {
            "depression": {
                "description": "A mood disorder causing persistent feelings of sadness and loss of interest.",
                "symptoms": [
                    "Persistent sad, anxious, or empty mood",
                    "Feelings of hopelessness or pessimism",
                    "Feelings of guilt, worthlessness, or helplessness",
                    "Loss of interest or pleasure in hobbies and activities",
                    "Decreased energy or fatigue",
                    "Difficulty concentrating, remembering, or making decisions",
                    "Difficulty sleeping, early-morning awakening, or oversleeping",
                    "Appetite and/or weight changes",
                    "Thoughts of death or suicide"
                ],
                "treatment": [
                    "Psychotherapy (talk therapy)",
                    "Medications (antidepressants)",
                    "Lifestyle changes (exercise, diet, sleep)",
                    "Social support",
                    "Mindfulness and meditation"
                ],
                "when_to_seek_help": [
                    "Symptoms persist for more than 2 weeks",
                    "Symptoms interfere with daily life",
                    "Having thoughts of self-harm or suicide",
                    "Difficulty functioning at work or home"
                ]
            },
            "anxiety": {
                "description": "A normal emotion that becomes a disorder when excessive and persistent.",
                "types": [
                    "Generalized Anxiety Disorder (GAD)",
                    "Panic Disorder",
                    "Social Anxiety Disorder",
                    "Specific Phobias",
                    "Separation Anxiety"
                ],
                "symptoms": [
                    "Excessive worrying",
                    "Restlessness or feeling on edge",
                    "Fatigue",
                    "Difficulty concentrating",
                    "Irritability",
                    "Muscle tension",
                    "Sleep disturbances",
                    "Physical symptoms (headaches, stomachaches)"
                ],
                "coping": [
                    "Deep breathing exercises",
                    "Progressive muscle relaxation",
                    "Mindfulness meditation",
                    "Regular exercise",
                    "Limiting caffeine and alcohol",
                    "Journaling",
                    "Social connection"
                ]
            },
            "stress": {
                "description": "The body's reaction to any change that requires an adjustment or response.",
                "causes": [
                    "Work or school pressures",
                    "Life changes (moving, divorce, job loss)",
                    "Financial problems",
                    "Relationship difficulties",
                    "Health issues",
                    "Traumatic events"
                ],
                "management": [
                    "Identify stressors",
                    "Practice time management",
                    "Set realistic goals",
                    "Maintain healthy lifestyle",
                    "Practice relaxation techniques",
                    "Build support network",
                    "Learn to say no",
                    "Take breaks and rest"
                ]
            },
            "self_care": {
                "description": "Deliberate actions to care for physical, mental, and emotional health.",
                "areas": [
                    "Physical: sleep, nutrition, exercise",
                    "Emotional: self-compassion, emotional regulation",
                    "Social: healthy relationships, boundaries",
                    "Spiritual: meaning, purpose, connection",
                    "Mental: learning, creativity, stimulation"
                ],
                "activities": [
                    "Take a warm bath",
                    "Read a book",
                    "Go for a walk in nature",
                    "Practice gratitude",
                    "Listen to calming music",
                    "Spend time with loved ones",
                    "Engage in a hobby",
                    "Practice yoga or stretching"
                ]
            },
            "mindfulness": {
                "description": "The practice of being fully present and engaged in the current moment.",
                "benefits": [
                    "Reduces stress and anxiety",
                    "Improves focus and concentration",
                    "Enhances self-awareness",
                    "Promotes emotional regulation",
                    "Improves sleep",
                    "Lowers blood pressure"
                ],
                "practices": [
                    "Focus on breath",
                    "Body scan meditation",
                    "Mindful eating",
                    "Mindful walking",
                    "Observing thoughts without judgment",
                    "Grounding techniques (5-4-3-2-1 method)"
                ]
            },
            "sleep": {
                "description": "Essential for mental and physical health.",
                "recommendations": [
                    "7-9 hours for adults",
                    "Consistent sleep schedule",
                    "Create a bedtime routine",
                    "Limit screen time before bed",
                    "Keep bedroom cool and dark",
                    "Avoid caffeine and heavy meals before bed",
                    "Get regular exercise (but not too close to bedtime)"
                ],
                "sleep_hygiene": [
                    "Go to bed and wake up at the same time every day",
                    "Use the bed only for sleep and intimacy",
                    "If you can't sleep, get up and do something relaxing",
                    "Limit naps to 20-30 minutes",
                    "Reduce fluid intake before bedtime"
                ]
            }
        }
    
    def _load_coping_strategies(self) -> Dict:
        """Load evidence-based coping strategies"""
        return {
            "emotional": [
                {
                    "name": "Journaling",
                    "description": "Write down your thoughts and feelings to process emotions.",
                    "steps": [
                        "Find a quiet space",
                        "Write freely without judgment",
                        "Focus on one emotion at a time",
                        "Reflect on what triggered the emotion",
                        "Notice patterns over time"
                    ]
                },
                {
                    "name": "Emotion Labeling",
                    "description": "Identify and name your emotions to reduce their intensity.",
                    "steps": [
                        "Pause and take a deep breath",
                        "Ask yourself: What am I feeling right now?",
                        "Name the emotion (e.g., angry, sad, anxious)",
                        "Rate its intensity from 1-10",
                        "Notice where you feel it in your body"
                    ]
                },
                {
                    "name": "Self-Compassion Break",
                    "description": "Practice kindness toward yourself in difficult moments.",
                    "steps": [
                        "Acknowledge your suffering",
                        "Recognize that suffering is part of being human",
                        "Place your hand over your heart",
                        "Say kind words to yourself",
                        "Remind yourself: I am enough"
                    ]
                }
            ],
            "physical": [
                {
                    "name": "Progressive Muscle Relaxation",
                    "description": "Tense and relax muscle groups to reduce physical tension.",
                    "steps": [
                        "Find a comfortable position",
                        "Start with your feet and work upward",
                        "Tense each muscle group for 5-10 seconds",
                        "Release and notice the difference",
                        "Move to the next muscle group",
                        "Finish with deep breaths"
                    ]
                },
                {
                    "name": "Diaphragmatic Breathing",
                    "description": "Deep breathing that engages the diaphragm for relaxation.",
                    "steps": [
                        "Place one hand on your chest, one on your belly",
                        "Inhale deeply through your nose for 4 seconds",
                        "Hold for 2 seconds",
                        "Exhale slowly through pursed lips for 6 seconds",
                        "Repeat for 5-10 minutes"
                    ]
                },
                {
                    "name": "Grounding Technique (5-4-3-2-1)",
                    "description": "Use your senses to anchor yourself in the present moment.",
                    "steps": [
                        "Name 5 things you can see",
                        "Name 4 things you can touch",
                        "Name 3 things you can hear",
                        "Name 2 things you can smell",
                        "Name 1 thing you can taste"
                    ]
                }
            ],
            "cognitive": [
                {
                    "name": "Cognitive Restructuring",
                    "description": "Challenge and change unhelpful thought patterns.",
                    "steps": [
                        "Identify the negative thought",
                        "Ask: Is this thought based on facts or assumptions?",
                        "Consider alternative explanations",
                        "Ask: What would I tell a friend in this situation?",
                        "Replace the thought with a more balanced one"
                    ]
                },
                {
                    "name": "Thought Records",
                    "description": "Track and analyze automatic negative thoughts.",
                    "columns": ["Situation", "Emotion", "Automatic Thought", "Evidence For", "Evidence Against", "Balanced Thought"]
                },
                {
                    "name": "Worry Time",
                    "description": "Set aside specific time to worry, reducing worry throughout the day.",
                    "steps": [
                        "Set aside 15-30 minutes each day as 'worry time'",
                        "When worries arise outside this time, write them down",
                        "Postpone worrying until the designated time",
                        "During worry time, allow yourself to worry freely",
                        "At the end, let go of the worries until tomorrow"
                    ]
                }
            ],
            "behavioral": [
                {
                    "name": "Behavioral Activation",
                    "description": "Engage in activities that bring pleasure or mastery to improve mood.",
                    "steps": [
                        "Identify activities you used to enjoy",
                        "Schedule one pleasant activity per day",
                        "Start with small, manageable activities",
                        "Track your mood before and after",
                        "Gradually increase activity level"
                    ]
                },
                {
                    "name": "Exposure Therapy (for anxiety)",
                    "description": "Gradually face feared situations to reduce anxiety.",
                    "steps": [
                        "Create a fear hierarchy (least to most feared)",
                        "Start with the least feared situation",
                        "Stay in the situation until anxiety decreases",
                        "Practice regularly",
                        "Gradually move up the hierarchy"
                    ]
                },
                {
                    "name": "Problem Solving",
                    "description": "Systematic approach to solving life problems.",
                    "steps": [
                        "Define the problem clearly",
                        "Brainstorm possible solutions",
                        "Evaluate pros and cons of each solution",
                        "Choose the best solution",
                        "Create an action plan",
                        "Implement and evaluate"
                    ]
                }
            ]
        }
    
    def _load_therapy_techniques(self) -> Dict:
        """Load various therapy techniques"""
        return {
            "cbt": {
                "name": "Cognitive Behavioral Therapy",
                "description": "Focuses on the relationship between thoughts, feelings, and behaviors.",
                "key_concepts": [
                    "Automatic thoughts",
                    "Cognitive distortions",
                    "Behavioral experiments",
                    "Thought challenging",
                    "Homework assignments"
                ],
                "cognitive_distortions": [
                    {"name": "All-or-Nothing Thinking", "example": "I failed this task, so I'm a complete failure."},
                    {"name": "Overgeneralization", "example": "I failed once, so I'll always fail."},
                    {"name": "Mental Filtering", "example": "Focusing only on the negative aspects of a situation."},
                    {"name": "Disqualifying the Positive", "example": "Dismissing positive experiences as flukes."},
                    {"name": "Jumping to Conclusions", "example": "Assuming the worst without evidence."},
                    {"name": "Magnification or Minimization", "example": "Blowing things out of proportion or shrinking their importance."},
                    {"name": "Emotional Reasoning", "example": "I feel worthless, so I must be worthless."},
                    {"name": "Should Statements", "example": "I should always be perfect."},
                    {"name": "Labeling", "example": "I'm a loser."},
                    {"name": "Personalization", "example": "Taking responsibility for things outside your control."}
                ]
            },
            "act": {
                "name": "Acceptance and Commitment Therapy",
                "description": "Focuses on accepting what is out of your control while committing to action that enriches your life.",
                "core_processes": [
                    "Acceptance",
                    "Cognitive Defusion",
                    "Present Moment Awareness",
                    "Self-as-Context",
                    "Values Clarification",
                    "Committed Action"
                ],
                "metaphors": [
                    "Passengers on the Bus",
                    "The Chessboard",
                    "The Quick Sand",
                    "The Monster"
                ]
            },
            "dbt": {
                "name": "Dialectical Behavior Therapy",
                "description": "Combines cognitive-behavioral techniques with mindfulness and acceptance strategies.",
                "modules": [
                    "Mindfulness",
                    "Distress Tolerance",
                    "Emotion Regulation",
                    "Interpersonal Effectiveness"
                ],
                "skills": [
                    {"name": "STOP Skill", "steps": ["Stop", "Take a step back", "Observe", "Proceed mindfully"]},
                    {"name": "TIPP Skill", "steps": ["Temperature change", "Intense exercise", "Paced breathing", "Paired muscle relaxation"]},
                    {"name": "DEAR MAN", "steps": ["Describe", "Express", "Assert", "Reinforce", "Mindfully", "Appear confident", "Negotiate"]},
                    {"name": "GIVE Skill", "steps": ["Gentle", "Interested", "Validate", "Easy manner"]},
                    {"name": "FAST Skill", "steps": ["Fair", "Apologies (no unnecessary)", "Stick to values", "Truthful"]}
                ]
            },
            "mindfulness_based": {
                "name": "Mindfulness-Based Therapies",
                "description": "Therapies that incorporate mindfulness practices.",
                "types": [
                    "Mindfulness-Based Stress Reduction (MBSR)",
                    "Mindfulness-Based Cognitive Therapy (MBCT)",
                    "Mindfulness-Based Relapse Prevention (MBRP)"
                ],
                "practices": [
                    "Body scan meditation",
                    "Sitting meditation",
                    "Walking meditation",
                    "Mindful eating",
                    "Loving-kindness meditation"
                ]
            }
        }
    
    def _load_resources(self) -> Dict:
        """Load mental health resources"""
        return {
            "hotlines": {
                "International": [
                    {"name": "International Association for Suicide Prevention", "phone": "Varies by country", "website": "https://www.iasp.info/resources/Crisis_Centres/"},
                    {"name": "Befrienders Worldwide", "phone": "", "website": "https://www.befrienders.org/"}
                ],
                "United States": [
                    {"name": "988 Suicide & Crisis Lifeline", "phone": "988", "website": "https://988lifeline.org/"},
                    {"name": "Crisis Text Line", "phone": "Text HOME to 741741", "website": "https://www.crisistextline.org/"},
                    {"name": "National Domestic Violence Hotline", "phone": "1-800-799-SAFE (7233)", "website": "https://www.thehotline.org/"},
                    {"name": "SAMHSA National Helpline", "phone": "1-800-662-HELP (4357)", "website": "https://www.samhsa.gov/find-help/national-helpline"}
                ],
                "United Kingdom": [
                    {"name": "Samaritans", "phone": "116 123", "website": "https://www.samaritans.org/"},
                    {"name": "Mind Infoline", "phone": "0300 123 3393", "website": "https://www.mind.org.uk/"},
                    {"name": "Campaign Against Living Miserably (CALM)", "phone": "0800 58 58 58", "website": "https://www.thecalmzone.net/"}
                ],
                "Canada": [
                    {"name": "Talk Suicide Canada", "phone": "1-833-456-4566", "website": "https://talksuicide.ca/"},
                    {"name": "Crisis Services Canada", "phone": "1-833-456-4566", "website": "https://www.crisisservicescanada.ca/"}
                ],
                "Australia": [
                    {"name": "Lifeline", "phone": "13 11 14", "website": "https://www.lifeline.org.au/"},
                    {"name": "Beyond Blue", "phone": "1300 22 4636", "website": "https://www.beyondblue.org.au/"}
                ]
            },
            "online_therapy": [
                {"name": "BetterHelp", "website": "https://www.betterhelp.com/", "description": "Online counseling with licensed therapists"},
                {"name": "Talkspace", "website": "https://www.talkspace.com/", "description": "Online therapy platform"},
                {"name": "7 Cups", "website": "https://www.7cups.com/", "description": "Free emotional support and online therapy"},
                {"name": "Woebot", "website": "https://woebothealth.com/", "description": "AI chatbot for mental health (evidence-based)"}
            ],
            "self_help": [
                {"name": "MoodTools", "website": "https://www.moodtools.org/", "description": "Free tools for depression and anxiety"},
                {"name": "Psychology Today", "website": "https://www.psychologytoday.com/", "description": "Therapist directory and mental health articles"},
                {"name": "National Institute of Mental Health", "website": "https://www.nimh.nih.gov/", "description": "Mental health information and resources"},
                {"name": "Mind", "website": "https://www.mind.org.uk/", "description": "UK mental health charity with resources"}
            ],
            "apps": [
                {"name": "Headspace", "platform": "iOS/Android", "description": "Meditation and mindfulness app"},
                {"name": "Calm", "platform": "iOS/Android", "description": "Meditation, sleep stories, and relaxation"},
                {"name": "Sanvello", "platform": "iOS/Android", "description": "CBT-based mood tracking and tools"},
                {"name": "What's Up", "platform": "iOS/Android", "description": "CBT and ACT tools for anxiety and depression"},
                {"name": "Finch", "platform": "iOS/Android", "description": "Self-care pet app for emotional support"}
            ]
        }
    
    def _load_crisis_keywords(self) -> List:
        """Load keywords that indicate potential crisis situations"""
        return [
            # Suicide-related
            "kill myself", "want to die", "suicide", "end my life", "can't go on",
            "no reason to live", "better off dead", "hurt myself", "self harm",
            "cut myself", "overdose", "jump off", "hang myself", "shoot myself",
            
            # Harm to others
            "kill someone", "hurt someone", "violent", "harm others", "shoot them",
            
            # Severe distress
            "can't take it anymore", "breaking down", "losing my mind", "going crazy",
            "out of control", "can't cope", "can't handle it", "giving up",
            
            # Abuse
            "abuse", "beaten", "raped", "molested", "assaulted", "hitting me",
            "hurting me", "scared for my life", "unsafe at home",
            
            # Psychosis
            "hearing voices", "seeing things", "hallucinations", "delusions",
            "paranoid", "people are after me", "they're watching me",
            
            # Substance abuse
            "overdosed", "too much drugs", "alcohol poisoning", "mixing pills",
            
            # Urgent medical
            "chest pain", "can't breathe", "heart attack", "stroke", "seizure"
        ]
    
    def detect_emotion(self, text: str) -> Emotion:
        """Detect the primary emotion in user input"""
        text_lower = text.lower()
        
        # Order matters: check more specific emotions first
        # STRESSED should be checked before ANXIOUS since "stressed" appears in both
        emotion_keywords = [
            (Emotion.STRESSED, ['stressed', 'overwhelmed', 'pressured', 'burned out', 'exhausted']),
            (Emotion.ANXIOUS, ['anxious', 'nervous', 'worried', 'scared', 'afraid', 'panic', 'tense']),
            (Emotion.HAPPY, ['happy', 'joy', 'excited', 'great', 'wonderful', 'amazing', 'good', 'fantastic']),
            (Emotion.SAD, ['sad', 'depressed', 'unhappy', 'miserable', 'heartbroken', 'grief', 'cry', 'tears']),
            (Emotion.ANGRY, ['angry', 'mad', 'furious', 'annoyed', 'irritated', 'rage', 'pissed']),
            (Emotion.CALM, ['calm', 'peaceful', 'relaxed', 'serene', 'tranquil', 'at ease']),
            (Emotion.CONFUSED, ['confused', 'lost', 'unsure', "don't know", 'puzzled', 'mixed up']),
            (Emotion.LONELY, ['lonely', 'alone', 'isolated', 'abandoned', 'empty', 'no one']),
            (Emotion.HOPEFUL, ['hopeful', 'optimistic', 'positive', 'looking forward', 'excited'])
        ]
        
        for emotion, keywords in emotion_keywords:
            for keyword in keywords:
                if keyword in text_lower:
                    return emotion
        
        return Emotion.NEUTRAL
    
    def assess_crisis_level(self, text: str) -> CrisisLevel:
        """Assess if the user is in crisis based on their input"""
        text_lower = text.lower()
        
        # Check for emergency keywords
        for keyword in self.crisis_keywords:
            if keyword in text_lower:
                # High priority keywords
                if any(kw in text_lower for kw in ['kill myself', 'suicide', 'end my life', 'want to die']):
                    return CrisisLevel.EMERGENCY
                elif any(kw in text_lower for kw in ['hurt myself', 'self harm', 'cut myself', 'overdose']):
                    return CrisisLevel.HIGH
                elif any(kw in text_lower for kw in ['abuse', 'raped', 'assaulted', 'unsafe']):
                    return CrisisLevel.HIGH
                elif any(kw in text_lower for kw in ['hearing voices', 'hallucinations', 'paranoid']):
                    return CrisisLevel.HIGH
                else:
                    return CrisisLevel.MEDIUM
        
        # Check for severe distress indicators
        distress_keywords = ['can\'t take it', 'breaking down', 'losing my mind', 'giving up']
        for keyword in distress_keywords:
            if keyword in text_lower:
                return CrisisLevel.MEDIUM
        
        return CrisisLevel.NONE
    
    def handle_crisis(self, user_input: str) -> str:
        """Handle crisis situations with appropriate responses"""
        self.crisis_level = self.assess_crisis_level(user_input)
        
        if self.crisis_level == CrisisLevel.EMERGENCY:
            return self._emergency_response()
        elif self.crisis_level == CrisisLevel.HIGH:
            return self._high_crisis_response()
        elif self.crisis_level == CrisisLevel.MEDIUM:
            return self._medium_crisis_response()
        
        return ""
    
    def _emergency_response(self) -> str:
        """Response for emergency crisis situations"""
        responses = [
            "I'm really concerned about your safety. Please call emergency services or go to the nearest emergency room immediately. In the US, call 911. In the UK, call 999. In the EU, call 112.",
            "Your safety is the most important thing right now. Please contact emergency services or go to the hospital. If you're in the US, you can also call or text 988 for the Suicide & Crisis Lifeline.",
            "I need you to get help right now. Please call emergency services or have someone take you to the hospital. You are not alone, and people want to help you."
        ]
        return random.choice(responses)
    
    def _high_crisis_response(self) -> str:
        """Response for high crisis situations"""
        responses = [
            "I'm very concerned about what you're going through. Please reach out to a crisis hotline immediately. In the US, you can call or text 988. In the UK, call Samaritans at 116 123. You deserve support and help.",
            "This sounds like a very serious situation. Please contact a mental health professional or crisis line right away. Your feelings are valid, and there are people who want to help you through this.",
            "I want to make sure you're safe. Please call a crisis hotline or speak to someone you trust immediately. You don't have to go through this alone."
        ]
        return random.choice(responses)
    
    def _medium_crisis_response(self) -> str:
        """Response for medium crisis situations"""
        responses = [
            "It sounds like you're going through a really tough time. This seems really distressing for you. Would you like me to share some crisis resources that might help? You don't have to face this alone.",
            "I can hear that you're in distress. It might be helpful to reach out to a mental health professional or someone you trust. Would you like information about support resources?",
            "This seems really overwhelming for you. Sometimes talking to a professional can make a big difference. Would you like me to share some options for getting support?"
        ]
        return random.choice(responses)
    
    def get_crisis_resources(self, location: str = None) -> str:
        """Get crisis resources based on location"""
        if location:
            location = location.capitalize()
            if location in self.resources["hotlines"]:
                resources = self.resources["hotlines"][location]
                response = f"Here are crisis resources for {location}:\n\n"
                for resource in resources:
                    phone = f"Phone: {resource['phone']}" if resource['phone'] else ""
                    response += f"• {resource['name']}: {phone}\n  Website: {resource['website']}\n\n"
                return response
        
        # Default to international and US resources
        response = "Here are some crisis resources:\n\n"
        
        # International
        response += "**International:**\n"
        for resource in self.resources["hotlines"]["International"]:
            response += f"• {resource['name']}: {resource['website']}\n"
        
        response += "\n**United States:**\n"
        for resource in self.resources["hotlines"]["United States"]:
            response += f"• {resource['name']}: {resource['phone']}\n  Website: {resource['website']}\n"
        
        response += "\n**Online Support:**\n"
        for resource in self.resources["online_therapy"]:
            response += f"• {resource['name']}: {resource['website']}\n  {resource['description']}\n"
        
        return response
    
    def greet_user(self) -> str:
        """Generate a greeting message"""
        greeting = random.choice(self.greetings).format(self.name)
        
        if not self.user_name:
            greeting += " What's your name?"
        else:
            greeting += f" How are you feeling today, {self.user_name}?"
        
        return greeting
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate a response"""
        user_input = user_input.strip()
        
        # Store conversation history
        self.conversation_history.append({
            "user": user_input,
            "timestamp": datetime.datetime.now().isoformat(),
            "emotion": self.detect_emotion(user_input).value
        })
        
        # Update current emotion
        self.current_emotion = self.detect_emotion(user_input)
        self.user_emotions.append(self.current_emotion.value)
        
        # Check for crisis situations first
        crisis_response = self.handle_crisis(user_input)
        if crisis_response:
            return crisis_response
        
        # Extract user name if not set
        if not self.user_name:
            name_pattern = r"(?:my name is|I'm|I am|call me|name's?)\s+([A-Za-z]+)"
            match = re.search(name_pattern, user_input, re.IGNORECASE)
            if match:
                self.user_name = match.group(1).capitalize()
                return f"Nice to meet you, {self.user_name}! How are you feeling today?"
        
        # Check for specific topics
        response = self._check_for_specific_topics(user_input)
        if response:
            return response
        
        # Check for questions about mental health conditions
        response = self._answer_mental_health_questions(user_input)
        if response:
            return response
        
        # Check for requests for coping strategies
        response = self._provide_coping_strategies(user_input)
        if response:
            return response
        
        # Check for therapy technique questions
        response = self._explain_therapy_techniques(user_input)
        if response:
            return response
        
        # Check for resource requests
        if any(word in user_input.lower() for word in ['help', 'resource', 'therapist', 'counselor', 'support']):
            return self._provide_resources()
        
        # General empathetic response
        return self._generate_empathetic_response(user_input)
    
    def _check_for_specific_topics(self, user_input: str) -> Optional[str]:
        """Check for specific conversation topics"""
        text_lower = user_input.lower()
        
        # Greetings and goodbyes
        if any(word in text_lower for word in ['hi', 'hello', 'hey', 'greetings']):
            if self.user_name:
                return f"Hello, {self.user_name}! How are you feeling today?"
            return self.greet_user()
        
        if any(word in text_lower for word in ['bye', 'goodbye', 'see you', 'later', 'exit', 'quit']):
            return random.choice(self.goodbyes)
        
        # How are you?
        if any(word in text_lower for word in ['how are you', "how're you", 'how do you feel']):
            return f"I'm here to support you, {self.user_name or 'friend'}. How about you? How are you feeling today?"
        
        # Thank you
        if any(word in text_lower for word in ['thank', 'thanks', 'appreciate']):
            return random.choice([
                "You're very welcome! I'm here to help.",
                "My pleasure! Remember, taking care of your mental health is important.",
                "Anytime! You deserve support and kindness. You're welcome."
            ])
        
        # Apologies
        if any(word in text_lower for word in ['sorry', 'apologize']):
            return random.choice([
                "No need to apologize. You're doing the best you can.",
                "Please don't apologize. Your feelings are valid.",
                "You have nothing to be sorry for. I'm here to listen."
            ])
        
        return None
    
    def _answer_mental_health_questions(self, user_input: str) -> Optional[str]:
        """Answer questions about mental health conditions"""
        text_lower = user_input.lower()
        
        for condition, info in self.knowledge_base.items():
            if condition in text_lower or condition.replace('_', ' ') in text_lower:
                response = f"**{condition.replace('_', ' ').title()}**\n\n"
                response += f"{info['description']}\n\n"
                
                if 'symptoms' in info:
                    response += "**Common symptoms include:**\n"
                    for symptom in info['symptoms']:
                        response += f"- {symptom}\n"
                    response += "\n"
                
                if 'treatment' in info:
                    response += "**Treatment options may include:**\n"
                    for treatment in info['treatment']:
                        response += f"- {treatment}\n"
                    response += "\n"
                
                if 'when_to_seek_help' in info:
                    response += "**When to seek professional help:**\n"
                    for reason in info['when_to_seek_help']:
                        response += f"- {reason}\n"
                
                response += f"\nWould you like more information about {condition.replace('_', ' ')} or help with coping strategies?"
                return response
        
        return None
    
    def _provide_coping_strategies(self, user_input: str) -> Optional[str]:
        """Provide coping strategies based on user needs"""
        text_lower = user_input.lower()
        
        # Check for specific strategy requests
        if any(word in text_lower for word in ['coping', 'cope', 'deal with', 'handle']):
            # Try to identify the emotion or situation
            emotion = self.current_emotion
            
            if emotion != Emotion.NEUTRAL and emotion != Emotion.UNKNOWN:
                strategies = self._get_strategies_for_emotion(emotion)
                if strategies:
                    return strategies
            
            # General coping strategies
            return self._get_general_coping_strategies()
        
        # Check for specific technique requests
        if any(word in text_lower for word in ['meditation', 'mindfulness', 'breathing', 'relaxation']):
            return self._get_mindfulness_strategies()
        
        if any(word in text_lower for word in ['journal', 'write', 'thoughts']):
            return self._get_journaling_strategies()
        
        return None
    
    def _get_strategies_for_emotion(self, emotion: Emotion) -> str:
        """Get coping strategies tailored to a specific emotion"""
        strategies_map = {
            Emotion.SAD: {
                "title": "Coping with Sadness",
                "strategies": [
                    "Allow yourself to feel the sadness without judgment",
                    "Reach out to someone you trust and share how you're feeling",
                    "Engage in activities that used to bring you joy",
                    "Practice self-compassion - be kind to yourself",
                    "Write about your feelings in a journal",
                    "Spend time in nature or with pets",
                    "Listen to music that validates your emotions",
                    "Consider talking to a therapist about persistent sadness"
                ]
            },
            Emotion.ANXIOUS: {
                "title": "Coping with Anxiety",
                "strategies": [
                    "Practice deep breathing: inhale for 4 seconds, hold for 4, exhale for 6",
                    "Ground yourself using the 5-4-3-2-1 technique",
                    "Challenge anxious thoughts: ask if they're based on facts or fears",
                    "Limit caffeine and sugar which can increase anxiety",
                    "Engage in regular exercise to reduce anxiety hormones",
                    "Practice progressive muscle relaxation",
                    "Write down your worries and set aside 'worry time'",
                    "Talk to someone about what's making you anxious"
                ]
            },
            Emotion.ANGRY: {
                "title": "Coping with Anger",
                "strategies": [
                    "Take slow, deep breaths to calm your nervous system",
                    "Count to 10 before responding or acting",
                    "Remove yourself from the situation if possible",
                    "Express your anger in a healthy way through exercise or art",
                    "Identify the trigger and underlying emotions (often hurt or fear)",
                    "Practice 'I' statements: 'I feel... when... because...'",
                    "Write about your anger and then tear up the paper",
                    "Use humor to diffuse the situation (when appropriate)"
                ]
            },
            Emotion.STRESSED: {
                "title": "Coping with Stress",
                "strategies": [
                    "Break tasks into smaller, manageable steps",
                    "Prioritize what's most important and let go of the rest",
                    "Practice time management and set realistic deadlines",
                    "Take regular breaks, even if just for a few deep breaths",
                    "Engage in physical activity to release tension",
                    "Practice mindfulness or meditation",
                    "Talk to someone about what's stressing you",
                    "Make time for activities you enjoy"
                ]
            },
            Emotion.LONELY: {
                "title": "Coping with Loneliness",
                "strategies": [
                    "Reach out to someone you haven't connected with in a while",
                    "Join a club, class, or group based on your interests",
                    "Volunteer for a cause you care about",
                    "Spend quality time with pets or in nature",
                    "Practice self-compassion and remind yourself you're worthy of connection",
                    "Engage in online communities with similar interests",
                    "Write a letter to someone you miss",
                    "Consider talking to a therapist about feelings of isolation"
                ]
            },
            Emotion.CONFUSED: {
                "title": "Coping with Confusion",
                "strategies": [
                    "Write down what you know and what you don't know",
                    "Break the problem into smaller parts",
                    "Ask for clarification or help from others",
                    "Take a break and come back to the problem later",
                    "Research the topic to gain more understanding",
                    "Talk through your thoughts with someone else",
                    "Trust that you don't need to have all the answers right now",
                    "Practice mindfulness to stay present with the uncertainty"
                ]
            }
        }
        
        if emotion in strategies_map:
            info = strategies_map[emotion]
            response = f"**{info['title']}**\n\n"
            response += "Here are some strategies that might help:\n\n"
            for i, strategy in enumerate(info['strategies'], 1):
                response += f"{i}. {strategy}\n"
            response += f"\nWould you like to explore any of these strategies in more detail?"
            return response
        
        return None
    
    def _get_general_coping_strategies(self) -> str:
        """Get general coping strategies"""
        response = "**General Coping Strategies**\n\n"
        response += "Here are some evidence-based strategies that can help with various emotions:\n\n"
        
        categories = [
            ("Emotional Strategies", self.coping_strategies["emotional"]),
            ("Physical Strategies", self.coping_strategies["physical"]),
            ("Cognitive Strategies", self.coping_strategies["cognitive"]),
            ("Behavioral Strategies", self.coping_strategies["behavioral"])
        ]
        
        for category, strategies in categories:
            response += f"**{category}:**\n"
            for strategy in strategies:
                response += f"- {strategy['name']}: {strategy['description']}\n"
            response += "\n"
        
        response += "Would you like me to explain any of these strategies in more detail?"
        return response
    
    def _get_mindfulness_strategies(self) -> str:
        """Get mindfulness and relaxation strategies"""
        response = "**Mindfulness and Relaxation Strategies**\n\n"
        response += "Here are some practices that can help calm your mind and body:\n\n"
        
        mindfulness_strategies = [
            {
                "name": "Basic Mindfulness Meditation",
                "steps": [
                    "Find a quiet place to sit comfortably",
                    "Close your eyes and focus on your breath",
                    "Notice the sensation of air entering and leaving your nostrils",
                    "When your mind wanders, gently bring your attention back to your breath",
                    "Start with 5-10 minutes and gradually increase"
                ]
            },
            {
                "name": "Body Scan Meditation",
                "steps": [
                    "Lie down or sit comfortably",
                    "Close your eyes and take a few deep breaths",
                    "Bring your attention to your toes and notice any sensations",
                    "Slowly move your attention up through each part of your body",
                    "Notice any tension, warmth, tingling, or other sensations without judgment",
                    "If you notice tension, imagine breathing into that area and releasing the tension"
                ]
            },
            {
                "name": "Loving-Kindness Meditation",
                "steps": [
                    "Sit comfortably and close your eyes",
                    "Take a few deep breaths",
                    "Silently repeat phrases like: 'May I be safe. May I be healthy. May I live with ease.'",
                    "After a few minutes, extend these wishes to others: 'May you be safe...'",
                    "Start with someone you love, then a neutral person, then someone difficult, then all beings"
                ]
            }
        ]
        
        for strategy in mindfulness_strategies:
            response += f"**{strategy['name']}:**\n"
            for step in strategy['steps']:
                response += f"- {step}\n"
            response += "\n"
        
        response += "Would you like guidance through one of these practices?"
        return response
    
    def _get_journaling_strategies(self) -> str:
        """Get journaling strategies"""
        response = "**Journaling for Mental Health**\n\n"
        response += "Journaling can be a powerful tool for processing emotions and gaining insight. Here are some approaches:\n\n"
        
        journaling_types = [
            {
                "name": "Stream of Consciousness",
                "description": "Write whatever comes to mind without filtering or editing.",
                "prompt": "Set a timer for 10 minutes and write continuously without stopping."
            },
            {
                "name": "Gratitude Journal",
                "description": "Focus on the positive aspects of your life.",
                "prompt": "Write down 3-5 things you're grateful for each day, no matter how small."
            },
            {
                "name": "Emotion Tracking",
                "description": "Track your emotions and their triggers.",
                "prompt": "Note the emotion, its intensity (1-10), the trigger, and how you coped."
            },
            {
                "name": "Letter Writing",
                "description": "Write letters you don't necessarily send.",
                "prompt": "Write a letter to someone (living or deceased) to express unspoken feelings."
            },
            {
                "name": "Problem-Solving Journal",
                "description": "Work through problems on paper.",
                "prompt": "Describe the problem, brainstorm solutions, evaluate pros and cons, choose an action."
            },
            {
                "name": "Unsent Letters",
                "description": "Write letters to express feelings you can't say aloud.",
                "prompt": "Write a letter to someone expressing what you wish you could say, then decide whether to send it."
            }
        ]
        
        for journal in journaling_types:
            response += f"**{journal['name']}:**\n"
            response += f"{journal['description']}\n"
            response += f"Prompt: {journal['prompt']}\n\n"
        
        response += "Would you like a specific journaling prompt to try right now?"
        return response
    
    def _explain_therapy_techniques(self, user_input: str) -> Optional[str]:
        """Explain therapy techniques"""
        text_lower = user_input.lower()
        
        for therapy, info in self.therapy_techniques.items():
            if therapy in text_lower or info["name"].lower() in text_lower:
                response = f"**{info['name']} ({therapy.upper()})**\n\n"
                response += f"{info['description']}\n\n"
                
                if 'key_concepts' in info:
                    response += "**Key Concepts:**\n"
                    for concept in info['key_concepts']:
                        response += f"- {concept}\n"
                    response += "\n"
                
                if 'core_processes' in info:
                    response += "**Core Processes:**\n"
                    for process in info['core_processes']:
                        response += f"- {process}\n"
                    response += "\n"
                
                if 'modules' in info:
                    response += "**Main Modules:**\n"
                    for module in info['modules']:
                        response += f"- {module}\n"
                    response += "\n"
                
                if 'skills' in info:
                    response += "**Key Skills:**\n"
                    for skill in info['skills']:
                        response += f"- {skill['name']}: {' → '.join(skill['steps'])}\n"
                    response += "\n"
                
                if 'cognitive_distortions' in info:
                    response += "**Common Cognitive Distortions:**\n"
                    for distortion in info['cognitive_distortions']:
                        response += f"- {distortion['name']}: {distortion['example']}\n"
                    response += "\n"
                
                response += f"Would you like to learn more about {info['name']} or try a related exercise?"
                return response
        
        return None
    
    def _provide_resources(self) -> str:
        """Provide mental health resources"""
        response = "**Mental Health Resources**\n\n"
        response += "Here are some resources that might be helpful:\n\n"
        
        response += "**Crisis Hotlines:**\n"
        response += "- 988 Suicide & Crisis Lifeline (US): Call or text 988\n"
        response += "- Samaritans (UK): 116 123\n"
        response += "- Talk Suicide Canada: 1-833-456-4566\n"
        response += "- Lifeline (Australia): 13 11 14\n\n"
        
        response += "**Online Therapy Platforms:**\n"
        for resource in self.resources["online_therapy"]:
            response += f"- {resource['name']}: {resource['website']}\n"
        response += "\n"
        
        response += "**Self-Help Resources:**\n"
        for resource in self.resources["self_help"]:
            response += f"- {resource['name']}: {resource['website']}\n"
        response += "\n"
        
        response += "**Recommended Apps:**\n"
        for app in self.resources["apps"]:
            response += f"- {app['name']} ({app['platform']}): {app['description']}\n"
        
        response += "\nWould you like more specific resources for a particular need or location?"
        return response
    
    def _generate_empathetic_response(self, user_input: str) -> str:
        """Generate an empathetic response based on user input"""
        emotion = self.current_emotion
        
        # Emotion-specific responses
        emotion_responses = {
            Emotion.HAPPY: [
                "That's wonderful to hear! What's making you feel so good?",
                "I'm so happy for you! Positive emotions are important for our well-being.",
                "That sounds great! How can you carry this positive feeling forward?",
                "Your happiness is contagious! What's bringing you joy today?"
            ],
            Emotion.SAD: [
                "I'm really sorry you're feeling this way. It's okay to feel sad, and your feelings are valid. Would you like to talk about what's making you feel this way?",
                "That sounds really tough. Sometimes just acknowledging our sadness can be a first step toward feeling better. I'm here to listen.",
                "It's completely normal to feel sad sometimes. Would it help to talk about what's on your mind?",
                "I can hear the pain in what you're saying. Your feelings matter, and it's important to honor them. Would you like to share more?"
            ],
            Emotion.ANXIOUS: [
                "That sounds really anxiety-provoking. Would it help to talk through what's making you feel this way?",
                "Anxiety can feel overwhelming, but remember that it will pass. Would you like to try a grounding technique together?",
                "I can sense your anxiety. Sometimes just naming it can take away some of its power. What's triggering these feelings?",
                "That sounds really stressful. Would you like to explore some coping strategies that might help calm your anxiety?"
            ],
            Emotion.ANGRY: [
                "I can hear how upset you are. Anger is a valid emotion, and it's often a sign that something important to us has been violated. Would you like to talk about what happened?",
                "That sounds really frustrating. Sometimes anger can be a secondary emotion - what might be underneath it?",
                "I can sense your anger. It's important to acknowledge it. Would you like to explore what triggered these feelings?",
                "Anger can be a powerful emotion. How are you taking care of yourself while feeling this way?"
            ],
            Emotion.CALM: [
                "It's great to hear you're feeling calm. What's helping you feel this way?",
                "Calmness is such a valuable state. How can you maintain this feeling?",
                "That sounds peaceful. What's contributing to your sense of calm?",
                "I'm glad you're feeling calm. Sometimes we can learn from these moments about what helps us feel centered."
            ],
            Emotion.CONFUSED: [
                "Confusion can feel really unsettling. Would it help to talk through what's confusing you?",
                "It's okay to feel confused sometimes. What's making you feel this way?",
                "That sounds really puzzling. Would you like to explore this together?",
                "Confusion is a natural part of learning and growing. What questions do you have?"
            ],
            Emotion.STRESSED: [
                "Stress can be really overwhelming. What's contributing to your stress right now?",
                "That sounds really taxing. Would it help to talk about what's stressing you?",
                "I can hear how stressed you are. Sometimes just acknowledging it can help. What's on your plate right now?",
                "Stress is a signal that we might need to make some changes. Would you like to explore some stress management techniques?"
            ],
            Emotion.LONELY: [
                "Loneliness can be really painful. I'm here with you right now. Would you like to talk about what's making you feel this way?",
                "That sounds really isolating. Remember that you're not alone, even if it feels that way. What would help you feel more connected?",
                "I can hear the loneliness in what you're saying. Sometimes reaching out to others can help. Would you like to talk about this?",
                "Loneliness is a valid feeling. What do you think might help you feel less alone?"
            ],
            Emotion.HOPEFUL: [
                "That's wonderful! Hope is such an important emotion. What's giving you hope right now?",
                "Hope can be a powerful motivator. What are you looking forward to?",
                "It's great to hear you're feeling hopeful. What's contributing to this feeling?",
                "Hope is a sign of resilience. What's inspiring you at the moment?"
            ],
            Emotion.NEUTRAL: [
                "How are you feeling about that?",
                "That's interesting. What thoughts or emotions come up for you?",
                "Tell me more about that.",
                "What's on your mind today?"
            ],
            Emotion.UNKNOWN: [
                "That sounds important. How are you feeling about it?",
                "I'm here to listen. What would you like to talk about?",
                "That's interesting. What emotions come up for you?",
                "How does that make you feel?"
            ]
        }
        
        if emotion in emotion_responses:
            return random.choice(emotion_responses[emotion])
        
        # Generic empathetic responses
        generic_responses = [
            "That sounds important. Would you like to talk more about it?",
            "I'm here to listen. What's on your mind?",
            "That's a valid feeling. How are you taking care of yourself?",
            "I appreciate you sharing that with me. How does it feel to talk about it?",
            "That sounds meaningful. What else would you like to share?"
        ]
        
        return random.choice(generic_responses)
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation"""
        if not self.conversation_history:
            return "No conversation history yet."
        
        duration = datetime.datetime.now() - self.session_start
        minutes = duration.total_seconds() / 60
        
        # Count emotions
        emotion_counts = {}
        for entry in self.conversation_history:
            emotion = entry['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Most common emotion
        most_common_emotion = max(emotion_counts, key=emotion_counts.get) if emotion_counts else "neutral"
        
        summary = f"**Conversation Summary**\n\n"
        summary += f"Duration: {minutes:.1f} minutes\n"
        summary += f"Messages exchanged: {len(self.conversation_history)}\n"
        summary += f"Most common emotion: {most_common_emotion}\n\n"
        
        summary += "**Emotion Breakdown:**\n"
        for emotion, count in emotion_counts.items():
            summary += f"- {emotion}: {count} times\n"
        
        return summary
    
    def save_conversation(self, filename: str = None) -> str:
        """Save conversation history to a file"""
        import os
        
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        data = {
            "user_name": self.user_name,
            "start_time": self.session_start.isoformat(),
            "end_time": datetime.datetime.now().isoformat(),
            "conversation_history": self.conversation_history,
            "emotion_history": self.user_emotions,
            "crisis_level": self.crisis_level.value
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return f"Conversation saved to {filename}"
    
    def load_conversation(self, filename: str) -> str:
        """Load conversation history from a file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.user_name = data.get("user_name")
            self.session_start = datetime.datetime.fromisoformat(data.get("start_time"))
            self.conversation_history = data.get("conversation_history", [])
            self.user_emotions = data.get("emotion_history", [])
            self.crisis_level = CrisisLevel(int(data.get("crisis_level", 0)))
            
            return f"Conversation loaded from {filename}"
        except Exception as e:
            return f"Error loading conversation: {e}"


def main():
    """Main function to run the chatbot"""
    print("=" * 60)
    print("MindCare: Psychology and Psychiatry Chatbot")
    print("=" * 60)
    print("Type 'quit', 'exit', or 'bye' to end the conversation")
    print("-" * 60)
    
    chatbot = PsychologyChatbot()
    
    # Initial greeting
    print(chatbot.greet_user())
    
    while True:
        try:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print(f"\n{chatbot.name}: {random.choice(chatbot.goodbyes)}")
                break
            
            response = chatbot.process_input(user_input)
            print(f"\n{chatbot.name}: {response}")
            
        except KeyboardInterrupt:
            print(f"\n{chatbot.name}: {random.choice(chatbot.goodbyes)}")
            break
        except EOFError:
            print(f"\n{chatbot.name}: {random.choice(chatbot.goodbyes)}")
            break
    
    # Offer to save conversation
    save = input("\nWould you like to save this conversation? (y/n): ").lower()
    if save == 'y':
        filename = input("Enter filename (or press Enter for default): ").strip()
        if not filename:
            filename = None
        print(chatbot.save_conversation(filename))


if __name__ == "__main__":
    main()
