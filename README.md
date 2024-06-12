# Github Copilot Chat History Export

This project provides a way to export the history of your Github Copilot chat usage for IntelliJ IDEA.

### Installation

#### Pip
```shell
pip install gh-che
```

#### Brew
```ruby
brew tap enciyo/taps
brew install gh-che
```

### Notes

- The output keeps track of the chat history after running the script. Previous chat history cannot be exported
- This project is still in development.
- This project is not affiliated with GitHub Copilot.
- The chat history is stored in a file named `{PROJECT_DIR}/ai/prompst` in the project root directory.
- This project use [mitmproxy](https://mitmproxy.org/) to intercept the traffic between the IDE and the Github Copilot
  server.
- This project can't catch the message rating. (Thumbs up, Thumbs down).
- We're waiting for official support from GitHub Copilot about exporting chat history.

#### Aim

- Export the chat history of Github Copilot for IntelliJ IDEA.
- Provide a way to view the chat history in a readable format. (.md,.json)
- Separate the chat history based on the branch. Review the chat history of a specific branch.

#### Usage

1. Open IntelliJ IDEA. (or any other JetBrains IDE)
2. Open Proxy Settings and set the port to 9696. (Settings -> Appearance & Behavior -> System Settings -> HTTP Proxy)
3. Run below command in terminal.

```shell
cd path/project/src
gh-che start
```

4. Now start conversation with GitHub Copilot.


#### Rating the message

You can rate the message by clicking the thumbs up or thumbs down button on the chat window. But this project can't
catch the rating. That's why we developed a way to rate the message manually.

You can rate the message by adding the below comment to the chat window.
These comments will not be visible in chat history. But it will be used to rate the message.

For thumbs down:

```shell
vote:bad
```

For thumbs up:

```shell
vote:good
```

#### Help

```shell
Usage: gh-che [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  author       Set the author name
  project      Set the project path.
  show-config  Show the configuration.
  start        Start the gh-che proxy server.
  stop         Stop the gh-che proxy server.
  version      Get the version
```

#### Contribution

For performance operations and errors, please open an issue and describe it in detail.
