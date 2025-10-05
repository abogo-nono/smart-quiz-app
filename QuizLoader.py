import json
import glob
import random
from typing import List, Dict, Any, Optional
from Question import Question
from SpacedRepetition import SpacedRepetitionManager


class QuizLoader:
    """Enhanced QuizLoader with spaced repetition support."""
    
    def __init__(self, db_folder: str = "db"):
        self.db_folder = db_folder
        self.spaced_rep_manager = SpacedRepetitionManager()
    
    def get_available_topics(self) -> List[str]:
        """Get list of available quiz topics."""
        json_files = glob.glob(f"{self.db_folder}/*.json")
        topics = []
        for file_path in json_files:
            topic_name = file_path.split('/')[-1].replace('.json', '').replace('_', ' ').title()
            topics.append((topic_name, file_path))
        return topics
    
    def load_questions_from_file(self, file_path: str) -> List[Question]:
        """Load questions from a JSON file."""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Extract topic name from file path
            topic_name = file_path.split('/')[-1].replace('.json', '').replace('_', ' ').title()
            
            questions = []
            
            # Handle both old format (list) and new format (dict with metadata)
            if isinstance(data, list):
                questions_data = data
            else:
                questions_data = data.get('questions', [])
            
            for item in questions_data:
                question = Question(
                    question=item['question'],
                    answers=item['answers'],
                    correct_answer=item['answer'],
                    hints=item['hints'],
                    topic=topic_name
                )
                questions.append(question)
            
            return questions
        except Exception as e:
            print(f"Error loading questions from {file_path}: {e}")
            return []
    
    def get_all_questions_from_topic(self, file_path: str) -> List[Question]:
        """Get all questions from a specific topic."""
        return self.load_questions_from_file(file_path)
    
    def get_spaced_repetition_quiz(self, username: str, file_path: str, max_questions: int = 10) -> List[Question]:
        """
        Generate a quiz using spaced repetition algorithm.
        Prioritizes questions that are due for review.
        """
        all_questions = self.load_questions_from_file(file_path)
        
        if not all_questions:
            return []
        
        # Get question IDs for all questions
        all_question_ids = [q.get_id() for q in all_questions]
        
        # Initialize questions that don't exist in spaced repetition data
        for question in all_questions:
            self.spaced_rep_manager.initialize_question(question.get_id(), username)
        
        # Get questions due for review
        due_questions = self.spaced_rep_manager.get_questions_due_for_review(username, all_question_ids)
        
        # Create a mapping of question ID to question object
        question_map = {q.get_id(): q for q in all_questions}
        
        # Sort due questions by priority (highest priority first)
        due_questions_with_priority = []
        for q_id in due_questions:
            priority = self.spaced_rep_manager.get_question_priority(q_id, username)
            due_questions_with_priority.append((priority, q_id))
        
        due_questions_with_priority.sort(reverse=True)  # Sort by priority (descending)
        
        # Select questions for the quiz
        selected_questions = []
        
        # First, add high-priority due questions
        for priority, q_id in due_questions_with_priority[:max_questions]:
            if q_id in question_map:
                selected_questions.append(question_map[q_id])
        
        # If we need more questions, add some random ones
        if len(selected_questions) < max_questions:
            remaining_questions = [q for q in all_questions if q not in selected_questions]
            remaining_needed = max_questions - len(selected_questions)
            
            if remaining_questions:
                random_questions = random.sample(
                    remaining_questions, 
                    min(remaining_needed, len(remaining_questions))
                )
                selected_questions.extend(random_questions)
        
        # Shuffle the final question order to avoid patterns
        random.shuffle(selected_questions)
        
        return selected_questions
    
    def get_difficult_questions_quiz(self, username: str, file_path: Optional[str] = None, max_questions: int = 10) -> List[Question]:
        """
        Generate a quiz focusing on questions the user finds most difficult.
        If file_path is None, includes questions from all topics.
        """
        if file_path:
            all_questions = self.load_questions_from_file(file_path)
        else:
            # Load questions from all topics
            all_questions = []
            topics = self.get_available_topics()
            for _, topic_file in topics:
                all_questions.extend(self.load_questions_from_file(topic_file))
        
        if not all_questions:
            return []
        
        # Get difficulty scores for all questions
        difficult_questions = []
        question_map = {q.get_id(): q for q in all_questions}
        
        for question in all_questions:
            user_key = f"{username}:{question.get_id()}"
            if user_key in self.spaced_rep_manager.question_data:
                data = self.spaced_rep_manager.question_data[user_key]
                # Calculate difficulty score based on success rate and ease factor
                success_rate = data['correct_attempts'] / max(1, data['total_attempts'])
                difficulty_score = (1 - success_rate) * 100 + (3.0 - data['ease_factor']) * 20
                
                # Only include questions that have been attempted
                if data['total_attempts'] > 0:
                    difficult_questions.append((difficulty_score, question.get_id()))
        
        # Sort by difficulty (most difficult first)
        difficult_questions.sort(reverse=True)
        
        # Select the most difficult questions
        selected_questions = []
        for difficulty_score, q_id in difficult_questions[:max_questions]:
            if q_id in question_map:
                selected_questions.append(question_map[q_id])
        
        # If we need more questions and haven't found enough difficult ones,
        # add some random questions
        if len(selected_questions) < max_questions:
            remaining_questions = [q for q in all_questions if q not in selected_questions]
            remaining_needed = max_questions - len(selected_questions)
            
            if remaining_questions:
                random_questions = random.sample(
                    remaining_questions,
                    min(remaining_needed, len(remaining_questions))
                )
                selected_questions.extend(random_questions)
        
        random.shuffle(selected_questions)
        return selected_questions
    
    def get_mixed_review_quiz(self, username: str, max_questions: int = 15) -> List[Question]:
        """
        Generate a mixed review quiz with questions from all topics,
        prioritizing spaced repetition and difficult questions.
        """
        all_questions = []
        topics = self.get_available_topics()
        
        # Load questions from all topics
        for _, topic_file in topics:
            all_questions.extend(self.load_questions_from_file(topic_file))
        
        if not all_questions:
            return []
        
        # Split quiz: 60% spaced repetition, 40% difficult questions
        sr_count = int(max_questions * 0.6)
        difficult_count = max_questions - sr_count
        
        # Get spaced repetition questions (from all topics)
        all_question_ids = [q.get_id() for q in all_questions]
        due_questions = self.spaced_rep_manager.get_questions_due_for_review(username, all_question_ids)
        
        question_map = {q.get_id(): q for q in all_questions}
        sr_questions = []
        
        # Sort due questions by priority
        due_with_priority = []
        for q_id in due_questions:
            priority = self.spaced_rep_manager.get_question_priority(q_id, username)
            due_with_priority.append((priority, q_id))
        
        due_with_priority.sort(reverse=True)
        
        # Add high-priority due questions
        for priority, q_id in due_with_priority[:sr_count]:
            if q_id in question_map:
                sr_questions.append(question_map[q_id])
        
        # Get difficult questions
        difficult_questions = self.get_difficult_questions_quiz(username, None, difficult_count)
        
        # Combine and shuffle
        selected_questions = sr_questions + difficult_questions
        
        # Remove duplicates while preserving order
        seen = set()
        unique_questions = []
        for q in selected_questions:
            if q.get_id() not in seen:
                unique_questions.append(q)
                seen.add(q.get_id())
        
        # Fill to max_questions if needed
        if len(unique_questions) < max_questions:
            remaining = [q for q in all_questions if q.get_id() not in seen]
            needed = max_questions - len(unique_questions)
            if remaining:
                additional = random.sample(remaining, min(needed, len(remaining)))
                unique_questions.extend(additional)
        
        random.shuffle(unique_questions)
        return unique_questions[:max_questions]