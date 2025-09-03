from fastapi.testclient import TestClient

from tests.mocks.appcore import FakeApp
from tests.mocks.cfg import FakeConfiguration


class TestHighLevelLogicsComplex:
    def test_integration_complex(self):

        config = FakeConfiguration()
        app = FakeApp(config)

        with TestClient(app.app) as client:
            # ===== 1. QUESTIONS =====

            # 1.1 get initial questions
            response = client.get("/questions/")
            assert response.status_code == 200
            initial_questions = response.json()
            assert len(initial_questions) == 3

            # 1.2 make new quest
            response = client.post(
                "/questions/", json={"text": "Новый вопрос для теста"}
            )
            assert response.status_code == 200
            new_question = response.json()
            assert new_question["text"] == "Новый вопрос для теста"

            # 1.3 check that the quest was added
            response = client.get("/questions/")

            assert response.status_code == 200
            questions_after_create = response.json()
            assert len(questions_after_create) == 4

            # ===== 2. ANSWERS =====

            # 2.1 сreate answer
            response = client.post(
                f"/questions/{new_question['id']}/answers/",
                json={"user_id": "test_user_1", "text": "Первый ответ на новый вопрос"},
            )
            assert response.status_code == 200
            new_answer = response.json()
            assert new_answer["question_id"] == new_question["id"]

            # 2.2 check existence of the new answer
            response = client.get(f"/questions/{new_question['id']}")
            assert response.status_code == 200
            question_with_answers = response.json()
            assert len(question_with_answers["answers"]) == 1

            # ===== 3. check mistakes =====

            # 3.1 try make answer for missing question
            response = client.post(
                "/questions/999/answers/",
                json={"user_id": "test_user", "text": "Ответ на несуществующий вопрос"},
            )
            assert response.status_code == 404

            # ===== 4. TEST DELETE =====

            # 4.1 del answer
            response = client.delete(f"/answers/{new_answer['id']}")
            assert response.status_code == 200
            assert response.json()["deleted"] is True

            # 4.2 del quest
            response = client.delete(f"/questions/{new_question['id']}")
            assert response.status_code == 200
            assert response.json()["deleted"] is True
            # todo: also check length in this test part
