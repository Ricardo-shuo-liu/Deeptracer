# 多智能体 PR 说明

## 1. PR 目标

本次 PR 的目标是将我这边实现的多智能体分析后端整合到项目中，同时尽量不改变原仓库已经存在的产品定位与外部使用方式。

这次改动聚焦在以下方向：

- 引入基于 LangGraph 的多阶段分析工作流
- 将代码分析拆分为本地分析层和智能体解释层
- 为结构、性能、内存、重构建议、教学说明分别建立独立 agent
- 保留在未配置大模型 API 时的可用性，保证分析流程不会因为模型不可用而中断
- 尽量不强推新的前端入口和新的产品交互方式

本次 PR 不以“替换原仓库前端”为目标。前端可以继续沿用原仓库版本，多智能体部分主要作为后端分析能力接入。

## 2. 改动范围概览

本次 PR 主要新增或调整了以下模块：

- `deeptracer/agents/`
  - 定义结构、性能、内存、重构、教学五类 agent
- `deeptracer/graph/`
  - 定义 LangGraph 工作流、状态结构、响应拼装逻辑
- `deeptracer/modeling/llm.py`
  - 统一管理 LLM 注入与运行时配置
- `deeptracer/server/analysis_service.py`
  - 本地分析核心，负责 AST、性能、内存和基础建议生成
- `deeptracer/server/app.py`
  - 提供统一的 Web 分析接口
- `deeptracer/server/pytutor_service.py`
  - 提供 Python Tutor 执行轨迹相关服务

## 3. 总体架构

新的分析链路不是“完全交给 AI 做分析”，而是分成两层：

1. 本地分析层
2. 智能体解释层

整体思路如下：

```text
用户输入代码 / 文件
    ->
本地分析服务
    - AST 结构分析
    - 实际执行性能分析
    - 实际执行内存分析
    - 规则化建议草稿
    ->
LangGraph 多智能体工作流
    - structure agent
    - performance agent
    - memory agent
    - refactor agent
    - teaching agent
    ->
统一响应拼装
    ->
前端展示
```

核心原则是：

- 本地工具负责“拿事实”
- LLM 负责“解释事实、整合结论、生成更自然的建议”

## 4. 工作流设计

LangGraph 工作流定义在 `deeptracer/graph/workflow.py` 中。

当前工作流是一个串行流程，而不是并行自治型多 agent 系统。整体链路如下：

```text
START
  ->
local_tools
  ->
structure
  ->
performance
  ->
memory
  ->
refactor
  ->
teaching
  ->
response
  ->
END
```

这样设计的原因是：

- 先用本地工具稳定拿到可复现的分析结果
- 再由不同 agent 逐步解释、补充和整合
- 保证没有模型时也能正常返回分析结果

## 5. 各模块职责分工

### 5.1 local_tools 节点

职责：

- 读取用户输入的代码或 Python 文件
- 调用本地分析服务
- 生成统一的 `local_analysis` 结构

输出内容包括：

- `heroMetrics`
- `analysisMap`
- `suggestions`
- `stages`
- `meta`

这一层是整个多智能体链路的事实来源。

### 5.2 structure agent

职责：

- 根据 AST 分析结果解释代码结构
- 指出最值得先看的函数
- 给出简洁的结构理解提示

输入：

- 原始代码
- `local_analysis["analysisMap"]["ast"]`

输出：

- `summary`
- `focus_function`
- `points`

### 5.3 performance agent

职责：

- 根据性能分析结果解释哪里慢
- 指出最相关的性能热点
- 避免夸大性能问题，只基于已有数据说明

输入：

- 原始代码
- `local_analysis["analysisMap"]["performance"]`

输出：

- `summary`
- `hottest_function`
- `points`

### 5.4 memory agent

职责：

- 根据内存分析结果解释内存压力来源
- 标记值得关注的位置
- 用更容易理解的方式描述内存问题

输入：

- 原始代码
- `local_analysis["analysisMap"]["memory"]`

输出：

- `summary`
- `focus_area`
- `points`

### 5.5 refactor agent

职责：

- 综合结构、性能、内存三个维度
- 在本地建议草稿基础上给出 1 到 3 条更完整的修改建议
- 保持建议适合初学者理解，不走过度复杂化路线

输入：

- 原始代码
- 本地分析结果
- 结构 agent 结果
- 性能 agent 结果
- 内存 agent 结果

输出：

- `suggestions`

### 5.6 teaching agent

职责：

- 将整体分析结果翻译成更容易理解的话
- 给出面向初学者的说明和下一步建议

输入：

- 原始代码
- 结构 / 性能 / 内存 / 重构建议结果

输出：

- `overview`
- `beginner_tip`
- `next_step`

### 5.7 response 节点

职责：

- 将本地分析结果和各个 agent 结果合并成前端消费的统一结构

最终会输出：

- `heroMetrics`
- `analysisMap`
- `suggestions`
- `stages`
- `teaching`
- `meta`

## 6. 本地分析是怎么做的

本地分析核心位于 `deeptracer/server/analysis_service.py`。

### 6.1 AST 结构分析

使用 Python 标准库 `ast`：

- 解析语法树
- 统计函数数量
- 估算函数复杂度
- 识别控制流节点
- 提取循环中的关键调用

主要用途：

- 给结构 agent 提供基础事实
- 给本地建议生成提供依据

### 6.2 性能分析

使用 `cProfile`：

- 实际执行用户代码
- 收集函数级别的调用时间
- 识别热点函数和热点行

说明：

- 这部分是“基于实际运行结果”的分析，不是纯静态猜测

### 6.3 内存分析

使用 `tracemalloc`：

- 记录运行期间的内存分配
- 识别内存热点位置
- 统计峰值内存

说明：

- 这里的结论依然来自本地执行，而不是 LLM 推断

### 6.4 本地建议草稿

除了结构、性能、内存摘要外，本地分析还会先生成一版规则化建议，例如：

- 拆分过长或过复杂函数
- 关注循环内热点调用
- 收敛调试输出
- 缩短大对象生命周期

这些建议会作为 `refactor agent` 的输入之一。

## 7. LLM 在这套架构里的作用

LLM 不是本项目的唯一分析器，也不会替代本地工具。

LLM 的主要职责是：

- 解释本地分析结果
- 把多维信息组织成更自然的描述
- 在已有事实基础上生成更适合阅读的建议
- 补足教学说明

可以把这套架构理解成：

- 本地工具负责分析
- LLM 负责理解与表达

## 8. 没有配置模型时会发生什么

如果没有配置模型 API，系统不会报废，也不会中断分析。

当前设计是自动降级：

- 本地分析照常执行
- agent 不调用真实 LLM
- agent 直接返回本地分析结果或规则化兜底结果

这意味着：

- 没有 API Key 时，系统依然可用
- 有 API Key 时，结果会更自然、更像“多智能体解释”

换句话说，降级不是“不能分析”，而是“只使用本地分析，不再调用大模型解释层”。

## 9. 当前模型配置方式

模型注入统一位于 `deeptracer/modeling/llm.py`。

当前实现默认按 OpenAI-compatible 方式接入：

- `DEEPTRACER_MODEL_PROVIDER`
- `DEEPTRACER_MODEL_NAME`
- `DEEPTRACER_MODEL_TEMPERATURE`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `OPENAI_BASE_URL`

### 9.1 默认行为

默认值：

- `DEEPTRACER_MODEL_PROVIDER=openai`
- `DEEPTRACER_MODEL_NAME` 优先，否则读取 `OPENAI_MODEL`
- 若都未设置，默认模型为 `gpt-4.1-mini`

### 9.2 OpenAI 官方配置示例

```powershell
$env:DEEPTRACER_MODEL_PROVIDER="openai"
$env:OPENAI_API_KEY="your-api-key"
$env:OPENAI_MODEL="gpt-4.1-mini"
```

### 9.3 第三方 OpenAI-compatible 平台配置示例

如果使用兼容 OpenAI 协议的第三方平台，也可以使用：

```powershell
$env:DEEPTRACER_MODEL_PROVIDER="openai"
$env:OPENAI_API_KEY="your-third-party-key"
$env:OPENAI_BASE_URL="https://your-provider.example.com/v1"
$env:OPENAI_MODEL="qwen-plus"
```

说明：

- 这里的 `OPENAI_API_KEY` 只是环境变量名
- 不代表必须使用 OpenAI 官方密钥
- 只要提供 OpenAI-compatible 接口即可复用当前实现

## 10. 如何运行

### 10.1 安装依赖

```powershell
pip install -e .
```

### 10.2 启动服务

当前 Web 服务主入口在：

- `deeptracer.server.app:main`

如果项目中保留了对应脚本入口，则可以直接启动；如果没有公开单独脚本，也可以通过 Python 方式启动对应模块。

### 10.3 调用分析接口

核心分析接口：

- `POST /api/analyze`

请求示例：

```json
{
  "code": "def hello():\n    print('hello')\n\nhello()"
}
```

或：

```json
{
  "path": "tests/test_sources/test_mem.py"
}
```

## 11. 返回数据结构

分析结果会统一返回给前端，主要字段包括：

- `heroMetrics`
- `analysisMap`
- `suggestions`
- `stages`
- `teaching`
- `meta`

其中 `meta` 中会附带：

- `taskId`
- `agentMode`
- `provider`
- `model`
- `llmConfigured`

这样前端可以明确知道：

- 当前是否启用了模型
- 当前分析模式是否为 LangGraph

## 12. 这次 PR 的边界

这次 PR 的重点是引入多智能体分析后端，不是重做整个产品表层。

因此本次改动更偏向：

- 架构层升级
- 分析链路升级
- 模型接入能力补充
- 结果组织方式增强

不强调：

- 全面替换原仓库前端
- 改变原仓库既有的项目身份信息
- 强行增加新的对外命令入口

## 13. 当前实现的定位

当前多智能体实现更准确的描述是：

“基于 LangGraph 的多角色串行分析流水线”

而不是：

“多个自治 agent 并行协商的复杂系统”

当前方案的优势是：

- 易于理解
- 易于调试
- 没有模型时也能正常运行
- 易于与现有前端整合

这也为后续继续演进留下了空间，例如：

- 并行 agent 执行
- agent 间交叉评审
- 更细的任务拆分
- 更多模型供应商支持

## 14. 总结

本次 PR 的核心价值在于：

- 将代码分析从单体式流程升级为分层、分角色的多智能体工作流
- 保留本地分析的稳定性和可解释性
- 在有模型时显著提升结果的自然语言质量和建议整合能力
- 在无模型时仍然保证项目可用
- 为后续继续扩展模型能力和工作流复杂度打下基础

