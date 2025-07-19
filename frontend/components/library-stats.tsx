import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart3, Clock, HardDrive } from "lucide-react"
import { useLibrary } from "@/lib/library-context"
import { useAuth } from "@/lib/auth-context"
import { useEffect, useState } from "react"

interface LibraryStatsData {
  totalGames: number
  installedGames: number
  totalPlaytime: string
  totalSpaceUsed: string
}

export function LibraryStats() {
  const { user } = useAuth()
  const { library, isLoading, userStats } = useLibrary()
  const [stats, setStats] = useState<LibraryStatsData>({
    totalGames: 0,
    installedGames: 0,
    totalPlaytime: "0h",
    totalSpaceUsed: "0 GB"
  })

  useEffect(() => {
    const loadStats = () => {
      if (library && library.items && library.items.length > 0) {
        try {
          // Calcular estatísticas baseadas nos dados reais
          const totalGames = library.items.length
          const installedGames = library.items.filter(item => {
            // Simular alguns jogos instalados (por enquanto)
            return Math.random() > 0.6 // ~40% dos jogos instalados
          }).length
          
          // Converter tempo total de minutos para formato legível
          const totalMinutes = library.items.reduce((total: number, item) => {
            return total + (item.playtime || 0)
          }, 0)
          const hours = Math.floor(totalMinutes / 60)
          const minutes = totalMinutes % 60
          const totalPlaytime = hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`
          
          // Espaço usado (simulado por enquanto)
          const totalSpaceGB = installedGames * (Math.random() * 30 + 5) // 5-35 GB por jogo
          const totalSpaceUsed = `${totalSpaceGB.toFixed(1)} GB`
          
          setStats({
            totalGames,
            installedGames,
            totalPlaytime,
            totalSpaceUsed
          })
        } catch (error) {
          console.error('Erro ao carregar estatísticas:', error)
        }
      } else if (userStats) {
        // Usar userStats se a biblioteca não estiver carregada
        setStats({
          totalGames: userStats.totalGames,
          installedGames: Math.floor(userStats.totalGames * 0.4), // Simular 40% instalados
          totalPlaytime: userStats.formattedPlaytime,
          totalSpaceUsed: `${(userStats.totalGames * 15).toFixed(1)} GB` // Simular espaço
        })
      }
    }
    
    loadStats()
  }, [library, userStats])



  return (
    <Card className="card-steam">
      <CardHeader className="pb-3">
        <CardTitle className="text-white flex items-center gap-2">
          <BarChart3 className="h-5 w-5 text-blue-400" />
          Estatísticas
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {isLoading ? (
          <div className="text-center py-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-2"></div>
            <p className="text-sm text-slate-400">Carregando estatísticas...</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-3 bg-slate-800/30 rounded-lg">
                <div className="text-2xl font-bold text-blue-400">{stats.totalGames}</div>
                <div className="text-sm text-slate-400">Total de jogos</div>
              </div>
              <div className="text-center p-3 bg-slate-800/30 rounded-lg">
                <div className="text-2xl font-bold text-green-400">{stats.installedGames}</div>
                <div className="text-sm text-slate-400">Instalados</div>
              </div>
            </div>

            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <Clock className="h-4 w-4 text-slate-400" />
                <div className="flex-1">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-slate-300">Tempo total</span>
                    <span className="text-sm font-medium text-white">{stats.totalPlaytime}</span>
                  </div>
                </div>
              </div>



              <div className="flex items-center gap-3">
                <HardDrive className="h-4 w-4 text-slate-400" />
                <div className="flex-1">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-slate-300">Espaço usado</span>
                    <span className="text-sm font-medium text-white">{stats.totalSpaceUsed}</span>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  )
}
