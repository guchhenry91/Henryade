MULTI-AGENT SYSTEM
==================

FILES
-----
main.py       - The multi-agent system (run this)
output.txt    - Auto-created after each run with the result

HOW TO RUN
----------
1. Install dependency:
   pip install anthropic

2. Set your API key:
   Windows:  set ANTHROPIC_API_KEY=sk-...
   Mac/Linux: export ANTHROPIC_API_KEY=sk-...

3. Run:
   python main.py

4. Type any topic or question when prompted.

HOW IT WORKS
------------
Your task
   ↓
Orchestrator (boss agent)
   ├── Researcher agent  → gathers facts
   └── Writer agent      → turns facts into clean output
   ↓
Final result printed + saved to output.txt

EXTEND IT
---------
Add more specialist agents by:
1. Defining a new function like:  def editor_agent(draft): ...
2. Calling it inside orchestrator() after the writer step
