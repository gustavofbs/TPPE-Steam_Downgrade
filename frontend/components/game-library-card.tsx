"use client"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Play,
  Download,
  Trash2,
  MoreVertical,
  Settings,
  FolderOpen,
  Clock,
  Trophy,
  Pause,
  RotateCcw,
} from "lucide-react"
import Image from "next/image"

interface Game {
  id: string | number
  title: string
  image: string
  isInstalled: boolean
  lastPlayed: string
  totalPlaytime: string
  achievements: { unlocked: number; total: number }
  installSize: string
  version: string
  status: "ready" | "installing" | "updating" | "downloading" | "not_installed"
  downloadProgress?: number
  isFavorite?: boolean
}

interface GameLibraryCardProps {
  game: Game
  viewMode: "grid" | "list"
}

export function GameLibraryCard({ game, viewMode }: GameLibraryCardProps) {
  const [isActionLoading, setIsActionLoading] = useState(false)

  const handleAction = async (action: string) => {
    setIsActionLoading(true)
    // Simulate action
    await new Promise((resolve) => setTimeout(resolve, 1000))
    console.log(`${action} ${game.title}`)
    setIsActionLoading(false)
  }

  const getStatusBadge = () => {
    switch (game.status) {
      case "downloading":
        return (
          <Badge className="bg-blue-600 hover:bg-blue-600">
            <Download className="h-3 w-3 mr-1" />
            Baixando {game.downloadProgress}%
          </Badge>
        )
      case "installing":
        return (
          <Badge className="bg-yellow-600 hover:bg-yellow-600">
            <Download className="h-3 w-3 mr-1" />
            Instalando
          </Badge>
        )
      case "updating":
        return (
          <Badge className="bg-orange-600 hover:bg-orange-600">
            <RotateCcw className="h-3 w-3 mr-1" />
            Atualizando {game.downloadProgress}%
          </Badge>
        )
      case "ready":
        return game.isInstalled ? <Badge className="bg-green-600 hover:bg-green-600">Instalado</Badge> : null
      default:
        return null
    }
  }

  const getPrimaryAction = () => {
    if (isActionLoading) {
      return (
        <Button disabled className="btn-steam">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
          Processando...
        </Button>
      )
    }

    switch (game.status) {
      case "ready":
        return game.isInstalled ? (
          <Button onClick={() => handleAction("play")} className="btn-steam">
            <Play className="h-4 w-4 mr-2" />
            Jogar
          </Button>
        ) : (
          <Button onClick={() => handleAction("install")} className="btn-steam">
            <Download className="h-4 w-4 mr-2" />
            Instalar
          </Button>
        )
      case "downloading":
      case "installing":
      case "updating":
        return (
          <Button onClick={() => handleAction("pause")} variant="outline" className="border-slate-600">
            <Pause className="h-4 w-4 mr-2" />
            Pausar
          </Button>
        )
      default:
        return (
          <Button onClick={() => handleAction("install")} className="btn-steam">
            <Download className="h-4 w-4 mr-2" />
            Instalar
          </Button>
        )
    }
  }

  if (viewMode === "list") {
    return (
      <Card className="card-steam hover:bg-slate-800/70 transition-all duration-300">
        <CardContent className="p-4">
          <div className="flex gap-4">
            <div className="relative w-20 h-28 flex-shrink-0">
              <Image src={game.image || "/placeholder.svg"} alt={game.title} fill className="object-cover rounded" />
              {getStatusBadge() && <div className="absolute -top-2 -right-2 z-10">{getStatusBadge()}</div>}
            </div>

            <div className="flex-1 flex justify-between items-center">
              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-white">{game.title}</h3>
                <div className="flex items-center gap-4 text-sm text-slate-400">
                  <div className="flex items-center gap-1">
                    <Clock className="h-4 w-4" />
                    <span>{game.lastPlayed}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Trophy className="h-4 w-4" />
                    <span>
                      {game.achievements.unlocked}/{game.achievements.total}
                    </span>
                  </div>
                </div>
                <p className="text-sm text-slate-500">
                  Tempo jogado: {game.totalPlaytime} • {game.installSize}
                </p>

                {(game.status === "downloading" || game.status === "updating") && game.downloadProgress && (
                  <div className="w-48">
                    <Progress value={game.downloadProgress} className="h-2" />
                  </div>
                )}
              </div>

              <div className="flex items-center gap-2">
                {getPrimaryAction()}

                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="outline" size="sm" className="border-slate-600 bg-transparent">
                      <MoreVertical className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent className="bg-slate-800 border-slate-700" align="end">
                    <DropdownMenuItem className="text-slate-300 hover:text-white hover:bg-slate-700">
                      <Settings className="mr-2 h-4 w-4" />
                      Propriedades
                    </DropdownMenuItem>
                    <DropdownMenuItem className="text-slate-300 hover:text-white hover:bg-slate-700">
                      <FolderOpen className="mr-2 h-4 w-4" />
                      Abrir pasta
                    </DropdownMenuItem>
                    {game.isInstalled && (
                      <>
                        <DropdownMenuSeparator className="bg-slate-700" />
                        <DropdownMenuItem className="text-red-400 hover:text-red-300 hover:bg-slate-700">
                          <Trash2 className="mr-2 h-4 w-4" />
                          Desinstalar
                        </DropdownMenuItem>
                      </>
                    )}
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="card-steam hover:bg-slate-800/70 transition-all duration-300 group overflow-hidden">
      <div className="flex gap-4 p-4">
        <div className="relative w-24 h-32 flex-shrink-0">
          <Image src={game.image || "/placeholder.svg"} alt={game.title} fill className="object-cover rounded" />
          {getStatusBadge() && <div className="absolute -top-2 -right-2 z-10">{getStatusBadge()}</div>}
        </div>

        <div className="flex-1 space-y-3">
          <div>
            <h3 className="text-lg font-semibold text-white group-hover:text-blue-300 transition-colors">
              {game.title}
            </h3>
            <p className="text-sm text-slate-400">Última vez jogado: {game.lastPlayed}</p>
          </div>

          <div className="flex items-center gap-4 text-sm text-slate-500">
            <span>Tempo: {game.totalPlaytime}</span>
            <span>
              Conquistas: {game.achievements.unlocked}/{game.achievements.total}
            </span>
          </div>

          {(game.status === "downloading" || game.status === "updating") && game.downloadProgress && (
            <div className="space-y-1">
              <Progress value={game.downloadProgress} className="h-2" />
              <p className="text-xs text-slate-400">{game.downloadProgress}% concluído</p>
            </div>
          )}

          <div className="flex gap-2 pt-2">
            {getPrimaryAction()}

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" size="sm" className="border-slate-600 bg-transparent">
                  <MoreVertical className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="bg-slate-800 border-slate-700" align="end">
                <DropdownMenuItem className="text-slate-300 hover:text-white hover:bg-slate-700">
                  <Settings className="mr-2 h-4 w-4" />
                  Propriedades
                </DropdownMenuItem>
                <DropdownMenuItem className="text-slate-300 hover:text-white hover:bg-slate-700">
                  <FolderOpen className="mr-2 h-4 w-4" />
                  Abrir pasta
                </DropdownMenuItem>
                {game.isInstalled && (
                  <>
                    <DropdownMenuSeparator className="bg-slate-700" />
                    <DropdownMenuItem className="text-red-400 hover:text-red-300 hover:bg-slate-700">
                      <Trash2 className="mr-2 h-4 w-4" />
                      Desinstalar
                    </DropdownMenuItem>
                  </>
                )}
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </div>
    </Card>
  )
}
