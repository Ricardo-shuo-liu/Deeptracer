# Deeptracer - 🤖 Intelligent Code Analysis & Refactoring Platform 🚀

[![Python >3.10.9](https://img.shields.io/badge/python-%3E3.10.9-blue.svg)](https://www.python.org/downloads/)
[![Code Analysis](https://img.shields.io/badge/Feature-Code%20Analysis-blueviolet.svg)](https://github.com/Ricardo-shuo-liu/deeptracer)
[![Performance Analysis](https://img.shields.io/badge/Feature-Performance%20Analysis-green.svg)](https://github.com/Ricardo-shuo-liu/deeptracer)
[![Memory Analysis](https://img.shields.io/badge/Feature-Memory%20Analysis-orange.svg)](https://github.com/Ricardo-shuo-liu/deeptracer)
[![AI Refactoring](https://img.shields.io/badge/Feature-AI%20Refactoring-purple.svg)](https://github.com/Ricardo-shuo-liu/deeptracer)

---

[🌐 切换到中文版本 (Switch to Chinese)](./README_zh.md)

---

## 📋 Project Overview

Deeptracer is an 🤖 AI-powered intelligent code analysis and refactoring platform. It provides professional code optimization solutions for developers through deep code understanding, multi-dimensional visual analysis, and natural language interaction 🚀.

### 🌟 Core Values

- **🧠 Intelligent Analysis**: Combines local tools and cloud agents to deliver in-depth code insights
- **📊 Multi-dimensional Visualization**: Intuitive display of performance, memory, and execution flow
- **💡 AI Refactoring Suggestions**: AI-generated concrete and actionable code optimization plans
- **🎨 User-friendly Interface**: Three adjustable panes, Git-style diff interface
- **🔒 Secure Execution Environment**: Code sandbox configuration with resource limit protection

### 📌 Roadmap

- **MVP Version**: Focus on core analysis pipeline and basic refactoring features
- **Full Version**: Extend with advanced features such as intelligent chat and dynamic updates

## ✨ Core Features

### 1. 🔍 Code Analysis Module

- **AST Structure Analysis**: Parses code into abstract syntax trees, identifies patterns and potential issues
- **Execution Flow Visualization**: Displays execution traces and variable state changes based on Python Tutor
- **Code Quality Assessment**: Detects common code issues and optimization opportunities

### 2. ⚡ Performance Analysis Module

- **Tools Used**: Pyinstrument
- **Features**: Function call time analysis, call graph visualization, performance bottleneck detection
- **Output**: JSON trace data, interactive timeline

### 3. 🧠 Memory Analysis Module

- **Tools Used**: Memray
- **Features**: Memory allocation tracking, memory leak detection, memory usage heatmap
- **Output**: HTML memory report, visual memory usage breakdown

### 4. 🤖 Intelligent Refactoring Suggestions

- **AI-driven**: Deep code understanding powered by the Coze agent platform
- **Concrete & Actionable**: Modifications displayed in a Git-style diff interface
- **Technical Explanations**: Each suggestion includes principles and impact assessment
- **Interactive Control**: Accept/reject individual suggestions, apply selected changes in batches

### 5. 🖥️ Visual Interface

- **Three-pane Layout**:
  - 📈 Analysis Visualization Pane: Multi-tab view for performance timeline, execution flow, and code structure
  - 💻 Code Refactoring Pane: Git-style diff interface with smart refactoring suggestions and controls
  - 💬 Agent Chat Pane: Technical explanations and natural language interaction
- **Interactive Features**: Draggable and resizable panes, responsive layout

## 🛠️ Tech Stack

### Frontend

- React 18 + TypeScript
- Vite (build tool)
- React Split Panes (layout)
- Monaco Editor (code editor)
- ECharts (visualization)
- Tailwind CSS (styling)

### Backend

- FastAPI (web framework)
- Python >3.10.9
- Analysis Tools:
  - Pyinstrument (performance)
  - Memray (memory)
  - Python Tutor (execution visualization)
  - AST module (code structure analysis)
- AI Platform: Coze API integration
- Template Engine: Jinja2

### Deployment

- Docker containerization
- Command-line interface

## 📦 Installation & Usage

### Requirements

- Python >3.10.9 (3.10.10+)
- Node.js 16+
- Modern browser (Chrome / Firefox / Safari)

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd deeptracer
```

2. **Install Python dependencies**

```bash
pip install -e .
```

3. **Install frontend dependencies**

```bash
npm install
```

### Basic Usage

#### CLI

```bash
# Configure your Coze key
deeptracer --key yourKeys

# Basic analysis
deeptracer script.py

# Enable full AST visualization
deeptracer script.py --all
# Short form
deeptracer script.py -a
```

#### Configuration

- **Environment Variables**:
  - `COZE_API_TOKEN`: Coze API token
  - `COZE_BOT_ID`: Coze bot ID
  - `COZE_WORKFLOW_ID`: Coze workflow ID

- **Config File**:
  - `~/.deeptracer/.env.local`: Local configuration

## 🏗️ System Architecture

### Overall Architecture

```
🤖 User CLI Input → 🚀 Analysis Engine → 📊 Data Collection → 💡 Agent Processing → 📋 Report Generation → 🖥️ Browser Display
```

### Layered Processing Pipeline 💫

1. **📊 Data Collection Layer**: Runs multiple analyzers in parallel (Pyinstrument, Memray, Python Tutor, AST parsing)
2. **💡 Intelligent Analysis Layer**: AI agent synthesizes insights and identifies optimization opportunities
3. **💡 Suggestion Generation Layer**: Generates concrete code modification plans
4. **💬 Interactive Response Layer**: Handles user feedback and chat requests

### Data Flow 💥

```
📄 Raw Code
    → 🚀 Parallel analysis execution
    → 📊 Unified data format
    → 💡 Agent processing
    → 💡 Structured suggestions
    → 🖥️ Frontend dynamic rendering
    → 💬 User interaction
    → 📋 Final output
```

## 🔧 Toolchain 🧐

| Type         | Tool         | Responsibility                          |
|--------------|--------------|-----------------------------------------|
| Performance  | Pyinstrument | Function timing, bottleneck detection   |
| Memory       | Memray       | Allocation tracking, leak detection     |
| Execution    | Python Tutor | Step tracing, variable state changes   |
| Code Structure | AST       | Parsing, abstract syntax tree generation|

## 📖 Development Guide

### Code Style 🫣

1. **Encoding**: All files must use UTF-8
2. **File I/O**: All `open` calls must explicitly set `encoding='utf-8'`
3. **Python Version**: Developed for Python >3.10.9
4. **Functions**: Use type annotations and docstrings

```python
def function(element: int) -> int:
    """Return 1 (explain the function purpose!)"""
    return 1
```

### Contribution Flow 🤗

1. Open an Issue to report bugs or propose features
2. Fork the repo and create a feature branch
3. Implement and test your changes
4. Submit a Pull Request with a clear description
5. Merge after code review

### Testing 🤤

- **Framework**: pytest
- **Test Directory**: Tests organized by module under `test/`
- **Local Tests**: Local test cases in `test_local/`

## 🙏 Acknowledgments 🤗

- [Pyinstrument](https://github.com/joerick/pyinstrument): Performance profiler 🥳
- [Memray](https://github.com/bloomberg/memray): Memory profiler 👾
- [Python Tutor](https://github.com/hcientist/OnlinePythonTutor): Execution visualizer 👻
- [cozepy](https://github.com/coze-dev/coze-py): AI agent platform 🤖
- [python-dotenv](https://github.com/theskumar/python-dotenv): Environment variables 😤
- [objprint](https://github.com/gaogaotiantian/objprint): Human-readable object printing 😈
- [tqdm](https://github.com/tqdm/tqdm): Progress bar 😇
- [pyvis](https://github.com/WestHealth/pyvis): Network visualization 🧩
- [networkx](https://github.com/networkx/networkx): Network analysis 🎲
- [fastapi](https://github.com/fastapi/fastapi): Backend core 🚀
- [uvicorn](https://github.com/Kludex/uvicorn): App server 💥

---

## 📞 Contact

For questions or feedback, feel free to open an Issue or contact us via email.

---

**🚀 Most importantly, have fun!** 🎉