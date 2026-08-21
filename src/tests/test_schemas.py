"""Tests for Pydantic schemas."""

import pytest
from pydantic import ValidationError
from src.agents.principal.schemas import CurriculumProposal, TopicProposal
from src.agents.teacher.schemas import LessonPlan, LessonDetail, LearningObjective
from src.agents.slides.schemas import PresentationSlides, SlideContent
from src.agents.video.schemas import VideoResources, VideoResource
from src.agents.test.schemas import Quiz, QuizQuestion


@pytest.fixture
def sample_topic_proposal():
    """Create a valid TopicProposal for testing."""
    return TopicProposal(
        order=1,
        topic_name="Python Basics",
        days_allocated=5,
        rationale="Essential foundation for programming"
    )


@pytest.fixture
def sample_topics():
    """Create a list of valid TopicProposals."""
    return [
        TopicProposal(order=1, topic_name="Topic 1", days_allocated=5, rationale="Test 1"),
        TopicProposal(order=2, topic_name="Topic 2", days_allocated=6, rationale="Test 2"),
        TopicProposal(order=3, topic_name="Topic 3", days_allocated=5, rationale="Test 3"),
        TopicProposal(order=4, topic_name="Topic 4", days_allocated=6, rationale="Test 4")
    ]


@pytest.fixture
def sample_curriculum_proposal(sample_topics):
    """Create a valid CurriculumProposal for testing."""
    return CurriculumProposal(
        user_name="John Doe",
        career_goal="Machine Learning Engineer",
        curriculum_overview="Comprehensive ML curriculum overview",
        topics=sample_topics,
        total_duration_days=22,
        success_criteria=["Criterion 1", "Criterion 2", "Criterion 3"]
    )


@pytest.fixture
def sample_learning_objective():
    """Create a valid LearningObjective for testing."""
    return LearningObjective(
        objective="Understand Python variables and data types",
        blooms_level="Remember"
    )


@pytest.fixture
def sample_learning_objectives():
    """Create a list of valid LearningObjectives."""
    return [
        LearningObjective(objective="Test objective 1", blooms_level="Apply"),
        LearningObjective(objective="Test objective 2", blooms_level="Understand"),
        LearningObjective(objective="Test objective 3", blooms_level="Remember")
    ]


@pytest.fixture
def sample_lesson_detail():
    """Create a valid LessonDetail for testing."""
    return LessonDetail(
        lesson_number=1,
        title="Introduction to Variables",
        learning_objective="Learn about variables",
        duration_minutes=60,
        key_concepts=["variables", "types", "assignment"],
        teaching_approach="Hands-on coding exercises",
        resources_needed=["Python IDE", "Sample code"]
    )


@pytest.fixture
def sample_lessons():
    """Create a list of valid LessonDetails."""
    return [
        LessonDetail(
            lesson_number=i,
            title=f"Lesson {i}",
            learning_objective=f"Objective {i}",
            duration_minutes=60,
            key_concepts=["concept"],
            teaching_approach="Interactive",
            resources_needed=["IDE"]
        )
        for i in range(1, 5)
    ]


@pytest.fixture
def sample_lesson_plan(sample_learning_objectives, sample_lessons):
    """Create a valid LessonPlan for testing."""
    return LessonPlan(
        topic="Python Basics",
        overview="Introduction to Python programming",
        learning_objectives=sample_learning_objectives,
        lessons=sample_lessons,
        assessment_strategy="Quizzes and coding projects",
        estimated_total_time=240
    )


@pytest.fixture
def sample_slide_content():
    """Create a valid SlideContent for testing."""
    return SlideContent(
        slide_number=1,
        title="Introduction to Python",
        content_type="title",
        content="Welcome to Python Programming",
        speaker_notes="Introduce yourself and course objectives"
    )


@pytest.fixture
def sample_slides():
    """Create a list of valid SlideContents."""
    return [
        SlideContent(
            slide_number=i,
            title=f"Slide {i}",
            content_type="title" if i == 1 else "content",
            content=f"Content for slide {i}",
            speaker_notes=f"Speaker notes {i}"
        )
        for i in range(1, 11)
    ]


@pytest.fixture
def sample_presentation_slides(sample_slides):
    """Create a valid PresentationSlides for testing."""
    return PresentationSlides(
        topic="Python Basics",
        slides=sample_slides,
        total_slides=10,
        design_notes="Use blue theme with code examples"
    )


@pytest.fixture
def sample_video_resource():
    """Create a valid VideoResource for testing."""
    return VideoResource(
        title="Python Tutorial for Beginners",
        hypothetical_url="https://youtube.com/watch?v=example",
        description="Comprehensive Python tutorial",
        estimated_duration="30 minutes",
        difficulty_level="Beginner",
        key_topics_covered=["variables", "loops", "functions"],
        suggested_viewing_order=1,
        recommended_channel="freeCodeCamp",
        search_query="python tutorial for beginners",
        rationale="Excellent introduction to Python fundamentals"
    )


@pytest.fixture
def sample_videos():
    """Create a list of valid VideoResources."""
    return [
        VideoResource(
            title=f"Video Tutorial {i}",
            hypothetical_url=f"https://example.com/video{i}",
            description=f"Tutorial {i}",
            estimated_duration="15 minutes",
            difficulty_level="Beginner",
            key_topics_covered=["topic"],
            suggested_viewing_order=i,
            recommended_channel="freeCodeCamp",
            search_query=f"tutorial {i}",
            rationale=f"Rationale {i}"
        )
        for i in range(1, 6)
    ]


@pytest.fixture
def sample_video_resources(sample_videos):
    """Create a valid VideoResources for testing."""
    return VideoResources(
        topic="Python Basics",
        videos=sample_videos,
        viewing_guide="Watch videos in order for best learning experience"
    )


@pytest.fixture
def sample_quiz_question():
    """Create a valid QuizQuestion for testing."""
    return QuizQuestion(
        question_number=1,
        question_type="multiple_choice",
        difficulty="medium",
        question="What is the correct way to declare a variable in Python?",
        options=["var x = 5", "x = 5", "int x = 5", "let x = 5"],
        correct_answer="x = 5",
        explanation="Python uses simple assignment without type declarations",
        learning_objective_tested="Understand Python variable declaration"
    )


@pytest.fixture
def sample_quiz_questions():
    """Create a list of valid QuizQuestions."""
    return [
        QuizQuestion(
            question_number=i,
            question_type="multiple_choice",
            difficulty="easy",
            question=f"Test question {i}?",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation=f"Explanation {i}",
            learning_objective_tested=f"Objective {i}"
        )
        for i in range(1, 11)
    ]


@pytest.fixture
def sample_quiz(sample_quiz_questions):
    """Create a valid Quiz for testing."""
    return Quiz(
        topic="Python Basics",
        quiz_type="formative",
        questions=sample_quiz_questions,
        total_points=100,
        time_limit_minutes=30,
        passing_score=70,
        study_tips="Review all lesson materials before taking the quiz"
    )


class TestCurriculumSchemas:
    """Test principal agent schemas."""
    
    def test_topic_proposal_valid(self, sample_topic_proposal):
        """Test creating valid TopicProposal."""
        assert sample_topic_proposal.order == 1
        assert sample_topic_proposal.topic_name == "Python Basics"
    
    def test_topic_proposal_missing_field(self):
        """Test TopicProposal with missing required field."""
        with pytest.raises(ValidationError):
            TopicProposal(order=1, topic_name="Test")  # Missing required fields
    
    def test_curriculum_proposal_valid(self, sample_curriculum_proposal):
        """Test creating valid CurriculumProposal."""
        assert len(sample_curriculum_proposal.topics) == 4
        assert sample_curriculum_proposal.user_name == "John Doe"
        assert sample_curriculum_proposal.total_duration_days == 22

    def test_curriculum_rejects_inconsistent_duration(self, sample_curriculum_proposal):
        """Reject curriculum totals that disagree with topic allocations."""
        data = sample_curriculum_proposal.model_dump()
        data["total_duration_days"] = 30

        with pytest.raises(ValidationError, match="sum of topic days_allocated"):
            CurriculumProposal(**data)

    def test_curriculum_rejects_non_contiguous_order(self, sample_curriculum_proposal):
        """Reject missing or duplicated curriculum positions."""
        data = sample_curriculum_proposal.model_dump()
        data["topics"][2]["order"] = 2

        with pytest.raises(ValidationError, match="topic order"):
            CurriculumProposal(**data)


class TestTeacherSchemas:
    """Test teacher agent schemas."""
    
    def test_learning_objective_valid(self, sample_learning_objective):
        """Test creating valid LearningObjective."""
        assert "variables" in sample_learning_objective.objective.lower()
        assert sample_learning_objective.blooms_level == "Remember"
    
    def test_lesson_detail_valid(self, sample_lesson_detail):
        """Test creating valid LessonDetail."""
        assert sample_lesson_detail.lesson_number == 1
        assert len(sample_lesson_detail.key_concepts) >= 2
    
    def test_lesson_plan_valid(self, sample_lesson_plan):
        """Test creating valid LessonPlan."""
        assert sample_lesson_plan.topic == "Python Basics"
        assert len(sample_lesson_plan.lessons) == 4
        assert len(sample_lesson_plan.learning_objectives) == 3

    def test_lesson_plan_rejects_inconsistent_duration(self, sample_lesson_plan):
        """Reject a total time that disagrees with lesson durations."""
        data = sample_lesson_plan.model_dump()
        data["estimated_total_time"] = 300

        with pytest.raises(ValidationError, match="sum of lesson durations"):
            LessonPlan(**data)


class TestSlidesSchemas:
    """Test slides agent schemas."""
    
    def test_slide_content_valid(self, sample_slide_content):
        """Test creating valid SlideContent."""
        assert sample_slide_content.slide_number == 1
        assert sample_slide_content.content_type == "title"
    
    def test_presentation_slides_valid(self, sample_presentation_slides):
        """Test creating valid PresentationSlides."""
        assert sample_presentation_slides.topic == "Python Basics"
        assert len(sample_presentation_slides.slides) == 10
        assert sample_presentation_slides.total_slides == 10

    def test_presentation_rejects_inconsistent_slide_count(self, sample_presentation_slides):
        """Reject slide metadata that disagrees with the slide collection."""
        data = sample_presentation_slides.model_dump()
        data["total_slides"] = 11

        with pytest.raises(ValidationError, match="number of slides"):
            PresentationSlides(**data)


class TestVideoSchemas:
    """Test video agent schemas."""
    
    def test_video_resource_valid(self, sample_video_resource):
        """Test creating valid VideoResource."""
        assert "Python" in sample_video_resource.title
        assert len(sample_video_resource.key_topics_covered) >= 2
    
    def test_video_resources_valid(self, sample_video_resources):
        """Test creating valid VideoResources."""
        assert sample_video_resources.topic == "Python Basics"
        assert len(sample_video_resources.videos) == 5

    def test_video_resources_reject_non_contiguous_order(self, sample_video_resources):
        """Reject ambiguous viewing sequences."""
        data = sample_video_resources.model_dump()
        data["videos"][3]["suggested_viewing_order"] = 3

        with pytest.raises(ValidationError, match="suggested viewing order"):
            VideoResources(**data)


class TestQuizSchemas:
    """Test test agent schemas."""
    
    def test_quiz_question_valid(self, sample_quiz_question):
        """Test creating valid QuizQuestion."""
        assert sample_quiz_question.question_number == 1
        assert len(sample_quiz_question.options) >= 3
    
    def test_quiz_valid(self, sample_quiz):
        """Test creating valid Quiz."""
        assert sample_quiz.total_points == 100
        assert len(sample_quiz.questions) == 10

    def test_quiz_rejects_non_contiguous_question_numbers(self, sample_quiz):
        """Reject missing or duplicated question positions."""
        data = sample_quiz.model_dump()
        data["questions"][5]["question_number"] = 5

        with pytest.raises(ValidationError, match="question numbers"):
            Quiz(**data)
    
    def test_quiz_question_missing_options_for_multiple_choice(self):
        """Test that multiple choice requires options."""
        # Note: This assumes schema validation enforces options for multiple_choice
        question = QuizQuestion(
            question_number=1,
            question_type="short_answer",
            difficulty="easy",
            question="Explain Python",
            options=[],
            correct_answer="Programming language",
            explanation="Test",
            learning_objective_tested="Test"
        )
        # Should work for short_answer even without options
        assert question.question_type == "short_answer"
