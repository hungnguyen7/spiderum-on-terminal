# spiderum-on-terminal

A simple tool to read Spiderum articles on terminal.

## Installation
```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Current Features
- Read the latest articles from Spiderum.
- Text-to-Speech feature.
- Enable/Disable showing images in the article.
- Save the article to a text file.

## Keyboard Shortcuts
- `N`: Fetch the next list of articles.
- `P`: Fetch the previous list of articles.
- `F`: Go to the first page of the list.
- `X`: Quit the program.
- `L`: To show list of articles.
- `V`: To enable/disable the text-to-speech feature.
- `I`: To enable/disable showing images in the article.
- `B`: To bookmark the article.
- `H`: To show the help menu.


**Notes:** On Windows, the Speak-to-Text feature uses the pyttsx3 library, which requires the Vietnamese voice to be enabled. To enable Vietnamese voice on Windows, follow the instructions in this [video tutorial](https://www.youtube.com/watch?v=aw7FVWOY1yE). On other operating systems, the feature will use the Google Text-to-Speech API to read the article.