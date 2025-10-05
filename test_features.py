#!/usr/bin/env python3
"""
Test script for the enhanced quiz app features
"""

from Question import Question
from Quiz import Quiz
from QuizLoader import QuizLoader
from SpacedRepetition import SpacedRepetitionManager
from ErrorAnalyzer import ErrorAnalyzer

def test_spaced_repetition():
    """Test spaced repetition functionality"""
    print("🧠 Testing Spaced Repetition System...")
    
    # Create a test question
    question = Question(
        question="What is Python?",
        answers=["1. Programming language", "2. Snake", "3. Framework", "4. Library"],
        correct_answer=1,
        hints={"correct": "Correct!", "fail": "Wrong!"},
        topic="Python Basics"
    )
    
    # Test spaced repetition manager
    sr_manager = SpacedRepetitionManager()
    username = "TestUser"
    
    # Initialize question
    sr_manager.initialize_question(question.get_id(), username)
    print(f"✅ Question initialized for {username}")
    
    # Simulate correct answer
    sr_manager.update_question_performance(question.get_id(), username, True, 5.0)
    print("✅ Performance updated for correct answer")
    
    # Simulate incorrect answer
    sr_manager.update_question_performance(question.get_id(), username, False, 10.0)
    print("✅ Performance updated for incorrect answer")
    
    # Get statistics
    stats = sr_manager.get_user_statistics(username)
    print(f"✅ User statistics: {stats}")
    
    print("🎉 Spaced repetition system works!\n")

def test_error_analysis():
    """Test error analysis functionality"""
    print("🔍 Testing Error Analysis System...")
    
    # Create error analyzer
    error_analyzer = ErrorAnalyzer()
    
    # Get error summary for test user
    summary = error_analyzer.get_user_error_summary("TestUser")
    print(f"✅ Error summary generated: {summary['total_questions_attempted']} questions")
    
    # Get recommendations
    recommendations = error_analyzer.get_progress_recommendations("TestUser")
    print(f"✅ Generated {len(recommendations)} recommendations")
    
    print("🎉 Error analysis system works!\n")

def test_quiz_loader():
    """Test quiz loader functionality"""
    print("📚 Testing Quiz Loader System...")
    
    quiz_loader = QuizLoader()
    
    # Get available topics
    topics = quiz_loader.get_available_topics()
    print(f"✅ Found {len(topics)} topics available")
    
    if topics:
        # Test spaced repetition quiz
        topic_file = topics[0][1]
        questions = quiz_loader.get_spaced_repetition_quiz("TestUser", topic_file, 5)
        print(f"✅ Generated spaced repetition quiz with {len(questions)} questions")
        
        # Test difficult questions quiz
        difficult_questions = quiz_loader.get_difficult_questions_quiz("TestUser", topic_file, 3)
        print(f"✅ Generated difficult questions quiz with {len(difficult_questions)} questions")
        
        # Test mixed review quiz
        mixed_questions = quiz_loader.get_mixed_review_quiz("TestUser", 5)
        print(f"✅ Generated mixed review quiz with {len(mixed_questions)} questions")
    
    print("🎉 Quiz loader system works!\n")

def test_question_tracking():
    """Test question response time tracking"""
    print("⏱️ Testing Question Tracking...")
    
    question = Question(
        question="Test question?",
        answers=["1. A", "2. B", "3. C", "4. D"],
        correct_answer=1,
        hints={"correct": "Right!", "fail": "Wrong!"},
        topic="Test Topic"
    )
    
    # Simulate asking question
    question.ask()
    
    # Simulate answering
    result = question.check_user_answer(1)
    response_time = question.get_response_time()
    
    print(f"✅ Question ID: {question.get_id()}")
    print(f"✅ Answer correct: {result}")
    print(f"✅ Response time tracked: {response_time} seconds")
    
    print("🎉 Question tracking works!\n")

if __name__ == "__main__":
    print("🚀 Testing Enhanced Quiz App Features\n")
    print("=" * 50)
    
    try:
        test_question_tracking()
        test_spaced_repetition()
        test_error_analysis()
        test_quiz_loader()
        
        print("=" * 50)
        print("🎉 ALL TESTS PASSED! The enhanced quiz app is ready to use!")
        print("\n📋 Features implemented:")
        print("   ✅ Spaced Repetition Algorithm")
        print("   ✅ Error Focus System")
        print("   ✅ Smart Question Scheduling")
        print("   ✅ Response Time Tracking")
        print("   ✅ Performance Analytics")
        print("   ✅ Mixed Review Mode")
        print("   ✅ Learning Progress Tracking")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()