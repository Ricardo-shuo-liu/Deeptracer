import { useState } from 'react'
import './App.css'
import ExecutionFlow from './components/ExecutionFlow'
import BarChart from './components/BarChart'
import LineChart from './components/LineChart'
import { mockViztracerData } from './mockData'
import { cleanViztracerData } from './utils/dataProcessor'

function App() {
  const [currentStep, setCurrentStep] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [data] = useState(cleanViztracerData(mockViztracerData))

  return (
    <div className="App">
      <header className="bg-blue-600 text-white py-4 px-6 shadow-md">
        <h1 className="text-2xl font-bold">Viztracer 数据可视化</h1>
      </header>
      <main className="flex flex-col lg:flex-row p-4 gap-4">
        {/* 左侧代码和执行流 */}
        <div className="lg:w-1/2 space-y-4">
          <ExecutionFlow 
            data={data} 
            currentStep={currentStep} 
            isPlaying={isPlaying} 
            setCurrentStep={setCurrentStep} 
            setIsPlaying={setIsPlaying} 
          />
        </div>
        {/* 右侧图表 */}
        <div className="lg:w-1/2 space-y-4">
          <BarChart data={data} />
          <LineChart data={data} />
        </div>
      </main>
    </div>
  )
}

export default App