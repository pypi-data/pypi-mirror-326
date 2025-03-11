# JinaFetch

A CLI tool to fetch web content and save it as Markdown using [Jina Reader API](https://github.com/jina-ai/reader).

## Features

- 🚀 Fast web content conversion to Markdown
- 🔑 Secure API key management via `.env`
- 🎨 Rich terminal output with success/error formatting
- 📂 Automatic filename generation with fallback

## Installation

```bash
pipx install jinafetch  # Recommended
# or
pip install jinafetch
```

## Usage

### Basic fetching
```bash
jinafetch fetch https://example.com
```

### Specify output file
```bash
jinafetch fetch https://example.com --output my_document.md
```

### Environment Configuration
1. Create a `.env` file in your project directory:
```env
JINA_API_KEY=your_api_key_here
```

## Error Handling
Common error scenarios include:
- 🔒 Missing API key
- 🌐 Network errors
- 💾 File write permissions
- 🔗 Invalid URLs

Errors display clear messages in red with details.

## Requirements
- Python 3.12+
- Valid Jina Reader API key

---

📝 Note: Requires valid authentication via Jina Reader API

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
