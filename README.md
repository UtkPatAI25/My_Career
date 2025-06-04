# Utkarsh Patel Personal AI Chatbot

This project is an AI-powered chatbot for Utkarsh Patel's personal website. Visitors can ask questions about Utkarsh's career, skills, experience, and more. The chatbot uses a custom agent framework, integrates with Gradio for the chat UI, and can send notifications via Pushover when a user shares contact details or asks an out-of-scope question.

---

## Features

- **Conversational AI**: Answers questions about Utkarsh's career, skills, experience, and projects.
- **Contact Collection**: Records user contact info (email, name, notes) via Pushover notifications.
- **Unknown Question Logging**: Notifies via Pushover if a question is out of scope or cannot be answered.
- **PDF/Text Profile Extraction**: Reads summary and LinkedIn information from provided files for accurate, up-to-date responses.
- **Gradio Chat UI**: User-friendly web interface for real-time chat.

---

## How It Works

1. **Environment Setup**: Loads credentials (like Pushover tokens) from a `.env` file using `python-dotenv`.
2. **Agent Tools**: Two main tools are available to the agent:
   - `record_user_details`: Records a visitor's contact information.
   - `record_unknown_question`: Logs questions the agent can't answer.
3. **Persona Loading**: On startup, reads Utkarsh's summary (`me/summary.txt`) and LinkedIn profile (`me/linkedin.pdf`) for context.
4. **System Prompt**: The agent is instructed to answer only relevant questions and log/record as specified.
5. **Chat Handling**: All chat history is managed and formatted for the agent, and responses are extracted in a robust way.
6. **Web UI**: Gradio is used to make the chatbot accessible via a simple web interface.

---

## Getting Started

### Prerequisites

- Python 3.8+
- [Pushover account](https://pushover.net/) for notifications
- Required Python packages:
  - `python-dotenv`
  - `requests`
  - `pypdf`
  - `gradio`
  - Agent framework containing `Agent`, `Runner`, and `function_tool`

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your `.env` file**

   Create a `.env` file in the project root with your Pushover credentials:

   ```
   PUSHOVER_TOKEN=your_pushover_app_token
   PUSHOVER_USER=your_pushover_user_key
   ```

4. **Add profile files**

   - Place your LinkedIn PDF at `me/linkedin.pdf`
   - Place your summary text at `me/summary.txt`

### Running the Chatbot

Run the main Python file:

```bash
python main.py
```

This will launch a Gradio web interface (by default at `http://localhost:7860`) where users can interact with the chatbot.

---

## File Structure

```
your-repo/
├── main.py
├── agents.py
├── requirements.txt
├── .env
└── me/
    ├── linkedin.pdf
    └── summary.txt
```

---

## Usage

- Ask about Utkarsh's career, skills, education, projects, or certifications.
- If you want to get in touch, provide your email or phone—your details will be recorded securely.
- Any out-of-scope questions will be logged for review, but not answered directly.

---

## Example Questions

- "Tell me about yourself"
- "What is your work experience?"
- "What is your education?"
- "What are your skills?"
- "What are your projects?"
- "What are your certifications?"
- "I would like to get in touch with you"

---

## Security & Privacy

- Contact details and unknown questions are sent via Pushover notifications and are not stored elsewhere.
- Make sure to secure your `.env` file and do not commit it to public repositories.

---

## Customization

- **Agent Behavior**: Modify the system prompt in `Me._build_system_prompt()` to change how the agent responds.
- **Add New Tools**: Decorate new functions with `@function_tool` to provide more capabilities to the agent.
- **UI**: Adjust Gradio interface options in the `__main__` block as needed.

---

## License

[MIT](LICENSE) (update as appropriate)

---

## Credits

Developed by Utkarsh Patel.  
Powered by Python, Gradio, and Pushover.
