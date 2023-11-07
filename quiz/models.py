from django.db import models
from course.models import Course, Announcement
from myapp.models import User
import random
from django.db.models.signals import post_delete
from django.dispatch import receiver



# Crate a quiz models
class Quiz(models.Model):
    """
    Model representing a quiz.
    """
    DIFF_CHOICES = (
        ('easy', 'easy'),
        ('medium', 'medium'),
        ('hard', 'hard'),
    )
    
    name = models.CharField(max_length=120)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quiz_chances = models.PositiveIntegerField(default=1)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text="required score in %")
    difficluty = models.CharField(max_length=6, choices=DIFF_CHOICES)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.name}-{self.course}"

    # returns a list of questions associated with the quiz using reverse query
    def get_questions(self):
        """
        Returns a list of questions associated with the quiz.
        Randomizes the order of questions.
        """
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]
    
    def save(self, *args, **kwargs):
        """
        Overrides the save method to create an associated announcement for the quiz.
        """
        # Call the parent class's save() method
        super().save(*args, **kwargs)
        
        # Create an announcement for the quiz
        announcement = Announcement.objects.create(
            title=f"New Quiz: {self.name}",
            content=f"A new quiz '{self.name}' has been scheduled for the course '{self.course}'."
                    f" It will start on {self.start_date} and end on {self.end_date}.",
            course=self.course
        )
        announcement.save()

    class Meta:
        verbose_name_plural = 'Quizes'
        
@receiver(post_delete, sender=Quiz)
def delete_related_announcement(sender, instance, **kwargs):
    """
    Signal handler to delete the associated announcement when a quiz is deleted.
    """
    try:
        announcement = Announcement.objects.get(course=instance.course, title=f"New Quiz: {instance.name}")
        announcement.delete()
    except Announcement.DoesNotExist:
        pass
        
# Create a question model
class Question(models.Model):
    """
    Model representing a question in a quiz.
    """
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        """
        Returns a list of answers associated with the question.
        """
        return self.answer_set.all()

# create an answer model
class Answer(models.Model):
    """
    Model representing an answer to a question.
    """
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"
    
# create a result model
class Result(models.Model):
    """
    Model representing the result of a user in a quiz.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='result')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(null=True)
    completion_time = models.FloatField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    # started = models.BooleanField(default=False)
    
    # chances_taken = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - result {self.quiz} - result {self.score}"
    