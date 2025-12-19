#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mockexam.settings')

# Setup Django
django.setup()

from blog.models import BlogPost

# Check existing notes
notes = BlogPost.objects.filter(post_type='notes')
print(f"Found {notes.count()} existing notes:")
for note in notes:
    print(f"- {note.title}")

# Create sample notes if none exist
if notes.count() == 0:
    print("\nCreating sample notes...")

    BlogPost.objects.create(
        title='CAT Quantitative Aptitude Notes',
        content='''Comprehensive notes for CAT Quantitative Aptitude section covering all important topics:

**Arithmetic Topics:**
- Number Systems
- Percentages and Profit & Loss
- Simple and Compound Interest
- Ratio and Proportion
- Time and Work
- Time, Speed and Distance

**Algebra Topics:**
- Linear Equations
- Quadratic Equations
- Inequalities
- Functions and Graphs
- Logarithms

**Geometry Topics:**
- Lines and Angles
- Triangles and Circles
- Coordinate Geometry
- Mensuration (2D and 3D)

**Modern Mathematics:**
- Permutations and Combinations
- Probability
- Set Theory
- Venn Diagrams

**Preparation Tips:**
- Focus on conceptual understanding
- Practice regularly with timed exercises
- Learn shortcut methods for calculations
- Analyze your mistakes and weak areas
- Take mock tests under exam conditions

These notes provide a complete foundation for CAT QA preparation.''',
        post_type='notes'
    )

    BlogPost.objects.create(
        title='GATE Computer Science Notes',
        content='''Detailed study notes for GATE CSE including all major topics:

**Algorithms and Data Structures:**
- Algorithm Analysis and Design
- Sorting and Searching Algorithms
- Graph Algorithms
- Dynamic Programming
- Greedy Algorithms
- Trees and Binary Search Trees
- Hashing and Hash Tables

**Operating Systems:**
- Process Management
- Memory Management
- File Systems
- CPU Scheduling
- Deadlocks
- Synchronization

**Databases:**
- Relational Model
- SQL Queries
- Normalization
- Transaction Management
- Indexing and Query Processing

**Computer Networks:**
- OSI and TCP/IP Models
- Network Protocols
- Routing Algorithms
- Transport Layer
- Application Layer

**Programming and Software Engineering:**
- C Programming
- Object-Oriented Programming
- Software Development Life Cycle
- Testing and Debugging

**Mathematics:**
- Discrete Mathematics
- Linear Algebra
- Probability and Statistics
- Graph Theory

**Preparation Strategy:**
- Master the fundamentals first
- Practice coding regularly
- Solve previous year papers
- Focus on time management
- Stay updated with current trends''',
        post_type='notes'
    )

    BlogPost.objects.create(
        title='CAT VARC Preparation Notes',
        content='''Complete notes for CAT Verbal Ability and Reading Comprehension:

**Verbal Ability Topics:**
- Grammar and Sentence Correction
- Vocabulary and Word Usage
- Para-jumbles and Para-completion
- Sentence Completion
- Critical Reasoning
- Analogies and Odd One Out

**Reading Comprehension Strategies:**
- Skimming and Scanning Techniques
- Identifying Main Ideas
- Understanding Tone and Purpose
- Inference and Assumption Questions
- Strengthening and Weakening Arguments

**Vocabulary Building:**
- Root Words and Prefixes/Suffixes
- Contextual Usage
- Synonyms and Antonyms
- Idioms and Phrases
- Foreign Words and Phrases

**Grammar Rules:**
- Subject-Verb Agreement
- Tenses and Voice
- Modifiers and Parallelism
- Pronoun Reference
- Punctuation

**Reading Practice:**
- Diverse Reading Materials
- Newspaper Articles
- Academic Texts
- Business and Economic Content
- Scientific and Technical Passages

**Test-Taking Strategies:**
- Time Management per Passage
- Question Selection Order
- Elimination Techniques
- Guessing Strategies
- Accuracy vs Speed Balance

**Practice Tips:**
- Read newspapers and magazines daily
- Maintain a vocabulary notebook
- Practice with timed exercises
- Analyze your reading speed and accuracy
- Focus on comprehension over speed initially''',
        post_type='notes'
    )

    print("Sample notes created successfully!")

# Check final count
notes = BlogPost.objects.filter(post_type='notes')
print(f"\nFinal count: {notes.count()} notes")
for note in notes:
    print(f"- {note.title}")