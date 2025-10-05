import json
import os
from datetime import datetime
from typing import List, Dict, Any


class ScoreTracker:
    def __init__(self, history_file: str = "score_history.json"):
        self.history_file = history_file
        self.history = self.load_history()
    
    def load_history(self) -> List[Dict[str, Any]]:
        """Load score history from JSON file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as file:
                    return json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_history(self) -> None:
        """Save score history to JSON file."""
        try:
            with open(self.history_file, 'w') as file:
                json.dump(self.history, file, indent=2)
        except Exception as e:
            print(f"Error saving score history: {e}")
    
    def add_score(self, quiz_result: Dict[str, Any]) -> None:
        """Add a new quiz result to the history."""
        self.history.append(quiz_result)
        self.save_history()
    
    def get_user_stats(self, username: str) -> Dict[str, Any]:
        """Get statistics for a specific user."""
        user_scores = [score for score in self.history if score['user_name'].lower() == username.lower()]
        
        if not user_scores:
            return {
                'total_quizzes': 0,
                'average_score': 0,
                'best_score': 0,
                'total_time': 0,
                'favorite_topic': 'None'
            }
        
        total_quizzes = len(user_scores)
        average_score = sum(score['percentage'] for score in user_scores) / total_quizzes
        best_score = max(score['percentage'] for score in user_scores)
        total_time = sum(score['time_taken'] for score in user_scores)
        
        # Find favorite topic (most attempted)
        topics = {}
        for score in user_scores:
            topic = score['quiz_title']
            topics[topic] = topics.get(topic, 0) + 1
        
        favorite_topic = max(topics.items(), key=lambda x: x[1])[0] if topics else 'None'
        
        return {
            'total_quizzes': total_quizzes,
            'average_score': round(average_score, 1),
            'best_score': round(best_score, 1),
            'total_time': total_time,
            'favorite_topic': favorite_topic,
            'recent_scores': user_scores[-5:]  # Last 5 attempts
        }
    
    def display_user_stats(self, username: str) -> None:
        """Display formatted statistics for a user."""
        stats = self.get_user_stats(username)
        
        print("\n" + "=" * 50)
        print(f"📊 STATISTICS FOR {username.upper()}")
        print("=" * 50)
        
        if stats['total_quizzes'] == 0:
            print("No quiz history found for this user.")
            return
        
        print(f"🎯 Total Quizzes Taken: {stats['total_quizzes']}")
        print(f"📈 Average Score: {stats['average_score']:.1f}%")
        print(f"🏆 Best Score: {stats['best_score']:.1f}%")
        print(f"⏱️  Total Time Spent: {self.format_time(stats['total_time'])}")
        print(f"❤️  Favorite Topic: {stats['favorite_topic']}")
        
        if stats['recent_scores']:
            print(f"\n📝 Recent Quiz Results:")
            for i, score in enumerate(stats['recent_scores'], 1):
                date_str = datetime.fromisoformat(score['date']).strftime("%Y-%m-%d %H:%M")
                print(f"  {i}. {score['quiz_title']}: {score['percentage']:.1f}% ({date_str})")
        
        print("=" * 50)
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performers across all users."""
        if not self.history:
            return []
        
        # Group by user and get their best scores
        user_best = {}
        for score in self.history:
            username = score['user_name'].lower()
            if username not in user_best or score['percentage'] > user_best[username]['percentage']:
                user_best[username] = score
        
        # Sort by percentage and return top performers
        leaderboard = sorted(user_best.values(), key=lambda x: x['percentage'], reverse=True)
        return leaderboard[:limit]
    
    def display_leaderboard(self, limit: int = 10) -> None:
        """Display the leaderboard."""
        leaderboard = self.get_leaderboard(limit)
        
        print("\n" + "=" * 50)
        print("🏆 LEADERBOARD - TOP PERFORMERS")
        print("=" * 50)
        
        if not leaderboard:
            print("No scores recorded yet!")
            return
        
        for i, score in enumerate(leaderboard, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            print(f"{medal} {score['user_name']}: {score['percentage']:.1f}% ({score['quiz_title']})")
        
        print("=" * 50)
    
    def format_time(self, seconds: int) -> str:
        """Format seconds into a readable time string."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"