// Viztracer 原始数据类型
export interface ViztracerRawEvent {
  name: string;
  ph: string; // 事件类型 ('B' 开始, 'E' 结束)
  ts: number; // 时间戳（微秒）
  pid: number; // 进程ID
  tid: number; // 线程ID
  cat?: string; // 类别
  args?: Record<string, any>;
}

export interface ViztracerRawData {
  traceEvents: ViztracerRawEvent[];
  displayTimeUnit?: string;
  otherData?: Record<string, any>;
}

// 清洗后的函数调用数据
export interface FunctionCall {
  id: string;
  name: string;
  startTime: number; // 开始时间（微秒）
  endTime: number; // 结束时间（微秒）
  duration: number; // 持续时间（微秒）
  depth: number; // 调用深度
  threadId: number;
  processId: number;
  parentId?: string;
  childrenIds: string[];
  isActive: boolean; // 是否当前正在执行
  lineNumber?: number; // 代码行号
}

// 清洗后的性能数据
export interface CleanedViztracerData {
  functionCalls: FunctionCall[];
  threads: number[];
  startTime: number;
  endTime: number;
  totalDuration: number;
}

// 执行步骤
export interface ExecutionStep {
  call: FunctionCall;
  action: 'enter' | 'exit';
  timestamp: number;
}