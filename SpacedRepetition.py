import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import hashlib


class SpacedRepetitionManager:
    """
    Manages spaced repetition algorithm for quiz questions.
    Based on SuperMemo SM-2 algorithm with modifications.
    """
    
    def __init__(self, data_file: str = "spaced_repetition_data.json"):
        self.data_file = data_file
        self.question_data = self.load_data()
    
    def load_data(self) -> Dict[str, Dict[str, Any]]:
        """Load spaced repetition data from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    return json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def save_data(self) -> None:
        """Save spaced repetition data to JSON file."""
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.question_data, file, indent=2, default=str)
        except Exception as e:
            print(f"Error saving spaced repetition data: {e}")
    
    def get_question_id(self, question_text: str, topic: str) -> str:
        """Generate unique ID for a question based on content and topic."""
        content = f"{topic}:{question_text}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def initialize_question(self, question_id: str, username: str) -> None:
        """Initialize a question in the spaced repetition system."""
        user_key = f"{username}:{question_id}"
        if user_key not in self.question_data:
            self.question_data[user_key] = {
                'ease_factor': 2.5,      # Starting ease factor
                'repetition': 0,         # Number of successful repetitions
                'interval': 1,           # Days until next review
                'next_review': datetime.now().isoformat(),
                'total_attempts': 0,
                'correct_attempts': 0,
                'last_response_time': 0,
                'avg_response_time': 0,
                'created_date': datetime.now().isoformat()
            }
    
    def update_question_performance(self, question_id: str, username: str, 
                                  was_correct: bool, response_time: float) -> None:
        """
        Update question performance based on user's answer.
        Implements modified SM-2 algorithm.
        """
        user_key = f"{username}:{question_id}"
        
        # Initialize if doesn't exist
        if user_key not in self.question_data:
            self.initialize_question(question_id, username)
        
        data = self.question_data[user_key]
        
        # Update basic stats
        data['total_attempts'] += 1
        if was_correct:
            data['correct_attempts'] += 1
        
        # Update response time
        data['last_response_time'] = response_time
        total_time = data['avg_response_time'] * (data['total_attempts'] - 1) + response_time
        data['avg_response_time'] = total_time / data['total_attempts']
        
        # SM-2 Algorithm implementation
        if was_correct:
            if data['repetition'] == 0:
                data['interval'] = 1
            elif data['repetition'] == 1:
                data['interval'] = 6
            else:
                data['interval'] = int(data['interval'] * data['ease_factor'])
            
            data['repetition'] += 1
        else:
            # Reset repetition count and set short interval for incorrect answers
            data['repetition'] = 0
            data['interval'] = 1
        
        # Update ease factor based on performance
        # Quality scale: 5 = perfect, 4 = correct with hesitation, 3 = correct with difficulty
        # 2 = incorrect but easy to recall, 1 = incorrect with difficulty, 0 = complete blackout
        
        if was_correct:
            # Adjust quality based on response time (faster = higher quality)
            if response_time <= 5:  # Very fast response
                quality = 5
            elif response_time <= 10:  # Fast response
                quality = 4
            else:  # Slow but correct
                quality = 3
        else:
            # Incorrect answer - quality based on how often they get it wrong
            success_rate = data['correct_attempts'] / data['total_attempts']
            if success_rate > 0.7:
                quality = 2  # Usually gets it right
            elif success_rate > 0.3:
                quality = 1  # Sometimes gets it right
            else:
                quality = 0  # Rarely gets it right
        
        # Update ease factor
        new_ease = data['ease_factor'] + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        data['ease_factor'] = max(1.3, new_ease)  # Minimum ease factor of 1.3
        
        # Calculate next review date
        next_review = datetime.now() + timedelta(days=data['interval'])
        data['next_review'] = next_review.isoformat()
        
        self.save_data()
    
    def get_questions_due_for_review(self, username: str, all_question_ids: List[str]) -> List[str]:
        """Get list of question IDs that are due for review."""
        now = datetime.now()
        due_questions = []
        
        for question_id in all_question_ids:
            user_key = f"{username}:{question_id}"
            
            if user_key not in self.question_data:
                # New question - always due for review
                due_questions.append(question_id)
            else:
                data = self.question_data[user_key]
                next_review = datetime.fromisoformat(data['next_review'])
                if now >= next_review:
                    due_questions.append(question_id)
        
        return due_questions
    
    def get_question_priority(self, question_id: str, username: str) -> float:
        """
        Calculate priority score for a question.
        Higher score = higher priority (should be reviewed sooner).
        """
        user_key = f"{username}:{question_id}"
        
        if user_key not in self.question_data:
            return 100.0  # New questions have highest priority
        
        data = self.question_data[user_key]
        
        # Calculate days overdue
        now = datetime.now()
        next_review = datetime.fromisoformat(data['next_review'])
        days_overdue = (now - next_review).days
        
        # Priority factors:
        # 1. How overdue the question is
        overdue_factor = max(0, days_overdue) * 10
        
        # 2. Success rate (lower success = higher priority)
        success_rate = data['correct_attempts'] / max(1, data['total_attempts'])
        difficulty_factor = (1 - success_rate) * 50
        
        # 3. Ease factor (lower ease = higher priority)
        ease_factor = (3.0 - data['ease_factor']) * 20
        
        # 4. Time since last review
        time_factor = min(days_overdue, 30)  # Cap at 30 days
        
        return overdue_factor + difficulty_factor + ease_factor + time_factor
    
    def get_user_statistics(self, username: str) -> Dict[str, Any]:
        """Get spaced repetition statistics for a user."""
        user_questions = {k: v for k, v in self.question_data.items() 
                         if k.startswith(f"{username}:")}
        
        if not user_questions:
            return {
                'total_questions': 0,
                'questions_mastered': 0,
                'questions_learning': 0,
                'questions_difficult': 0,
                'average_ease': 0,
                'total_reviews': 0
            }
        
        total_questions = len(user_questions)
        mastered = sum(1 for data in user_questions.values() 
                      if data['repetition'] >= 3 and data['ease_factor'] >= 2.5)
        learning = sum(1 for data in user_questions.values() 
                      if 1 <= data['repetition'] < 3)
        difficult = sum(1 for data in user_questions.values() 
                       if data['ease_factor'] < 2.0)
        
        avg_ease = sum(data['ease_factor'] for data in user_questions.values()) / total_questions
        total_reviews = sum(data['total_attempts'] for data in user_questions.values())
        
        return {
            'total_questions': total_questions,
            'questions_mastered': mastered,
            'questions_learning': learning, 
            'questions_difficult': difficult,
            'average_ease': round(avg_ease, 2),
            'total_reviews': total_reviews
        }
    
    def get_review_schedule(self, username: str, days: int = 7) -> Dict[str, List[str]]:
        """Get review schedule for the next N days."""
        schedule = {}
        now = datetime.now()
        
        for i in range(days):
            date = now + timedelta(days=i)
            date_key = date.strftime('%Y-%m-%d')
            schedule[date_key] = []
        
        # Find questions scheduled for review in the next N days
        for key, data in self.question_data.items():
            if key.startswith(f"{username}:"):
                next_review = datetime.fromisoformat(data['next_review'])
                if now <= next_review <= now + timedelta(days=days):
                    date_key = next_review.strftime('%Y-%m-%d')
                    if date_key in schedule:
                        question_id = key.split(':', 1)[1]
                        schedule[date_key].append(question_id)
        
        return schedule