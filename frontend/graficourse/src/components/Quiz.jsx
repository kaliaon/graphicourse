import React, { useState, useEffect, useRef } from "react";
import styled from "styled-components";

import { useNavigate } from "react-router-dom";

const Quiz = ({ quizData, nextLessonId, prevLessonId, courseId }) => {
  const navigate = useNavigate();
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [quizResult, setQuizResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isReviewMode, setIsReviewMode] = useState(false);

  // Process quiz data to ensure it's in a consistent format
  const processedQuizData = React.useMemo(() => {
    if (!quizData) return null;

    // Handle the new API test format
    if (quizData.questions && Array.isArray(quizData.questions)) {
      // If it has 'questions' array with question_type property, it's the new format
      if (
        quizData.questions.length > 0 &&
        "question_type" in quizData.questions[0]
      ) {
        return {
          title: quizData.title || "Тест",
          description: quizData.description || "Сабақ бойынша тест",
          time_limit_minutes: quizData.time_limit || 30,
          passing_score: quizData.passing_score || 70,
          questions: quizData.questions.map((q) => ({
            id: q.id,
            text: q.text,
            points: q.points,
            explanation: q.explanation,
            correct_answer: q.correct_answer,
            type: q.question_type === "MCQ" ? "multiple_choice" : "open_ended",
            choices: q.choices.map((c) => ({
              id: c.id,
              text: c.text,
              is_correct: c.is_correct,
            })),
          })),
        };
      }
    }

    // Return the original data if it's already in the expected format
    return quizData;
  }, [quizData]);

  // Initialize quiz when processedQuizData changes
  useEffect(() => {
    if (!processedQuizData) return;

    // Initialize answers object
    const initialAnswers = {};
    processedQuizData.questions.forEach((question) => {
      if (question.type === "multiple_choice") {
        initialAnswers[question.id] = {
          questionId: question.id,
          selectedChoiceIds: [],
        };
      } else if (question.type === "open_ended") {
        initialAnswers[question.id] = {
          questionId: question.id,
          textAnswer: "",
        };
      }
    });
    setUserAnswers(initialAnswers);
  }, [processedQuizData]);

  // Validate if quiz data is available
  if (
    !processedQuizData ||
    !processedQuizData.questions ||
    processedQuizData.questions.length === 0
  ) {
    return (
      <QuizContainer>
        <ErrorMessage>
          Тест деректері қолжетімді емес немесе жарамсыз.
        </ErrorMessage>
      </QuizContainer>
    );
  }

  const currentQuestion = processedQuizData.questions[currentQuestionIndex];

  // Handle answer change for multiple choice questions
  const handleMultipleChoiceAnswer = (choiceId) => {
    setUserAnswers((prev) => ({
      ...prev,
      [currentQuestion.id]: {
        questionId: currentQuestion.id,
        selectedChoiceIds: [choiceId], // Single selection for now
      },
    }));
  };

  // Handle answer change for open-ended questions
  const handleOpenEndedAnswer = (text) => {
    setUserAnswers((prev) => ({
      ...prev,
      [currentQuestion.id]: {
        questionId: currentQuestion.id,
        textAnswer: text,
      },
    }));
  };

  // Navigate to next question
  const handleNextQuestion = () => {
    if (currentQuestionIndex < processedQuizData.questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  // Navigate to previous question
  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  // Format time as MM:SS
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, "0")}:${remainingSeconds
      .toString()
      .padStart(2, "0")}`;
  };

  // Submit quiz answers
  const handleSubmitQuiz = async () => {
    if (quizSubmitted) return;

    setLoading(true);
    setQuizSubmitted(true);

    // Normally here we would submit to the backend API
    // For now, we'll simulate a result calculation

    try {
      // Simulate API call delay
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Calculate score (in real app, this would come from the API)
      let correctAnswers = 0;
      let totalPoints = 0;

      processedQuizData.questions.forEach((question) => {
        const userAnswer = userAnswers[question.id];
        if (question.type === "multiple_choice" && userAnswer) {
          const selectedChoiceId = userAnswer.selectedChoiceIds[0];
          const correctChoice = question.choices.find(
            (choice) => choice.is_correct
          );

          if (correctChoice && selectedChoiceId === correctChoice.id) {
            correctAnswers++;
            totalPoints += question.points;
          }
        }
        // For open-ended questions, we would need backend validation
      });

      const percentageScore =
        (totalPoints /
          processedQuizData.questions.reduce((sum, q) => sum + q.points, 0)) *
        100;
      const passed = percentageScore >= processedQuizData.passing_score;

      setQuizResult({
        score: percentageScore.toFixed(1),
        correctAnswers,
        totalQuestions: processedQuizData.questions.length,
        passed,
      });
    } catch (err) {
      setError(
        "Тест жауаптарын жіберу кезінде қате орын алды. Қайталап көріңіз."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleStartReview = () => {
    setIsReviewMode(true);
    setCurrentQuestionIndex(0);
  };

  const handleFinishReview = () => {
    setIsReviewMode(false);
  };

  // Show results after submission
  if (quizSubmitted && quizResult && !isReviewMode) {
    return (
      <QuizContainer>
        <ResultsContainer>
          <ResultsIcon isSuccess={quizResult.passed}>
            {quizResult.passed ? "🏆" : "📝"}
          </ResultsIcon>
          <ResultsHeader>Тест аяқталды</ResultsHeader>

          {quizResult.passed ? (
            <ResultsSuccess>Құттықтаймыз! Сіз тесттен өттіңіз.</ResultsSuccess>
          ) : (
            <ResultsFailure>
              Өкінішке орай, сіз тесттен өте алмадыңыз.
            </ResultsFailure>
          )}

          <ResultsDetails>
            <ResultItem>
              <span>Нәтиже:</span> <ResultValue>{quizResult.score}%</ResultValue>
            </ResultItem>
            <ResultItem>
              <span>Дұрыс жауаптар:</span>{" "}
              <ResultValue>
                {quizResult.correctAnswers} / {quizResult.totalQuestions}
              </ResultValue>
            </ResultItem>
            <ResultItem>
              <span>Өту балы:</span>{" "}
              <ResultValue>{processedQuizData.passing_score}%</ResultValue>
            </ResultItem>
          </ResultsDetails>

          <ResultsActions>
            <ReviewButton onClick={handleStartReview}>
              Жауаптарды тексеру
            </ReviewButton>
            <ReturnButton onClick={() => window.location.reload()}>
              Қайта тапсыру
            </ReturnButton>
          </ResultsActions>

          <ResultsNavigation>
            {prevLessonId && (
              <NavLessonButton
                onClick={() => {
                  navigate(`/course/${courseId}/lesson/${prevLessonId}`);
                  window.scrollTo(0, 0);
                }}
              >
                ← Алдыңғы тақырып
              </NavLessonButton>
            )}
            {nextLessonId && (
              <NavLessonButton
                isNext
                onClick={() => {
                  navigate(`/course/${courseId}/lesson/${nextLessonId}`);
                  window.scrollTo(0, 0);
                }}
              >
                Келесі тақырып →
              </NavLessonButton>
            )}
          </ResultsNavigation>
        </ResultsContainer>
      </QuizContainer>
    );
  }

  // Show loading state during submission
  if (loading) {
    return (
      <QuizContainer>
        <LoadingContainer>
          <LoadingText>Жауаптар тексерілуде...</LoadingText>
        </LoadingContainer>
      </QuizContainer>
    );
  }

  return (
    <QuizContainer>
      <QuizHeader>
        <QuizTitle>
          {isReviewMode ? "Жауаптарды тексеру" : processedQuizData.title}
        </QuizTitle>
        {!isReviewMode && <QuizDescription>{processedQuizData.description}</QuizDescription>}
        <QuizInfoBar>
          <QuizProgress>
            Сұрақ {currentQuestionIndex + 1} /{" "}
            {processedQuizData.questions.length}
          </QuizProgress>
          {isReviewMode && (
            <ReviewBadge isCorrect={
              currentQuestion.type === "multiple_choice"
                ? currentQuestion.choices.find(c => c.is_correct)?.id === userAnswers[currentQuestion.id]?.selectedChoiceIds[0]
                : false // Simplified for review
            }>
              {currentQuestion.type === "multiple_choice"
                ? (currentQuestion.choices.find(c => c.is_correct)?.id === userAnswers[currentQuestion.id]?.selectedChoiceIds[0] ? "Дұрыс" : "Қате")
                : "Тексерілмеді"}
            </ReviewBadge>
          )}
        </QuizInfoBar>
      </QuizHeader>

      <QuestionContainer>
        <QuestionNumber>Сұрақ {currentQuestionIndex + 1}</QuestionNumber>
        <QuestionText>{currentQuestion.text}</QuestionText>

        {currentQuestion.type === "multiple_choice" ? (
          <ChoicesContainer>
            {currentQuestion.choices.map((choice) => (
              <ChoiceItem
                key={choice.id}
                isSelected={userAnswers[currentQuestion.id]?.selectedChoiceIds.includes(choice.id)}
                isReview={isReviewMode}
                isCorrect={choice.is_correct}
                isWrongReview={isReviewMode && userAnswers[currentQuestion.id]?.selectedChoiceIds.includes(choice.id) && !choice.is_correct}
              >
                <ChoiceInput
                  type="radio"
                  id={`choice-${choice.id}`}
                  name={`question-${currentQuestion.id}`}
                  disabled={isReviewMode}
                  checked={userAnswers[currentQuestion.id]?.selectedChoiceIds.includes(choice.id)}
                  onChange={() => handleMultipleChoiceAnswer(choice.id)}
                />
                <ChoiceLabel htmlFor={`choice-${choice.id}`}>
                  {choice.text}
                  {isReviewMode && choice.is_correct && <CorrectMark>✓</CorrectMark>}
                </ChoiceLabel>
              </ChoiceItem>
            ))}
          </ChoicesContainer>
        ) : (
          <OpenEndedContainer>
            <OpenEndedInput
              placeholder="Жауабыңызды осында жазыңыз..."
              disabled={isReviewMode}
              value={userAnswers[currentQuestion.id]?.textAnswer || ""}
              onChange={(e) => handleOpenEndedAnswer(e.target.value)}
            />
            {isReviewMode && (
              <CorrectAnswerSection>
                <CorrectAnswerTitle>Дұрыс жауап:</CorrectAnswerTitle>
                <CorrectAnswerBody>{currentQuestion.correct_answer || "Үлгі жауап қолжетімді емес"}</CorrectAnswerBody>
              </CorrectAnswerSection>
            )}
          </OpenEndedContainer>
        )}

        {isReviewMode && currentQuestion.explanation && (
          <ExplanationSection>
            <ExplanationTitle>Түсіндірме:</ExplanationTitle>
            <ExplanationBody>{currentQuestion.explanation}</ExplanationBody>
          </ExplanationSection>
        )}
      </QuestionContainer>

      <NavigationContainer>
        <div style={{ display: 'flex', gap: '10px' }}>
          <NavButton onClick={handlePreviousQuestion} disabled={currentQuestionIndex === 0}>
            Алдыңғы
          </NavButton>

          {currentQuestionIndex < processedQuizData.questions.length - 1 ? (
            <NavButton onClick={handleNextQuestion}>Келесі</NavButton>
          ) : isReviewMode ? (
            <SubmitButton onClick={handleFinishReview}>Нәтижелерге оралу</SubmitButton>
          ) : (
            <SubmitButton onClick={handleSubmitQuiz}>Тестті аяқтау</SubmitButton>
          )}
        </div>
      </NavigationContainer>

      {error && <ErrorMessage>{error}</ErrorMessage>}

      <NavigationFooter>
        {prevLessonId && (
          <NavLessonButton
            onClick={() => {
              navigate(`/course/${courseId}/lesson/${prevLessonId}`);
              window.scrollTo(0, 0);
            }}
          >
            ← Алдыңғы тақырып
          </NavLessonButton>
        )}
        {nextLessonId && (
          <NavLessonButton
            isNext
            onClick={() => {
              navigate(`/course/${courseId}/lesson/${nextLessonId}`);
              window.scrollTo(0, 0);
            }}
          >
            Келесі тақырып →
          </NavLessonButton>
        )}
      </NavigationFooter>
    </QuizContainer>
  );
};

export default Quiz;

// Styled Components
const QuizContainer = styled.div`
  width: 100%;
  margin: 40px auto;
  background: white;
  padding: 40px;
  border-radius: 24px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
  max-width: 850px;
  border: 1px solid #f1f5f9;
`;

const QuizHeader = styled.div`
  margin-bottom: 40px;
  border-bottom: 2px solid #f1f5f9;
  padding-bottom: 24px;
`;

const QuizTitle = styled.h2`
  font-size: 2.2rem;
  color: #1a1f2e;
  margin-bottom: 12px;
  font-weight: 800;
  letter-spacing: -0.02em;
`;

const QuizDescription = styled.p`
  color: #666;
  font-size: 1rem;
  margin-bottom: 15px;
`;

const QuizInfoBar = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
`;

const QuizProgress = styled.div`
  font-weight: 500;
  color: #555;
`;

const ReviewBadge = styled.div`
  background-color: ${props => props.isCorrect ? '#dcfce7' : '#fee2e2'};
  color: ${props => props.isCorrect ? '#15803d' : '#b91c1c'};
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
`;

const QuestionContainer = styled.div`
  margin-bottom: 32px;
  background-color: white;
  padding: 0;
  border-radius: 0;
`;

const QuestionNumber = styled.div`
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #1a1f2e;
  margin-bottom: 8px;
  background: #f1f5f9;
  display: inline-block;
  padding: 4px 12px;
  border-radius: 6px;
`;

const QuestionText = styled.h3`
  font-size: 1.5rem;
  color: #1a1f2e;
  margin-bottom: 24px;
  line-height: 1.4;
  font-weight: 600;
`;

const QuestionPoints = styled.div`
  display: none;
`;

const ChoicesContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 12px;
`;

const ChoiceItem = styled.div`
  padding: 16px 20px;
  border: 2px solid ${props => {
    if (props.isReview) {
      if (props.isCorrect) return '#22c55e';
      if (props.isWrongReview) return '#ef4444';
      return '#e2e8f0';
    }
    return props.isSelected ? '#1a1f2e' : '#e2e8f0';
  }};
  border-radius: 12px;
  cursor: ${props => props.isReview ? 'default' : 'pointer'};
  display: flex;
  align-items: center;
  transition: all 0.2s ease;
  background-color: ${props => {
    if (props.isReview) {
      if (props.isCorrect) return '#f0fdf4';
      if (props.isWrongReview) return '#fef2f2';
      return 'white';
    }
    return props.isSelected ? '#f8fafc' : 'white';
  }};
  position: relative;

  &:hover {
    border-color: ${props => !props.isReview ? '#1a1f2e' : ''};
    background-color: ${props => !props.isReview ? '#f8fafc' : ''};
  }
`;

const ChoiceInput = styled.input`
  display: none;
`;

const ChoiceLabel = styled.label`
  flex: 1;
  cursor: inherit;
  font-weight: 500;
  color: #334155;
`;

const OpenEndedContainer = styled.div`
  margin-top: 15px;
  width: 100%;
`;

const OpenEndedInput = styled.textarea`
  width: 100%;
  height: 120px;
  padding: 16px 20px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-family: inherit;
  font-size: 1rem;
  resize: none;
  line-height: 1.6;
  background-color: #f8fafc;
  transition: all 0.2s ease;

  &:focus {
    outline: none;
    border-color: #1a1f2e;
    background-color: white;
    box-shadow: 0 0 0 4px rgba(26, 31, 46, 0.05);
  }

  &:disabled {
    background-color: #f1f5f9;
    cursor: default;
    color: #475569;
  }

  &::placeholder {
    color: #94a3b8;
  }
`;

const NavigationContainer = styled.div`
  display: flex;
  justify-content: space-between;
  margin-top: 25px;
`;

const NavButton = styled.button`
  background-color: white;
  color: #1a1f2e;
  border: 2px solid #e2e8f0;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);

  &:hover:not(:disabled) {
    background-color: #f8fafc;
    border-color: #cbd5e1;
    transform: translateY(-1px);
  }

  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
`;

const SubmitButton = styled.button`
  background-color: #1a1f2e;
  color: white;
  border: none;
  padding: 12px 28px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);

  &:hover {
    background-color: #0f172a;
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  }
`;

const ResultsContainer = styled.div`
  text-align: center;
  padding: 20px;
`;

const ResultsIcon = styled.div`
  font-size: 5rem;
  margin-bottom: 25px;
  display: block;
  color: ${props => props.isSuccess ? '#22c55e' : '#64748b'};
`;

const ResultsActions = styled.div`
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 30px;
  flex-wrap: wrap;
`;

const ReviewButton = styled.button`
  background-color: white;
  color: #1a1f2e;
  border: 2px solid #1a1f2e;
  padding: 12px 25px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background-color: #f8fafc;
    transform: translateY(-2px);
  }
`;

const CorrectMark = styled.span`
  color: #22c55e;
  margin-left: 10px;
  font-weight: bold;
`;

const ExplanationSection = styled.div`
  margin-top: 20px;
  padding: 15px;
  background-color: #eff6ff;
  border-left: 4px solid #3b82f6;
  border-radius: 4px 8px 8px 4px;
`;

const ExplanationTitle = styled.h4`
  margin: 0 0 8px 0;
  color: #1e40af;
  font-size: 0.95rem;
`;

const ExplanationBody = styled.p`
  margin: 0;
  color: #1e40af;
  font-size: 0.9rem;
  line-height: 1.5;
`;

const CorrectAnswerSection = styled.div`
  margin-top: 15px;
  padding: 12px;
  background-color: #f0fdf4;
  border: 1px solid #bbfcce;
  border-radius: 8px;
`;

const CorrectAnswerTitle = styled.div`
  font-weight: bold;
  font-size: 0.85rem;
  color: #15803d;
  margin-bottom: 5px;
`;

const CorrectAnswerBody = styled.div`
  font-size: 0.95rem;
  color: #166534;
`;

const ResultsHeader = styled.h2`
  font-size: 2rem;
  color: #333;
  margin-bottom: 20px;
`;

const ResultsSuccess = styled.div`
  font-size: 1.5rem;
  color: #27ae60;
  margin-bottom: 20px;
  font-weight: 500;
`;

const ResultsFailure = styled.div`
  font-size: 1.5rem;
  color: #e74c3c;
  margin-bottom: 20px;
  font-weight: 500;
`;

const ResultsDetails = styled.div`
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  margin: 20px auto;
  max-width: 400px;
`;

const ResultItem = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 1.1rem;
  padding: 5px 0;
`;

const ResultValue = styled.span`
  font-weight: 700;
  color: #1a1f2e;
`;

const ReturnButton = styled.button`
  background-color: #f1f5f9;
  color: #475569;
  border: none;
  padding: 12px 28px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background-color: #e2e8f0;
    color: #1a1f2e;
  }
`;

const NavigationFooter = styled.div`
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
  border-top: 1px solid #eee;
  padding-top: 20px;
  flex-wrap: wrap;
`;

const ResultsNavigation = styled.div`
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
  flex-wrap: wrap;
`;

const NavLessonButton = styled.button`
  background-color: ${props => props.isNext ? '#1a1f2e' : 'white'};
  color: ${props => props.isNext ? 'white' : '#1a1f2e'};
  border: 2px solid ${props => props.isNext ? '#1a1f2e' : '#e2e8f0'};
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover {
    background-color: ${props => props.isNext ? '#0f172a' : '#f8fafc'};
    border-color: ${props => props.isNext ? '#0f172a' : '#cbd5e1'};
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  }
`;

const LoadingContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  text-align: center;
`;

const LoadingText = styled.div`
  margin-top: 20px;
  font-size: 1.1rem;
  color: #64748b;
  font-weight: 500;
`;

const ErrorMessage = styled.div`
  margin-top: 20px;
  padding: 15px;
  background-color: #fef2f2;
  border: 1px solid #fee2e2;
  border-radius: 8px;
  color: #b91c1c;
  text-align: center;
  font-weight: 500;
`;

