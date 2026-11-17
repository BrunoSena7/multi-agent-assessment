import json
from types import SimpleNamespace

from orchestrator import MultiAgentAssessment, to_markdown


class FakeCompletions:
    def __init__(self):
        self.outputs = [
            {"questions": [{"id": 1, "type": "multiple_choice", "question": "2 + 2?", "options": {"A": "3", "B": "4"}, "correct_answer": "B", "explanation": "Soma básica.", "points": 2}]},
            {"answers": [{"id": 1, "answer": "B"}]},
            {"score": 99, "max_score": 99, "corrections": [{"id": 1, "awarded_points": 2, "max_points": 2, "expected_answer": "B", "feedback": "Correto."}], "overall_feedback": "Bom trabalho."},
        ]
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        payload = self.outputs.pop(0)
        message = SimpleNamespace(content=json.dumps(payload))
        choice = SimpleNamespace(message=message)
        return SimpleNamespace(choices=[choice])


class FakeClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=FakeCompletions())


def test_three_agents_run_sequentially_and_student_does_not_receive_answer_key():
    client = FakeClient()
    pipeline = MultiAgentAssessment(client=client)
    result = pipeline.run("Matemática", "Aritmética", question_count=1)
    calls = client.chat.completions.calls
    assert len(calls) == 3
    assert "correct_answer" not in calls[1]["messages"][1]["content"]
    assert result["review"]["score"] == 2
    assert result["review"]["max_score"] == 2


def test_report_contains_score_and_role_outputs():
    pipeline = MultiAgentAssessment(client=FakeClient())
    report = to_markdown(pipeline.run("Matemática", "Aritmética", question_count=1))
    assert "Nota" in report
    assert "2.0 / 2.0" in report
    assert "Feedback geral" in report
