import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { BarChart3, Clock, Trophy, HardDrive } from "lucide-react"

interface User {
  username: string
  totalGames: number
  installedGames: number
  totalPlaytime: string
  totalAchievements: number
  maxAchievements: number
}

interface LibraryStatsProps {
  user: User
}

export function LibraryStats({ user }: LibraryStatsProps) {
  const achievementPercentage = (user.totalAchievements / user.maxAchievements) * 100

  return (
    <Card className="card-steam">
      <CardHeader className="pb-3">
        <CardTitle className="text-white flex items-center gap-2">
          <BarChart3 className="h-5 w-5 text-blue-400" />
          Estatísticas
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center p-3 bg-slate-800/30 rounded-lg">
            <div className="text-2xl font-bold text-blue-400">{user.totalGames}</div>
            <div className="text-sm text-slate-400">Total de jogos</div>
          </div>
          <div className="text-center p-3 bg-slate-800/30 rounded-lg">
            <div className="text-2xl font-bold text-green-400">{user.installedGames}</div>
            <div className="text-sm text-slate-400">Instalados</div>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <Clock className="h-4 w-4 text-slate-400" />
            <div className="flex-1">
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-300">Tempo total</span>
                <span className="text-sm font-medium text-white">{user.totalPlaytime}</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Trophy className="h-4 w-4 text-slate-400" />
            <div className="flex-1">
              <div className="flex justify-between items-center mb-1">
                <span className="text-sm text-slate-300">Conquistas</span>
                <span className="text-sm font-medium text-white">
                  {user.totalAchievements}/{user.maxAchievements}
                </span>
              </div>
              <Progress value={achievementPercentage} className="h-2" />
              <div className="text-xs text-slate-400 mt-1">{achievementPercentage.toFixed(1)}% desbloqueadas</div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <HardDrive className="h-4 w-4 text-slate-400" />
            <div className="flex-1">
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-300">Espaço usado</span>
                <span className="text-sm font-medium text-white">245.8 GB</span>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
