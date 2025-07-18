import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Star, ThumbsUp, ThumbsDown, Users } from "lucide-react"

interface GameReviewsProps {
  rating: number
  ratingCount: number
}

export function GameReviews({ rating, ratingCount }: GameReviewsProps) {
  // Mock review data
  const reviewBreakdown = [
    { stars: 5, count: 8520, percentage: 55 },
    { stars: 4, count: 4630, percentage: 30 },
    { stars: 3, count: 1540, percentage: 10 },
    { stars: 2, count: 462, percentage: 3 },
    { stars: 1, count: 308, percentage: 2 },
  ]

  const recentReviews = [
    {
      id: 1,
      author: "GamerPro2024",
      rating: 5,
      date: "2 dias atrás",
      helpful: 45,
      content:
        "Incrível! Superou todas as expectativas. A história é envolvente, os gráficos são impressionantes e a jogabilidade é fluida. Vale cada centavo!",
      playtime: "25.5 horas",
    },
    {
      id: 2,
      author: "CasualPlayer",
      rating: 4,
      date: "1 semana atrás",
      helpful: 23,
      content:
        "Muito bom jogo, mas alguns bugs menores. A Valve entregou um produto sólido. Recomendo para fãs da série.",
      playtime: "12.3 horas",
    },
    {
      id: 3,
      author: "HardcoreGamer",
      rating: 5,
      date: "2 semanas atrás",
      helpful: 67,
      content:
        "Obra-prima! A espera valeu a pena. Cada detalhe foi cuidadosamente pensado. Este jogo define um novo padrão para a indústria.",
      playtime: "45.2 horas",
    },
  ]

  return (
    <div className="space-y-6">
      {/* Overall Rating */}
      <Card className="card-steam">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <Star className="h-5 w-5 text-yellow-400" />
            Avaliações dos Usuários
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Rating Summary */}
            <div className="text-center space-y-4">
              <div className="text-6xl font-bold text-yellow-400">{rating}</div>
              <div className="flex items-center justify-center gap-1">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star
                    key={i}
                    className={`h-6 w-6 ${i < Math.floor(rating) ? "text-yellow-400 fill-current" : "text-slate-600"}`}
                  />
                ))}
              </div>
              <p className="text-slate-400">Baseado em {ratingCount.toLocaleString()} avaliações</p>
            </div>

            {/* Rating Breakdown */}
            <div className="space-y-2">
              {reviewBreakdown.map((item) => (
                <div key={item.stars} className="flex items-center gap-3">
                  <div className="flex items-center gap-1 w-12">
                    <span className="text-sm text-slate-300">{item.stars}</span>
                    <Star className="h-3 w-3 text-yellow-400 fill-current" />
                  </div>
                  <Progress value={item.percentage} className="flex-1 h-2" />
                  <span className="text-sm text-slate-400 w-12 text-right">{item.percentage}%</span>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recent Reviews */}
      <Card className="card-steam">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <Users className="h-5 w-5 text-blue-400" />
            Avaliações Recentes
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {recentReviews.map((review) => (
            <div key={review.id} className="border-b border-slate-700 last:border-b-0 pb-4 last:pb-0">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-medium text-white">{review.author}</span>
                    <div className="flex items-center gap-1">
                      {Array.from({ length: 5 }).map((_, i) => (
                        <Star
                          key={i}
                          className={`h-3 w-3 ${i < review.rating ? "text-yellow-400 fill-current" : "text-slate-600"}`}
                        />
                      ))}
                    </div>
                  </div>
                  <div className="flex items-center gap-3 text-xs text-slate-400">
                    <span>{review.date}</span>
                    <span>Tempo jogado: {review.playtime}</span>
                  </div>
                </div>
              </div>

              <p className="text-slate-300 text-sm mb-3 leading-relaxed">{review.content}</p>

              <div className="flex items-center gap-4 text-xs text-slate-400">
                <button className="flex items-center gap-1 hover:text-green-400 transition-colors">
                  <ThumbsUp className="h-3 w-3" />
                  <span>Útil ({review.helpful})</span>
                </button>
                <button className="flex items-center gap-1 hover:text-red-400 transition-colors">
                  <ThumbsDown className="h-3 w-3" />
                  <span>Não útil</span>
                </button>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
