from ddgs import DDGS
from simpleeval import simple_eval

def search_web(query: str) -> str:
    """Searches the web for up-to-date information, news, or factual answers.
    Use this tool when you do not know the answer to a question or need to verify facts.
    
    Args:
        query: The specific search query string to look up.
        
    Returns:
        A string containing a summary of the top web search results.
    """

    try:
        # Limited to 3 results
        results = DDGS().text(query, max_results=3)
        if not results:
            return "No results found."

        formatted_results = []
        for res in results:
            formatted_results.append(f"Title: {res.get('title')}\nSnippet: {res.get('body')}")

        return "\n\n".join(formatted_results)

    except Exception as e:
        return f"Search failed with error: {str(e)}"


def calculate(expression: str) -> str:
    """Evaluates a mathematical equation and returns the numerical result.
    Use this tool ONLY for math, arithmetic, and numerical calculations.
    Do NOT use this tool for web searches or text queries.
    
    Args:
        expression: A string containing a valid mathematical expression (e.g., '10 * (3 + 2)').
        
    Returns:
        The calculated result as a string.
    """
    try:
        result = simple_eval(expression)
        return str(result)

    except Exception as e:
        return f"Calculation failed with error: {str(e)}"