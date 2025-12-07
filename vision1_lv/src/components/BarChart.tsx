import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import { CleanedViztracerData } from '../types';

interface BarChartProps {
  data: CleanedViztracerData;
}

const BarChart: React.FC<BarChartProps> = ({ data }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  // 初始化图表
  useEffect(() => {
    if (chartRef.current) {
      chartInstance.current = echarts.init(chartRef.current);

      // 图表配置
      const option = {
        title: {
          text: '函数耗时排行榜',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: '{b}: {c} 微秒'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: '耗时 (微秒)',
          axisLabel: {
            formatter: '{value}'
          }
        },
        yAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            formatter: '{value}()',
            rotate: 0
          }
        },
        series: [
          {
            name: '耗时',
            type: 'bar',
            data: [],
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#83bff6' },
                { offset: 0.5, color: '#188df0' },
                { offset: 1, color: '#188df0' }
              ])
            },
            emphasis: {
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  { offset: 0, color: '#2378f7' },
                  { offset: 0.7, color: '#2378f7' },
                  { offset: 1, color: '#83bff6' }
                ])
              }
            }
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
      // 按函数名分组并计算总耗时
      const functionMap = new Map<string, number>();
      
      data.functionCalls.forEach(call => {
        const currentTime = functionMap.get(call.name) || 0;
        functionMap.set(call.name, currentTime + call.duration);
      });

      // 转换为图表数据格式
      const chartData = Array.from(functionMap.entries())
        .map(([name, duration]) => ({ name, duration }))
        .sort((a, b) => b.duration - a.duration); // 按耗时降序排序

      // 更新图表
      chartInstance.current.setOption({
        yAxis: {
          data: chartData.map(item => item.name)
        },
        series: [
          {
            data: chartData.map(item => item.duration)
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

export default BarChart;