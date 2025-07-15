"use client"

import { useState, useEffect } from "react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import { CheckCircle, XCircle, AlertTriangle, Info, X } from "lucide-react"

interface AlertMessage {
  id: string
  type: "success" | "error" | "warning" | "info"
  message: string
  duration?: number
}

// Mock alerts - replace with actual alert system
const mockAlerts: AlertMessage[] = [
  // { id: "1", type: "success", message: "Login realizado com sucesso!", duration: 5000 },
  // { id: "2", type: "error", message: "Erro ao processar pagamento.", duration: 0 },
]

export function AlertSystem() {
  const [alerts, setAlerts] = useState<AlertMessage[]>(mockAlerts)

  const removeAlert = (id: string) => {
    setAlerts((prev) => prev.filter((alert) => alert.id !== id))
  }

  useEffect(() => {
    alerts.forEach((alert) => {
      if (alert.duration && alert.duration > 0) {
        const timer = setTimeout(() => {
          removeAlert(alert.id)
        }, alert.duration)

        return () => clearTimeout(timer)
      }
    })
  }, [alerts])

  if (alerts.length === 0) return null

  const getAlertIcon = (type: AlertMessage["type"]) => {
    switch (type) {
      case "success":
        return <CheckCircle className="h-4 w-4" />
      case "error":
        return <XCircle className="h-4 w-4" />
      case "warning":
        return <AlertTriangle className="h-4 w-4" />
      case "info":
        return <Info className="h-4 w-4" />
    }
  }

  const getAlertStyles = (type: AlertMessage["type"]) => {
    switch (type) {
      case "success":
        return "border-green-500/50 bg-green-500/10 text-green-400"
      case "error":
        return "border-red-500/50 bg-red-500/10 text-red-400"
      case "warning":
        return "border-yellow-500/50 bg-yellow-500/10 text-yellow-400"
      case "info":
        return "border-blue-500/50 bg-blue-500/10 text-blue-400"
    }
  }

  return (
    <div className="fixed top-20 right-4 z-50 space-y-2 max-w-md">
      {alerts.map((alert) => (
        <Alert key={alert.id} className={`${getAlertStyles(alert.type)} animate-in slide-in-from-right`}>
          <div className="flex items-start justify-between">
            <div className="flex items-center space-x-2">
              {getAlertIcon(alert.type)}
              <AlertDescription className="font-medium">{alert.message}</AlertDescription>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => removeAlert(alert.id)}
              className="h-6 w-6 p-0 hover:bg-transparent"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </Alert>
      ))}
    </div>
  )
}
