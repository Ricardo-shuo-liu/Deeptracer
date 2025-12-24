import Split from "react-split"

export default function ThreePane() {
  return (
    <div className="h-[calc(100vh-3rem)]">
      <Split className="flex h-full" sizes={[33, 34, 33]} minSize={200} gutterSize={8} direction="horizontal">
        <div className="h-full overflow-auto p-3 bg-white border-r">
          <div className="font-medium">窗口一</div>
        </div>
        <div className="h-full overflow-auto p-3 bg-white border-r">
          <div className="font-medium">窗口二</div>
        </div>
        <div className="h-full overflow-auto p-3 bg-white">
          <div className="font-medium">窗口三</div>
        </div>
      </Split>
    </div>
  )
}
