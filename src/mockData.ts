import { ViztracerRawData } from './types';

// 模拟的 Viztracer 数据，与用户提供的图片示例匹配
export const mockViztracerData: ViztracerRawData = {
  traceEvents: [
    // func1 的调用
    {
      name: 'func1',
      ph: 'B',
      ts: 1000,
      pid: 1234,
      tid: 5678,
      args: { line: 1 }
    },
    {
      name: 'func1',
      ph: 'E',
      ts: 2000,
      pid: 1234,
      tid: 5678,
      args: { line: 5 }
    },
    
    // func2 的调用
    {
      name: 'func2',
      ph: 'B',
      ts: 2000,
      pid: 1234,
      tid: 5678,
      args: { line: 6 }
    },
    {
      name: 'func2',
      ph: 'E',
      ts: 3500,
      pid: 1234,
      tid: 5678,
      args: { line: 10 }
    },
    
    // main 函数调用 func2
    {
      name: '__main__',
      ph: 'B',
      ts: 500,
      pid: 1234,
      tid: 5678,
      args: { line: 11 }
    },
    {
      name: '__main__',
      ph: 'E',
      ts: 4000,
      pid: 1234,
      tid: 5678,
      args: { line: 13 }
    }
  ],
  displayTimeUnit: 'ms'
};

