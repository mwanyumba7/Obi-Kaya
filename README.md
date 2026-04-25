<div align="center">
 
# 🌐👥 Obi Kaya

### *Your Smart Community Assistant*

[![Google AI](https://img.shields.io/badge/Google%20AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google/)

---

Obi-Kaya is a Smart Community Assistant Agent designed to empower community organizers/managers or anyone in DevRel, especially in Sub-Saharan Africa, to maximize their community's impact, secure partnerships, and sustain engagement. The agent analyzes community data, generates actionable recommendations, crafts partnership/sponsorship pitches, and provides strategies for ongoing engagement. It is multilingual and can respond in most African languages.

</div>

## Project Structure

```
obi_kaya_agent/
    __init__.py
    agent.py
    .env
```

- `agent.py`: Main file containing the agent definition and all tool implementations.
- `__init__.py`: Marks the directory as a Python package.

## Requirements
- Python 3.8+
- [google-adk](https://pypi.org/project/google-adk/)
- [google-genai](https://googleapis.github.io/python-genai/)

## Installation

1. **Clone or Fork the Repository**
   ```sh
   git clone https://github.com/<your-username>/Obi-Kaya.git
   cd Obi-Kaya
   ```
   *(If you haven't already, fork the repo at https://github.com/mwanyumba7/Obi-Kaya and clone your fork)*

2. **Create a Virtual Environment (Recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Activate the Virtual Environment You Created Above**

For Windows: 
   ```sh
   source venv/Scripts/activate
   ```

For Mac or Linux: 
   ```sh
   source venv/bin/activate
   ```

4. **Install Required Packages**

```sh
pip install google-adk google-genai
```

## Step-by-Step Guide: Building the Agent

### 1. Project Setup
- Ensure your folder structure matches the one above.
- All code will be in `obi_kaya_agent/agent.py`.

### 2. Implementing the Tools

#### a. `generate_recommendations_from_input`
This tool analyzes community data (text or PDF content) and returns structured, actionable recommendations in three categories:
- Event Ideas & Timing
- Social Media Strategy
- Ongoing Engagement (Beyond Events)

**How it works:**
- Accepts user input (text or extracted PDF content).
- Builds a prompt for the Gemini LLM to generate recommendations.
- Returns a dictionary with recommendations organized by category.

#### b. `generate_partnership_pitch`
This tool generates a personalized partnership/sponsorship pitch using community data (text, Google Word, or PDF content). The pitch includes:
- Community Overview
- Engagement Metrics
- Impact Statements
- Value Proposition
- Next Steps

**How it works:**
- Accepts user input (text or extracted report content).
- Builds a prompt for the Gemini LLM to generate a structured pitch.
- Returns a dictionary with the pitch organized by section.

#### c. `answer_community_general_question`
This tool answers general questions about community building, being a tech community organizer, creating and measuring impact, and troubleshooting Bevy platform issues.

**How it works:**
- Accepts a question as input.
- Builds a prompt for the Gemini LLM, referencing best practices and support resources.
- Returns a dictionary with the question and a detailed answer.

### 3. Defining the Agent
The agent is defined in `agent.py` using the `Agent` class from `google.adk.agents`. It includes:
- Name, model, description, and detailed instructions.
- The three tools above registered in the `tools` list.

### 4. Running and Viewing the Agent in ADK Web UI

1. **Start the ADK Web UI**
   ```sh
   adk web
   ```
2. Open your browser and go to the URL provided (usually http://localhost:8080).
3. Select your agent (`obi_kaya_agent`) and interact with it using the web interface.

### 5. 🛠️  Troubleshooting & Quick Fixes
1. Allow Cross-Origin Requests (CORS)
If you are running the agent in Google Cloud Shell or accessing it via a public IP (you can notice it by the 105.x.x.x IP in your logs ), the server likely blocks the request because the "Origin" doesn't match localhost.

Try running the command with the --allow_origins flag set to wildcard:

`adk web --allow_origins "*"`

## Example Usage

- **Get recommendations:** Upload a PDF report or paste community data, and ask for event or engagement ideas.
- **Generate a partnership pitch:** Provide your community stats and request a sponsorship pitch.
- **Ask a general question:** "How do I increase engagement in my developer community?" or "How do I troubleshoot event registration on Bevy?"

## Code Explanation

All tools are implemented as Python functions in `agent.py`. Each tool:
- Accepts input (text, question, or report content).
- Builds a prompt for the Gemini LLM.
- Handles the LLM response and returns structured output.

The agent is then instantiated with these tools, a description, and clear instructions on what topics it can help with.

## Support & Resources
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Google Gen AI SDK Documentation](https://googleapis.github.io/python-genai/)
- [Bevy support](https://help.bevy.com/hc/en-us/categories/22880458639767-Community-Enterprise-Pro)
- [Bevy blog](https://bevy.com/b/blog)
- [FasterCapital: Measuring Community Impact](https://fastercapital.com/topics/measuring-and-analyzing-community-growth-and-impact.html)
- [David Spinks' Community Insights](https://davidspinks.substack.com/)
