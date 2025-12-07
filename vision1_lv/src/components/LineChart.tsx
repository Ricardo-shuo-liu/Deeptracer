import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import { CleanedViztracerData } from '../types';

interface LineChartProps {
  data: CleanedViztracerData;
}

const LineChart: React.FC<LineChartProps> = ({ data }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  // 初始化图表
  useEffect(() => {
    if (chartRef.current) {
      chartInstance.current = echarts.init(chartRef.current);

      // 图表配置
      const option = {
        title: {
          text: '函数调用时间线',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          formatter: function(params: any) {
            return `${params[0].name}: ${params[0].value} 微秒<br/>函数: ${params[0].data.functionName}`;
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'time',
          name: '时间',
          axisLabel: {
            formatter: function(value: number) {
              // 将时间戳转换为相对时间（秒）
              const relativeTime = (value - data.startTime) / 1000000;
              return `${relativeTime.toFixed(2)}s`;
            }
          },
          splitLine: {
            show: true
          }
        },
        yAxis: {
          type: 'value',
          name: '线程ID',
          splitLine: {
            show: true
          }
        },
        dataZoom: [
          {
            type: 'inside',
            start: 0,
            end: 100
          },
          {
            start: 0,
            end: 100
          }
        ],
        series: [
          {
            name: '函数调用',
            type: 'line',
            symbol: 'circle',
            symbolSize: 8,
            lineStyle: {
              width: 2
            },
            itemStyle: {
              color: '#3b82f6'
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(59, 130, 246, 0.5)' },
                { offset: 1, color: 'rgba(59, 130, 246, 0.1)' }
              ])
            },
            data: []
          }
        ]
      };

      chartInstance.current.setOption(option);

      // 窗口大小变化时重新调整图表
      const handleResize = () => {
        chartInstance.current?.resize();
      };

      window.addEventListener('resize', handleResize);

      return () => {
        window.removeEventListener('resize', handleResize);
        chartInstance.current?.dispose();
      };
    }
  }, []);

  // 更新图表数据
  useEffect(() => {
    if (chartInstance.current && data.functionCalls.length > 0) {
      // 准备时间线数据
      const timelineData = data.functionCalls.map(call => ({
        name: new Date(call.startTime / 1000).toLocaleTimeString(),
        value: call.startTime,
        functionName: call.name
      }));

      // 按时间排序
      timelineData.sort((a, b) => a.value - b.value);

      // 添加结束时间点
      data.functionCalls.forEach(call => {
        timelineData.push({
          name: new Date(call.endTime / 1000).toLocaleTimeString(),
          value: call.endTime,
          functionName: call.name
        });
      });

      // 再次排序
      timelineData.sort((a, b) => a.value - b.value);

      // 更新图表
      chartInstance.current.setOption({
        xAxis: {
          min: data.startTime,
          max: data.endTime
        },
        series: [
          {
            data: timelineData
          }
        ]
      });
    }
  }, [data]);

  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <div 
        ref={chartRef} 
        style={{ height: '300px', width: '100%' }}
      ></div>
    </div>
  );
};

export default LineChart;