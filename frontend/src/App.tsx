import { AppStateProvider } from "@/state/AppState"
import ThreePane from "@/layouts/ThreePane"

export default function App() {
  return (
    <AppStateProvider>
      <div className="h-full bg-gray-100">
        <header className="h-12 px-4 flex items-center justify-between bg-white border-b">
          <div className="font-semibold">Deeptracer</div>
          <div className="text-sm text-gray-500">React 18 • TypeScript • Vite • Tailwind</div>
        </header>
        <ThreePane />
      </div>
    </AppStateProvider>
  )
}
