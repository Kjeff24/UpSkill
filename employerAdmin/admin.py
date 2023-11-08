from django.contrib import admin
from django.db.models import Max
from random import randint
from django.utils.safestring import mark_safe
from django.contrib.admin import register
from employerAdmin.employer_admin import employer_admin_site
from quiz.models import Quiz, Question, Answer, Result
from course.models import *
from event.models import *
from myapp.models import User


@register(User, site=employer_admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_email_verified', 'last_login')
    
    def get_queryset(self, request):
        # Filter queryset to show only the courses created by the logged-in employer
        qs = super().get_queryset(request)
        if request.user.is_employer:
            return qs.filter(my_employer=request.user) | qs.filter(id=request.user.id)
        else:
            return qs
    
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "course":
    #         kwargs["queryset"] = Course.objects.filter(instructor=request.user)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ParticipantsInline(admin.TabularInline):
    """
    Inline model admin for Participants.

    Provides an inline editing interface for Participants model within QuestionAdmin.
    """
    model = Participants
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filter the users and rooms displayed in the user and room fields to show only those created by the logged-in admin
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(my_employer=request.user)
        elif db_field.name == 'room':
            kwargs['queryset'] = Room.objects.filter(course__instructor=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



@register(Course, site=employer_admin_site)
class CourseAdmin(admin.ModelAdmin):
    inlines = [ParticipantsInline]
    # Customize the fields displayed in the admin list view for courses
    list_display = ('name', 'instructor', 'created', 'updated')
    
    def get_queryset(self, request):
        # Filter queryset to show only the courses created by the logged-in employer
        qs = super().get_queryset(request)
        if request.user.is_employer:
            return qs.filter(instructor=request.user)
        else:
            return qs
        
    def save_model(self, request, obj, form, change):
        # Set the currently logged-in user as the instructor for new courses
        if not change:
            obj.instructor = request.user
        super().save_model(request, obj, form, change)
        
    def get_form(self, request, obj=None, **kwargs):
        # Remove the instructor field from the form
        form = super().get_form(request, obj, **kwargs)
        form.base_fields.pop('instructor', None)  # Remove the field if it exists
        return form
    
    
@register(Participants, site=employer_admin_site)
class ParticipantsAdmin(admin.ModelAdmin):
    # Customize the fields displayed in the admin list view for participants
    list_display = ('user', 'course')
    
    def get_queryset(self, request):
        # Filter queryset to show only the courses created by the logged-in employer
        qs = super().get_queryset(request)
        if request.user.is_employer:
            return qs.filter(course__instructor=request.user)
        else:
            return qs
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            kwargs["queryset"] = Course.objects.filter(instructor=request.user)
        elif db_field.name == "room":
            kwargs["queryset"] = Room.objects.filter(course__instructor=request.user)
        elif db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(my_employer=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@register(Resource, site=employer_admin_site)
class ResourceAdmin(admin.ModelAdmin):
    # Customize the fields displayed in the admin list view for resources
    list_display = ('name', 'course', 'created', 'updated')
    
    def get_queryset(self, request):
        # Filter queryset to show only the courses created by the logged-in employer
        qs = super().get_queryset(request)
        if request.user.is_employer:
            return qs.filter(course__instructor=request.user)
        else:
            return qs
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            kwargs["queryset"] = Course.objects.filter(instructor=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@register(Announcement, site=employer_admin_site)
class AnnouncementAdmin(admin.ModelAdmin):
    # Customize the fields displayed in the admin list view for announcements
    list_display = ('title', 'course', 'date', 'created', 'updated')
    
    def get_queryset(self, request):
        # Filter queryset to show only the courses created by the logged-in employer
        qs = super().get_queryset(request)
        if request.user.is_employer:
            return qs.filter(course__instructor=request.user)
        else:
            return qs
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            kwargs["queryset"] = Course.objects.filter(instructor=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@register(Room, site=employer_admin_site)
class RoomAdmin(admin.ModelAdmin):
    # Customize the fields displayed in the admin list view for rooms
    list_display = ('room_topic', 'course', 'created', 'updated')
    
    def get_queryset(self, request):
        # Filter queryset to show only the courses created by the logged-in employer
        qs = super().get_queryset(request)
        if request.user.is_employer:
            return qs.filter(course__instructor=request.user)
        else:
            return qs
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            kwargs["queryset"] = Course.objects.filter(instructor=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Quiz 

@register(Quiz, site=employer_admin_site)
class QuizAdmin(admin.ModelAdmin):
    # Customize the fields displayed in the admin list view for quizzes
    list_display = ('name', 'course', 'number_of_questions', 'time', 'required_score_to_pass', 'difficluty')
    
    def get_queryset(self, request):
        # Filter queryset to show only the courses created by the logged-in employer
        qs = super().get_queryset(request)
        if request.user.is_employer:
            return qs.filter(course__instructor=request.user)
        else:
            return qs
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            kwargs["queryset"] = Course.objects.filter(instructor=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class AnswerInline(admin.TabularInline):
    """
    Inline model admin for Answer.

    Provides an inline editing interface for Answer model within QuestionAdmin.
    """
    model = Answer

@register(Question, site=employer_admin_site)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    # Customize the fields displayed in the admin list view for questions
    list_display = ('text', 'quiz', 'created')
    
    change_list_template = 'admin/question_change_list.html'
    
    def get_queryset(self, request):
        # Filter queryset to show only the courses created by the logged-in employer
        qs = super().get_queryset(request)
        if request.user.is_employer:
            return qs.filter(quiz__course__instructor=request.user)
        else:
            return qs
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "quiz":
            kwargs["queryset"] = Quiz.objects.filter(course__instructor=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        return response


@register(Result, site=employer_admin_site)
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
    
    def get_queryset(self, request):
        # Filter queryset to show only the courses created by the logged-in employer
        qs = super().get_queryset(request)
        if request.user.is_employer:
            return qs.filter(quiz__course__instructor=request.user)
        else:
            return qs
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "quiz":
            kwargs["queryset"] = Quiz.objects.filter(course__instructor=request.user)
        elif db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(my_employer=request.user) 
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
            

@register(Event, site=employer_admin_site)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'start', 'end')
    
    def get_queryset(self, request):
        # Filter queryset to show only the courses created by the logged-in employer
        qs = super().get_queryset(request)
        if request.user.is_employer:
            return qs.filter(course__instructor=request.user)
        else:
            return qs
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            kwargs["queryset"] = Course.objects.filter(instructor=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
def generate_random_color():
        return f'rgba({randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)})'