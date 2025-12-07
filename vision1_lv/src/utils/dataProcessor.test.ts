import { describe, it, expect, beforeEach } from '@jest/globals';
import { cleanViztracerData, generateExecutionSteps, defaultCleaningConfig, CleaningConfig } from './dataProcessor';
import { ViztracerRawData, ViztracerRawEvent, CleanedViztracerData } from '../types';

// 测试数据
const mockRawData: ViztracerRawData = {
  traceEvents: [
    // 函数调用开始和结束事件
    { name: 'functionA', ph: 'B', ts: 1000, pid: 1, tid: 1, args: { line: 10 } },
    { name: 'functionB', ph: 'B', ts: 1500, pid: 1, tid: 1, args: { line: 20 } },
    { name: 'functionB', ph: 'E', ts: 2000, pid: 1, tid: 1 },
    { name: 'functionA', ph: 'E', ts: 2500, pid: 1, tid: 1 },
    // 短函数调用，应该被过滤
    { name: 'shortFunc', ph: 'B', ts: 3000, pid: 1, tid: 1, args: { line: 30 } },
    { name: 'shortFunc', ph: 'E', ts: 3050, pid: 1, tid: 1 }, // 持续时间50微秒，低于默认阈值100
    // 线程2的调用
    { name: 'functionC', ph: 'B', ts: 1200, pid: 1, tid: 2, args: { line: 40 } },
    { name: 'functionC', ph: 'E', ts: 1800, pid: 1, tid: 2 },
  ],
};

describe('Data Processor Tests', () => {
  describe('cleanViztracerData', () => {
    it('should clean and process raw viztracer data correctly with default config', () => {
      const result = cleanViztracerData(mockRawData);
      
      // 验证基本数据结构
      expect(result).toHaveProperty('functionCalls');
      expect(result).toHaveProperty('threads');
      expect(result).toHaveProperty('startTime');
      expect(result).toHaveProperty('endTime');
      expect(result).toHaveProperty('totalDuration');
      
      // 验证线程数
      expect(result.threads).toEqual([1, 2]);
      
      // 验证时间范围
      expect(result.startTime).toBe(1000);
      expect(result.endTime).toBe(2500);
      expect(result.totalDuration).toBe(1500);
      
      // 验证函数调用数量（shortFunc应该被过滤）
      expect(result.functionCalls.length).toBe(3); // functionA, functionB, functionC
      
      // 验证函数调用存在性
      const functionA = result.functionCalls.find(call => call.name === 'functionA');
      const functionB = result.functionCalls.find(call => call.name === 'functionB');
      const functionC = result.functionCalls.find(call => call.name === 'functionC');
      
      expect(functionA).toBeDefined();
      expect(functionB).toBeDefined();
      expect(functionC).toBeDefined();
      
      // 验证调用的基本属性
      if (functionA) {
        expect(functionA.name).toBe('functionA');
        expect(functionA.threadId).toBe(1);
        expect(functionA.duration).toBe(1500); // 2500 - 1000
      }
      
      if (functionB) {
        expect(functionB.name).toBe('functionB');
        expect(functionB.threadId).toBe(1);
        expect(functionB.duration).toBe(500); // 2000 - 1500
      }
      
      if (functionC) {
        expect(functionC.name).toBe('functionC');
        expect(functionC.threadId).toBe(2);
        expect(functionC.duration).toBe(600); // 1800 - 1200
      }
    });
    
    it('should filter short duration events based on minDuration config', () => {
      const config: CleaningConfig = {
        ...defaultCleaningConfig,
        minDuration: 200, // 提高阈值到200微秒
      };
      
      const result = cleanViztracerData(mockRawData, config);
      
      // functionB 持续时间500微秒，functionC 持续时间600微秒，都应该保留
      // functionA 持续时间1500微秒，应该保留
      expect(result.functionCalls.length).toBe(3);
    });
    
    it('should disable aggregation when enableAggregation is false', () => {
      const config: CleaningConfig = {
        ...defaultCleaningConfig,
        enableAggregation: false,
      };
      
      // 添加连续的相同函数调用进行测试
      const testDataWithDuplicates: ViztracerRawData = {
        traceEvents: [
          { name: 'duplicateFunc', ph: 'B', ts: 1000, pid: 1, tid: 1 },
          { name: 'duplicateFunc', ph: 'E', ts: 1100, pid: 1, tid: 1 },
          { name: 'duplicateFunc', ph: 'B', ts: 1200, pid: 1, tid: 1 },
          { name: 'duplicateFunc', ph: 'E', ts: 1300, pid: 1, tid: 1 },
        ],
      };
      
      const result = cleanViztracerData(testDataWithDuplicates, config);
      
      // 不启用聚合时，应该保留两个调用
      expect(result.functionCalls.length).toBe(2);
    });
    
    it('should handle single thread data correctly', () => {
      const singleThreadData: ViztracerRawData = {
        traceEvents: [
          { name: 'func1', ph: 'B', ts: 1000, pid: 1, tid: 1 },
          { name: 'func1', ph: 'E', ts: 2000, pid: 1, tid: 1 },
        ],
      };
      
      const result = cleanViztracerData(singleThreadData);
      
      expect(result.threads).toEqual([1]);
      expect(result.functionCalls.length).toBe(1);
    });
  });
  
  describe('generateExecutionSteps', () => {
    it('should generate correct execution steps from cleaned data', () => {
      const cleanedData: CleanedViztracerData = {
        functionCalls: [
          {
            id: 'func1-1000-1',
            name: 'func1',
            startTime: 1000,
            endTime: 2000,
            duration: 1000,
            depth: 0,
            threadId: 1,
            processId: 1,
            childrenIds: ['func2-1500-1'],
            isActive: false,
            lineNumber: 10,
          },
          {
            id: 'func2-1500-1',
            name: 'func2',
            startTime: 1500,
            endTime: 1800,
            duration: 300,
            depth: 1,
            threadId: 1,
            processId: 1,
            parentId: 'func1-1000-1',
            childrenIds: [],
            isActive: false,
            lineNumber: 20,
          },
        ],
        threads: [1],
        startTime: 1000,
        endTime: 2000,
        totalDuration: 1000,
      };
      
      const steps = generateExecutionSteps(cleanedData);
      
      // 应该生成4个步骤：func1进入，func2进入，func2退出，func1退出
      expect(steps.length).toBe(4);
      
      // 验证步骤顺序和内容
      expect(steps[0]).toEqual({
        call: cleanedData.functionCalls[0],
        action: 'enter',
        timestamp: 1000,
      });
      
      expect(steps[1]).toEqual({
        call: cleanedData.functionCalls[1],
        action: 'enter',
        timestamp: 1500,
      });
      
      expect(steps[2]).toEqual({
        call: cleanedData.functionCalls[1],
        action: 'exit',
        timestamp: 1800,
      });
      
      expect(steps[3]).toEqual({
        call: cleanedData.functionCalls[0],
        action: 'exit',
        timestamp: 2000,
      });
      
      // 验证按时间排序
      for (let i = 0; i < steps.length - 1; i++) {
        expect(steps[i].timestamp).toBeLessThanOrEqual(steps[i + 1].timestamp);
      }
    });
  });
});
