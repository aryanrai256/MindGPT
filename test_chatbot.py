#!/usr/bin/env python3
"""
Test suite for the Psychology Chatbot
"""

import unittest
import tempfile
import os
import json
from main import PsychologyChatbot, Emotion, CrisisLevel


class TestPsychologyChatbot(unittest.TestCase):
    """Test cases for the PsychologyChatbot class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.chatbot = PsychologyChatbot("TestBot")
    
    def test_initialization(self):
        """Test that the chatbot initializes correctly"""
        self.assertEqual(self.chatbot.name, "TestBot")
        self.assertEqual(self.chatbot.conversation_history, [])
        self.assertEqual(self.chatbot.user_emotions, [])
        self.assertEqual(self.chatbot.current_emotion, Emotion.NEUTRAL)
        self.assertEqual(self.chatbot.crisis_level, CrisisLevel.NONE)
        self.assertIsNotNone(self.chatbot.knowledge_base)
        self.assertIsNotNone(self.chatbot.coping_strategies)
        self.assertIsNotNone(self.chatbot.therapy_techniques)
        self.assertIsNotNone(self.chatbot.resources)
        self.assertIsNotNone(self.chatbot.crisis_keywords)
    
    def test_detect_emotion(self):
        """Test emotion detection"""
        # Test happy
        self.assertEqual(self.chatbot.detect_emotion("I'm so happy today!"), Emotion.HAPPY)
        self.assertEqual(self.chatbot.detect_emotion("This is amazing!"), Emotion.HAPPY)
        
        # Test sad
        self.assertEqual(self.chatbot.detect_emotion("I feel so sad"), Emotion.SAD)
        self.assertEqual(self.chatbot.detect_emotion("I'm depressed"), Emotion.SAD)
        
        # Test anxious
        self.assertEqual(self.chatbot.detect_emotion("I'm feeling anxious"), Emotion.ANXIOUS)
        self.assertEqual(self.chatbot.detect_emotion("I'm worried about everything"), Emotion.ANXIOUS)
        
        # Test angry
        self.assertEqual(self.chatbot.detect_emotion("I'm so angry!"), Emotion.ANGRY)
        self.assertEqual(self.chatbot.detect_emotion("This makes me furious"), Emotion.ANGRY)
        
        # Test calm
        self.assertEqual(self.chatbot.detect_emotion("I feel calm and peaceful"), Emotion.CALM)
        
        # Test confused
        self.assertEqual(self.chatbot.detect_emotion("I'm so confused"), Emotion.CONFUSED)
        
        # Test stressed - this should now work correctly
        self.assertEqual(self.chatbot.detect_emotion("I'm really stressed out"), Emotion.STRESSED)
        
        # Test lonely
        self.assertEqual(self.chatbot.detect_emotion("I feel so lonely"), Emotion.LONELY)
        
        # Test hopeful
        self.assertEqual(self.chatbot.detect_emotion("I'm feeling hopeful"), Emotion.HOPEFUL)
        
        # Test neutral
        self.assertEqual(self.chatbot.detect_emotion("The sky is blue"), Emotion.NEUTRAL)
        
        # Test unknown - returns NEUTRAL for unrecognized input
        self.assertEqual(self.chatbot.detect_emotion("xyz123"), Emotion.NEUTRAL)
    
    def test_assess_crisis_level(self):
        """Test crisis level assessment"""
        # Test emergency level
        self.assertEqual(self.chatbot.assess_crisis_level("I want to kill myself"), CrisisLevel.EMERGENCY)
        self.assertEqual(self.chatbot.assess_crisis_level("I'm going to end my life"), CrisisLevel.EMERGENCY)
        self.assertEqual(self.chatbot.assess_crisis_level("suicide is the only option"), CrisisLevel.EMERGENCY)
        
        # Test high crisis level
        self.assertEqual(self.chatbot.assess_crisis_level("I want to hurt myself"), CrisisLevel.HIGH)
        self.assertEqual(self.chatbot.assess_crisis_level("I'm going to cut myself"), CrisisLevel.HIGH)
        self.assertEqual(self.chatbot.assess_crisis_level("I was raped"), CrisisLevel.HIGH)
        self.assertEqual(self.chatbot.assess_crisis_level("I'm hearing voices"), CrisisLevel.HIGH)
        
        # Test medium crisis level
        self.assertEqual(self.chatbot.assess_crisis_level("I can't take it anymore"), CrisisLevel.MEDIUM)
        self.assertEqual(self.chatbot.assess_crisis_level("I'm breaking down"), CrisisLevel.MEDIUM)
        
        # Test no crisis
        self.assertEqual(self.chatbot.assess_crisis_level("I had a good day"), CrisisLevel.NONE)
        self.assertEqual(self.chatbot.assess_crisis_level("Hello, how are you?"), CrisisLevel.NONE)
    
    def test_handle_crisis(self):
        """Test crisis handling"""
        # Test emergency response
        response = self.chatbot.handle_crisis("I want to kill myself")
        self.assertIn("emergency", response.lower())
        self.assertEqual(self.chatbot.crisis_level, CrisisLevel.EMERGENCY)
        
        # Test high crisis response
        self.chatbot.crisis_level = CrisisLevel.NONE  # Reset
        response = self.chatbot.handle_crisis("I'm going to hurt myself")
        self.assertIn("crisis", response.lower())
        self.assertEqual(self.chatbot.crisis_level, CrisisLevel.HIGH)
        
        # Test medium crisis response - check for any of the possible responses
        self.chatbot.crisis_level = CrisisLevel.NONE  # Reset
        response = self.chatbot.handle_crisis("I can't take it anymore")
        self.assertTrue(any(word in response.lower() for word in ["tough time", "distress", "overwhelming", "professional"]))
        self.assertEqual(self.chatbot.crisis_level, CrisisLevel.MEDIUM)
        
        # Test no crisis
        self.chatbot.crisis_level = CrisisLevel.NONE  # Reset
        response = self.chatbot.handle_crisis("I had a good day")
        self.assertEqual(response, "")
        self.assertEqual(self.chatbot.crisis_level, CrisisLevel.NONE)
    
    def test_greet_user(self):
        """Test greeting functionality"""
        # Test without user name
        greeting = self.chatbot.greet_user()
        self.assertIn("TestBot", greeting)
        self.assertIn("What's your name", greeting)
        
        # Test with user name
        self.chatbot.user_name = "Alice"
        greeting = self.chatbot.greet_user()
        self.assertIn("Alice", greeting)
        self.assertIn("How are you feeling", greeting)
    
    def test_process_input_name_extraction(self):
        """Test name extraction from user input"""
        response = self.chatbot.process_input("My name is Alice")
        self.assertEqual(self.chatbot.user_name, "Alice")
        self.assertIn("Alice", response)
        
        # Reset and test another format
        self.chatbot.user_name = None
        response = self.chatbot.process_input("I'm Bob")
        self.assertEqual(self.chatbot.user_name, "Bob")
        self.assertIn("Bob", response)
    
    def test_process_input_mental_health_questions(self):
        """Test responses to mental health questions"""
        response = self.chatbot.process_input("What is depression?")
        self.assertIn("depression", response.lower())
        self.assertIn("mood disorder", response.lower())
        
        response = self.chatbot.process_input("Tell me about anxiety")
        self.assertIn("anxiety", response.lower())
        self.assertIn("excessive", response.lower())
    
    def test_process_input_coping_strategies(self):
        """Test coping strategy responses"""
        response = self.chatbot.process_input("How can I cope with stress?")
        self.assertIn("stress", response.lower())
        
        response = self.chatbot.process_input("I need coping strategies")
        self.assertIn("coping", response.lower())
    
    def test_process_input_therapy_techniques(self):
        """Test therapy technique explanations"""
        response = self.chatbot.process_input("What is CBT?")
        self.assertIn("cognitive behavioral therapy", response.lower())
        
        response = self.chatbot.process_input("Tell me about ACT")
        self.assertIn("acceptance and commitment therapy", response.lower())
    
    def test_process_input_greetings(self):
        """Test greeting responses"""
        self.chatbot.user_name = "Alice"
        response = self.chatbot.process_input("Hello")
        self.assertIn("Alice", response)
        
        response = self.chatbot.process_input("Hi there")
        self.assertIn("Alice", response)
    
    def test_process_input_goodbyes(self):
        """Test goodbye responses - updated to match actual responses"""
        response = self.chatbot.process_input("Goodbye")
        # Check for any of the possible goodbye responses
        self.assertTrue(any(word in response.lower() for word in ["take care", "here whenever", "be kind", "reach out"]))
        
        response = self.chatbot.process_input("Bye")
        self.assertTrue(any(word in response.lower() for word in ["take care", "here whenever", "be kind", "reach out"]))
    
    def test_process_input_thanks(self):
        """Test thank you responses - updated to match actual responses"""
        response = self.chatbot.process_input("Thank you")
        # Check for any of the possible thank you responses
        self.assertTrue(any(word in response.lower() for word in ["welcome", "pleasure", "anytime", "deserve"]))
        
        response = self.chatbot.process_input("Thanks")
        self.assertTrue(any(word in response.lower() for word in ["welcome", "pleasure", "anytime", "deserve"]))
    
    def test_get_crisis_resources(self):
        """Test crisis resource retrieval"""
        # Test with location
        resources = self.chatbot.get_crisis_resources("United States")
        self.assertIn("United States", resources)
        self.assertIn("988", resources)
        
        # Test without location (default)
        resources = self.chatbot.get_crisis_resources()
        self.assertIn("International", resources)
        self.assertIn("United States", resources)
    
    def test_get_conversation_summary(self):
        """Test conversation summary"""
        # Add some conversation history
        self.chatbot.process_input("Hello, I'm feeling sad today")
        self.chatbot.process_input("I'm also feeling anxious")
        
        summary = self.chatbot.get_conversation_summary()
        self.assertIn("Conversation Summary", summary)
        self.assertIn("Messages exchanged", summary)
        self.assertIn("Emotion Breakdown", summary)
    
    def test_save_and_load_conversation(self):
        """Test saving and loading conversations"""
        # Add some conversation history
        self.chatbot.user_name = "TestUser"
        self.chatbot.process_input("Hello")
        self.chatbot.process_input("I'm feeling happy today")
        
        # Save conversation
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_filename = f.name
        
        try:
            save_result = self.chatbot.save_conversation(temp_filename)
            self.assertIn("saved", save_result.lower())
            
            # Verify file exists and contains data
            with open(temp_filename, 'r') as f:
                data = json.load(f)
            
            self.assertEqual(data['user_name'], "TestUser")
            self.assertEqual(len(data['conversation_history']), 2)
            
            # Test loading
            new_chatbot = PsychologyChatbot()
            load_result = new_chatbot.load_conversation(temp_filename)
            self.assertIn("loaded", load_result.lower())
            self.assertEqual(new_chatbot.user_name, "TestUser")
            self.assertEqual(len(new_chatbot.conversation_history), 2)
            
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
    
    def test_emotion_tracking(self):
        """Test that emotions are tracked correctly"""
        self.chatbot.process_input("I'm feeling happy")
        self.assertEqual(self.chatbot.current_emotion, Emotion.HAPPY)
        self.assertEqual(len(self.chatbot.user_emotions), 1)
        self.assertEqual(self.chatbot.user_emotions[0], Emotion.HAPPY.value)
        
        self.chatbot.process_input("Now I'm feeling sad")
        self.assertEqual(self.chatbot.current_emotion, Emotion.SAD)
        self.assertEqual(len(self.chatbot.user_emotions), 2)
        self.assertEqual(self.chatbot.user_emotions[1], Emotion.SAD.value)
    
    def test_conversation_history(self):
        """Test that conversation history is recorded"""
        self.chatbot.process_input("First message")
        self.chatbot.process_input("Second message")
        
        self.assertEqual(len(self.chatbot.conversation_history), 2)
        self.assertEqual(self.chatbot.conversation_history[0]['user'], "First message")
        self.assertEqual(self.chatbot.conversation_history[1]['user'], "Second message")
        self.assertIn('timestamp', self.chatbot.conversation_history[0])
        self.assertIn('emotion', self.chatbot.conversation_history[0])
    
    def test_knowledge_base_content(self):
        """Test that knowledge base has expected content"""
        self.assertIn('depression', self.chatbot.knowledge_base)
        self.assertIn('anxiety', self.chatbot.knowledge_base)
        self.assertIn('stress', self.chatbot.knowledge_base)
        self.assertIn('self_care', self.chatbot.knowledge_base)
        self.assertIn('mindfulness', self.chatbot.knowledge_base)
        self.assertIn('sleep', self.chatbot.knowledge_base)
        
        # Check depression content
        depression = self.chatbot.knowledge_base['depression']
        self.assertIn('description', depression)
        self.assertIn('symptoms', depression)
        self.assertIn('treatment', depression)
        self.assertIn('when_to_seek_help', depression)
    
    def test_coping_strategies_content(self):
        """Test that coping strategies are loaded correctly"""
        self.assertIn('emotional', self.chatbot.coping_strategies)
        self.assertIn('physical', self.chatbot.coping_strategies)
        self.assertIn('cognitive', self.chatbot.coping_strategies)
        self.assertIn('behavioral', self.chatbot.coping_strategies)
        
        # Check emotional strategies
        emotional = self.chatbot.coping_strategies['emotional']
        self.assertGreater(len(emotional), 0)
        self.assertIn('name', emotional[0])
        self.assertIn('description', emotional[0])
        self.assertIn('steps', emotional[0])
    
    def test_therapy_techniques_content(self):
        """Test that therapy techniques are loaded correctly"""
        self.assertIn('cbt', self.chatbot.therapy_techniques)
        self.assertIn('act', self.chatbot.therapy_techniques)
        self.assertIn('dbt', self.chatbot.therapy_techniques)
        self.assertIn('mindfulness_based', self.chatbot.therapy_techniques)
        
        # Check CBT content
        cbt = self.chatbot.therapy_techniques['cbt']
        self.assertEqual(cbt['name'], "Cognitive Behavioral Therapy")
        self.assertIn('key_concepts', cbt)
        self.assertIn('cognitive_distortions', cbt)
    
    def test_resources_content(self):
        """Test that resources are loaded correctly"""
        self.assertIn('hotlines', self.chatbot.resources)
        self.assertIn('online_therapy', self.chatbot.resources)
        self.assertIn('self_help', self.chatbot.resources)
        self.assertIn('apps', self.chatbot.resources)
        
        # Check hotlines
        hotlines = self.chatbot.resources['hotlines']
        self.assertIn('International', hotlines)
        self.assertIn('United States', hotlines)
        self.assertIn('United Kingdom', hotlines)
    
    def test_crisis_keywords_content(self):
        """Test that crisis keywords are loaded correctly"""
        self.assertGreater(len(self.chatbot.crisis_keywords), 0)
        self.assertIn("kill myself", self.chatbot.crisis_keywords)
        self.assertIn("suicide", self.chatbot.crisis_keywords)
        self.assertIn("abuse", self.chatbot.crisis_keywords)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_empty_input(self):
        """Test handling of empty input"""
        chatbot = PsychologyChatbot()
        response = chatbot.process_input("")
        # Should still generate some response
        self.assertIsInstance(response, str)
    
    def test_whitespace_only_input(self):
        """Test handling of whitespace-only input"""
        chatbot = PsychologyChatbot()
        response = chatbot.process_input("   ")
        # Should still generate some response
        self.assertIsInstance(response, str)
    
    def test_very_long_input(self):
        """Test handling of very long input"""
        chatbot = PsychologyChatbot()
        long_input = "A" * 10000  # Very long string
        response = chatbot.process_input(long_input)
        # Should still generate some response
        self.assertIsInstance(response, str)
    
    def test_special_characters(self):
        """Test handling of special characters"""
        chatbot = PsychologyChatbot()
        special_input = "I'm feeling @#$%^&*() sad today!"
        response = chatbot.process_input(special_input)
        self.assertIsInstance(response, str)
    
    def test_unicode_input(self):
        """Test handling of unicode input"""
        chatbot = PsychologyChatbot()
        unicode_input = "Je me sens triste aujourd'hui 😢"
        response = chatbot.process_input(unicode_input)
        self.assertIsInstance(response, str)
    
    def test_mixed_case_input(self):
        """Test handling of mixed case input"""
        chatbot = PsychologyChatbot()
        mixed_input = "I'm FeElInG AnXiOuS ToDaY"
        response = chatbot.process_input(mixed_input)
        self.assertIsInstance(response, str)
        # Should detect anxiety regardless of case
        self.assertEqual(chatbot.current_emotion, Emotion.ANXIOUS)


if __name__ == '__main__':
    unittest.main()
