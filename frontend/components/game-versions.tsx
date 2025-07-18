"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Check, Package } from "lucide-react"

interface Version {
  id: number
  name: string
  price: number
  original_price: number
  description: string
  features: string[]
}

interface GameVersionsProps {
  versions: Version[]
  onVersionSelect: (version: Version) => void
}

export function GameVersions({ versions, onVersionSelect }: GameVersionsProps) {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(price)
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {versions.map((version) => (
        <Card key={version.id} className="card-steam hover:bg-slate-800/70 transition-all duration-300">
          <CardHeader className="pb-3">
            <CardTitle className="text-white flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Package className="h-5 w-5 text-blue-400" />
                {version.name}
              </div>
              {version.original_price > version.price && (
                <Badge className="bg-green-600 hover:bg-green-600">
                  -{Math.round(((version.original_price - version.price) / version.original_price) * 100)}%
                </Badge>
              )}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-slate-400 text-sm">{version.description}</p>

            <div className="space-y-2">
              <h4 className="text-white font-medium">Inclui:</h4>
              <ul className="space-y-1">
                {version.features.map((feature, index) => (
                  <li key={index} className="flex items-center gap-2 text-sm text-slate-300">
                    <Check className="h-4 w-4 text-green-400 flex-shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>
            </div>

            <div className="pt-4 border-t border-slate-700">
              <div className="flex items-center justify-between mb-3">
                <div>
                  {version.original_price > version.price && (
                    <span className="text-slate-500 line-through text-sm block">
                      {formatPrice(version.original_price)}
                    </span>
                  )}
                  <span className="text-2xl font-bold text-green-400">{formatPrice(version.price)}</span>
                </div>
              </div>

              <Button onClick={() => onVersionSelect(version)} className="w-full btn-steam">
                Selecionar Esta Edição
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
