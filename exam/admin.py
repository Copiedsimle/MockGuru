from django.contrib import admin
from .models import Exam, Section, Subsection, QuestionPaper, Question
from django import forms

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
	list_display = ("name", "description", "date", "has_two_subsections")
	list_filter = ("has_two_subsections",)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
	list_display = ("name", "subtype", "exam")

@admin.register(Subsection)
class SubsectionAdmin(admin.ModelAdmin):
	list_display = ("name", "section")

@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
	list_display = ("title", "exam", "section", "subsection", "duration", "created_at")
	list_filter = ("exam", "section", "subsection")
	search_fields = ("title",)



# Custom form for Question to filter section/subsection/question_paper by exam
class QuestionAdminForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if 'exam' in self.data:
			try:
				exam_id = int(self.data.get('exam'))
				self.fields['section'].queryset = Section.objects.filter(exam_id=exam_id)
				self.fields['question_paper'].queryset = QuestionPaper.objects.filter(exam_id=exam_id)
			except (ValueError, TypeError):
				self.fields['section'].queryset = Section.objects.none()
				self.fields['question_paper'].queryset = QuestionPaper.objects.none()
		elif self.instance.pk and self.instance.exam:
			self.fields['section'].queryset = Section.objects.filter(exam=self.instance.exam)
			self.fields['question_paper'].queryset = QuestionPaper.objects.filter(exam=self.instance.exam)
		else:
			self.fields['section'].queryset = Section.objects.none()
			self.fields['question_paper'].queryset = QuestionPaper.objects.none()
		if 'section' in self.data:
			try:
				section_id = int(self.data.get('section'))
				self.fields['subsection'].queryset = Subsection.objects.filter(section_id=section_id)
			except (ValueError, TypeError):
				self.fields['subsection'].queryset = Subsection.objects.none()
		elif self.instance.pk and self.instance.section:
			self.fields['subsection'].queryset = Subsection.objects.filter(section=self.instance.section)
		else:
			self.fields['subsection'].queryset = Subsection.objects.none()


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	form = QuestionAdminForm
	list_display = ("text", "question_type", "exam", "section", "subsection", "question_paper")
	list_filter = ("exam", "section", "subsection", "question_paper")
