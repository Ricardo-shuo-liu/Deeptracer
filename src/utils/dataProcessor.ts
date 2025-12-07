import { ViztracerRawData, ViztracerRawEvent, CleanedViztracerData, FunctionCall } from '../types';

// 数据清洗配置
export interface CleaningConfig {
  minDuration: number; // 最小持续时间（微秒），低于此值的事件将被过滤
  maxDepth: number; // 最大调用深度，超过此深度的调用将被剪枝
  enableAggregation: boolean; // 是否启用聚合
  aggregationThreshold: number; // 聚合阈值（微秒）
}

// 默认清洗配置
export const defaultCleaningConfig: CleaningConfig = {
  minDuration: 100, // 0.1 毫秒
  maxDepth: 10,
  enableAggregation: true,
  aggregationThreshold: 500, // 0.5 毫秒
};

/**
 * 清洗 Viztracer 原始数据
 * @param rawData 原始 Viztracer 数据
 * @param config 清洗配置
 * @returns 清洗后的数据
 */
export function cleanViztracerData(rawData: ViztracerRawData, config: CleaningConfig = defaultCleaningConfig): CleanedViztracerData {
  const { traceEvents } = rawData;
  const functionCalls: FunctionCall[] = [];
  const callStack: FunctionCall[] = [];
  const eventMap: Map<string, ViztracerRawEvent> = new Map();
  const threads = new Set<number>();
  let minTime = Infinity;
  let maxTime = 0;

  // 首先将所有事件按时间戳排序
  const sortedEvents = [...traceEvents].sort((a, b) => a.ts - b.ts);

  // 处理开始事件，构建调用栈
  for (const event of sortedEvents) {
    if (event.ph === 'B') {
      // 开始事件
      eventMap.set(`${event.name}-${event.ts}-${event.tid}`, event);
      threads.add(event.tid);
    } else if (event.ph === 'E') {
      // 结束事件，寻找对应的开始事件
      const startEventKey = `${event.name}-${event.ts}-${event.tid}`;
      let startEvent = eventMap.get(startEventKey);
      
      // 如果找不到精确匹配，尝试查找最近的同名开始事件
      if (!startEvent) {
        // 这是一个简化的查找方式，实际应用中可能需要更复杂的匹配逻辑
        const candidateEvents = Array.from(eventMap.entries())
          .filter(([key, e]) => key.startsWith(`${event.name}-`) && key.endsWith(`-${event.tid}`))
          .map(([_, e]) => e)
          .filter(e => e.ts <= event.ts);
        
        if (candidateEvents.length > 0) {
          startEvent = candidateEvents[candidateEvents.length - 1];
        }
      }

      if (startEvent) {
        const duration = event.ts - startEvent.ts;
        
        // 过滤掉极短的调用
        if (duration < config.minDuration) {
          continue;
        }

        // 计算调用深度
        const depth = callStack.filter(call => call.threadId === event.tid && call.endTime === 0).length;
        
        // 剪枝过深的调用
        if (depth > config.maxDepth) {
          continue;
        }

        const call: FunctionCall = {
          id: `${startEvent.name}-${startEvent.ts}-${startEvent.tid}`,
          name: startEvent.name,
          startTime: startEvent.ts,
          endTime: event.ts,
          duration,
          depth,
          threadId: event.tid,
          processId: event.pid,
          parentId: undefined,
          childrenIds: [],
          isActive: false,
          lineNumber: startEvent.args?.line,
        };

        // 处理父子关系
        const currentThreadCalls = callStack.filter(c => c.threadId === event.tid && c.endTime === 0);
        if (currentThreadCalls.length > 0) {
          const parentCall = currentThreadCalls[currentThreadCalls.length - 1];
          call.parentId = parentCall.id;
          parentCall.childrenIds.push(call.id);
        }

        functionCalls.push(call);
        callStack.push(call);
        
        // 更新时间范围
        minTime = Math.min(minTime, startEvent.ts);
        maxTime = Math.max(maxTime, event.ts);
      }
    }
  }

  // 清理调用栈，设置结束时间
  for (const call of callStack) {
    if (call.endTime === 0) {
      call.endTime = maxTime;
      call.duration = call.endTime - call.startTime;
    }
  }

  // 如果启用聚合，合并连续的相同函数调用
  if (config.enableAggregation) {
    const aggregatedCalls: FunctionCall[] = [];
    let lastCall: FunctionCall | null = null;

    for (const call of functionCalls.sort((a, b) => a.startTime - b.startTime)) {
      if (lastCall && 
          call.name === lastCall.name && 
          call.threadId === lastCall.threadId &&
          call.startTime - lastCall.endTime < config.aggregationThreshold) {
        // 合并调用
        lastCall.endTime = call.endTime;
        lastCall.duration = lastCall.endTime - lastCall.startTime;
        lastCall.childrenIds = [...lastCall.childrenIds, ...call.childrenIds];
      } else {
        aggregatedCalls.push(call);
        lastCall = call;
      }
    }

    return {
      functionCalls: aggregatedCalls,
      threads: Array.from(threads),
      startTime: minTime,
      endTime: maxTime,
      totalDuration: maxTime - minTime,
    };
  }

  return {
    functionCalls,
    threads: Array.from(threads),
    startTime: minTime,
    endTime: maxTime,
    totalDuration: maxTime - minTime,
  };
}

/**
 * 生成执行步骤序列
 * @param data 清洗后的数据
 * @returns 执行步骤数组
 */
export function generateExecutionSteps(data: CleanedViztracerData) {
  const steps: Array<{ call: FunctionCall; action: 'enter' | 'exit'; timestamp: number }> = [];

  // 为每个函数调用添加进入和退出步骤
  for (const call of data.functionCalls) {
    steps.push({
      call,
      action: 'enter',
      timestamp: call.startTime,
    });
    steps.push({
      call,
      action: 'exit',
      timestamp: call.endTime,
    });
  }

  // 按时间戳排序
  return steps.sort((a, b) => a.timestamp - b.timestamp);
}