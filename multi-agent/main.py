"""
Multi-Agent System - Simple Example
------------------------------------
How it works:
  1. Orchestrator receives your task
  2. It calls Researcher agent to gather info
  3. It calls Writer agent to produce output
  4. Final result is printed

Setup:
  pip install anthropic
  set ANTHROPIC_API_KEY=your-key-here
"""

import os
from anthropic import Anthropic

client = Anthropic()


# ── AGENT DEFINITIONS ──────────────────────────────────────────────────────────

def researcher_agent(topic: str) -> str:
    """Specialist: returns a factual summary on a topic."""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system="You are a research specialist. Return clear, factual bullet-point summaries. Be concise.",
        messages=[{"role": "user", "content": f"Research this topic and summarise key facts: {topic}"}],
    )
    return response.content[0].text


def writer_agent(research: str, format: str = "short report") -> str:
    """Specialist: turns research into polished writing."""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        system="You are a professional writer. Turn research notes into clear, readable content.",
        messages=[
            {
                "role": "user",
                "content": f"Using this research:\n\n{research}\n\nWrite a {format}.",
            }
        ],
    )
    return response.content[0].text


# ── ORCHESTRATOR ───────────────────────────────────────────────────────────────

def orchestrator(task: str) -> str:
    """
    Boss agent: decides which specialists to call and in what order.
    For this example the flow is fixed: Research → Write.
    In a real system you'd let Claude decide dynamically using tool_use.
    """
    print(f"\n[Orchestrator] Task received: {task}")

    print("[Orchestrator] Calling Researcher agent...")
    research = researcher_agent(task)
    print(f"[Researcher] Done.\n{research}\n")

    print("[Orchestrator] Calling Writer agent...")
    final_output = writer_agent(research, format="concise summary")
    print(f"[Writer] Done.")

    return final_output


# ── RUN ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    task = input("Enter a topic or task: ").strip()
    if not task:
        task = "How does the Python asyncio event loop work?"

    result = orchestrator(task)

    print("\n" + "=" * 60)
    print("FINAL OUTPUT")
    print("=" * 60)
    print(result)

    # Save output
    output_path = os.path.join(os.path.dirname(__file__), "output.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Task: {task}\n\n{result}")
    print(f"\n[Saved to {output_path}]")
