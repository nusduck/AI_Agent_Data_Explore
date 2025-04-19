# 🤖 AI Agent Data Explore

A powerful, user-friendly **Streamlit** application for end-to-end data analysis and exploration—with AI-powered insights.

## ✨ Features
- **📂 Data Upload:** Easily upload CSV, Excel, or JSON files  
- 😈 **Model Setting:** Easily choose the right model  
- **🔍 Data Overview:** Instantly view data statistics, samples, and descriptive info  
- **⚙️ Analysis Target:** Define your analysis goals (*default:* “help me explore the data, show the insights”)  
- **🗺️ Analysis Plan:** Review the generated plan and give your feedback  
- **📊 Result Viewer:** Browse historical analysis reports & visualizations  
- **⭐ Evaluation:** Rate the quality and relevance of the analysis  

---

## 💡 UI Flow  
![image-20250419091330960](http://hexo.kygoho.win/upload/uploads/a99aa585-d745-4f59-b910-416a3ee4cf30.png)

[Visit the UI](https://app.uizard.io/p/65bf10b5)

## 🕸️ Agents Graph  
![image-20250417201155362](http://hexo.kygoho.win/upload/uploads/1a85a006-a525-4093-a344-4779e8a6159e.png)

---

## 🚀 Quick Start

### 📦 Local Installation

1. **Clone the Repo:**
   ```bash
   git clone https://github.com/nusduck/AI_Agent_Data_Explore.git
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key:**
   Create and edit `.env` file:
   ```env
   OPENAI_API_KEY=Your_API_KEY
   LANGSMITH_API_KEY=Your_API_KEY
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
   LANGSMITH_PROJECT=Your_LangSmith_project
   TAVILY_API_KEY=Your_API_KEY
   DEEPSEEK_API_KEY=Your_API_KEY
   GOOGLE_API_KEY=Your_API_KEY
   ```

4. **Run Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

5. Open [http://localhost:8501](http://localhost:8501) in your browser.

---

### 🐳 Deploy with Docker Compose

> **Recommended for easy deployment and isolation**

1. **Create a `.env` file in the project root:**
   ```env
   OPENAI_API_KEY=Your_API_KEY
   LANGSMITH_API_KEY=Your_API_KEY
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
   LANGSMITH_PROJECT=Your_LangSmith_project
   TAVILY_API_KEY=Your_API_KEY
   DEEPSEEK_API_KEY=Your_API_KEY
   GOOGLE_API_KEY=Your_API_KEY
   ```

2. **Prepare local directories:**
   ```bash
   mkdir -p data outputs
   ```

3. **Use the docker-compose.yml below:**
   ```yaml
   version: '3.8'
   services:
     ai_agent:
       image: iamaduck/ai_agent:latest
       container_name: ai_agent
       ports:
         - "8501:8501"
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
2. Choose the model you want  
3. Review the automatically generated data summary  
4. Optionally, adjust the analysis target  
5. Click **Start Analysis**  
6. Inspect the proposed analysis plan and refine as needed  
7. View reports & visualizations in the “Analysis Results” panel  
8. View the report quality in Evaluation panel  

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

## 🔮 Future Improvements

 1. **Code Review in Evaluation Phase**
- **Current:** Analysis quality is evaluated only via LLM.
- **Improvement:** Integrate code review during the evaluation stage to make comprehensively assess
- **Benefit:**  Reproduce using code

 2. **From Static to Interactive Visualizations**
- **Current:** Visuals are static (matplotlib, seaborn).
- **Improvement:** Adopt interactive libraries such as **Plotly** or **Altair** with zoom, hover, filtering, etc.
- **Benefit:** Boosts user experience and supports deeper insight exploration.

 3. **Architecture Shift: Plan-Execute ➜ Supervisor-Team Collaboration**
- **Current:**  `Plan(Replan) ➝ Execute ➝ Report` structure.
- **Improvement:** Adopt a **Supervisor + Specialized Agent Team** structure:
  - **Supervisor:** Understands user intent, allocates sub-tasks.
  - **Team Members:** EDA agent, modeling agent, visualization agent, reporting agent, evaluating agent etc.
- **Benefit:** Supports parallelism, dynamic re-planning, multi-agent cooperation.

 4. **User Memory Integration**
- **Current:** No permenent memory—preferences.
- **Improvement:** Add permenent memory modules.
- **Benefit:** Enables **personalized** and **continually evolving** AI analysis experience.