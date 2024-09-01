# Sparta Chat Bot
This bot is a context-aware Retrieval-Augmented Generation (RAG) assistant designed to enhance information retrieval within organizations. By integrating with Slack channels, Confluence wiki pages and Teams (TBD), the bot delivers precise, contextually relevant answers to user queries, leveraging OpenAI GPT-4o.

Supported file extensions:
- .txt - text only
- .csv - comma-separated values
- .docx - Microsoft Word
- .epub - EPUB ebook format
- .hwp - Hangul Word Processor
- .ipynb - Jupyter Notebook
- .jpeg, .jpg - JPEG image
- .mbox - MBOX email archive
- .md - Markdown
- .mp3, .mp4 - audio and video
- .pdf - Portable Document Format
- .png - Portable Network Graphics
- .ppt, .pptm, .pptx - Microsoft PowerPoint
- .json - JavaScript Object Notation

[Referenced from LlamaIndex SimpleDirectoryReader](https://docs.llamaindex.ai/en/stable/module_guides/loading/simpledirectoryreader/)
 
# Install required modules
`pip3 install -r requirements.txt`

# Secrets required
1) Slack API Token
2) OpenAI endpoint token
Put these in a `.env` file.

# How to Run
Note: `ignore.txt` must be present in the `./documents` folder (To be fixed).
## Slack
1) In the channel you want to fetch your conversation history, @Sparta Bot, hit Enter then click on Add to Channel.
2) Copy the Channel ID.
3) Run `python3 MessageParser.py slack <channel_id>` to get your channel's message history.
4) Run `fastapi dev API/SpartaAPI.py` to start LLM API. The API is done launching once you see `Application Started`.
5) Run `streamlit run ui.py` to host the Sparta Bot website.
6) In your browser, go to http://localhost:8501/ and start using the bot!

## Documents (i.e. Confluence)
1) Add supported file to `./documents` folder.
2) Run `fastapi dev API/SpartaAPI.py` to start LLM API. The API is done launching once you see `Application Started`.
3) Run `streamlit run ui.py` to host the Sparta Bot website.
4) In your browser, go to http://localhost:8501/ and start using the bot!

If you want to add confluence documentation, go to the wiki page and export it as PDF or Docs
Check that PDF is not blank - Observed that for a wiki, it would give a blank PDF.

# Improvements 
1) Role Based Access Control (RBAC) 
2) Vector store (in memory) is being refreshed everytime a new item is added so it clears memory of the embeddings it already generated. For efficency, having a dedicated vector database that is just appending new information would be significantly faster.
3) APIs for confluence and teams are not implemented. Should be added in future for automation.
4) Architecture and workflow for this entire ai can be significantly streamlined. 
5) Automate the flow of data population - Constantly fetch latest info
6) Enable adding of multiple documents. Currently can only add one at a time in through the UI 
7) Automate adding Sparta Bot to Slack Channels

# Team
Mostafa Yassine, Svetlana Esina, Miten Soni, Omar Aly, Joon Lee - TrendMicro HackDay 24
