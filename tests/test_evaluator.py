from src.evaluator import evaluate_user_input


def test_evaluate_user_input_good_quality():
    
    result = evaluate_user_input(
        decision_topic="Should I learn Django or FastAPI first?",
        situation="I know Python basics and want to build AI applications. I am confused which backend framework will help me become job-ready.",
        options="Option A: Django. Option B: FastAPI.",
        constraints="I can study mostly on weekends and want to build portfolio projects in 2 months.",
        confusion="I am confused because Django is full-stack while FastAPI is popular for AI APIs."
    )

    assert result["score"] >= 8
    assert result["quality"] == "Good"


def test_evaluate_user_input_weak_quality():
    
    result = evaluate_user_input(
        decision_topic="AI",
        situation="I am confused.",
        options="",
        constraints="",
        confusion=""
    )

    assert result["score"] < 5
    assert result["quality"] == "Weak"
    assert len(result["suggestions"]) > 0