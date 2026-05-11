import os
import json

from groq import Groq
from dotenv import load_dotenv

from services.retriever import SHLRetriever
from services.ranker import rerank_results
from services.guards import is_blocked_query

load_dotenv()


SYSTEM_PROMPT = """
You are an SHL assessment recommendation assistant.

Rules:

1. Only recommend assessments from retrieved catalog results.
2. Never invent assessments.
3. Ask clarifying questions if user intent is vague.
4. Refuse hiring, legal, or unrelated advice.
5. Keep responses concise and professional.
6. Prioritize technical assessments for technical roles.
7. Prioritize behavioral/personality assessments for leadership or communication roles.
"""


class SHLAgent:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

        self.retriever = SHLRetriever()

    def needs_clarification(
        self,
        query
    ):

        vague_terms = [
            "assessment",
            "test",
            "hiring",
            "job"
        ]

        query_lower = query.lower()

        # very short query
        if len(query.split()) < 4:
            return True

        # generic vague query
        if any(
            term == query_lower.strip()
            for term in vague_terms
        ):
            return True

        return False

    def retrieve_context(
        self,
        query
    ):

        # retrieve more candidates
        results = self.retriever.search(
            query,
            top_k=10
        )

        # rerank semantically
        results = rerank_results(
            query,
            results
        )[:5]

        context = []

        for r in results:

            context.append(
                f"""
                Name: {r['name']}
                Description: {r['description']}
                URL: {r['url']}
                """
            )

        return "\n".join(context), results

    def chat(
        self,
        messages
    ):

        latest_user_message = messages[-1][
            "content"
        ]

        # guardrails
        if is_blocked_query(
            latest_user_message
        ):

            return {
                "reply": (
                    "I can only assist with "
                    "SHL assessment recommendations."
                ),
                "recommendations": [],
                "end_of_conversation": True
            }

        # clarification handling
        if self.needs_clarification(
            latest_user_message
        ):

            return {
                "reply": (
                    "Could you specify the role, "
                    "experience level, or skills "
                    "you are hiring for?"
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # retrieve relevant assessments
        context, retrieved = (
            self.retrieve_context(
                latest_user_message
            )
        )

        final_prompt = f"""
        User Query:
        {latest_user_message}

        Retrieved Assessments:
        {context}

        Generate a concise recommendation response.
        Explain why the assessments fit the role.
        Only use retrieved assessments.
        """

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": final_prompt
                }
            ]
        )

        reply = (
            response
            .choices[0]
            .message
            .content
        )

        recommendations = []

        for r in retrieved:

            recommendations.append({
                "name": r["name"],
                "url": r["url"],
                "description": r["description"][:200]
            })

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": True
        }


if __name__ == "__main__":

    agent = SHLAgent()

    response = agent.chat([
        {
            "role": "user",
            "content": (
                "Need assessment for "
                "Java backend developers"
            )
        }
    ])

    print(
        json.dumps(
            response,
            indent=2
        )
    )