import time
import hashlib


class Question:
    def __init__(self, question: str, answers: list[str], correct_answer: int, hints: dict[str, str], topic: str = "") -> None:
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer
        self.hints = hints
        self.topic = topic
        self.response_start_time = None
        self.response_time = 0
        
    def get_id(self) -> str:
        """Generate unique ID for this question based on content and topic."""
        content = f"{self.topic}:{self.question}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def ask(self) -> None:
        print(f"\n📝 {self.question}")
        print("-" * 30)
        for answer in self.answers:
            print(f"   {answer}")
        print()
        # Start timing the response
        self.response_start_time = time.time()
    
    def check_user_answer(self, user_input: int) -> bool:
        # Calculate response time
        if self.response_start_time:
            self.response_time = time.time() - self.response_start_time
        return user_input == self.correct_answer
    
    def get_response_time(self) -> float:
        """Get the time taken to answer this question in seconds."""
        return self.response_time

