import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Monitor, Zap } from "lucide-react"

interface Requirements {
  os: string
  processor: string
  memory: string
  graphics: string
  directx: string
  storage: string
  sound_card: string
  additional_notes: string
}

interface SystemRequirementsProps {
  requirements: {
    minimum: Requirements
    recommended: Requirements
  }
}

export function SystemRequirements({ requirements }: SystemRequirementsProps) {
  const RequirementCard = ({ title, reqs, icon: Icon }: { title: string; reqs: Requirements; icon: any }) => (
    <Card className="card-steam">
      <CardHeader className="pb-3">
        <CardTitle className="text-white flex items-center gap-2">
          <Icon className="h-5 w-5 text-blue-400" />
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="grid gap-3 text-sm">
          <div className="flex justify-between">
            <span className="text-slate-400">Sistema Operacional:</span>
            <span className="text-white text-right">{reqs.os}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Processador:</span>
            <span className="text-white text-right">{reqs.processor}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Memória:</span>
            <span className="text-white text-right">{reqs.memory}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Placa de Vídeo:</span>
            <span className="text-white text-right">{reqs.graphics}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">DirectX:</span>
            <span className="text-white text-right">{reqs.directx}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Armazenamento:</span>
            <span className="text-white text-right">{reqs.storage}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Placa de Som:</span>
            <span className="text-white text-right">{reqs.sound_card}</span>
          </div>
          {reqs.additional_notes && (
            <div className="pt-2 border-t border-slate-700">
              <span className="text-slate-400 text-xs">Observações:</span>
              <p className="text-slate-300 text-xs mt-1">{reqs.additional_notes}</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <RequirementCard title="Requisitos Mínimos" reqs={requirements.minimum} icon={Monitor} />
      <RequirementCard title="Requisitos Recomendados" reqs={requirements.recommended} icon={Zap} />
    </div>
  )
}
