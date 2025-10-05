from typing import Dict, List, Any, Optional
from SpacedRepetition import SpacedRepetitionManager


class ErrorAnalyzer:
    """
    Analyzes user errors and provides insights for focused learning.
    Integrates with SpacedRepetition for comprehensive error tracking.
    """
    
    def __init__(self, spaced_rep_manager: Optional[SpacedRepetitionManager] = None):
        self.spaced_rep_manager = spaced_rep_manager or SpacedRepetitionManager()
    
    def get_user_error_summary(self, username: str) -> Dict[str, Any]:
        """Get comprehensive error analysis for a user."""
        user_data = {}
        
        # Filter data for the specific user
        for key, data in self.spaced_rep_manager.question_data.items():
            if key.startswith(f"{username}:"):
                question_id = key.split(':', 1)[1]
                user_data[question_id] = data
        
        if not user_data:
            return {
                'total_questions_attempted': 0,
                'total_errors': 0,
                'error_rate': 0,
                'most_difficult_questions': [],
                'topics_with_most_errors': [],
                'improvement_suggestions': []
            }
        
        # Calculate basic statistics
        total_attempts = sum(data['total_attempts'] for data in user_data.values())
        total_errors = sum(data['total_attempts'] - data['correct_attempts'] 
                          for data in user_data.values())
        error_rate = (total_errors / total_attempts * 100) if total_attempts > 0 else 0
        
        # Find most difficult questions
        difficult_questions = []
        for question_id, data in user_data.items():
            if data['total_attempts'] >= 2:  # Only consider questions attempted multiple times
                success_rate = data['correct_attempts'] / data['total_attempts']
                difficulty_score = (1 - success_rate) * 100 + (3.0 - data['ease_factor']) * 20
                
                if success_rate < 0.7:  # Less than 70% success rate
                    difficult_questions.append({
                        'question_id': question_id,
                        'success_rate': round(success_rate * 100, 1),
                        'attempts': data['total_attempts'],
                        'difficulty_score': round(difficulty_score, 1),
                        'ease_factor': round(data['ease_factor'], 2)
                    })
        
        # Sort by difficulty score (highest first)
        difficult_questions.sort(key=lambda x: x['difficulty_score'], reverse=True)
        
        # Analyze topics with most errors (this would need topic mapping)
        # For now, we'll use a simplified approach
        error_patterns = self._analyze_error_patterns(user_data)
        
        return {
            'total_questions_attempted': len(user_data),
            'total_attempts': total_attempts,
            'total_errors': total_errors,
            'error_rate': round(error_rate, 1),
            'most_difficult_questions': difficult_questions[:10],
            'error_patterns': error_patterns,
            'improvement_suggestions': self._generate_improvement_suggestions(
                error_rate, difficult_questions, user_data
            )
        }
    
    def _analyze_error_patterns(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze patterns in user errors."""
        patterns = {
            'questions_mastered': 0,
            'questions_struggling': 0,
            'questions_learning': 0,
            'avg_response_time': 0,
            'slow_questions': []
        }
        
        total_response_time = 0
        response_count = 0
        
        for question_id, data in user_data.items():
            success_rate = data['correct_attempts'] / max(1, data['total_attempts'])
            
            if success_rate >= 0.8 and data['repetition'] >= 3:
                patterns['questions_mastered'] += 1
            elif success_rate < 0.5:
                patterns['questions_struggling'] += 1
            else:
                patterns['questions_learning'] += 1
            
            # Track response times
            if data['avg_response_time'] > 0:
                total_response_time += data['avg_response_time']
                response_count += 1
                
                # Questions that take too long (>20 seconds average)
                if data['avg_response_time'] > 20:
                    patterns['slow_questions'].append({
                        'question_id': question_id,
                        'avg_time': round(data['avg_response_time'], 1),
                        'attempts': data['total_attempts']
                    })
        
        patterns['avg_response_time'] = round(
            total_response_time / max(1, response_count), 1
        )
        patterns['slow_questions'].sort(key=lambda x: x['avg_time'], reverse=True)
        patterns['slow_questions'] = patterns['slow_questions'][:5]
        
        return patterns
    
    def _generate_improvement_suggestions(self, error_rate: float, 
                                        difficult_questions: List[Dict], 
                                        user_data: Dict[str, Any]) -> List[str]:
        """Generate personalized improvement suggestions."""
        suggestions = []
        
        if error_rate > 50:
            suggestions.append("📚 Your error rate is quite high. Consider reviewing basic concepts before attempting quizzes.")
        elif error_rate > 30:
            suggestions.append("🎯 Focus on your weak areas using the 'Focus on Mistakes' mode.")
        elif error_rate > 15:
            suggestions.append("✨ You're doing well! Use 'Smart Review' to reinforce your learning.")
        else:
            suggestions.append("🌟 Excellent performance! Try 'Mixed Review' to maintain your knowledge.")
        
        if len(difficult_questions) > 5:
            suggestions.append(f"🔍 You have {len(difficult_questions)} challenging questions. "
                             "Use spaced repetition to gradually master them.")
        
        # Check response times
        avg_times = [data['avg_response_time'] for data in user_data.values() 
                    if data['avg_response_time'] > 0]
        if avg_times:
            avg_time = sum(avg_times) / len(avg_times)
            if avg_time > 15:
                suggestions.append("⏱️ Try to improve your response time by reviewing concepts more frequently.")
            elif avg_time < 5:
                suggestions.append("🚀 Great response times! You might be ready for more advanced topics.")
        
        # Check for consistent patterns
        very_easy_questions = sum(1 for data in user_data.values() 
                                 if data['ease_factor'] > 2.8 and data['repetition'] >= 2)
        
        if very_easy_questions > len(user_data) * 0.7:
            suggestions.append("🎓 You've mastered most questions! Consider exploring new topics.")
        
        return suggestions[:4]  # Limit to 4 suggestions
    
    def get_topic_error_analysis(self, username: str) -> Dict[str, Any]:
        """
        Analyze errors by topic. 
        Note: This requires topic information to be stored with questions.
        """
        # This is a placeholder for topic-based analysis
        # In a full implementation, you'd need to track which topic each question belongs to
        
        user_error_summary = self.get_user_error_summary(username)
        
        return {
            'message': 'Topic-based analysis requires question-topic mapping',
            'total_errors': user_error_summary['total_errors'],
            'suggestions': user_error_summary['improvement_suggestions']
        }
    
    def get_learning_streak(self, username: str) -> Dict[str, Any]:
        """Calculate learning streaks and consistency."""
        # This would require tracking daily quiz activity
        # For now, return basic consistency metrics
        
        user_data = {}
        for key, data in self.spaced_rep_manager.question_data.items():
            if key.startswith(f"{username}:"):
                user_data[key] = data
        
        if not user_data:
            return {'streak': 0, 'consistency': 'No data'}
        
        # Calculate a simple consistency score based on repetition levels
        total_repetitions = sum(data['repetition'] for data in user_data.values())
        avg_repetitions = total_repetitions / len(user_data)
        
        if avg_repetitions >= 3:
            consistency = 'Excellent'
        elif avg_repetitions >= 2:
            consistency = 'Good'
        elif avg_repetitions >= 1:
            consistency = 'Fair'
        else:
            consistency = 'Needs Improvement'
        
        return {
            'total_questions': len(user_data),
            'avg_repetitions': round(avg_repetitions, 1),
            'consistency': consistency,
            'total_attempts': sum(data['total_attempts'] for data in user_data.values())
        }
    
    def get_progress_recommendations(self, username: str) -> List[str]:
        """Get specific recommendations for user progress."""
        error_summary = self.get_user_error_summary(username)
        recommendations = []
        
        if error_summary['total_questions_attempted'] == 0:
            return ["🚀 Start with a regular quiz to establish your baseline performance!"]
        
        if error_summary['error_rate'] > 40:
            recommendations.extend([
                "📖 Review fundamental concepts before taking more quizzes",
                "🎯 Use 'Focus on Mistakes' mode to target your weak areas",
                "⏰ Take your time - accuracy is more important than speed"
            ])
        elif error_summary['error_rate'] > 20:
            recommendations.extend([
                "🧠 Use 'Smart Review' to leverage spaced repetition",
                "🔄 Try 'Mixed Review' for comprehensive practice",
                "📊 Monitor your progress in the Learning Progress section"
            ])
        else:
            recommendations.extend([
                "🌟 Excellent work! Consider exploring new topics",
                "🔄 Use 'Mixed Review' to maintain your knowledge",
                "🎓 You might be ready for more advanced questions"
            ])
        
        # Add specific recommendations based on patterns
        if len(error_summary['most_difficult_questions']) > 3:
            recommendations.append(
                f"🎯 Focus on your {len(error_summary['most_difficult_questions'])} "
                "most difficult questions using spaced repetition"
            )
        
        return recommendations[:5]