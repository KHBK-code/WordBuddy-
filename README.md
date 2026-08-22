# WordBuddy-
Kid-friendly AI helper that explains big words — IBM AI Builders Challenge (Wildcard)
# WordBuddy

Kid-friendly AI helper that explains big words so children who struggle with reading can understand them with confidence.

**IBM AI Builders Challenge — August 2026**  
**Theme:** Wildcard — Intelligent Systems for the Future of Work

## Problem
Many children get stuck on long or unfamiliar words. That makes reading feel hard and can stop them from finishing a book or assignment.

## Solution
WordBuddy takes a hard word or short sentence and explains it in simple language:
- syllable breakdown
- easy definition
- example sentences
- a friendly analogy
- a short practice question

## AI Approach & Architecture
- Streamlit app for a simple kid-friendly UI
- LLM (planned: IBM Granite or similar) with a child-safe system prompt
- Structured JSON output for consistent explanations

## How IBM Bob Was Used
- Plan mode: architecture and file structure
- Code mode: app, prompts, tests
- Ask mode: debugging and README help

*(Add more details as you build.)*

## How to Run
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
