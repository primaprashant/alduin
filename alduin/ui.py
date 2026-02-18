"""Rich console UI components for Alduin."""

import json
import random

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from alduin import personality, theme

MAX_RESULT_LENGTH = 100


def clear_previous_line() -> None:
    """Clear the previous line in the terminal."""
    print("\033[1A\033[2K", end="", flush=True)


def print_banner(console: Console) -> None:
    """Display the startup banner.

    Args:
        console: The Rich Console to print to.
    """

    content = Text()
    content.append(personality.BANNER, style=theme.BANNER_TEXT_STYLE)
    content.append("\n")
    content.append(random.choice(personality.STARTUP_QUOTES), style="italic")

    console.print(
        Panel(
            content,
            title="[assistant_name]🐉 Alduin[/assistant_name]",
            title_align="left",
            subtitle="[system]Hit Ctrl+C to quit[/system]",
            subtitle_align="right",
            border_style=theme.BANNER_BORDER,
            padding=(0, 1),
        )
    )
    console.print()


def print_goodbye(console: Console) -> None:
    """Display a goodbye message when the user exits.

    Args:
        console: The Rich Console to print to.
    """

    goodbye = random.choice(personality.GOODBYE_MESSAGES)
    console.print(f"\n[system]🐲 {goodbye}[/system]")


def print_user_message(console: Console, text: str) -> None:
    """Display the user's message as a styled panel.

    Args:
        console: The Rich Console to print to.
        text: The user's message to display.
    """

    console.print(
        Panel(
            text,
            title="[user_prompt]🧑‍💻 You[/user_prompt]",
            title_align="left",
            border_style=theme.USER_BORDER,
            padding=(0, 1),
        )
    )


def print_assistant_reply(console: Console, text: str, input_tokens: int, output_tokens: int) -> None:
    """Display the assistant's markdown reply with token usage.

    Args:
        console: The Rich Console to print to.
        text: The assistant's reply in markdown format.
        input_tokens: The number of tokens in the user's input.
        output_tokens: The number of tokens in the assistant's output.
    """

    subtitle = f"[system]tokens: {input_tokens} in · {output_tokens} out[/system]"
    console.print(
        Panel(
            Markdown(text),
            title="[assistant_name]🐉 Alduin[/assistant_name]",
            title_align="left",
            subtitle=subtitle,
            subtitle_align="right",
            border_style=theme.ASSISTANT_BORDER,
            padding=(0, 1),
        )
    )
    console.print()


def print_tool_request(console: Console, name: str, args: dict) -> None:
    """Display a panel when a tool call is about to execute.

    Args:
        console: The Rich Console to print to.
        name: The name of the tool being called.
        args: The arguments being passed to the tool.
    """

    args_text = json.dumps(args, indent=2)
    content = Text()
    content.append("Tool: ", style="bold")
    content.append(f"{name}\n", style=theme.TOOL_NAME_STYLE)
    content.append("Arguments:\n", style="bold")
    content.append(args_text, style=theme.MUTED_STYLE)

    console.print(
        Panel(
            content,
            title="[tool]🔧 Tool Call[/tool]",
            title_align="left",
            border_style=theme.TOOL_BORDER,
            padding=(0, 1),
        )
    )


def print_tool_result(console: Console, name: str, result: str) -> None:
    """Display the result of a successful tool call.

    The result is truncated if it exceeds MAX_RESULT_LENGTH characters to keep the UI clean.

    Args:
        console: The Rich Console to print to.
        name: The name of the tool that was called.
        result: The result returned by the tool.
    """

    display = result if len(result) <= MAX_RESULT_LENGTH else result[:MAX_RESULT_LENGTH] + "\n… (truncated)"

    content = Text()
    content.append(name, style=theme.TOOL_NAME_STYLE)
    content.append(" completed\n", style=theme.SUCCESS_STYLE)
    content.append(display, style=theme.MUTED_STYLE)

    console.print(
        Panel(
            content,
            title="[tool]✅ Tool Result[/tool]",
            title_align="left",
            border_style=theme.TOOL_RESULT_BORDER,
            padding=(0, 1),
        )
    )


def print_tool_error(console: Console, name: str, error: str) -> None:
    """Display a panel when a tool call fails.

    Args:
        console: The Rich Console to print to.
        name: The name of the tool that was called.
        error: The error message returned by the tool.
    """

    content = Text()
    content.append(name, style=theme.TOOL_NAME_STYLE)
    content.append(" failed\n", style=theme.ERROR_TEXT_STYLE)
    content.append(error, style="red")

    console.print(
        Panel(
            content,
            title="[error]❌ Tool Error[/error]",
            title_align="left",
            border_style=theme.ERROR_BORDER,
            padding=(0, 1),
        )
    )


def print_debug(console: Console, message: str) -> None:
    """Display a subtle debug/info message.

    Args:
        console: The Rich Console to print to.
        message: The debug message to display.
    """

    console.print(
        Panel(
            Text(message, style=theme.MUTED_STYLE),
            title="[system]🐞 Debug[/system]",
            title_align="left",
            border_style=theme.DEBUG_BORDER,
            padding=(0, 1),
        )
    )


def print_error(console: Console, message: str) -> None:
    """Display a prominent error panel.

    Args:
        console: The Rich Console to print to.
        message: The error message to display.
    """

    console.print(
        Panel(
            Text(message, style=theme.ERROR_TEXT_STYLE),
            title="[error]❌ Error[/error]",
            title_align="left",
            border_style=theme.ERROR_BORDER,
            padding=(0, 1),
        )
    )


def confirm(console: Console, message: str) -> bool:
    """Show a confirmation prompt and return True if the user approves.

    Args:
        console: The Rich Console to print to.
        message: The message to display before the prompt.
    """

    console.print(
        Panel(
            Text(message, style=theme.TOOL_NAME_STYLE),
            title="[tool]⚡ Confirmation[/tool]",
            title_align="left",
            border_style=theme.TOOL_BORDER,
            padding=(0, 1),
        )
    )
    try:
        answer = input("Allow? [y/N]: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        return False
    return answer in ("y", "yes")

