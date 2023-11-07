from django.contrib import admin
from django.db.models import Max
from django.utils.safestring import mark_safe
from random import randint
from collections import OrderedDict
from .models import Question, Answer, Quiz, Result


# Display answers in tabular format in question
class AnswerInline(admin.TabularInline):
    """
    Admin inline class for displaying answers in tabular format within a question.
    """
    model = Answer
    

class QuestionAdmin(admin.ModelAdmin):
    """
    Admin model class for configuring the display of Question model in the admin interface.
    """
    change_list_template = 'admin/question_change_list.html'
    
    inlines = [AnswerInline]
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        return response
        

def generate_random_color():
        return f'rgba({randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)})'

class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'quiz_highest_score', 'passed', 'completion_time', 'created')
    
    change_list_template = 'admin/result_change_list.html'
    
    def quiz_highest_score(self, obj):
        quiz_highest_score = Result.objects.filter(quiz=obj.quiz, user=obj.user).aggregate(Max('score'))['score__max']
        if obj.score == quiz_highest_score:
            return quiz_highest_score
        else:
            return ''
    quiz_highest_score.short_description = 'User Highest Score'
    
    def passed(self, obj):
        required_score_to_pass = obj.quiz.required_score_to_pass
        if obj.score >= required_score_to_pass:
            return True
        else:
            return False
    passed.boolean = True
    passed.short_description = 'Passed'
    
    
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        quizzes = Quiz.objects.all()
        quiz_tables = []
        for quiz in quizzes:
            results = qs.filter(quiz=quiz)
            
            # Filter results based on required score to pass
            required_score_to_pass = quiz.required_score_to_pass
            passed_results = [result for result in results if result.score >= required_score_to_pass]

            if passed_results:
                table = f'<hr/><br/><h2>{quiz.name}</h2>'
                table += '<table>'
                table += '<tr><th>User</th><th>Score</th><th>Highest Score</th><th>Passed</th><th>Completion Time</th><th>Created</th></tr>'
                for result in results:
                    highest_score = self.quiz_highest_score(result)
                    passed = self.passed(result)
                    passed_icon = '✅' if passed else '❌'
                    table += f'<tr><td>{result.user}</td><td>{result.score}</td><td>{highest_score}</td><td>{passed_icon}</td><td>{result.completion_time}</td><td>{result.created}</td></tr>'
                table += '</table>'
                quiz_tables.append(table)
                
                # Generate random colors for each bar
                bar_colors = [generate_random_color() for _ in passed_results]
                
                # Create bar chart using chart.js
                user_scores = {}

                for result in passed_results:
                    user = str(result.user)
                    score = result.score
                    if user not in user_scores:
                        user_scores[user] = score

                # Now user_scores contains unique scores for each user

                users = list(user_scores.keys())
                scores = list(user_scores.values())
                chart_data = {
                    'labels': users,
                    'datasets': [{
                        'label': f'{quiz.name} Scores',
                        'data': scores,
                        'backgroundColor': bar_colors,
                        'hoverBackgroundColor': '#4e73df',
                        'borderColor': '#fffff',
                    }]
                }
                chart_options = {
                    'maintainAspectRatio': 'true',
                    'scales': {
                        'y': {
                            'beginAtZero': 'true'
                        }
                    }
                }
                chart_html = f'''
                    <canvas id="{quiz.pk}-chart" style="padding-top: 30px;"></canvas>
                    <script>
                        var ctx = document.getElementById("{quiz.pk}-chart");
                        var myChart = new Chart(ctx, {{
                            type: "bar",
                            data: {chart_data},
                            options: {chart_options}
                        }});
                    </script>
                '''
                quiz_tables.append(chart_html)
        
        response.context_data['quiz_tables'] = mark_safe(''.join(quiz_tables))
        return response



# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Result, ResultAdmin)