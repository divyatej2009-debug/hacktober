import os
from model import OpenAIModelTester

def main():
    print("=== Initializing OpenAI Diagnostic Project ===")
    
    # Quick check for API key configuration
    if not os.environ.get("OPENAI_API_KEY"):
        print("[WARNING] OPENAI_API_KEY environment variable is not set.")
        print('In PowerShell, set it for this session with: $env:OPENAI_API_KEY = "your-key-here"')
        print("Then run python main.py again in the same terminal.")
        return

    tester = OpenAIModelTester(model_name="gpt-4o")
    
    test_query = "Please run a system diagnostic check and confirm if our OpenAI setup is functional."
    print(f"\n[User Query]: {test_query}\n")
    
    print("[Executing API Call & Tool Hook]...")
    result = tester.run_connectivity_test(test_query)
    
    print("\n--- Model Response ---")
    print(result)
    print("------------------------")

if __name__ == "__main__":
    main()
