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

On Windows, the Speak-to-Text feature uses the pyttsx3 library, which requires the Vietnamese voice to be enabled. To enable Vietnamese voice on Windows, follow the instructions in this [video tutorial](https://www.youtube.com/watch?v=aw7FVWOY1yE).

On other operating systems, the feature will use the Google Text-to-Speech API to read the article.