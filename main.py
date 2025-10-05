#!/usr/bin/python3

"""
Mini Quiz App - Enhanced Version
Features:
- Multiple quiz topics
- Timer functionality
- Score tracking across sessions
    print(f"{Colors.GREEN}4.{Colors.END} 🔄 Mixed Review")
    print(f"{Colors.GREEN}5.{Colors.END} 📊 View My Statistics")
    print(f"{Colors.GREEN}6.{Colors.END} 🏆 View Leaderboard")
    print(f"{Colors.GREEN}7.{Colors.END} 📈 Learning Progress")
    print(f"{Colors.GREEN}8.{Colors.END} 🔍 Error Analysis")
    print(f"{Colors.GREEN}9.{Colors.END} ❌ Exit")terface
- Statistics and leaderboard
"""

import json
import os
import glob
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

from Question import Question
from Quiz import Quiz
from ScoreTracker import ScoreTracker
from QuizLoader import QuizLoader
from SpacedRepetition import SpacedRepetitionManager
from ErrorAnalyzer import ErrorAnalyzer


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def print_animated_text(text: str, delay: float = 0.05):
    """Print text with typing animation effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def print_header(title: str):
    """Print a fancy header."""
    clear_screen()
    print(Colors.CYAN + "=" * 60 + Colors.END)
    print(Colors.BOLD + Colors.HEADER + f"🎓 {title.center(50)} 🎓" + Colors.END)
    print(Colors.CYAN + "=" * 60 + Colors.END)
    print()


def load_quiz_from_json(filename: str) -> Dict[str, Any]:
    """Load quiz data from a JSON file."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{Colors.RED}Error: Could not find file {filename}{Colors.END}")
        return {}
    except json.JSONDecodeError:
        print(f"{Colors.RED}Error: Invalid JSON format in {filename}{Colors.END}")
        return {}


def get_available_quizzes() -> List[Dict[str, str]]:
    """Get list of available quiz files."""
    quiz_files = glob.glob("db/*.json")
    quizzes = []
    
    for file_path in quiz_files:
        quiz_data = load_quiz_from_json(file_path)
        if quiz_data:
            # Handle both old format (list) and new format (dict)
            if isinstance(quiz_data, list):
                # Old format - infer title from filename
                filename = os.path.basename(file_path)
                title = filename.replace('.json', '').replace('_', ' ').title()
                quizzes.append({
                    'file': file_path,
                    'title': title,
                    'description': f"Quiz with {len(quiz_data)} questions",
                    'duration': 0
                })
            else:
                # New format - use metadata
                quizzes.append({
                    'file': file_path,
                    'title': quiz_data.get('title', 'Unknown Quiz'),
                    'description': quiz_data.get('description', 'No description'),
                    'duration': quiz_data.get('duration', 0)
                })
    
    return quizzes


def display_quiz_menu(quizzes: List[Dict[str, str]]) -> int:
    """Display quiz selection menu and return user choice."""
    print(Colors.BOLD + "📚 Available Quiz Topics:" + Colors.END)
    print(Colors.BLUE + "-" * 40 + Colors.END)
    
    for i, quiz in enumerate(quizzes, 1):
        duration = quiz.get('duration', 0)
        duration_text = f"({duration//60}min)" if isinstance(duration, int) and duration > 0 else "(No time limit)"
        print(f"{Colors.GREEN}{i}.{Colors.END} {Colors.BOLD}{quiz['title']}{Colors.END} {Colors.YELLOW}{duration_text}{Colors.END}")
        print(f"   {quiz['description']}")
        print()
    
    while True:
        try:
            choice = int(input(f"{Colors.CYAN}Choose a quiz (1-{len(quizzes)}): {Colors.END}"))
            if 1 <= choice <= len(quizzes):
                return choice - 1
            else:
                print(f"{Colors.RED}Please enter a number between 1 and {len(quizzes)}{Colors.END}")
        except ValueError:
            print(f"{Colors.RED}Please enter a valid number!{Colors.END}")


def create_questions_from_data(quiz_data: Any) -> List[Question]:
    """Create Question objects from JSON data."""
    questions = []
    
    # Handle both old format (list) and new format (dict)
    if isinstance(quiz_data, list):
        questions_data = quiz_data
    else:
        questions_data = quiz_data.get('questions', [])
    
    for item in questions_data:
        if isinstance(item, dict):
            question = Question(
                item.get('question', ''),
                item.get('answers', []),
                item.get('answer', 1),
                item.get('hints', {})
            )
            questions.append(question)
    return questions


def display_main_menu() -> int:
    """Display main menu and return user choice."""
    print(Colors.BOLD + "🎯 MAIN MENU" + Colors.END)
    print(Colors.BLUE + "-" * 20 + Colors.END)
    print(f"{Colors.GREEN}1.{Colors.END} 🎮 Take a Regular Quiz")
    print(f"{Colors.GREEN}2.{Colors.END} 🧠 Smart Review (Spaced Repetition)")
    print(f"{Colors.GREEN}3.{Colors.END} 🎯 Focus on Mistakes")
    print(f"{Colors.GREEN}4.{Colors.END} 🔄 Mixed Review")
    print(f"{Colors.GREEN}5.{Colors.END} 📊 View My Statistics")
    print(f"{Colors.GREEN}6.{Colors.END} 🏆 View Leaderboard")
    print(f"{Colors.GREEN}7.{Colors.END} 📈 Learning Progress")
    print(f"{Colors.GREEN}8.{Colors.END} 🔍 Error Analysis")
    print(f"{Colors.GREEN}9.{Colors.END} ❌ Exit")
    print()
    
    while True:
        try:
            choice = int(input(f"{Colors.CYAN}Choose an option (1-9): {Colors.END}"))
            if 1 <= choice <= 9:
                return choice
            else:
                print(f"{Colors.RED}Please enter a number between 1 and 9{Colors.END}")
        except ValueError:
            print(f"{Colors.RED}Please enter a valid number!{Colors.END}")


def get_user_name() -> str:
    """Get and validate user name."""
    while True:
        name = input(f"{Colors.CYAN}What's your name? {Colors.END}").strip()
        if name:
            return name
        print(f"{Colors.RED}Please enter a valid name!{Colors.END}")


def display_topic_selection(quiz_loader: QuizLoader) -> Optional[str]:
    """Display topic selection and return selected file path."""
    topics = quiz_loader.get_available_topics()
    
    if not topics:
        print(f"{Colors.RED}No quiz topics found!{Colors.END}")
        return None
    
    print(Colors.BOLD + "📚 Available Topics:" + Colors.END)
    print(Colors.BLUE + "-" * 30 + Colors.END)
    
    for i, (topic_name, file_path) in enumerate(topics, 1):
        print(f"{Colors.GREEN}{i}.{Colors.END} {Colors.BOLD}{topic_name}{Colors.END}")
    
    print()
    
    while True:
        try:
            choice = int(input(f"{Colors.CYAN}Choose a topic (1-{len(topics)}): {Colors.END}"))
            if 1 <= choice <= len(topics):
                return topics[choice - 1][1]  # Return file path
            else:
                print(f"{Colors.RED}Please enter a number between 1 and {len(topics)}{Colors.END}")
        except ValueError:
            print(f"{Colors.RED}Please enter a valid number!{Colors.END}")


def run_quiz_with_questions(questions: List[Question], user_name: str, quiz_title: str, 
                           use_spaced_repetition: bool = False) -> Optional[Dict[str, Any]]:
    """Run a quiz with the given questions."""
    if not questions:
        print(f"{Colors.RED}No questions available for this quiz!{Colors.END}")
        return None
    
    print_header(f"QUIZ: {quiz_title}")
    print(f"{Colors.BOLD}Hello {user_name}! Get ready for the quiz!{Colors.END}")
    print(f"{Colors.YELLOW}Questions: {len(questions)}{Colors.END}")
    
    if use_spaced_repetition:
        print(f"{Colors.CYAN}🧠 Using Smart Spaced Repetition Algorithm{Colors.END}")
    
    print()
    input(f"{Colors.GREEN}Press Enter to start...{Colors.END}")
    
    # Create and start quiz
    quiz = Quiz(user_name, quiz_title, 0, use_spaced_repetition)
    result = quiz.start_quiz(questions)
    
    return result


def display_spaced_repetition_stats(username: str):
    """Display spaced repetition learning statistics."""
    spaced_rep = SpacedRepetitionManager()
    stats = spaced_rep.get_user_statistics(username)
    
    print(Colors.BOLD + f"🧠 Learning Progress for {username}" + Colors.END)
    print(Colors.BLUE + "=" * 50 + Colors.END)
    
    if stats['total_questions'] == 0:
        print(f"{Colors.YELLOW}No learning data yet. Take some Smart Review quizzes to see your progress!{Colors.END}")
        return
    
    print(f"{Colors.GREEN}📊 Total Questions Studied: {Colors.BOLD}{stats['total_questions']}{Colors.END}")
    print(f"{Colors.GREEN}🎯 Questions Mastered: {Colors.BOLD}{stats['questions_mastered']}{Colors.END}")
    print(f"{Colors.YELLOW}📚 Questions Learning: {Colors.BOLD}{stats['questions_learning']}{Colors.END}")
    print(f"{Colors.RED}🔄 Difficult Questions: {Colors.BOLD}{stats['questions_difficult']}{Colors.END}")
    print(f"{Colors.CYAN}⚡ Average Ease Factor: {Colors.BOLD}{stats['average_ease']}{Colors.END}")
    print(f"{Colors.BLUE}🔁 Total Reviews: {Colors.BOLD}{stats['total_reviews']}{Colors.END}")
    
    # Show review schedule for next 7 days
    schedule = spaced_rep.get_review_schedule(username, 7)
    print(f"\n{Colors.BOLD}📅 Upcoming Reviews:{Colors.END}")
    
    has_reviews = False
    for date_str, question_ids in schedule.items():
        if question_ids:
            has_reviews = True
            date_obj = datetime.fromisoformat(date_str + "T00:00:00")
            day_name = date_obj.strftime("%A")
            print(f"{Colors.GREEN}{day_name} ({date_str}): {len(question_ids)} questions{Colors.END}")
    
    if not has_reviews:
        print(f"{Colors.YELLOW}No reviews scheduled for the next 7 days.{Colors.END}")
    
    print(f"\n{Colors.CYAN}💡 Tip: Questions you answer correctly will appear less frequently,")
    print(f"while difficult questions will be reviewed more often!{Colors.END}")


def display_error_analysis(username: str):
    """Display comprehensive error analysis for a user."""
    error_analyzer = ErrorAnalyzer()
    analysis = error_analyzer.get_user_error_summary(username)
    
    print(Colors.BOLD + f"🔍 Error Analysis for {username}" + Colors.END)
    print(Colors.BLUE + "=" * 60 + Colors.END)
    
    if analysis['total_questions_attempted'] == 0:
        print(f"{Colors.YELLOW}No quiz data found. Take some quizzes first to see your error analysis!{Colors.END}")
        return
    
    # Overall statistics
    print(f"{Colors.GREEN}📊 Overall Performance:{Colors.END}")
    print(f"   Questions Attempted: {Colors.BOLD}{analysis['total_questions_attempted']}{Colors.END}")
    print(f"   Total Attempts: {Colors.BOLD}{analysis['total_attempts']}{Colors.END}")
    print(f"   Total Errors: {Colors.BOLD}{analysis['total_errors']}{Colors.END}")
    print(f"   Error Rate: {Colors.BOLD}{analysis['error_rate']}%{Colors.END}")
    
    # Error rate color coding
    if analysis['error_rate'] > 40:
        error_color = Colors.RED
    elif analysis['error_rate'] > 20:
        error_color = Colors.YELLOW
    else:
        error_color = Colors.GREEN
    
    print(f"   Performance: {error_color}", end="")
    if analysis['error_rate'] < 15:
        print("Excellent! 🌟")
    elif analysis['error_rate'] < 30:
        print("Good 👍")
    elif analysis['error_rate'] < 50:
        print("Needs Improvement 📚")
    else:
        print("Requires Focus 🎯")
    print(Colors.END)
    
    # Most difficult questions
    if analysis['most_difficult_questions']:
        print(f"\n{Colors.RED}🎯 Most Challenging Questions:{Colors.END}")
        print(f"   {'Rank':<4} {'Success Rate':<12} {'Attempts':<8} {'Difficulty':<10}")
        print(f"   {'-'*4} {'-'*12} {'-'*8} {'-'*10}")
        
        for i, q in enumerate(analysis['most_difficult_questions'][:5], 1):
            success_color = Colors.RED if q['success_rate'] < 30 else Colors.YELLOW if q['success_rate'] < 60 else Colors.GREEN
            print(f"   {i:<4} {success_color}{q['success_rate']:<12.1f}%{Colors.END} "
                  f"{q['attempts']:<8} {q['difficulty_score']:<10.1f}")
    
    # Error patterns
    patterns = analysis['error_patterns']
    print(f"\n{Colors.BLUE}📈 Learning Patterns:{Colors.END}")
    print(f"   🎓 Mastered Questions: {Colors.GREEN}{patterns['questions_mastered']}{Colors.END}")
    print(f"   📚 Learning Questions: {Colors.YELLOW}{patterns['questions_learning']}{Colors.END}")
    print(f"   🔄 Struggling Questions: {Colors.RED}{patterns['questions_struggling']}{Colors.END}")
    print(f"   ⏱️  Average Response Time: {Colors.CYAN}{patterns['avg_response_time']} seconds{Colors.END}")
    
    # Slow questions
    if patterns['slow_questions']:
        print(f"\n{Colors.YELLOW}⏰ Questions Taking Too Long:{Colors.END}")
        for q in patterns['slow_questions'][:3]:
            print(f"   Question ID: {q['question_id']} - {q['avg_time']} seconds average")
    
    # Improvement suggestions
    print(f"\n{Colors.CYAN}💡 Personalized Recommendations:{Colors.END}")
    for i, suggestion in enumerate(analysis['improvement_suggestions'], 1):
        print(f"   {i}. {suggestion}")
    
    # Progress recommendations
    progress_recs = error_analyzer.get_progress_recommendations(username)
    if progress_recs:
        print(f"\n{Colors.GREEN}🚀 Next Steps:{Colors.END}")
        for i, rec in enumerate(progress_recs[:3], 1):
            print(f"   {i}. {rec}")
    
    # Learning consistency
    streak_info = error_analyzer.get_learning_streak(username)
    print(f"\n{Colors.BOLD}📊 Learning Consistency: {streak_info['consistency']}{Colors.END}")
    print(f"   Average Repetitions per Question: {streak_info['avg_repetitions']}")
    print(f"   Total Learning Sessions: {streak_info['total_attempts']}")


def main():
    """Main application function."""
    score_tracker = ScoreTracker()
    quiz_loader = QuizLoader()
    
    while True:
        print_header("MINI QUIZ APP")
        
        print_animated_text("Welcome to the Enhanced Mini Quiz App! 🚀", 0.03)
        print()
        
        choice = display_main_menu()
        
        if choice == 1:  # Take a Regular Quiz
            print_header("REGULAR QUIZ")
            
            # Get available quizzes
            quizzes = get_available_quizzes()
            
            if not quizzes:
                print(f"{Colors.RED}No quiz files found in the db/ directory!{Colors.END}")
                input(f"{Colors.CYAN}Press Enter to continue...{Colors.END}")
                continue
            
            # Select quiz
            quiz_index = display_quiz_menu(quizzes)
            selected_quiz = quizzes[quiz_index]
            
            # Load quiz data
            quiz_data = load_quiz_from_json(selected_quiz['file'])
            if not quiz_data:
                continue
            
            # Get user name
            print()
            user_name = get_user_name()
            
            # Create questions
            questions = create_questions_from_data(quiz_data)
            
            # Run the quiz
            quiz_title = quiz_data.get('title', selected_quiz['title'])
            result = run_quiz_with_questions(questions, user_name, quiz_title, False)
            
            # Save result to history
            if result:
                score_tracker.add_score(result)
            
            input(f"{Colors.CYAN}\\nPress Enter to continue...{Colors.END}")
        
        elif choice == 2:  # Smart Review (Spaced Repetition)
            print_header("SMART REVIEW - SPACED REPETITION")
            
            user_name = get_user_name()
            
            print(f"{Colors.CYAN}🧠 Smart Review uses spaced repetition to help you master topics efficiently!{Colors.END}")
            print(f"{Colors.YELLOW}Questions you struggle with will appear more frequently.{Colors.END}")
            print()
            
            # Select topic
            file_path = display_topic_selection(quiz_loader)
            if not file_path:
                input(f"{Colors.CYAN}Press Enter to continue...{Colors.END}")
                continue
            
            # Get questions using spaced repetition
            questions = quiz_loader.get_spaced_repetition_quiz(user_name, file_path, 10)
            
            if not questions:
                print(f"{Colors.YELLOW}No questions available for review right now. Try taking a regular quiz first!{Colors.END}")
                input(f"{Colors.CYAN}Press Enter to continue...{Colors.END}")
                continue
            
            topic_name = file_path.split('/')[-1].replace('.json', '').replace('_', ' ').title()
            result = run_quiz_with_questions(questions, user_name, f"Smart Review: {topic_name}", True)
            
            if result:
                score_tracker.add_score(result)
                print(f"\n{Colors.GREEN}✨ Your learning progress has been updated!{Colors.END}")
            
            input(f"{Colors.CYAN}\\nPress Enter to continue...{Colors.END}")
        
        elif choice == 3:  # Focus on Mistakes
            print_header("FOCUS ON MISTAKES")
            
            user_name = get_user_name()
            
            print(f"{Colors.RED}🎯 This mode focuses on questions you find most difficult!{Colors.END}")
            print(f"{Colors.YELLOW}Practice your weak areas to improve faster.{Colors.END}")
            print()
            
            print("Choose your focus:")
            print(f"{Colors.GREEN}1.{Colors.END} Focus on mistakes from a specific topic")
            print(f"{Colors.GREEN}2.{Colors.END} Focus on mistakes from all topics")
            print()
            
            while True:
                try:
                    focus_choice = int(input(f"{Colors.CYAN}Choose (1-2): {Colors.END}"))
                    if focus_choice in [1, 2]:
                        break
                    print(f"{Colors.RED}Please enter 1 or 2{Colors.END}")
                except ValueError:
                    print(f"{Colors.RED}Please enter a valid number!{Colors.END}")
            
            if focus_choice == 1:
                file_path = display_topic_selection(quiz_loader)
                if not file_path:
                    input(f"{Colors.CYAN}Press Enter to continue...{Colors.END}")
                    continue
                questions = quiz_loader.get_difficult_questions_quiz(user_name, file_path, 10)
                topic_name = file_path.split('/')[-1].replace('.json', '').replace('_', ' ').title()
                quiz_title = f"Mistake Focus: {topic_name}"
            else:
                questions = quiz_loader.get_difficult_questions_quiz(user_name, None, 15)
                quiz_title = "Mistake Focus: All Topics"
            
            if not questions:
                print(f"{Colors.YELLOW}No difficult questions found. Take some quizzes first to identify your weak areas!{Colors.END}")
                input(f"{Colors.CYAN}Press Enter to continue...{Colors.END}")
                continue
            
            result = run_quiz_with_questions(questions, user_name, quiz_title, True)
            
            if result:
                score_tracker.add_score(result)
                print(f"\n{Colors.GREEN}🎯 Keep practicing to master these challenging topics!{Colors.END}")
            
            input(f"{Colors.CYAN}\\nPress Enter to continue...{Colors.END}")
        
        elif choice == 4:  # Mixed Review
            print_header("MIXED REVIEW")
            
            user_name = get_user_name()
            
            print(f"{Colors.BLUE}🔄 Mixed Review combines spaced repetition with mistake focus!{Colors.END}")
            print(f"{Colors.YELLOW}This gives you a comprehensive review across all topics.{Colors.END}")
            print()
            
            questions = quiz_loader.get_mixed_review_quiz(user_name, 15)
            
            if not questions:
                print(f"{Colors.YELLOW}No questions available for mixed review. Take some regular quizzes first!{Colors.END}")
                input(f"{Colors.CYAN}Press Enter to continue...{Colors.END}")
                continue
            
            result = run_quiz_with_questions(questions, user_name, "Mixed Review: All Topics", True)
            
            if result:
                score_tracker.add_score(result)
                print(f"\n{Colors.GREEN}🌟 Great job on your comprehensive review!{Colors.END}")
            
            input(f"{Colors.CYAN}\\nPress Enter to continue...{Colors.END}")
        
        elif choice == 5:  # View Statistics
            print_header("USER STATISTICS")
            name = get_user_name()
            score_tracker.display_user_stats(name)
            input(f"{Colors.CYAN}Press Enter to continue...{Colors.END}")
        
        elif choice == 6:  # View Leaderboard
            print_header("LEADERBOARD")
            score_tracker.display_leaderboard()
            input(f"{Colors.CYAN}Press Enter to continue...{Colors.END}")
        
        elif choice == 7:  # Learning Progress
            print_header("LEARNING PROGRESS")
            name = get_user_name()
            display_spaced_repetition_stats(name)
            input(f"{Colors.CYAN}Press Enter to continue...{Colors.END}")
        
        elif choice == 8:  # Error Analysis
            print_header("ERROR ANALYSIS")
            name = get_user_name()
            display_error_analysis(name)
            input(f"{Colors.CYAN}Press Enter to continue...{Colors.END}")
        
        elif choice == 9:  # Exit
            print_header("GOODBYE!")
            print_animated_text("Thank you for using the Mini Quiz App! 👋", 0.03)
            print_animated_text("Keep learning and have fun! 🎓✨", 0.03)
            break


if __name__ == "__main__":
    main()
