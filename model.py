import os
from openai import AuthenticationError, OpenAI, RateLimitError
from tool import get_system_diagnostic, DIAGNOSTIC_TOOL_SCHEMA

class OpenAIModelTester:
    def __init__(self, model_name: str = "gpt-4o"):
        # Automatically loads OPENAI_API_KEY from environment variables
        self.client = OpenAI()
        self.model_name = model_name
        self.system_prompt = self._load_skill_instructions()

    def _load_skill_instructions(self) -> str:
        skill_path = os.path.join(os.path.dirname(__file__), "SKILL.md")
        if os.path.exists(skill_path):
            with open(skill_path, "r", encoding="utf-8") as f:
                return f.read()
        return "You are a helpful diagnostic AI assistant."

    def run_connectivity_test(self, user_message: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]

        try:
            # Initial call to the model
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=[DIAGNOSTIC_TOOL_SCHEMA],
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message

            # Check if the model wants to call our local tool
            if response_message.tool_calls:
                messages.append(response_message)
                
                for tool_call in response_message.tool_calls:
                    if tool_call.function.name == "get_system_diagnostic":
                        tool_result = get_system_diagnostic()
                        
                        # Append tool execution result back to conversation
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(tool_result)
                        })

                # Follow-up call with tool output to generate final response
                second_response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages
                )
                return second_response.choices[0].message.content

            return response_message.content

        except AuthenticationError:
            return (
                "[ERROR] OpenAI rejected OPENAI_API_KEY (HTTP 401). "
                "Check that the key is valid and active, then update it in your "
                "PowerShell session and run the script again. Do not share your key."
            )
        except RateLimitError:
            return (
                "[ERROR] OpenAI rejected the request due to quota or rate limits (HTTP 429). "
                "Check your API billing, available credits, usage limits, and rate limits. "
                "If the account is out of credits, add credits before retrying."
            )
        except Exception as e:
            return f"[ERROR] OpenAI API connectivity failed: {str(e)}"
