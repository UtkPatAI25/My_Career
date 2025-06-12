# Utkarsh Patel AI Career Chatbot

This project is an AI-powered chatbot for Utkarsh Patel's personal/professional website. It allows visitors to interactively ask questions about Utkarsh’s career, skills, projects, and more, and can securely collect contact information or log out-of-scope questions via Pushover notifications.


![image](https://github.com/user-attachments/assets/4c15fcc6-314d-4175-84c1-b9f7a7afeb72)



---

## Features

- **Conversational AI**: Answers questions about Utkarsh's background, work experience, projects, and skills using custom instructions and context from profile files.
- **Contact Logging**: Captures and notifies via Pushover when users share their email, name, or notes for networking.
- **Unknown Question Logging**: Automatically notifies via Pushover if a question is outside the provided context or cannot be answered.
- **Profile Extraction**: Reads Utkarsh's summary and LinkedIn profile from local files for accurate, updated responses.
- **Modern Web UI**: Utilizes Gradio for a simple, interactive chat interface.

---

## How It Works

1. **Environment Setup**: Loads environment variables (including Pushover API credentials) from a `.env` file.
2. **Agent Tools**: Two agent tools are registered:
   - `record_user_details`: Logs user contact details via Pushover.
   - `record_unknown_question`: Logs questions the agent can't answer via Pushover.
3. **Profile Loading**: On startup, the agent reads `me/linkedin.pdf` and `me/summary.txt` for context.
4. **Agent Instructions**: The agent is guided by a system prompt that encourages professional, relevant, and friendly answers, and routes contact/out-of-scope handling through the proper tools.
5. **Chat Handling**: All chat history is managed for context, and agent responses are robustly extracted.
6. **Web Interface**: Gradio presents an easy-to-use chat UI for user interaction.

---

## Getting Started

### Prerequisites

- Python 3.10+
- [Pushover account](https://pushover.net/) (for notifications)
- Required Python packages:
  - `python-dotenv`
  - `requests`
  - `pypdf`
  - `gradio`
  - Custom agent framework (must provide `Agent`, `Runner`, and `function_tool`)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/UtkPatAI25/My_Career.git
   cd My_Career
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your `.env` file**

   Create a `.env` file in the root directory with:
   ```

   PUSHOVER_TOKEN=your_pushover_app_token
   PUSHOVER_USER=your_pushover_user_key
   OPENAI_API_KEY=your_openai_api_key
   ```

4. **Add profile files**

   - Place your LinkedIn PDF at `me/linkedin.pdf`
   - Place your summary text at `me/summary.txt`

---

## Usage

To launch the chatbot, simply run:

```bash
python app.py
```

The Gradio interface will be available locally (by default at http://localhost:7860).

---

## Example Questions

- "Tell me about yourself"
- "What is your work experience?"
- "What is your education?"
- "What are your skills?"
- "What are your projects?"
- "what are your expertise?"
- "what are the certifications you have?"
- "I would like to get in touch with you"

---

## File Structure

```
My_Career/
├── app.py
├── requirements.txt
├── .env
└── me/
    ├── linkedin.pdf
    └── summary.txt
```

---

## Security & Privacy

- Contact and unknown questions are sent via Pushover notification and are not stored elsewhere.
- Keep your `.env` file private and do not commit it to public repositories.

---

## Customization

- **Agent Prompt**: Edit the `_build_system_prompt()` method in `app.py` for different behaviors or instructions.
- **New Tools**: Add new tool functions and decorate them with `@function_tool` to extend agent capabilities.
- **UI**: Change Gradio settings in the `__main__` block for a customized user experience.

---

## License

MIT (or as specified)

---

## Credits

Developed by Utkarsh Patel.  
Powered by Python, Gradio, and Pushover.
