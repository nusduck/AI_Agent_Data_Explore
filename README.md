# 🤖 AI Agent Data Explore
A powerful, user-friendly **Streamlit** application for end-to-end data analysis and exploration—with AI-powered insights.

## ✨ Features
- **📂 Data Upload:** Easily upload CSV, Excel, or JSON files
- **🔍 Data Overview:** Instantly view data statistics, samples, and descriptive info
- **⚙️ Analysis Target:** Define your analysis goals (*default:* “help me explore the data, show the insights”)
- **🗺️ Analysis Plan:** Review the generated plan and give your feedback
- **📊 Result Viewer:** Browse historical analysis reports & visualizations
- **⭐ Evaluation:** Rate the quality and relevance of the analysis
---
## 💡 UI Flow
![UI Flow](http://hexo.kygoho.win/upload/uploads/4fae295c-4e11-4603-918d-cc8ae028f8ac.png)
## 🕸️ Agents Graph
![image-20250413221203748](http://hexo.kygoho.win/upload/uploads/623a4c71-f49d-41a7-894f-cf65a300c818.png)
---
## 🚀 Quick Start
### 📦 Local Installation
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Set up API key:**
   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```
3. **Run Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```
4. Visit [http://localhost:8501](http://localhost:8501) in your browser.
---
### 🐳 Deploy with Docker Compose
> **Recommended for easy deployment and isolation**
1. **Create a `.env` file in the project root:**
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
2. **Prepare local directories:**
   ```
   mkdir -p data outputs
   ```
3. **Use the docker-compose.yml below:**
   <details>
   <summary> Docker <img src="https://img.icons8.com/color/24/000000/docker.png" width="18"/></summary>
   </details>
   ```
   version: '3.8'
   services:
     ai_agent:
       image: iamaduck/ai_agent:latest
       container_name: ai_agent
       ports:
         - "8501:8501"   # Streamlit UI
       volumes:
         - ./.env:/app/.env
         - ./data:/app/data
         - ./outputs:/app/outputs
       restart: unless-stopped
       environment:
         - PYTHONUNBUFFERED=1
   ```
4. **Start the application:**
   ```bash
   docker-compose up -d
   ```
5. Open [http://localhost:8501](http://localhost:8501) in your browser.
---
## 🔁 Full Workflow
1. Upload your data file via the sidebar
2. Review the automatically generated data summary
3. Optionally, adjust the analysis target
4. Click **Start Analysis**
5. Inspect the proposed analysis plan and refine as needed
6. View reports & visualizations in the “Analysis Results” panel
7. Evaluate report quality to improve future outputs
---
## 📑 Notes & Tips
- All reports are stored in `outputs/{uuid}/`
- Switch between different analysis runs using the dropdown in Results
- Multi-panel grid visualizations for easy exploration and comparison
- Feedback on analysis results is highly encouraged!
---
## 🧩 Tech Stack
- ![streamlit logo](https://img.icons8.com/color/24/000000/streamlit.png) **Streamlit**
- ![python logo](https://img.icons8.com/color/24/000000/python.png) **Python 3.11+**
- ![docker logo](https://img.icons8.com/color/24/000000/docker.png) **Docker (optional)**
---
Enjoy exploring your data with AI-driven analysis! 🚀
