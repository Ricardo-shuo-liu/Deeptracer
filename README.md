# Deeptracer - 🤖 An Intelligent Code Analysis & Refactoring Platform 🚀

[![Python >3.10.9](https://img.shields.io/badge/python-%3E3.10.9-blue.svg)](https://www.python.org/downloads/)
[![Code Analysis](https://img.shields.io/badge/Feature-Code_Analysis-blueviolet.svg)](https://github.com/Ricardo-shuo-liu/deeptracer)
[![Performance Analysis](https://img.shields.io/badge/Feature-Performance_Analysis-green.svg)](https://github.com/Ricardo-shuo-liu/deeptracer)
[![AI Refactoring](https://img.shields.io/badge/Feature-AI_Refactoring-purple.svg)](https://github.com/Ricardo-shuo-liu/deeptracer)

---

[🌐 切换到中文版本 (Switch to Chinese)](./README_zh.md)

---

## 📋 Project Overview

Deeptracer is an 🤖 AI-powered intelligent code analysis and refactoring platform that delivers professional code optimization solutions for developers through deep code understanding, multi-dimensional visual analysis, and natural language interaction 🚀.

### 🌟 Core Values

- **🧠 Intelligent Analysis**: Combines local tools and cloud agents to provide in-depth code insights
- **📊 Multi-dimensional Visualization**: Intuitive display of performance, memory, and execution flow
- **💡 Smart Refactoring Suggestions**: AI-generated concrete and actionable code optimization plans
- **🎨 User-friendly Interface**: Resizable three-pane layout with Git-style diff interface
- **🔒 Secure Execution Environment**: Code sandbox configuration with resource limit protection

### 📌 Version Roadmap

- **MVP Version**: Focus on core analysis workflows and basic refactoring features
- **Full Version**: Extend advanced features such as intelligent dialogue and dynamic updates

## ✨ Core Features

### 1. 🔍 Code Analysis Module

- **AST Structure Analysis**: Parses code to generate abstract syntax trees, identifying code patterns and potential issues
- **Execution Flow Visualization**: Displays execution traces and variable state changes based on Python Tutor
- **Code Quality Assessment**: Detects common code issues and optimization opportunities

### 2. ⚡ Performance Analysis Module

- **Tool Used**: Pyinstrument
- **Features**: Function call time analysis, call relationship visualization, performance bottleneck detection
- **Output**: JSON-formatted trace data with interactive timeline

### 3. 🤖 AI Refactoring Suggestions

- **AI-driven**: Deep code understanding based on the Coze agent platform
- **Concrete & Actionable**: Git-style diff interface to display modification suggestions
- **Technical Explanations**: Each suggestion includes technical principles and impact assessments
- **Interactive Control**: Accept/reject individual refactoring suggestions, apply selected changes in bulk

### 4. 🖥️ Visual Interface

- **Three-pane Layout**:
  - 📈 Analysis Visualization Pane: Multi-tab view for performance timelines, execution flows, and code structures
  - 💻 Code Refactoring Pane: Diff interface with smart refactoring suggestions and interactive controls
  - 💬 Agent Dialogue Pane: Technical explanations and natural language interaction interface
- **Interactive Features**: Freely draggable pane resizing, responsive layout adaptation

## 🛠️ Tech Stack

### Frontend
- **Core Framework**: Vue.js 2.6.14 (data-driven view rendering, state management, event binding)
- **UI Component Library**: Element UI 2.15.13 (pre-built components like buttons, dialogs, tooltips, etc.)
- **Foundational Technologies**:
  - HTML5 (semantic tags, iframe embedding for third-party visualizations)
  - CSS3 (Flexbox layout, responsive design, custom scrollbars, media queries)
  - JavaScript (ES6+ syntax, Promise async operations, Clipboard API, custom Diff algorithm)
- **Interactive Capabilities**:
  - Custom code Diff comparison logic (classifying lines as added/deleted/modified/unchanged)
  - Python Tutor iframe integration (code execution visualization)
  - Responsive layout (side-by-side panes on large screens, stacked panes on small screens)

### Backend

- FastAPI (web framework)
- Python >3.10.9
- Analysis Tools:
  - Pyinstrument (performance profiling)
  - Python Tutor (execution visualization)
  - AST module (code structure analysis)
- AI Platform: Coze API integration
- Template Engine: Jinja2

### Deployment

- Docker containerization
- Command-line interface

## 📦 Installation & Usage

### Prerequisites

- Python >=3.10.9 (3.10.9+)
- Modern web browser (Chrome/Firefox/Safari)

### Installation Steps

1. **Clone the Repository**

```bash
git clone <repository-url>
cd deeptracer
```

2. **Install Python Dependencies**

```bash
pip install -e .
```

### Basic Usage

#### Command-line Interface

```bash
# Configure your Coze key
deeptracer --key yourKeys

# Basic analysis command
deeptracer script.py

# Enable full AST visualization
deeptracer script.py --all
# Or use the short form
deeptracer script.py -a
```

#### Configuration

- **Environment Variables**:
  - `COZE_API_TOKEN`: Coze API token
  - `COZE_BOT_ID`: Coze bot ID
  - `COZE_WORKFLOW_ID`: Coze workflow ID

- **Configuration File**:
  - `~/.deeptracer/.env.local`: Local configuration file

## 🏗️ System Architecture

### Overall Architecture

```
🤖 User CLI Input → 🚀 Analysis Engine → 📊 Data Collection → 💡 Agent Processing → 📋 Report Generation → 🖥️ Browser Rendering
```

### Layered Processing Pipeline 💫

1. **📊 Data Collection Layer**: Executes multiple analysis tools in parallel (Pyinstrument, Memray, Python Tutor, AST parsing)
2. **💡 Intelligent Analysis Layer**: AI agent synthesizes insights to identify optimization opportunities
3. **💡 Suggestion Generation Layer**: Generates concrete code modification plans
4. **💬 Interactive Response Layer**: Handles user feedback and dialogue requests

### Data Flow 💥

```
📄 Original Code
    → 🚀 Parallel Analysis Tool Execution
    → 📊 Unified Data Format
    → 💡 Agent Processing
    → 💡 Structured Suggestions
    → 🖥️ Frontend Dynamic Rendering
    → 💬 User Interaction
    → 📋 Final Output
```

## 🔧 Toolchain 🧐

| Tool Type       | Tool Used       | Responsible Function                                  |
|-----------------|-----------------|--------------------------------------------------------|
| Performance     | Pyinstrument    | Function call time analysis, performance bottleneck detection |
| Execution Vis   | Python Tutor    | Execution flow visualization, variable state tracking |
| Code Structure  | AST Module      | Code structure parsing, abstract syntax tree generation |

## 📖 Development Guide

### Coding Standards 🫣

1. **File Encoding**: All files must use UTF-8 encoding
2. **File I/O**: All file `open` operations must explicitly specify `encoding='utf-8'`
3. **Python Version**: Develop exclusively with Python >=3.10.9
4. **Function Definitions**: Use type hints and docstrings

```python
def function(element: int) -> int:
    """Returns 1 (Explain the function's purpose!)"""
    return 1
```

### Contribution Workflow 🤗

1. Submit an Issue to report bugs or propose features
2. Fork the repository and create a feature branch
3. Implement the feature and write tests
4. Submit a Pull Request describing the changes
5. Merge after code review approval

### Testing 🤤

- **Test Framework**: pytest
- **Test Directory**: `test/` organized by module
- **Local Tests**: `test_local/` for local test cases

## 🙏 Acknowledgments 🤗

- [Pyinstrument](https://github.com/joerick/pyinstrument): Performance profiling tool 🥳
- [Python Tutor](https://pythontutor.com/): Execution visualization tool 👻
- [cozepy](https://github.com/coze-dev/coze-py): AI agent platform 🤖
- [python-dotenv](https://github.com/theskumar/python-dotenv): Environment variable loader 😤
- [tqdm](https://github.com/tqdm/tqdm): Progress bar 😇
- [pyvis](https://github.com/WestHealth/pyvis): Network visualization 🧩
- [networkx](https://github.com/networkx/networkx): Network analysis 🎲
- [fastapi](https://github.com/fastapi/fastapi): Backend core framework 🚀
- [uvicorn](https://github.com/Kludex/uvicorn): ASGI server for app deployment 💥
- [Vue.js](https://vuejs.org/): Frontend core framework ✨
- [Element UI](https://element.eleme.io/#/en-US): Frontend UI component library 🎨

---

## 📞 Contact

For questions or suggestions, please reach out via Issue or email.

---

**🚀 Most importantly, have fun!** 🎉

---