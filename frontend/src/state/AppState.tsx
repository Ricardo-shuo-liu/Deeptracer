import { createContext, useContext, useMemo, useState, ReactNode } from "react"

type AppStateValue = {
  loading: boolean
  error: string | null
  filters: string[]
  selectedId: string | null
  setLoading: (v: boolean) => void
  setError: (v: string | null) => void
  setFilters: (v: string[]) => void
  setSelectedId: (v: string | null) => void
}

const AppStateContext = createContext<AppStateValue | null>(null)

export function AppStateProvider({ children }: { children: ReactNode }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [filters, setFilters] = useState<string[]>([])
  const [selectedId, setSelectedId] = useState<string | null>(null)

  const value = useMemo(
    () => ({ loading, error, filters, selectedId, setLoading, setError, setFilters, setSelectedId }),
    [loading, error, filters, selectedId]
  )

  return <AppStateContext.Provider value={value}>{children}</AppStateContext.Provider>
}

export function useAppState() {
  const ctx = useContext(AppStateContext)
  if (!ctx) throw new Error("AppStateProvider 未挂载")
  return ctx
}
