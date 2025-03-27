from langchain_community.tools.tavily_search import TavilySearchResults

def create_web_search_tool():
    web_search_tool = TavilySearchResults(max_results=5)
    return web_search_tool

if __name__ == "__main__":
    web_search_tool = create_web_search_tool()
    print(web_search_tool.invoke("What is the capital of France?"))