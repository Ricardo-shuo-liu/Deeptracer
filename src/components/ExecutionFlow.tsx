import React, { useEffect, useState, useRef } from 'react';
import { CleanedViztracerData, FunctionCall } from '../types';
import { generateExecutionSteps } from '../utils/dataProcessor';
import mockCode from '../data/example.py?raw';

interface ExecutionFlowProps {
  data: CleanedViztracerData;
  currentStep: number;
  isPlaying: boolean;
  setCurrentStep: (step: number) => void;
  setIsPlaying: (isPlaying: boolean) => void;
}

const ExecutionFlow: React.FC<ExecutionFlowProps> = ({
  data,
  currentStep,
  isPlaying,
  setCurrentStep,
  setIsPlaying
}) => {
  const [executionSteps, setExecutionSteps] = useState<Array<{ call: FunctionCall; action: 'enter' | 'exit'; timestamp: number }>>([]);
  const [activeLines, setActiveLines] = useState<Set<number>>(new Set());
  const [activeFunction, setActiveFunction] = useState<string | null>(null);
  const animationRef = useRef<NodeJS.Timeout | null>(null);
  const totalStepsRef = useRef<number>(0);

  // 生成执行步骤
  useEffect(() => {
    const steps = generateExecutionSteps(data);
    setExecutionSteps(steps);
    totalStepsRef.current = steps.length;
  }, [data]);

  // 动画播放逻辑
  useEffect(() => {
    if (isPlaying) {
      animationRef.current = setInterval(() => {
        setCurrentStep(prev => {
          const nextStep = prev + 1;
          if (nextStep >= totalStepsRef.current) {
            setIsPlaying(false);
            return prev;
          }
          return nextStep;
        });
      }, 1000); // 每秒执行一步
    } else {
      if (animationRef.current) {
        clearInterval(animationRef.current);
        animationRef.current = null;
      }
    }

    return () => {
      if (animationRef.current) {
        clearInterval(animationRef.current);
        animationRef.current = null;
      }
    };
  }, [isPlaying, setCurrentStep, setIsPlaying]);

  // 更新当前执行状态
  useEffect(() => {
    if (executionSteps.length === 0) return;

    const activeCalls = new Set<FunctionCall>();
    const lines = new Set<number>();

    // 执行到当前步骤之前的所有操作
    for (let i = 0; i <= currentStep && i < executionSteps.length; i++) {
      const step = executionSteps[i];
      const { call, action } = step;

      if (action === 'enter') {
        activeCalls.add(call);
        if (call.lineNumber) {
          lines.add(call.lineNumber);
        }
      } else {
        activeCalls.delete(call);
      }
    }

    setActiveLines(lines);
    setActiveFunction(activeCalls.size > 0 ? Array.from(activeCalls)[activeCalls.size - 1].name : null);
  }, [currentStep, executionSteps]);

  // 代码行渲染
  const renderCodeLines = () => {
    const lines = mockCode.split('\n');
    return lines.map((line, index) => {
      const lineNumber = index + 1;
      const isActive = activeLines.has(lineNumber);
      const isCurrent = lineNumber === getCurrentLineNumber();

      return (
        <div 
          key={lineNumber}
          className={`flex items-center gap-3 py-1 px-2 ${isCurrent ? 'bg-green-100' : ''}`}
        >
          <div className="w-8 text-right text-gray-500">{lineNumber}</div>
          <div 
            className={`flex-1 text-left font-mono ${isActive ? 'font-bold' : ''}`}
            style={{
              color: isCurrent ? '#22c55e' : isActive ? '#ef4444' : '#374151'
            }}
          >
            {line}
          </div>
        </div>
      );
    });
  };

  // 获取当前执行行号
  const getCurrentLineNumber = (): number | undefined => {
    if (executionSteps.length === 0 || currentStep >= executionSteps.length) return undefined;
    
    const step = executionSteps[currentStep];
    return step.call.lineNumber;
  };

  // 控制按钮点击处理
  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleStepForward = () => {
    if (currentStep < executionSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleStepBackward = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleFirstStep = () => {
    setCurrentStep(0);
  };

  const handleLastStep = () => {
    setCurrentStep(executionSteps.length - 1);
  };

  // 渲染调用关系图
  const renderCallGraph = () => {
    const functions = new Set<string>();
    data.functionCalls.forEach(call => functions.add(call.name));
    const functionList = Array.from(functions);

    return (
      <div className="bg-white p-4 rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-lg font-semibold">函数调用关系</h3>
          <div className="text-sm text-gray-500">
            当前: {activeFunction || '无'}
          </div>
        </div>
        <div className="space-y-2">
          {functionList.map((func, index) => (
            <div 
              key={func}
              className={`flex items-center gap-2 p-2 rounded ${activeFunction === func ? 'bg-blue-100 border-l-4 border-blue-500' : 'bg-gray-50'}`}
            >
              <div className={`w-4 h-4 rounded-full ${activeFunction === func ? 'bg-blue-500' : 'bg-gray-300'}`}></div>
              <div className="font-mono">{func}()</div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-4">
      {/* 代码展示 */}
      <div className="bg-white p-4 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-2">Python 代码</h3>
        <div className="border rounded-lg p-2">
          {renderCodeLines()}
        </div>
      </div>

      {/* 函数调用关系图 */}
      {renderCallGraph()}

      {/* 控制栏 */}
      <div className="bg-white p-4 rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-lg font-semibold">执行控制</h3>
          <div className="text-sm text-gray-500">
            步骤 {currentStep + 1} / {executionSteps.length}
          </div>
        </div>
        <div className="flex gap-2 items-center">
          <button 
            onClick={handleFirstStep}
            className="px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded"
            disabled={currentStep === 0}
          >
            &lt;&lt; 第一
          </button>
          <button 
            onClick={handleStepBackward}
            className="px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded"
            disabled={currentStep === 0}
          >
            &lt; 上一步
          </button>
          <button 
            onClick={handlePlayPause}
            className="px-4 py-1 bg-blue-500 hover:bg-blue-600 text-white rounded"
          >
            {isPlaying ? '暂停' : '播放'}
          </button>
          <button 
            onClick={handleStepForward}
            className="px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded"
            disabled={currentStep >= executionSteps.length - 1}
          >
            下一步 &gt;
          </button>
          <button 
            onClick={handleLastStep}
            className="px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded"
            disabled={currentStep >= executionSteps.length - 1}
          >
            最后 &gt;&gt;
          </button>
          <div className="flex-1 ml-4">
            <input
              type="range"
              min="0"
              max={executionSteps.length - 1}
              value={currentStep}
              onChange={(e) => setCurrentStep(parseInt(e.target.value))}
              className="w-full"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExecutionFlow;