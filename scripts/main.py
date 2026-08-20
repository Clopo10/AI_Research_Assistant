import os
from google import genai
from google.genai import types

# Import custom files
from tools import search_web, calculate
from prompts import SYSTEM_INSTRUCTION, REPORT_GENERATION_PROMPT

def main():
    print("=== AI Research Assistant ===")
    
    # Get the API Key securely
    api_key = os.environ.get("GEMINI_API_KEY") 
    if not api_key:
        api_key = input("Please enter your Google Gemini API Key: ")
        
    client = genai.Client(api_key=api_key)

    # Configure the model with tools and instructions
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[search_web, calculate],
        temperature=0.0
    )

    # Initialize the continuous chat session
    print("\n[System] Initializing Gemini 3.6 Flash chat session...")
    chat = client.chats.create(
        model='gemini-3.6-flash',
        config=config
    )
    
    # Get the user's research query
    query = input("\nEnter your complex research question:\n")
    
    print("\n[Agent is reasoning, searching, and calculating...]")
    
    # Send the query
    initial_response = chat.send_message(query)
    
    print("--- Initial Agent Findings ---")
    print(initial_response.text)
    
    # Generate the final report deliverable
    print("\n==================================================")
    print("Synthesizing final report based on gathered memory...")
    
    # We send the follow-up prompt to the exact same chat object to maintain memory
    report_response = chat.send_message(REPORT_GENERATION_PROMPT)
    
    print("\n--- Final Research Report ---")
    print(report_response.text)

    # Cost Estimation
    # We can extract the exact token counts from the final response object 
    try:
        usage = report_response.usage_metadata
        input_tokens = usage.prompt_token_count
        output_tokens = usage.candidates_token_count
        
        # Current Gemini 2.5 Flash pricing: $0.30 per 1M input, $2.50 per 1M output
        input_cost = (input_tokens / 1_000_000) * 0.30
        output_cost = (output_tokens / 1_000_000) * 2.50
        total_cost = input_cost + output_cost
        
        print("\n--- Cost Estimation ---")
        print(f"Total Input Tokens:  {input_tokens} (${input_cost:.6f})")
        print(f"Total Output Tokens: {output_tokens} (${output_cost:.6f})")
        print(f"Total Run Cost:      ${total_cost:.6f}")
    except Exception as e:
        print(f"\n[Could not calculate token usage: {e}]")

if __name__ == "__main__":
    main()