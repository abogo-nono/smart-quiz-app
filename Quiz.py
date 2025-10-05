
import time
import threading
from datetime import datetime
from Question import Question
from SpacedRepetition import SpacedRepetitionManager


class Quiz:
    def __init__(self, name: str, title: str, duration: int = 0, use_spaced_repetition: bool = False) -> None:
        self.user_name = name
        self.quiz_title = title
        self.score = 0
        self.quiz = []
        self.duration = duration  # Duration in seconds (0 = no time limit)
        self.start_time = None
        self.time_up = False
        self.timer_thread = None
        self.use_spaced_repetition = use_spaced_repetition
        self.spaced_rep_manager = SpacedRepetitionManager() if use_spaced_repetition else None
        self.question_results = []  # Track individual question results

    def timer_countdown(self) -> None:
        """Background timer that sets time_up flag when duration expires."""
        if self.duration > 0:
            time.sleep(self.duration)
            self.time_up = True
            print(f"\n⏰ TIME'S UP! Quiz ended automatically.")

    def get_elapsed_time(self) -> int:
        """Get elapsed time in seconds since quiz started."""
        if self.start_time:
            return int(time.time() - self.start_time)
        return 0

    def get_remaining_time(self) -> int:
        """Get remaining time in seconds."""
        if self.duration > 0:
            elapsed = self.get_elapsed_time()
            return max(0, self.duration - elapsed)
        return 0

    def format_time(self, seconds: int) -> str:
        """Format seconds into MM:SS format."""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def start_quiz(self, questions: list[Question]) -> dict:
        self.quiz = questions
        self.start_time = time.time()
        
        # Start timer if duration is set
        if self.duration > 0:
            print(f"⏱️  Quiz Duration: {self.format_time(self.duration)}")
            print("=" * 50)
            self.timer_thread = threading.Thread(target=self.timer_countdown)
            self.timer_thread.daemon = True
            self.timer_thread.start()

        for i, question in enumerate(self.quiz, 1):
            if self.time_up:
                print(f"\n⏰ Quiz ended due to time limit!")
                break
                
            # Show progress and time info
            remaining = self.get_remaining_time()
            if self.duration > 0:
                print(f"Question {i}/{len(self.quiz)} | Time Remaining: {self.format_time(remaining)}")
                
                # Warning when time is running low
                if remaining <= 60 and remaining > 0:
                    print("⚠️  Less than 1 minute remaining!")
            else:
                print(f"Question {i}/{len(self.quiz)}")
            
            question.ask()
            
            while True:
                if self.time_up:
                    print("Time's up! Moving to results...")
                    break
                    
                try:
                    user_answer = int(input('What is the correct answer? '))
                    break
                except ValueError:
                    print("Please enter a valid number!")
            
            # Check if answer is correct
            is_correct = False
            if not self.time_up:
                is_correct = question.check_user_answer(user_answer)
                
                if is_correct:
                    print(f"✅ {question.hints['correct']}")
                    self.score += 1
                else:
                    print(f"❌ {question.hints['fail']}")
                
                # Update spaced repetition data
                if self.use_spaced_repetition and self.spaced_rep_manager:
                    self.spaced_rep_manager.update_question_performance(
                        question.get_id(), 
                        self.user_name, 
                        is_correct, 
                        question.get_response_time()
                    )
                
                # Store individual question result
                self.question_results.append({
                    'question_id': question.get_id(),
                    'question_text': question.question,
                    'user_answer': user_answer,
                    'correct_answer': question.correct_answer,
                    'is_correct': is_correct,
                    'response_time': question.get_response_time(),
                    'topic': question.topic
                })
            
            if not self.time_up:
                print("-" * 50)

        return self.end_quiz()

    def end_quiz(self) -> dict:
        elapsed_time = self.get_elapsed_time()
        
        print("\n" + "=" * 50)
        print("           QUIZ COMPLETED!")
        print("=" * 50)
        
        percentage = (self.score / len(self.quiz)) * 100 if len(self.quiz) > 0 else 0
        
        print(f"\nHello {self.user_name}!")
        print(f"Quiz: {self.quiz_title}")
        print(f"Your Score: {self.score} / {len(self.quiz)} ({percentage:.1f}%)")
        print(f"Time Taken: {self.format_time(elapsed_time)}")
        
        if self.time_up:
            print("⏰ Quiz ended due to time limit")
        
        if percentage >= 80:
            print("🎉 Excellent work! You're a star!")
        elif percentage >= 60:
            print("👍 Good job! Keep it up!")
        elif percentage >= 40:
            print("📚 Not bad, but there's room for improvement!")
        else:
            print("💪 Don't give up! Practice makes perfect!")
        
        print("\nThank you for taking the quiz!")
        print("=" * 50)
        
        return {
            'user_name': self.user_name,
            'quiz_title': self.quiz_title,
            'score': self.score,
            'total_questions': len(self.quiz),
            'percentage': percentage,
            'time_taken': elapsed_time,
            'date': datetime.now().isoformat(),
            'time_up': self.time_up,
            'question_results': self.question_results,
            'used_spaced_repetition': self.use_spaced_repetition
        }
