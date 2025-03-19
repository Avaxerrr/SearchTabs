# SearchTabs

SearchTabs is a lightweight desktop wrapper application for Perplexity with a tabbed interface, built using PySide6 (Qt for Python). This unofficial app provides a more efficient way to use Perplexity with multiple tabs, offering a potentially lower resource footprint compared to Electron-based alternatives.

## Why "SearchTabs"?
The name "SearchTabs" was chosen to highlight the app's primary differentiating feature - the ability to use multiple search tabs in a single window - while also respecting trademark considerations. Unlike names that might incorporate "Perplexity" directly, "SearchTabs" establishes this application as an independent tool that enhances the Perplexity web experience through tabbed browsing, without implying any official affiliation.

## Features

- **Tabbed Interface**: Unlike the official Perplexity desktop app, SearchTabs allows you to open multiple Perplexity sessions in tabs
- **Keyboard Shortcuts**: Includes essential shortcuts for tab management and navigation
- **Lower Resource Usage**: Built with Python and PySide6 instead of Electron, potentially offering better performance and lower memory consumption
- **Theme Management**: Supports light and dark themes with automatic detection

## Installation

### Dependencies
- Python 3.6+
- PySide6
- darkdetect

```bash
pip install PySide6 darkdetect
```

### Running the Application
```bash
python main.py
```

## Usage

### Current Shortcuts
- **New Tab**: Ctrl+T
- **Close Tab**: Ctrl+W
- **Refresh Page**: Ctrl+R
- **Switch Between Tabs**: Ctrl+Tab

### Upcoming Features
- **Find in Page**: Ctrl+F functionality
- **System Tray Integration**: Minimize to system tray
- **Always on Top**: Option to keep the window above other applications
- **Additional Shortcuts**: More keyboard shortcuts for improved productivity

## Screenshots

![image](https://github.com/user-attachments/assets/efb88f47-0ccf-4e8f-820b-aedf300fb0f1)
![image](https://github.com/user-attachments/assets/9143c958-31d6-4943-9e28-fd5a00292932)



## Roadmap

- Find in page functionality (Ctrl+F)
- System tray integration
- Always on top option
- Performance optimization
- Additional customization options

## Contributing

Contributions to SearchTabs are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the existing style and includes appropriate comments.

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2023 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Disclaimer

SearchTabs is not affiliated with, associated with, or endorsed by Perplexity AI. This is an unofficial application created to provide a tabbed interface for accessing Perplexity's web services. Users should comply with Perplexity's terms of service when using this application.

The primary purpose of this application is to provide a tabbed interface and potentially lower resource consumption compared to Electron-based alternatives. All Perplexity content is accessed through their official website, and this application does not modify, store, or redistribute any of Perplexity's proprietary content or services.
