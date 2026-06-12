"""Load test harness. Run: locust -f locustfile.py --host http://localhost:50505"""
import json
import random

from locust import HttpUser, between, task

SAMPLE_QUESTIONS = [
    "What does the paper say about chunking strategy?",
    "Summarize the key findings.",
    "What were the limitations called out by the authors?",
    "Compare the two ingestion approaches.",
    "What does the speaker say about graph databases?",
]


class ChatUser(HttpUser):
    wait_time = between(2, 8)

    @task(10)
    def chat(self):
        body = {
            "messages": [{"role": "user", "content": random.choice(SAMPLE_QUESTIONS)}],
            "stream": True,
            "context": {"overrides": {"use_verifier": True, "use_graphrag": True}},
        }
        with self.client.post(
            "/chat",
            data=json.dumps(body),
            headers={"Content-Type": "application/json", "Accept": "text/event-stream"},
            catch_response=True,
            stream=True,
        ) as r:
            if r.status_code != 200:
                r.failure(f"status {r.status_code}")
                return
            for _ in r.iter_lines():
                pass

    @task(1)
    def config(self):
        self.client.get("/config")
