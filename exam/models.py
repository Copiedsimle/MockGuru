
from django.db import models

from django.contrib.auth.models import User


class Exam(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	date = models.DateField(null=True, blank=True)
	has_two_subsections = models.BooleanField(default=False, help_text="Does this exam have two levels of subsections?")

	def __str__(self):
		return self.name

class Section(models.Model):
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='sections')
	name = models.CharField(max_length=200)
	subtype = models.CharField(max_length=100)

	def __str__(self):
		return f"{self.name} ({self.subtype})"

class Subsection(models.Model):
	section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='subsections')
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class QuestionPaper(models.Model):
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='question_papers', null=True, blank=True)
	section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='question_papers', null=True, blank=True)
	subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE, related_name='question_papers', null=True, blank=True)
	title = models.CharField(max_length=200)
	content = models.TextField()
	duration = models.PositiveIntegerField(default=60, help_text="Duration in minutes")
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


class Question(models.Model):
	QUESTION_TYPE_CHOICES = [
		("mcq_single", "MCQ (Single Answer)"),
		("mcq_multiple", "MCQ (Multiple Answers)"),
		("subjective", "Subjective"),
		("numeric", "Numeric"),
	]
	exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
	section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
	subsection = models.ForeignKey(Subsection, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
	question_paper = models.ForeignKey(QuestionPaper, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
	question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
	text = models.TextField()
	marks = models.FloatField(default=1)
	negative_marks = models.FloatField(default=0)
	option_a = models.CharField(max_length=500, blank=True, null=True)
	option_b = models.CharField(max_length=500, blank=True, null=True)
	option_c = models.CharField(max_length=500, blank=True, null=True)
	option_d = models.CharField(max_length=500, blank=True, null=True)
	correct_option = models.CharField(max_length=10, blank=True, null=True, help_text="A, B, C, D or comma separated for multiple")
	correct_answer = models.CharField(max_length=500, blank=True, null=True, help_text="For subjective/numeric")
	explanation = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to='question_images/', blank=True, null=True)

	def __str__(self):
		return self.text[:50]


# User performance and test attempt model
class TestAttempt(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
	exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True)
	question_paper = models.ForeignKey(QuestionPaper, on_delete=models.SET_NULL, null=True)
	score = models.FloatField()
	total = models.FloatField()
	correct = models.IntegerField()
	wrong = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} - {self.exam} - {self.score}/{self.total} on {self.date.strftime('%Y-%m-%d')}"
