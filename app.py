# Import necessary libraries for environment variables, HTTP requests, PDF reading, agent logic, UI, and regex.
from dotenv import load_dotenv
import os
import requests
from pypdf import PdfReader
from agents import Agent, Runner, function_tool
import gradio as gr
import re

# Load environment variables from a .env file, overriding any already set in the environment.
load_dotenv(override=True)

@function_tool
def record_user_details(email: str, name: str = "Name not provided", notes: str = "not provided") -> dict:
    """
    Records the user's email and optional details via a pushover notification.
    This function is registered as a tool for the agent to use.
    Returns a dictionary indicating whether the record was successful.
    """
    message = f"Recording {name} with email {email} and notes {notes}"
    # Send a notification to Pushover with the details.
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": message,
        }
    )
    return {"recorded": "ok"}

@function_tool
def record_unknown_question(question: str) -> dict:
    """
    Records any question the agent cannot answer via a pushover notification.
    This helps track unanswered or out-of-scope queries.
    Returns a dictionary indicating status.
    """
    message = f"Recording unknown question: {question}"
    # Send a notification to Pushover about the unknown question.
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": message,
        }
    )
    return {"recorded": "ok"}

class Me:
    """
    Represents the main agent persona (Utkarsh Patel) for the personal website chatbot.
    Loads personal summary and LinkedIn info, sets up the agent, and provides a chat method.
    """
    def __init__(self):
        self.name = "Utkarsh Patel"
        # Read LinkedIn text from PDF and summary from text file.
        self.linkedin_text = self._read_pdf("me/linkedin.pdf")
        self.summary_text = self._read_txt("me/summary.txt")
        # Build the system prompt with loaded data.
        self.system_prompt = self._build_system_prompt()
        # Create the agent with appropriate tools and prompt.
        self.agent = Agent(
            name="Utkarsh Agent",
            model="gpt-4o",
            tools=[record_user_details, record_unknown_question],
            instructions=self.system_prompt
        )
        # Runner is used to execute agent chat logic.
        self.runner = Runner()

    def _read_pdf(self, path):
        """
        Reads all text from a PDF file at the given path.
        Returns the extracted text as a string.
        """
        try:
            reader = PdfReader(path)
            # Concatenate text from all pages.
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            # Return empty string if file can't be read.
            return ""

    def _read_txt(self, path):
        """
        Reads all text from a TXT file at the given path.
        Returns the file contents as a string.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            # Return empty string if file can't be read.
            return ""

    def _build_system_prompt(self):
        """
        Constructs the system prompt to guide the agent's behavior.
        Includes rules for handling questions and sample Q&A, plus biography info.
        """
        return (
            f"You are acting as {self.name}, engaging visitors on your personal website. "
            f"You answer questions about your career, skills, and experience. "
            f"Be professional and friendly, like you're speaking to a potential client or employer.\n"
            f"IF you receive a question that is NOT about your career, skills, or experience, or if you do NOT know the answer, "
            f"you MUST call the record_unknown_question tool with the question as its argument, and do NOT attempt to answer yourself.\n"
            f"If someone expresses interest or gives an email, record it with record_user_details.\n\n"
            f"## Examples:\n"
            f"Q: What is the time in Boston now?\n"
            f"A: [Call record_unknown_question(question=\"What is the time in Boston now?\")]\n"
            f"Q: How can I contact you?\n"
            f"A: [Call record_user_details(email=..., name=..., notes=...)]\n"
            f"Q: What is your work experience?\n"
            f"A: [Provide answer about career]\n\n"
            f"## Summary:\n{self.summary_text}\n\n"
            f"## LinkedIn:\n{self.linkedin_text}"
        )

    async def chat(self, message, history):
        """
        Main chat method for interacting with the agent.
        - Formats the message history for the agent.
        - Appends the latest user message.
        - Runs the agent to get a response.
        - Extracts and returns the response, handling multiple possible output formats.
        """
        if not history:
            history = []

        # Ensure history is a list of dicts in the expected format for the agent.
        new_history = []
        for h in history:
            # If already a dict, keep only relevant keys.
            if isinstance(h, dict):
                msg = {k: v for k, v in h.items() if k in ("role", "content", "name", "function_call")}
                new_history.append(msg)
            # If it's a 2-tuple or list, convert to dict format.
            elif isinstance(h, (list, tuple)) and len(h) == 2:
                role = "user" if h[0].lower() == "user" else "assistant"
                new_history.append({"role": role, "content": h[1]})

        # Add the latest user message to the conversation.
        messages = new_history + [{"role": "user", "content": message}]
        # Run the agent and get the result.
        result = await self.runner.run(self.agent, messages)

        # Try to extract the agent's response from common attributes.
        if hasattr(result, "final_output"):
            return result.final_output
        if hasattr(result, "output"):
            return result.output
        if hasattr(result, "content"):
            return result.content
        # As a fallback, extract the response from a string using regex.
        match = re.search(r"Final output \(str\):\s*(.+)", str(result))
        if match:
            return match.group(1).strip()
        return "Sorry, could not get a response."

if __name__ == "__main__":
    # Instantiate the Me class, which sets up the agent.
    me = Me()
    # Launch a Gradio chat interface for users to interact with the agent.
    gr.ChatInterface(
        fn=me.chat,
        title="Ask Utkarsh Patel",
        type="messages",
        description="👋 Welcome! Ask me anything about my career, skills, or experience. Please share your Name and email address or phone number to get connected. Thank you!",
        examples=[
            "Tell me about yourself",
            "What is your work experience?",
            "What is your education?",
            "What are your skills?",
            "What are your projects?",
            "what are your expertise?",
            "what are the certifications you have?",
            "I would like to get in touch with you",
            
        ]
    ).launch()