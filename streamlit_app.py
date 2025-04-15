import streamlit as st
import pandas as pd
import os
import glob
import uuid
import traceback
from langgraph.types import Command
from core.graph import workflow
from core.state import GraphState
from utils.data_loader import DataLoader

# Set page config and apply custom CSS for a futuristic look
st.set_page_config(page_title="Data Analysis Assistant", layout="wide")

# Custom CSS for futuristic styling with better visibility
st.markdown("""
<style>
    /* Main theme colors - lighter futuristic palette for better visibility */
    :root {
        --bg-color: #f8f9fa;
        --text-color: #212529;
        --accent-color: #0466c8;
        --accent-hover: #0353a4;
        --secondary-bg: #ffffff;
        --border-color: #dee2e6;
        --success-color: #38b000;
        --warning-color: #ee9b00;
        --danger-color: #d90429;
    }
    
    /* Overall styling */
    .main {
        background-color: var(--bg-color);
        color: var(--text-color);
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: var(--accent-color) !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 1.5rem !important;
        background: linear-gradient(90deg, #0466c8, #48cae4);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        text-shadow: none !important;
    }
    
    /* Cards and containers */
    .stExpander, div[data-testid="stExpander"] {
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        background-color: var(--secondary-bg) !important;
        overflow: hidden !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }
    
    /* Give dataframes a sleek look */
    .dataframe {
        border-radius: 8px !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, var(--accent-color), #48cae4) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 4px 10px rgba(4, 102, 200, 0.3) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(4, 102, 200, 0.4) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: var(--secondary-bg) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    
    /* File uploader */
    .stUploadButton>button {
        background-color: var(--secondary-bg) !important;
        border: 2px dashed var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    /* Progress bars and spinners */
    .stProgress > div > div {
        background-color: var(--accent-color) !important;
    }
    
    /* Success/error/info/warning messages */
    .element-container [data-testid="stAlert"] {
        border-radius: 8px !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }
    
    /* Image display */
    img {
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        margin: 1rem 0 !important;
        transition: transform 0.3s !important;
        border: 1px solid var(--border-color) !important;
    }
    
    img:hover {
        transform: scale(1.02) !important;
    }
    
    /* Text areas */
    .stTextArea textarea {
        background-color: var(--secondary-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-color) !important;
    }
    
    /* Markdown text */
    .markdown-text-container {
        padding: 1rem !important;
        background-color: var(--secondary-bg) !important;
        border-radius: 8px !important;
        border-left: 3px solid var(--accent-color) !important;
        margin: 1rem 0 !important;
        color: var(--text-color) !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }
    
    /* Fancy radio buttons for feedback */
    .fancy-radio {
        display: flex;
        gap: 12px;
        margin: 20px 0;
    }
    
    .fancy-radio-option {
        flex: 1;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        border: 2px solid transparent;
        transition: all 0.3s;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .fancy-radio-option:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    
    .fancy-radio-option.selected {
        border-color: var(--accent-color);
        background: linear-gradient(145deg, #e6f2ff, #cce4ff);
        box-shadow: 0 4px 12px rgba(4, 102, 200, 0.2);
    }
    
    .fancy-radio-icon {
        font-size: 24px;
        margin-bottom: 8px;
    }
    
    .fancy-radio-label {
        font-weight: 600;
    }
    
    /* Override stRadio default styling */
    div[data-testid="stRadio"] {
        visibility: hidden;
        height: 0;
        position: absolute;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--secondary-bg) !important;
        border-radius: 8px 8px 0 0 !important;
        border: 1px solid var(--border-color) !important;
        border-bottom: none !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--accent-color) !important;
        color: white !important;
    }
</style>

<!-- JavaScript for custom radio buttons and tab switching -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Initialize custom radio buttons
    function setupCustomRadios() {
        const radioContainer = document.querySelector('div[data-testid="stRadio"]');
        if (!radioContainer) return;
        
        const options = radioContainer.querySelectorAll('input[type="radio"]');
        if (!options.length) return;
        
        const fancyRadio = document.createElement('div');
        fancyRadio.className = 'fancy-radio';
        
        options.forEach((option, i) => {
            const isChecked = option.checked;
            const label = option.nextElementSibling.textContent;
            
            const fancyOption = document.createElement('div');
            fancyOption.className = `fancy-radio-option${isChecked ? ' selected' : ''}`;
            fancyOption.setAttribute('data-value', i);
            
            const icon = document.createElement('div');
            icon.className = 'fancy-radio-icon';
            icon.innerHTML = i === 0 ? '👍' : '✏️';
            
            const textLabel = document.createElement('div');
            textLabel.className = 'fancy-radio-label';
            textLabel.textContent = label;
            
            fancyOption.appendChild(icon);
            fancyOption.appendChild(textLabel);
            fancyRadio.appendChild(fancyOption);
            
            fancyOption.addEventListener('click', function() {
                options[i].click();
                document.querySelectorAll('.fancy-radio-option').forEach(el => {
                    el.classList.remove('selected');
                });
                this.classList.add('selected');
            });
        });
        
        // Insert our custom radio after the original
        radioContainer.parentNode.insertBefore(fancyRadio, radioContainer.nextSibling);
    }
    
    // Check if we need to switch tabs
    function checkForTabSwitch() {
        if (window.sessionStorage.getItem('switch_to_results') === 'true') {
            // Find the results tab and click it
            const tabs = document.querySelectorAll('[data-baseweb="tab"]');
            if (tabs.length >= 3) {
                tabs[2].click(); // Click the third tab (Results)
                window.sessionStorage.removeItem('switch_to_results');
            }
        }
    }
    
    // Run our setup with a slight delay to ensure DOM is ready
    setTimeout(() => {
        setupCustomRadios();
        checkForTabSwitch();
        
        // Set up a MutationObserver to watch for DOM changes
        const observer = new MutationObserver(() => {
            setupCustomRadios();
            checkForTabSwitch();
        });
        
        observer.observe(document.body, { 
            childList: true, 
            subtree: true 
        });
    }, 1000);
});
</script>
""", unsafe_allow_html=True)

# Initialize DataLoader
data_loader = DataLoader()

# App title and description
st.title("Data Analysis Assistant")
st.markdown("""
<div class="markdown-text-container">
    <p>Upload your dataset, define your analysis target, and get AI-powered insights instantly.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for uploading data and configuring analysis
with st.sidebar:
    st.header("Data Upload")
    
    uploaded_file = st.file_uploader("Choose a data file", type=["csv", "xlsx", "xls", "json"])
    
    if uploaded_file is not None:
        # Save the uploaded file
        file_extension = uploaded_file.name.split(".")[-1]
        temp_file_path = f"data/temp_upload.{file_extension}"
        os.makedirs("data", exist_ok=True)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Load the data
        df, error = data_loader.load_data(temp_file_path)
        
        if error:
            st.error(f"Error loading data: {error}")
        else:
            st.success(f"✅ {uploaded_file.name} loaded successfully")
            st.session_state.df = df
            st.session_state.data_path = temp_file_path
    # Add GitHub link
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <a href="https://github.com/nusduck/AI_Agent_Data_Explore" target="_blank" style="text-decoration: none;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; padding: 8px 16px; background: linear-gradient(90deg, #0466c8, #48cae4); color: white; border-radius: 25px; font-weight: 600; box-shadow: 0 4px 10px rgba(4, 102, 200, 0.3);">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                </svg>
                View on GitHub
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Function to switch to results tab
def switch_to_results_tab():
    # Use session storage to communicate with JavaScript
    st.markdown("""
    <script>
        window.sessionStorage.setItem('switch_to_results', 'true');
        window.location.reload();
    </script>
    """, unsafe_allow_html=True)

# Initialize session state for tab tracking
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0

# Main content area with tabs
if 'df' in st.session_state:
    # Create tabs for better organization
    tabs = ["📊 Data Exploration", "🔍 Analysis", "📈 Results", "🧪 Evaluation"]
    active_tab = st.session_state.get('active_tab', 0)
    tab1, tab2, tab3, tab4 = st.tabs(tabs)
    
    with tab1:
        # Data information tab
        st.header("Data Information")
        
        # Quick stats in a nice layout
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", f"{len(st.session_state.df):,}")
        col2.metric("Columns", f"{len(st.session_state.df.columns):,}")
        col3.metric("Memory Usage", f"{st.session_state.df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB")
        
        data_info_expander = st.expander("View Detailed Data Information", expanded=False)
        with data_info_expander:
            # Display basic data info
            st.subheader("Data Description")
            data_description = data_loader.generate_data_description(st.session_state.df)
            st.markdown(f"""
            <div class="markdown-text-container">
                {data_description.replace('\n', '<br>')}
            </div>
            """, unsafe_allow_html=True)
            
            # Display sample data
            st.subheader("Data Sample")
            st.dataframe(st.session_state.df.head(), use_container_width=True)
            
            # Display detailed data info as fancy tables instead of JSON
            st.subheader("Detailed Data Information")
            detailed_info = data_loader.get_data_info(st.session_state.df)
            
            # Basic info as a dataframe
            basic_info = {
                "Metric": ["Number of Rows", "Number of Columns", "Memory Usage (bytes)"],
                "Value": [
                    detailed_info["num_rows"], 
                    detailed_info["num_columns"],
                    detailed_info["memory_usage"]
                ]
            }
            st.dataframe(pd.DataFrame(basic_info), use_container_width=True)
            
            # Columns info as a dataframe
            columns_info = []
            for col in detailed_info["column_names"]:
                col_type = detailed_info["dtypes"][col]
                missing = detailed_info["missing_values"][col]
                missing_pct = (missing / detailed_info["num_rows"]) * 100 if detailed_info["num_rows"] > 0 else 0
                
                columns_info.append({
                    "Column": col,
                    "Type": col_type,
                    "Missing Values": missing,
                    "Missing %": f"{missing_pct:.2f}%"
                })
            
            st.dataframe(pd.DataFrame(columns_info), use_container_width=True)
            
            # Display numeric stats if available
            if "numeric_stats" in detailed_info:
                st.subheader("Numeric Column Statistics")
                numeric_stats = []
                for col, stats in detailed_info["numeric_stats"].items():
                    numeric_stats.append({
                        "Column": col,
                        "Min": stats["min"],
                        "Max": stats["max"],
                        "Mean": stats["mean"],
                        "Median": stats["median"],
                        "Std Dev": stats["std"]
                    })
                st.dataframe(pd.DataFrame(numeric_stats), use_container_width=True)
            
            # Display categorical stats if available
            if "categorical_stats" in detailed_info:
                st.subheader("Categorical Column Statistics")
                for col, stats in detailed_info["categorical_stats"].items():
                    st.write(f"**{col}** - Unique Values: {stats['unique_values']}")
                    top_values_df = pd.DataFrame(
                        {"Value": list(stats["top_values"].keys()), 
                        "Count": list(stats["top_values"].values())}
                    )
                    st.dataframe(top_values_df, use_container_width=True)
    
    with tab2:
        # Analysis configuration
        st.header("Analysis Configuration")
        
        st.markdown("""
        <div class="markdown-text-container">
            <p>Describe what you want to learn from your data. Be specific or keep it open-ended.</p>
        </div>
        """, unsafe_allow_html=True)
        
        default_target = "help me explore the data, show the insights"
        analysis_target = st.text_area("Enter your analysis target", value=default_target, height=100)
        
        # Analysis execution
        col1, col2 = st.columns([1, 3])
        with col1:
            start_analysis = st.button("Start Analysis")
        
        # Store workflow state
        if start_analysis:
            try:
                # Generate a unique ID for this analysis run
                session_id = uuid.uuid4()
                st.session_state.number = session_id
                
                # Initialize graph state
                state = GraphState(
                    target=analysis_target,
                    number=session_id,
                    raw_data_path=st.session_state.data_path,
                    raw_data_description=data_loader.generate_data_description(st.session_state.df),
                    raw_data_samples=data_loader.get_data_samples(st.session_state.df).to_dict(),
                    pending_human_input=False
                )
                
                # Configure thread
                thread_config = {"configurable": {"thread_id": str(session_id)}}
                
                # Invoke workflow
                with st.spinner("🧠 Generating analysis plan..."):
                    result = workflow().invoke(state, config=thread_config)
                    st.session_state.thread_config = thread_config
                    st.session_state.analysis_plan = result.get("analysis_plan", "No analysis plan was generated.")
                
                # Store the session ID for result retrieval
                st.session_state.session_id = session_id
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                st.session_state.error = str(e)
                st.session_state.traceback = traceback.format_exc()
        
        # Display analysis plan if available
        if 'analysis_plan' in st.session_state:
            st.header("Analysis Plan")
            
            st.markdown(f"""
            <div class="markdown-text-container">
                {st.session_state.analysis_plan.replace('\n', '<br>')}
            </div>
            """, unsafe_allow_html=True)
            
            # User feedback with improved logic - using standard radio but will be styled with JS
            st.subheader("Your Feedback")
            
            # Replace radio buttons with a clearer button-based approach
            st.write("Choose your action:")
            col_go, col_edit = st.columns(2)
            
            with col_go:
                go_button = st.button("👍 Go with this plan", use_container_width=True)
            
            with col_edit:
                edit_button = st.button("✏️ Edit the plan", use_container_width=True)
            
            # Initialize session state for tracking the selected action if not already done
            if "feedback_action" not in st.session_state:
                st.session_state.feedback_action = None
            
            # Update session state based on button clicks
            if go_button:
                st.session_state.feedback_action = "go"
                st.session_state.user_feedback = "Proceed with the plan as is."
            
            if edit_button:
                st.session_state.feedback_action = "edit"
            
            # Show input field if "Edit" is selected
            if st.session_state.feedback_action == "edit":
                user_feedback = st.text_area("Provide your edits or feedback", height=100)
                if user_feedback:
                    st.session_state.user_feedback = user_feedback
            
            feedback_col1, feedback_col2 = st.columns([1, 3])
            with feedback_col1:
                # Only show Submit button if an action is selected
                submit_feedback = st.button("Submit Feedback") if st.session_state.feedback_action else False
            
            if submit_feedback:
                try:
                    with st.spinner("🧠 Processing your feedback..."):
                        # Resume workflow with user feedback, passing both action and review
                        final_result = workflow().invoke(
                            Command(resume={"action": st.session_state.feedback_action, "review": st.session_state.user_feedback}), 
                            config=st.session_state.thread_config
                        )
                        st.session_state.evaluation_results = final_result.get("evaluation_results", "No evaluation results available.")
                        st.success("Analysis complete! View your results now.")
                        
                        # Add a button to jump to results
                        if st.button("View Results"):
                            switch_to_results_tab()
                        
                        # Also set flag for auto-switching
                        st.session_state.active_tab = 2  # Index of results tab
                        switch_to_results_tab()
                        
                except Exception as e:
                    st.warning(f"Note: There was an issue processing your feedback: {str(e)}")
    
    with tab3:
        # Results section
        st.header("Analysis Results")
        
        # Show error details if available (but don't stop showing results)
        if 'error' in st.session_state:
            with st.expander("View Error Details", expanded=False):
                st.error(st.session_state.error)
                st.code(st.session_state.traceback)
        
        # Automatically show current session results instead of selection
        current_session_id = str(st.session_state.session_id) if 'session_id' in st.session_state else None
        
        if current_session_id:
            # Look for results directories
            results_dir = f"outputs/{current_session_id}"
            
            if os.path.isdir(results_dir):
                st.success(f"🎉 Showing results for current analysis")
                
                # Check for analysis report in multiple locations - recursive search for .md files
                md_files = []
                for root, _, files in os.walk(results_dir):
                    for file in files:
                        if file.endswith('.md'):
                            md_files.append(os.path.join(root, file))
                csv_files = []
                txt_files = []
                for root, _, files in os.walk(results_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            csv_files.append(os.path.join(root, file))
                        elif file.endswith('.txt'):
                            txt_files.append(os.path.join(root, file))
                
                if md_files or csv_files or txt_files:
                    st.subheader("Analysis Reports")
                    
                    # Display all found markdown files with clear headings
                    for md_file in md_files:
                        report_name = os.path.basename(md_file).replace('.md', '').replace('_', ' ').title()
                        # st.markdown(f"#### {report_name}")
                        
                        # Read and display the markdown content
                        try:
                            with open(md_file, 'r') as f:
                                report_content = f.read()
                                # Use st.markdown for proper rendering of md files
                                st.markdown(report_content)
                        except Exception as e:
                            st.error(f"Error reading {report_name}: {str(e)}")
                    
                    # Look for CSV and TXT files - add after markdown display
                    
                    
                    if csv_files or txt_files:
                        st.subheader("Result Appendix")
                        
                        # Display CSV files as dataframes
                        for csv_file in csv_files:
                            file_name = os.path.basename(csv_file).replace('.csv', '').replace('_', ' ').title()
                            st.markdown(f"##### {file_name}")
                            try:
                                df = pd.read_csv(csv_file)
                                st.dataframe(df, use_container_width=True)
                            except Exception as e:
                                st.error(f"Error reading CSV file {file_name}: {str(e)}")
                        
                        # Display TXT files as text
                        for txt_file in txt_files:
                            file_name = os.path.basename(txt_file).replace('.txt', '').replace('_', ' ').title()
                            st.markdown(f"##### {file_name}")
                            try:
                                with open(txt_file, 'r') as f:
                                    txt_content = f.read()
                                    st.text_area(label="", value=txt_content, height=300, disabled=True)
                            except Exception as e:
                                st.error(f"Error reading TXT file {file_name}: {str(e)}")
                else:
                    # If no report is found, check if analysis is still running
                    st.info("Analysis is currently running. Results will appear here when complete.")
                
                # Display visualizations - check multiple possible paths
                viz_dirs = [
                    f"{results_dir}/visualization/",
                    f"{results_dir}/visualizations/",
                    f"{results_dir}/viz/",
                    f"{results_dir}/images/"
                ]
                
                viz_files = []
                for viz_dir in viz_dirs:
                    if os.path.exists(viz_dir):
                        viz_files.extend(glob.glob(f"{viz_dir}*.png"))
                        viz_files.extend(glob.glob(f"{viz_dir}*.jpg"))
                        viz_files.extend(glob.glob(f"{viz_dir}*.jpeg"))
                
                if viz_files:
                    st.subheader("Visualizations")
                    
                    # Create a grid layout for visualizations
                    cols = st.columns(2)
                    for i, viz_file in enumerate(viz_files):
                        with cols[i % 2]:
                            filename = os.path.basename(viz_file)
                            caption = filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', '').replace('_', ' ')
                            st.image(viz_file, caption=caption)
                elif md_files:
                    # Only show this message if we have a report but no visualizations
                    st.info("No visualizations were generated for this analysis.")
            else:
                # Provide a better message while waiting for results
                st.info("Your analysis is running. Results will appear here automatically when complete.")
                st.markdown("""
                <div class="markdown-text-container">
                    <p>The AI is currently analyzing your data. This process typically takes 1-2 minutes.</p>
                    <p>When complete, your results will appear here automatically.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Add a refresh button
                if st.button("Refresh Results"):
                    st.rerun()
    
    # Add a new tab for evaluation results
    with tab4:
        st.header("Evaluation Results")
        
        if 'evaluation_results' in st.session_state:
            st.markdown("""
            <div class="markdown-text-container">
                <p>Below are the evaluation results of the analysis.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display evaluation results in markdown format
            evaluation_results = st.session_state.evaluation_results
            st.markdown(evaluation_results)
        else:
            st.info("Evaluation results will appear here after the analysis is complete.")
            st.markdown("""
            <div class="markdown-text-container">
                <p>The evaluation provides metrics and insights about the quality and reliability of the analysis.</p>
                <p>Run a complete analysis to see the evaluation results.</p>
            </div>
            """, unsafe_allow_html=True)
else:
    # Welcome screen with instructions
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 70vh; flex-direction: column;">
        <div style="text-align: center; max-width: 600px; margin: auto; padding: 2rem; background-color: #ffffff; border-radius: 12px; border: 1px solid #dee2e6; box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
            <h2 style="margin-bottom: 1.5rem;">Welcome to the Data Analysis Assistant</h2>
            <p style="margin-bottom: 2rem; font-size: 1.1rem; color: #212529;">Upload your dataset using the sidebar to get started with AI-powered data analysis.</p>
            <div style="display: flex; justify-content: center;">
                <div style="background: linear-gradient(90deg, #0466c8, #48cae4); padding: 8px 16px; border-radius: 25px; font-weight: 600; display: inline-flex; align-items: center; box-shadow: 0 4px 10px rgba(4, 102, 200, 0.3); color: white;">
                    <span style="margin-right: 8px;">👈</span> Upload a Dataset
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)