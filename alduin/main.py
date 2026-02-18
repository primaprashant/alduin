"""Alduin - A minimal CLI coding agent."""

import os
from typing import Any

import anthropic
import dotenv
from rich.console import Console

from alduin import llm, system_prompt, theme, ui


def agent_loop(client: anthropic.Anthropic, console: Console) -> None:
    """Run the main agent loop: read input, call LLM, execute tools, repeat.

    Args:
        client: The initialized Anthropic client.
        console: The Rich Console for logging and UI.
    """

    conversation: list[dict[str, Any]] = []

    while True:
        try:
            user_input = input("🧑‍💻 You: ").strip()
        except (KeyboardInterrupt, EOFError):
            ui.clear_previous_line()
            ui.print_goodbye(console)
            return

        if not user_input:
            continue

        conversation.append({"role": "user", "content": user_input})

        ui.clear_previous_line()
        ui.print_user_message(console, user_input)

        # import the call method from the llm module
        # make call to the llm api

        llm_response = llm.call(
            client=client,
            console=console,
            system_prompt=system_prompt.get(),
            messages=conversation,
            tool_schemas=[],
        )

        conversation.append({"role": "assistant", "content": llm_response.content})

        # display llm response

        for block in llm_response.content:
            ui.print_assistant_reply(
                console=console,
                text=block.text,
                input_tokens=llm_response.usage.input_tokens,
                output_tokens=llm_response.usage.output_tokens,
            )


def main() -> None:
    """Entry point for the Alduin CLI agent.

    Initializes console, checks API key, and starts the agent loop.
    """

    console = Console(theme=theme.ALDUIN_THEME)
    ui.print_banner(console)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        ui.print_error(console, "ANTHROPIC_API_KEY environment variable is not set.")
        return

    client = anthropic.Anthropic(api_key=api_key)
    agent_loop(client=client, console=console)


if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
