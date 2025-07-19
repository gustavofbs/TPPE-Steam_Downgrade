import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Star, ThumbsUp, ThumbsDown, Users, Plus, Edit, Trash2 } from "lucide-react"
import { useState, useEffect } from "react"
import { ReviewsAPI, Review, CreateReviewData } from "@/lib/reviews-api"
import { useAuth } from "@/lib/auth-context"

interface GameReviewsProps {
  gameId: number
  gameName: string
}

export function GameReviews({ gameId, gameName }: GameReviewsProps) {
  const { user } = useAuth();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [userReview, setUserReview] = useState<Review | null>(null);
  const [editingReview, setEditingReview] = useState<Review | null>(null);
  
  // Form state
  const [formData, setFormData] = useState<CreateReviewData>({
    game: gameId,
    rating: 5,
    title: '',
    content: '',
    is_recommended: true,
    is_spoiler: false,
  });

  useEffect(() => {
    loadReviews();
  }, [gameId]);

  const loadReviews = async () => {
    try {
      setIsLoading(true);
      const response = await ReviewsAPI.getGameReviews(gameId, {
        page_size: 10,
        ordering: '-created_at'
      });
      setReviews(response.results);
      
      // Verificar se o usuário já tem uma review
      if (user) {
        const userReviewData = await ReviewsAPI.getUserReviewForGame(gameId, user.id);
        setUserReview(userReviewData);
      }
    } catch (err) {
      setError('Erro ao carregar avaliações');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;

    try {
      if (editingReview) {
        const updatedReview = await ReviewsAPI.updateReview(editingReview.id, formData);
        setUserReview(updatedReview);
        setEditingReview(null);
      } else {
        const newReview = await ReviewsAPI.createReview(formData);
        setUserReview(newReview);
        setShowCreateForm(false);
      }
      
      // Recarregar reviews
      await loadReviews();
      
      // Reset form
      setFormData({
        game: gameId,
        rating: 5,
        title: '',
        content: '',
        is_recommended: true,
        is_spoiler: false,
      });
    } catch (err) {
      console.error('Erro ao salvar avaliação:', err);
    }
  };

  const handleDeleteReview = async (reviewId: number) => {
    if (!confirm('Tem certeza que deseja excluir sua avaliação?')) return;
    
    try {
      await ReviewsAPI.deleteReview(reviewId);
      setUserReview(null);
      await loadReviews();
    } catch (err) {
      console.error('Erro ao excluir avaliação:', err);
    }
  };

  const handleVote = async (reviewId: number, voteType: 'helpful' | 'not_helpful') => {
    if (!user) return;
    
    try {
      await ReviewsAPI.voteOnReview(reviewId, voteType);
      await loadReviews(); // Recarregar para atualizar contadores
    } catch (err) {
      console.error('Erro ao votar:', err);
    }
  };

  const startEdit = (review: Review) => {
    setEditingReview(review);
    setFormData({
      game: gameId,
      rating: review.rating,
      title: review.title,
      content: review.content,
      is_recommended: review.is_recommended,
      is_spoiler: review.is_spoiler,
    });
    setShowCreateForm(true);
  };

  // Calcular estatísticas
  const totalReviews = reviews.length;
  const averageRating = totalReviews > 0 
    ? reviews.reduce((sum, review) => sum + review.rating, 0) / totalReviews 
    : 0;
  const recommendationPercentage = totalReviews > 0
    ? (reviews.filter(r => r.is_recommended).length / totalReviews) * 100
    : 0;

  // Calcular distribuição de estrelas
  const ratingDistribution = [5, 4, 3, 2, 1].map(stars => {
    const count = reviews.filter(r => r.rating === stars).length;
    const percentage = totalReviews > 0 ? (count / totalReviews) * 100 : 0;
    return { stars, count, percentage };
  });
  if (isLoading) {
    return (
      <Card className="bg-slate-800/50 border-slate-700">
        <CardContent className="p-6">
          <div className="text-center text-slate-400">Carregando avaliações...</div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="bg-slate-800/50 border-slate-700">
        <CardContent className="p-6">
          <div className="text-center text-red-400">{error}</div>
        </CardContent>
      </Card>
    );
  }

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
              <div className="text-6xl font-bold text-yellow-400">{averageRating.toFixed(1)}</div>
              <div className="flex items-center justify-center gap-1">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star
                    key={i}
                    className={`h-6 w-6 ${i < Math.floor(averageRating) ? "text-yellow-400 fill-current" : "text-slate-600"}`}
                  />
                ))}
              </div>
              <p className="text-slate-400">Baseado em {totalReviews.toLocaleString()} avaliações</p>
              <p className="text-sm text-green-400">{recommendationPercentage.toFixed(0)}% recomendam este jogo</p>
            </div>

            {/* Rating Breakdown */}
            <div className="space-y-2">
              {ratingDistribution.map((item) => (
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
          {/* Botão para criar review */}
          {user && !userReview && (
            <Button 
              onClick={() => setShowCreateForm(true)}
              className="w-full bg-blue-600 hover:bg-blue-700 mb-4"
            >
              <Plus className="h-4 w-4 mr-2" />
              Escrever Avaliação
            </Button>
          )}
          
          {/* Review do usuário */}
          {userReview && (
            <div className="border border-blue-600/50 rounded-lg p-4 mb-4">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-medium text-blue-400">Sua Avaliação</span>
                    <div className="flex items-center gap-1">
                      {Array.from({ length: 5 }).map((_, i) => (
                        <Star
                          key={i}
                          className={`h-3 w-3 ${i < userReview.rating ? "text-yellow-400 fill-current" : "text-slate-600"}`}
                        />
                      ))}
                    </div>
                  </div>
                  <div className="flex items-center gap-3 text-xs text-slate-400">
                    <span>{new Date(userReview.created_at).toLocaleDateString('pt-BR')}</span>
                    <span>Tempo jogado: {Math.floor(userReview.playtime_at_review / 60)}h {userReview.playtime_at_review % 60}m</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button 
                    size="sm" 
                    variant="outline" 
                    onClick={() => startEdit(userReview)}
                    className="border-slate-600 text-slate-300 hover:bg-slate-700"
                  >
                    <Edit className="h-3 w-3" />
                  </Button>
                  <Button 
                    size="sm" 
                    variant="outline" 
                    onClick={() => handleDeleteReview(userReview.id)}
                    className="border-red-600 text-red-400 hover:bg-red-900/20"
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </div>
              </div>
              <h4 className="font-medium text-white mb-2">{userReview.title}</h4>
              <p className="text-slate-300 text-sm mb-3">{userReview.content}</p>
              <div className="flex items-center gap-4 text-xs text-slate-400">
                <span className={`px-2 py-1 rounded ${userReview.is_recommended ? 'bg-green-900/30 text-green-400' : 'bg-red-900/30 text-red-400'}`}>
                  {userReview.is_recommended ? 'Recomendado' : 'Não Recomendado'}
                </span>
                {userReview.is_spoiler && (
                  <span className="px-2 py-1 rounded bg-orange-900/30 text-orange-400">Contém Spoilers</span>
                )}
              </div>
            </div>
          )}
          
          {reviews.map((review) => (
            <div key={review.id} className="border-b border-slate-700 last:border-b-0 pb-4 last:pb-0">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-medium text-white">{review.user_detail.username}</span>
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
                    <span>{new Date(review.created_at).toLocaleDateString('pt-BR')}</span>
                    <span>Tempo jogado: {Math.floor(review.playtime_at_review / 60)}h {review.playtime_at_review % 60}m</span>
                  </div>
                </div>
              </div>

              <h4 className="font-medium text-white mb-2">{review.title}</h4>
              <p className="text-slate-300 text-sm mb-3 leading-relaxed">{review.content}</p>
              
              <div className="flex items-center gap-4 text-xs text-slate-400 mb-3">
                <span className={`px-2 py-1 rounded ${review.is_recommended ? 'bg-green-900/30 text-green-400' : 'bg-red-900/30 text-red-400'}`}>
                  {review.is_recommended ? 'Recomendado' : 'Não Recomendado'}
                </span>
                {review.is_spoiler && (
                  <span className="px-2 py-1 rounded bg-orange-900/30 text-orange-400">Contém Spoilers</span>
                )}
              </div>

              <div className="flex items-center gap-4 text-xs text-slate-400">
                <button 
                  className="flex items-center gap-1 hover:text-green-400 transition-colors"
                  onClick={() => handleVote(review.id, 'helpful')}
                  disabled={!user}
                >
                  <ThumbsUp className="h-3 w-3" />
                  <span>Útil ({review.helpful_votes})</span>
                </button>
                <button 
                  className="flex items-center gap-1 hover:text-red-400 transition-colors"
                  onClick={() => handleVote(review.id, 'not_helpful')}
                  disabled={!user}
                >
                  <ThumbsDown className="h-3 w-3" />
                  <span>Não útil ({review.not_helpful_votes})</span>
                </button>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
      
      {/* Formulário para criar/editar review */}
      {showCreateForm && (
        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white">
              {editingReview ? 'Editar Avaliação' : 'Escrever Avaliação'}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmitReview} className="space-y-4">
              <div>
                <Label htmlFor="rating" className="text-white">Nota (1-5 estrelas)</Label>
                <div className="flex items-center gap-2 mt-2">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      type="button"
                      onClick={() => setFormData(prev => ({ ...prev, rating: star }))}
                      className="p-1"
                    >
                      <Star
                        className={`h-6 w-6 ${
                          star <= formData.rating
                            ? "text-yellow-400 fill-current"
                            : "text-gray-600 hover:text-yellow-300"
                        }`}
                      />
                    </button>
                  ))}
                  <span className="ml-2 text-white">{formData.rating} estrela{formData.rating !== 1 ? 's' : ''}</span>
                </div>
              </div>
              
              <div>
                <Label htmlFor="title" className="text-white">Título da Avaliação</Label>
                <Input
                  id="title"
                  value={formData.title}
                  onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                  placeholder="Resuma sua experiência..."
                  className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-400"
                  required
                />
              </div>
              
              <div>
                <Label htmlFor="content" className="text-white">Sua Avaliação</Label>
                <Textarea
                  id="content"
                  value={formData.content}
                  onChange={(e) => setFormData(prev => ({ ...prev, content: e.target.value }))}
                  placeholder="Compartilhe sua experiência com outros jogadores..."
                  className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-400 min-h-[120px]"
                  required
                />
              </div>
              
              <div className="flex items-center gap-4">
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="recommended"
                    checked={formData.is_recommended}
                    onCheckedChange={(checked) => setFormData(prev => ({ ...prev, is_recommended: !!checked }))}
                  />
                  <Label htmlFor="recommended" className="text-white">Recomendo este jogo</Label>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="spoiler"
                    checked={formData.is_spoiler}
                    onCheckedChange={(checked) => setFormData(prev => ({ ...prev, is_spoiler: !!checked }))}
                  />
                  <Label htmlFor="spoiler" className="text-white">Contém spoilers</Label>
                </div>
              </div>
              
              <div className="flex gap-3">
                <Button type="submit" className="bg-blue-600 hover:bg-blue-700">
                  {editingReview ? 'Atualizar' : 'Publicar'} Avaliação
                </Button>
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={() => {
                    setShowCreateForm(false);
                    setEditingReview(null);
                    setFormData({
                      game: gameId,
                      rating: 5,
                      title: '',
                      content: '',
                      is_recommended: true,
                      is_spoiler: false,
                    });
                  }}
                  className="border-slate-600 text-slate-300 hover:bg-slate-700"
                >
                  Cancelar
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
