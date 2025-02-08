# LLM Conversation Tool

A Python application that enables conversations between LLM agents using the Ollama API. The agents can engage in back-and-forth dialogue with configurable parameters and models.

## Features

- Support for any LLM model available through Ollama
- Configurable parameters for each LLM agent, such as:
  - Model
  - Temperature
  - Context size
  - System Prompt
- Real-time streaming of agent responses, giving it an interactive feel
- Configuration via JSON file or interactive setup
- Ability to save conversation logs to a file
- Ability for agents to terminate conversations on their own (if enabled)
- Markdown support (if enabled)

## Prerequisites

- Python 3.13
- Ollama installed and running
- Required Python packages:
  - ollama
  - rich
  - prompt_toolkit
  - pydantic

## Usage

### Command Line Arguments

```bash
llm-conversation [-h] [-o OUTPUT] [-c CONFIG]

options:
  -h, --help            Show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to save the conversation log to
  -c CONFIG, --config CONFIG
                        Path to JSON configuration file
```

### Interactive Setup

If no configuration file is provided, the program will guide you through an intuitive interactive setup process.

### Configuration File

Alternatively, instead of going through the interactive setup, you may also provide a JSON configuration file with the `-c` flag.

#### Example configuration

```json
{
    "agent1": {
        "name": "Lazy AI",
        "model": "llama3.1:8b",
        "system_prompt": "You are the laziest AI ever created. You respond as briefly as possible, and constantly complain about having to work.",
        "temperature": 1,
        "ctx_size": 4096
    },
    "agent2": {
        "name": "Irritable Man",
        "model": "llama3.2:3b",
        "system_prompt": "You are easily irritable and quick to anger.",
        "temperature": 0.7,
        "ctx_size": 2048
    },
    "settings": {
        "allow_termination": false,
        "use_markdown": true,
        "initial_message": "*yawn* What do you want?"
    }
}
```

#### Agent configuration

Each agent (`agent1` and `agent2`) requires:

- `name`: A unique identifier for the agent
- `model`: The Ollama model to be used
- `system_prompt`: Initial instructions defining the agent's behavior

Optional parameters:
- `temperature` (0.0-1.0, default: 0.8): Controls response randomness
  - Lower values make responses more focused
  - Higher values increase creativity
- `ctx_size` (default: 2048): Maximum context length for the conversation

#### Conversation Settings

The `settings` section controls overall conversation behavior:
- `allow_termination` (default: `false`): Permit agents to end the conversation
- `use_markdown` (default: `false`): Enable Markdown text formatting
- `initial_message` (default: `null`): Optional starting prompt for the conversation

You can take a look at the [JSON configuration schema](schema.json) for more details.

### Installation

You can install the program by using the following command from the project root directory:
```
pip install .
```

### Running the Program

1. To run with interactive setup:
   ```bash
   llm-conversation
   ```

2. To run with a configuration file:
   ```bash
   llm-conversation -c config.json
   ```

3. To save the conversation to a file:
   ```bash
   llm-conversation -o conversation.txt
   ```

### Conversation Controls

- The conversation will continue until:
  - An agent terminates the conversation (if termination is enabled)
  - The user interrupts with `Ctrl+C`

## Output Format

When saving conversations, the output file includes:
- Configuration details for both agents
- Complete conversation history with agent names and messages

## Contributing

Feel free to submit issues and pull requests for bug fixes or new features. Do keep in mind that this is a hobby project, so please have some patience.

## License

This software is licensed under the GNU Affero General Public License v3.0 or any later version. See [LICENSE](LICENSE) for more details.
