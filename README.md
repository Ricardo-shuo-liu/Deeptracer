# Deeptracer - 🤖 Intelligent Code Analysis and Refactoring Platform 🚀

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code Analysis](https://img.shields.io/badge/Feature-Code%20Analysis-blueviolet.svg)](https://github.com/yourusername/deeptracer)
[![Performance Analysis](https://img.shields.io/badge/Feature-Performance%20Analysis-green.svg)](https://github.com/yourusername/deeptracer)
[![Memory Analysis](https://img.shields.io/badge/Feature-Memory%20Analysis-orange.svg)](https://github.com/yourusername/deeptracer)
[![AI Refactoring](https://img.shields.io/badge/Feature-AI%20Refactoring-purple.svg)](https://github.com/yourusername/deeptracer)

---

[🌐 切换到简体中文版本 (Switch to Simplified Chinese)](./README_zh.md)

---

## 📋 Project Overview

Deeptracer is an 🤖 AI-driven intelligent code analysis and refactoring platform that provides professional code optimization solutions through deep code understanding, multi-dimensional visual analysis, and natural language interaction 🚀.

### 🌟 Core Values

- **🧠 Intelligent Analysis**: Combines local tools with cloud-based agents for deep code insights
- **📊 Multi-dimensional Visualization**: Intuitive display of performance, memory, and execution flow
- **💡 Smart Refactoring Suggestions**: AI-generated specific and executable code modification proposals
- **🎨 User-friendly Interface**: Three-window adjustable layout with Git-style diff interface
- **🔒 Secure Execution Environment**: Code sandbox configuration and resource limit protection

### 📌 Version Planning

- **MVP Version**: Focus on core analysis workflow and basic refactoring features
- **Full Version**: Extend with advanced features like intelligent dialogue and dynamic updates

## ✨ Core Features

### 1. 🔍 Code Analysis Module

- **AST Structure Analysis**: Parses code to generate abstract syntax trees, identifying code patterns and potential issues
- **Execution Flow Visualization**: Shows execution traces and variable state changes based on Python Tutor
- **Code Quality Assessment**: Identifies common code problems and optimization opportunities

### 2. ⚡ Performance Analysis Module

- **Tool Used**: Pyinstrument
- **Features**: Function call time analysis, call relationship visualization, performance bottleneck detection
- **Output**: JSON format trace data with interactive timeline

### 3. 🧠 Memory Analysis Module

- **Tool Used**: Memray
- **Features**: Memory allocation tracking, memory leak detection, memory usage heatmap
- **Output**: HTML format memory report with visual memory usage

### 4. 🤖 Smart Refactoring Suggestions

- **AI-driven**: Based on Coze agent platform's deep code understanding
- **Specific and Executable**: Git-style diff interface showing modification suggestions
- **Technical Explanations**: Each suggestion comes with technical principle explanations and modification impact assessments
- **Interactive Control**: Accept/reject individual refactoring suggestions, batch apply selected modifications

### 5. 🖥️ Visual Interface

- **Three-window Layout**:
  - 📈 Analysis Visualization Window: Multi-tab views of performance timeline, execution flow, and code structure
  - 💻 Code Refactoring Window: Git-style diff interface with smart refactoring suggestions and interactive controls
  - 💬 Agent Dialogue Window: Technical explanation and natural language interaction interface
- **Interactive Features**: Freely draggable window splits, responsive layout adaptation

## 🛠️ Technology Stack

### Frontend

- React 18 + TypeScript
- Vite (build tool)
- React Split Panes (window layout)
- Monaco Editor (code editor)
- ECharts (chart visualization)
- Tailwind CSS (styling framework)

### Backend

- FastAPI (Web framework)
- Python 3.10
- Analysis Tools:
  - Pyinstrument (performance analysis)
  - Memray (memory analysis)
  - Python Tutor (execution visualization)
  - AST module (code structure analysis)
- AI Platform: Coze API integration
- Template Engine: Jinja2

### Deployment

- Docker containerization
- Command-line tool

## 📦 Installation and Usage

### Environment Requirements

- Python 3.10+
- Node.js 16+
- Modern browser (Chrome/Firefox/Safari)

### Installation Steps

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

#### Command Line Interface

```bash
# Basic analysis command
deptracer script.py

# Optional parameters
deptracer --output <output-path> script.py
deptracer --verbose script.py
```

#### Configuration Instructions

- **Environment Variables**:
  - `COZE_API_TOKEN`: Coze API token
  - `COZE_BOT_ID`: Coze bot ID
  - `COZE_WORKFLOW_ID`: Coze workflow ID

- **Configuration Files**:
  - `deeptracer/workflow/.env.local`: Local configuration file

## 🏗️ System Architecture

### Overall Architecture

```
🤖 User CLI Input → 🚀 Analysis Engine → 📊 Data Collection → 💡 Agent Processing → 📋 Report Generation → 🖥️ Browser Display
```

### Layered Processing Pipeline

1. **📊 Data Collection Layer**: Parallel execution of multiple analysis tools (Pyinstrument, Memray, Python Tutor, AST parsing)
2. **💡 Intelligent Analysis Layer**: AI agent comprehensive interpretation to identify optimization opportunities
3. **💡 Suggestion Generation Layer**: Generate specific code modification schemes
4. **💬 Interactive Response Layer**: Handle user feedback and dialogue requests

### Data Flow Process

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

## 🔧 Toolchain Description

| Tool Type | Tool Used | Responsible Functions |
|---------|----------|---------------------|
| Performance Analysis | Pyinstrument | Function call time analysis, performance bottleneck detection |
| Memory Analysis | Memray | Memory allocation tracking, memory leak detection |
| Execution Visualization | Python Tutor | Execution flow, variable state changes |
| Code Structure Analysis | AST Module | Code structure parsing, abstract syntax tree generation |

## 📖 Development Guide

### Coding Standards

1. **File Encoding**: All files must use UTF-8 encoding
2. **File Operations**: All file opens must explicitly specify encoding='utf-8'
3. **Python Version**: Unified development with Python 3.10
4. **Function Definition**: Use type annotations and docstrings

```python
def function(element:int)->int:
    """Returns 1 (description of the function's purpose!)"""
    return 1
```

### Contribution Process

1. Submit an Issue to report problems or feature suggestions
2. Fork the repository and create a feature branch
3. Implement features and write tests
4. Submit a Pull Request, explaining feature changes
5. Merge after code review approval

### Testing Instructions

- **Testing Framework**: pytest
- **Test Directory**: Test cases organized by module in the `test/` directory
- **Local Testing**: Local test cases stored in the `test_local/` directory

## 🙏 Acknowledgments

- [Pyinstrument](https://github.com/joerick/pyinstrument): Performance analysis tool
- [Memray](https://github.com/bloomberg/memray): Memory analysis tool
- [Python Tutor](https://github.com/pgbovine/OnlinePythonTutor): Execution visualization tool
- [Coze](https://www.coze.com/): Agent platform

---

## 📞 Contact Information

For questions or suggestions, please contact us through Issues or email.

---

**🚀 Most importantly, have fun!** 🎉
