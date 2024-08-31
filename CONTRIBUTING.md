# Contributing to Sparta Chat Bot
Thank you for your interest in contributing to Sparta Chat Bot! Your contributions are crucial in enhancing this context-aware Retrieval-Augmented Generation (RAG) assistant designed to improve information retrieval within organizations.

## Getting Started
### 1. Fork the Repository
- Navigate to the Sparta Chat Bot repository on GitHub.
- Click the "Fork" button in the upper right-hand corner.
### 2. Clone Your Fork
- Clone your forked repository to your local machine:
```
git clone https://github.com/your-username/sparta-chat-bot.git
cd sparta-chat-bot
```
### 3. Set Up the Development Environment
- Ensure you have Python 3.8+ installed.
- Create a virtual environment:
```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
- Install the required dependencies:
```
pip3 install -r requirements.txt
```
### 4. Running Sparta Chat Bot Locally
- Set up the necessary environment variables in a .env file:
```
SLACK_API_TOKEN: Your Slack API token.
OPENAI_API_KEY: Your OpenAI endpoint token.
```

- **To fetch Slack conversation history:**

    - Add Sparta Chat Bot to the Slack channel by mentioning ***@Sparta Bot*** and clicking *Add to Channel*.
    - Copy the Channel ID.
    - Run the following command to get your channel's message history:
    ```
    python3 MessageParser.py slack <channel_id>
    ```
- **To start the API and UI:**

    - Start the LLM API:
    ```
    python3 API/SpartaAPI.py
    ```
    *The API is ready when you see **Application Started**.*

    - Start the Sparta Bot website:
    ```
    streamlit run ui.py
    ```
    - Open your browser and go to http://localhost:8501/ to start using the bot.

- **To add documents (e.g., Confluence content):**

    - Add supported files (see the README for supported file types) to the *./documents* folder.
    - Restart the LLM API and UI.

## Contribution Guidelines
### 1. Reporting Bugs
- Search through the existing issues to ensure the bug hasn't been reported.
- Open a new issue with detailed information about the bug, including steps to reproduce, expected behavior, and screenshots if applicable.
### 2. Requesting Features
- Open an issue with the "Feature Request" label.
- Provide a clear and concise description of the feature, explaining its usefulness and potential implementation.
### 3. Making Changes
- Create a new branch for your feature or bugfix:
```
git checkout -b feature/your-feature-name
```
- Write clean, readable, and self-explanatory code.
- Ensure your code adheres to the project's coding standards and includes appropriate tests.
- Commit your changes with meaningful commit messages:
```
git commit -m "Add feature: your feature name"
```
- Push your branch to GitHub:
```
git push origin feature/your-feature-name
```
### 4. Submitting a Pull Request
- Navigate to the original repository and open a "Compare & Pull Request."
- Provide a clear description of the changes, referencing any related issues.
- A maintainer will review your pull request, suggest any necessary changes, and merge it once it's ready.

## Areas for Improvement
The Sparta Chat Bot is a work in progress, and several areas need enhancement:

- Role-Based Access Control (RBAC)
- Persistent Vector Store: Implementing a vector database to retain embeddings for faster data retrieval.
- Confluence and Teams API Integration
- Streamlining Workflow: Simplify the architecture and data population flow.
- Automated Slack Channel Integration
- Support for Multiple Document Uploads

Your contributions in these areas are highly encouraged!

## Code of Conduct
Please review and follow our Code of Conduct to ensure a welcoming and respectful environment for everyone involved.

## License
By contributing to Sparta Chat Bot, you agree that your contributions will be licensed under the project's MIT License.
