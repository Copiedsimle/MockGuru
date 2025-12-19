from django.http import HttpResponse, JsonResponse
import json
def attempt_paper(request, slug):
	paper = get_object_or_404(QuestionPaper, slug=slug)
	questions = list(paper.questions.all())
	if request.method == 'POST':
		# Process answers and calculate score
		total = 0
		correct = 0
		wrong = 0
		score = 0
		details = []
		for idx, q in enumerate(questions):
			ans = request.POST.get(f'q{idx}')
			is_correct = False
			awarded = 0
			if q.question_type.startswith('mcq'):
				if q.question_type == 'mcq_single':
					if ans and ans == q.correct_option:
						is_correct = True
						awarded = q.marks
					elif ans:
						awarded = -q.negative_marks
				elif q.question_type == 'mcq_multiple':
					# For multiple correct, expect comma-separated or list
					user_ans = request.POST.getlist(f'q{idx}')
					correct_ans = [o.strip() for o in (q.correct_option or '').split(',') if o.strip()]
					if set(user_ans) == set(correct_ans):
						is_correct = True
						awarded = q.marks
					elif user_ans:
						awarded = -q.negative_marks
			elif q.question_type == 'numeric':
				if ans and str(ans).strip() == str(q.correct_answer).strip():
					is_correct = True
					awarded = q.marks
				elif ans:
					awarded = -q.negative_marks
			elif q.question_type == 'subjective':
				awarded = 0  # Subjective not auto-scored
			total += q.marks
			if is_correct:
				correct += 1
				score += awarded
			elif awarded < 0:
				wrong += 1
				score += awarded
			details.append({
				'question': q.text,
				'your_answer': ans,
				'is_correct': is_correct,
				'marks_awarded': awarded,
				'explanation': q.explanation,
			})
		# Save attempt if user is authenticated
		if request.user.is_authenticated:
			from .models import TestAttempt
			TestAttempt.objects.create(
				user=request.user,
				exam=paper.exam,
				question_paper=paper,
				score=score,
				total=total,
				correct=correct,
				wrong=wrong
			)
		return render(request, 'exam/attempt_result.html', {
			'questionpaper': paper,
			'score': score,
			'total': total,
			'correct': correct,
			'wrong': wrong,
			'details': details,
		})
	# GET: render exam interface
	questions_json = []
	for q in questions:
		questions_json.append({
			'id': q.id,
			'question_type': q.question_type,
			'text': q.text,
			'marks': q.marks,
			'negative_marks': q.negative_marks,
			'option_a': q.option_a,
			'option_b': q.option_b,
			'option_c': q.option_c,
			'option_d': q.option_d,
			'image': q.image.url if q.image else '',
		})
	return render(request, 'exam/attempt_paper.html', {
		'questionpaper': paper,
		'questions': json.dumps(questions_json),
		'duration': paper.duration,
	})
from django.shortcuts import render, get_object_or_404

from .models import Exam, Section, Subsection, QuestionPaper, Question
from .forms import BulkQuestionUploadForm
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import csv, zipfile, io
from django.contrib import messages
from django.shortcuts import redirect
from django.core.files.base import ContentFile

from .models import TestAttempt
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max

def bulk_upload_questions(request):
	if request.method == 'POST':
		form = BulkQuestionUploadForm(request.POST, request.FILES)
		if form.is_valid():
			csv_file = form.cleaned_data['csv_file']
			zip_file = form.cleaned_data.get('zip_file')
			images = {}
			if zip_file:
				with zipfile.ZipFile(zip_file) as z:
					for filename in z.namelist():
						images[filename] = z.read(filename)
			decoded_csv = csv_file.read().decode('utf-8').splitlines()
			reader = csv.DictReader(decoded_csv)
			for row in reader:
				# expects: exam, section, subsection, paper, question_type, text, marks, negative_marks, option_a, option_b, option_c, option_d, correct_option, correct_answer, explanation, image
				exam, _ = Exam.objects.get_or_create(name=row['exam'])
				section, _ = Section.objects.get_or_create(exam=exam, name=row['section'], subtype=row.get('subtype', ''))
				subsection = None
				if row.get('subsection'):
					subsection, _ = Subsection.objects.get_or_create(section=section, name=row['subsection'])
				paper, _ = QuestionPaper.objects.get_or_create(
					exam=exam,
					section=section,
					subsection=subsection,
					title=row['paper']
				)
				image_file = None
				if row.get('image') and row['image'] in images:
					image_file = ContentFile(images[row['image']], name=row['image'])
				Question.objects.create(
					question_paper=paper,
					question_type=row.get('question_type', ''),
					text=row.get('text', ''),
					marks=row.get('marks', 1),
					negative_marks=row.get('negative_marks', 0),
					option_a=row.get('option_a', ''),
					option_b=row.get('option_b', ''),
					option_c=row.get('option_c', ''),
					option_d=row.get('option_d', ''),
					correct_option=row.get('correct_option', ''),
					correct_answer=row.get('correct_answer', ''),
					explanation=row.get('explanation', ''),
					image=image_file
				)
			messages.success(request, 'Bulk upload completed!')
			return redirect('bulk_upload_questions')
	else:
		form = BulkQuestionUploadForm()
	return render(request, 'exam/bulk_upload.html', {'form': form})

def exam_list(request):
	exams = Exam.objects.all()
	return render(request, 'exam/exam_list.html', {'exams': exams})

def exam_detail(request, slug):
	exam = get_object_or_404(Exam, slug=slug)
	exams = Exam.objects.all()
	return render(request, 'exam/exam_detail.html', {'exam': exam, 'exam_list': exams})

def section_detail(request, pk):
	section = get_object_or_404(Section, pk=pk)
	return render(request, 'exam/section_detail.html', {'section': section})

def subsection_detail(request, pk):
	subsection = get_object_or_404(Subsection, pk=pk)
	return render(request, 'exam/subsection_detail.html', {'subsection': subsection})

def questionpaper_detail(request, slug):
	questionpaper = get_object_or_404(QuestionPaper, slug=slug)
	return render(request, 'exam/questionpaper_detail.html', {'questionpaper': questionpaper})


# User Authentication Views
def login_view(request):
	if request.user.is_authenticated:
		return redirect('exam_list')
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('exam_list')
		else:
			messages.error(request, 'Invalid username or password')
	return render(request, 'account/login.html')

def signup_view(request):
	if request.user.is_authenticated:
		return redirect('exam_list')
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Account created successfully. Please log in.')
			return redirect('login')
	else:
		form = UserRegistrationForm()
	return render(request, 'account/signup.html', {'form': form})

def logout_view(request):
	logout(request)
	return redirect('login')


# Dashboard view for user performance
@login_required
def dashboard(request):
	user = request.user
	attempts = TestAttempt.objects.filter(user=user).order_by('-date')
	metrics = {
		'total_tests': attempts.count(),
		'avg_score': round(attempts.aggregate(Avg('score'))['score__avg'] or 0, 2),
		'best_score': attempts.aggregate(Max('score'))['score__max'] or 0,
		'recent_score': attempts.first().score if attempts.exists() else 0,
	}
	recent_attempts = attempts[:10]
	chart_labels = [a.date.strftime('%d %b') for a in attempts.order_by('date')]
	chart_scores = [a.score for a in attempts.order_by('date')]
	chart = {
		'labels': chart_labels,
		'scores': chart_scores,
	}
	return render(request, 'exam/dashboard.html', {
		'user': user,
		'metrics': metrics,
		'recent_attempts': recent_attempts,
		'chart': chart,
	})

def robots_txt(request):
    sitemap_url = request.build_absolute_uri('/sitemap.xml')
    content = f"""User-agent: *
Disallow: /admin/
Allow: /

Sitemap: {sitemap_url}"""
    return HttpResponse(content, content_type="text/plain")
