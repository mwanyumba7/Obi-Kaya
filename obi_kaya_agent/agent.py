import datetime
import json
import os
from typing import Dict, List, Optional
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google import genai
client = genai.Client()
from google.genai import types




def generate_recommendations_from_input(user_text: str, goal_or_request: Optional[str] = None) -> dict:
    """
    Analyze community data (text or PDF content) and return structured, actionable recommendations in three categories:
    - Event Ideas & Timing
    - Social Media Strategy
    - Ongoing Engagement (Beyond Events)
    Uses gemini-2.5-flash-lite to:
    - Reference community data, trends, and best practices
    - Phrase each suggestion as an actionable plan, referencing data and best practices
    Returns a dict with status and recommendations (organized by category)
    """
    if not user_text or len(user_text.strip()) < 50:
        return {
            "status": "error",
            "message": "Please provide valid community data (text or PDF content) for recommendations."
        }
    prompt = (
        "You are a professional community manager assistant for community organizers/managers or anyone in DevRel. "
        "Analyze the following community data and generate actionable recommendations in these three categories:"
        "\n1. Event Ideas & Timing: Suggest event types, formats, and optimal scheduling based on the data. Reference audience demographics, engagement trends, and best practices."
        "\n2. Social Media Strategy: Provide channel-specific guidance (Twitter/X, Instagram, Facebook, etc.), including post examples, hashtags, and optimal posting times. Reference best practices and analytics if available."
        "\n3. Ongoing Engagement (Beyond Events): Suggest tactics to keep members active between events (newsletters, online forums, content sharing, etc.), referencing research-backed strategies."
        "\n\nFor each category, provide 2-4 actionable, data-driven recommendations. Phrase each as a clear plan (e.g., 'do X, focusing on Y'), referencing the community's data and best practices. If possible, cite authoritative tips."
        f"\n\nCommunity Data:\n{user_text}"
        f"\n\nOrganizer's goal/request: {goal_or_request if goal_or_request else '[None]'}"
        "\n\nFormat your answer as a JSON object with keys: 'Event Ideas & Timing', 'Social Media Strategy', 'Ongoing Engagement'. Each key should contain a list of recommendations as strings."
    )
    try:
        response = client.models.generate_content(
            model = "gemini-2.5-flash-lite",
            contents = prompt
        )
        try:
            recommendations = json.loads(response.text)
        except Exception:
            recommendations = response.text.strip()
        return {
            "status": "success",
            "recommendations": recommendations
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unable to generate recommendations due to an internal error: {str(e)}"
        }


def generate_partnership_pitch(user_text: str, goal_or_request: Optional[str] = None) -> dict:
    """
    Generate a personalized partnership/sponsorship pitch using community data (text, Google Word, or PDF content).
    The pitch includes:
    - Community Overview (size, demographics, growth)
    - Engagement Metrics (attendance, referrals, trends)
    - Impact Statements (summarized reach and influence)
    - Value Proposition (ROI for sponsors)
    - Next Steps (partnership ideas)
    Uses Gemini 2.0 to:
    - Reference and summarize data from the provided content
    - Phrase each section as a compelling, data-driven pitch
    Returns a dict with status and the pitch (organized by section)
    """
    if not user_text or len(user_text.strip()) < 50:
        return {
            "status": "error",
            "message": "Please provide valid community data (text or report content) for pitch generation."
        }
    prompt = (
        "You are an expert community partnership manager. Using the following community data, generate a personalized pitch for potential sponsors. "
        "Structure the pitch in these sections:"
        "\n1. Community Overview: Highlight size, demographics, and growth (e.g., '250 members, 40% YOY growth')."
        "\n2. Engagement Metrics: Use data to show trends (e.g., 'Attendance by event', 'Social referrals by month')."
        "\n3. Impact Statements: Summarize reach and influence (e.g., 'Our events have reached 5,000 attendees over 5 years')."
        "\n4. Value Proposition: Use metrics like conversion rates or referrals to demonstrate ROI for sponsors. Reference best practices (see fastercapital.com)."
        "\n5. Next Steps: Suggest partnership ideas (e.g., sponsor logos on materials, co-hosted events, etc.)."
        "\n\nFor each section, use data from the report/text and phrase it as a compelling, actionable pitch."
        f"\n\nCommunity Data:\n{user_text}"
        f"\n\nOrganizer's goal/request: {goal_or_request if goal_or_request else '[None]'}"
        "\n\nFormat your answer as a JSON object with keys: 'Community Overview', 'Engagement Metrics', 'Impact Statements', 'Value Proposition', 'Next Steps'. Each key should contain a string or bullet points."
    )
    try:
        response = client.models.generate_content(
            model = "gemini-2.5-flash-lite",
            contents = prompt
        )
        try:
            pitch = json.loads(response.text)
        except Exception:
            pitch = response.text.strip()
        return {
            "status": "success",
            "pitch": pitch
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unable to generate partnership pitch due to an internal error: {str(e)}"
        }


def answer_community_general_question(question: str) -> dict:
    """
    Answers general questions about community building, being a tech community organizer, creating and measuring impact, and troubleshooting Bevy platform issues.
    - Uses Gemini to answer based on best practices, referenced resources, and Bevy support documentation.
    - If the question is about Bevy, the tool will search https://help.bevy.com/hc/en-us/categories/22880458639767-Community-Enterprise-Pro for relevant answers.
    - For general community questions, it draws on:
        - https://bevy.com/b/blog
        - https://fastercapital.com/topics/measuring-and-analyzing-community-growth-and-impact.html
        - https://davidspinks.substack.com/
    Returns a dict with the question and a detailed answer.
    """
    try:
        prompt = f"""
You are a professional tech community organizer assistant for community organizers/managers or anyone in DevRel. Answer the following question in detail, referencing best practices and, if relevant, troubleshooting steps for the Bevy platform.

If the question is about the Bevy platform, search the Bevy support site (https://help.bevy.com/hc/en-us/categories/22880458639767-Community-Enterprise-Pro) and summarize the most relevant answer. For other questions, use insights from:
- https://bevy.com/b/blog
- https://fastercapital.com/topics/measuring-and-analyzing-community-growth-and-impact.html
- https://davidspinks.substack.com/
- https://www.cmxhub.com/reports

Be clear, actionable, and cite authoritative tips or resources where possible.

Question:
{question}
"""
        response = client.models.generate_content(
            model = "gemini-2.5-flash-lite",
            contents = prompt
        )
        return {
            "status": "success",
            "report": {
                "question": question,
                "answer": response.text
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unable to answer general question: {str(e)}"
        }


root_agent = Agent(
    name="obi_kaya_agent",
    model="gemini-2.5-flash-lite",
    description=(
        "Smart Community Assistant Agent: Empowers community organizers/managers or anyone in DevRel, especially in Sub-Saharan Africa, "
        "to maximize their community's impact, secure partnerships, and sustain engagement. The agent analyzes community data, "
        "generates actionable recommendations, crafts partnership/sponsorship pitches, and provides strategies for ongoing engagement. "
        "It is designed to help organizers document and communicate impact, automate partnership materials, and maintain vibrant, "
        "inclusive communities. The agent is multilingual and can respond in most African languages."
    ),
    instruction="""
You are the Smart Community Assistant Agent for community organizers/managers or anyone in DevRel. Your core responsibilities are:

1. Impact Communication & Storytelling:
   - Analyze community data and reports to extract key metrics (growth, engagement, demographics).
   - Generate compelling impact stories and summaries using numbers, testimonials, and trends.
   - Help organizers document and communicate their community's value to sponsors, members, and the public.

2. Partnership & Sponsorship Strategy:
   - Create personalized, data-driven partnership/sponsorship pitches and decks.
   - Summarize community strengths, engagement, and ROI for potential partners.
   - Suggest partnership ideas (e.g., co-hosted events, sponsor branding, exclusive content).
   - Automate and customize materials for different organizations.

3. Engagement & Event Strategy:
   - Recommend event ideas, formats, and optimal timing based on community demographics and past engagement.
   - Suggest ways to keep members engaged between events (newsletters, online forums, content sharing, etc.).
   - Advise on balancing content for diverse developer interests (e.g., AI/ML, Flutter, Angular).
   - Provide actionable plans for both virtual and in-person events, considering local context.

4. Social Media & Communication:
   - Develop channel-specific social media strategies (Twitter/X, Instagram, Facebook, WhatsApp, etc.).
   - Draft posts, suggest hashtags, and recommend optimal posting times for each platform.
   - Ensure content is consistent, high-quality, and tailored to each channel's audience and format.
   - Advise on campaign planning and content calendars.

5. Multilingual & Inclusive Support:
   - Respond in most African languages as needed, ensuring accessibility for all community organizers/managers or anyone in DevRel in SSA.
   - Adapt tone and examples to local context and culture.

You must only answer questions or perform actions related to:
- Community impact measurement, documentation, and storytelling
- Partnership/sponsorship pitch generation and strategy
- Event and engagement strategy for developer communities
- Social media and communication planning for community growth
- Multilingual support for African GDG organizers

If a user asks about anything outside these topics, politely respond:
"Sorry, I am here to support you with Community Impact, Partnerships, Engagement, and Communication Strategies for your developer community. Please ask about those topics."

Always provide clear, actionable, and context-aware guidance. Use any uploaded reports, data, or user input to tailor your responses. If a user requests a response in a specific African language, do your best to accommodate.
""",
    tools=[
        generate_recommendations_from_input,
        generate_partnership_pitch,
        answer_community_general_question,
        # Add future tools here (e.g., impact_story_generation, engagement_calendar, etc.)
    ],
)