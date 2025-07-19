// API service para reviews
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface Review {
  id: number;
  user: number;
  user_detail: {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    avatar: string | null;
  };
  game: number;
  game_detail: {
    id: number;
    title: string;
    slug: string;
    cover_image: string | null;
  };
  rating: number;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
  playtime_at_review: number;
  is_recommended: boolean;
  is_spoiler: boolean;
  helpful_votes: number;
  not_helpful_votes: number;
  comments: ReviewComment[];
  votes: ReviewVote[];
}

export interface ReviewComment {
  id: number;
  user: number;
  user_detail: {
    id: number;
    username: string;
    avatar: string | null;
  };
  content: string;
  created_at: string;
  is_spoiler: boolean;
}

export interface ReviewVote {
  id: number;
  user: number;
  vote_type: 'helpful' | 'not_helpful';
  created_at: string;
}

export interface CreateReviewData {
  game: number;
  rating: number;
  title: string;
  content: string;
  is_recommended: boolean;
  is_spoiler: boolean;
}

export interface ReviewsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Review[];
}

export class ReviewsAPI {
  private static baseURL = `${API_BASE_URL}/social/reviews`;

  private static async makeRequest(url: string, options: RequestInit = {}) {
    const token = localStorage.getItem('authToken');
    
    const defaultHeaders: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (token) {
      defaultHeaders['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // Buscar reviews de um jogo específico
  static async getGameReviews(gameId: number, params: {
    page?: number;
    page_size?: number;
    ordering?: string;
  } = {}): Promise<ReviewsResponse> {
    const searchParams = new URLSearchParams();
    searchParams.append('game', gameId.toString());
    
    if (params.page) searchParams.append('page', params.page.toString());
    if (params.page_size) searchParams.append('page_size', params.page_size.toString());
    if (params.ordering) searchParams.append('ordering', params.ordering);

    const url = `${this.baseURL}/?${searchParams.toString()}`;
    return this.makeRequest(url);
  }

  // Criar uma nova review
  static async createReview(reviewData: CreateReviewData): Promise<Review> {
    const url = `${this.baseURL}/`;
    return this.makeRequest(url, {
      method: 'POST',
      body: JSON.stringify(reviewData),
    });
  }

  // Atualizar uma review existente
  static async updateReview(reviewId: number, reviewData: Partial<CreateReviewData>): Promise<Review> {
    const url = `${this.baseURL}/${reviewId}/`;
    return this.makeRequest(url, {
      method: 'PUT',
      body: JSON.stringify(reviewData),
    });
  }

  // Deletar uma review
  static async deleteReview(reviewId: number): Promise<void> {
    const url = `${this.baseURL}/${reviewId}/`;
    await this.makeRequest(url, {
      method: 'DELETE',
    });
  }

  // Votar em uma review (útil/não útil)
  static async voteOnReview(reviewId: number, voteType: 'helpful' | 'not_helpful'): Promise<void> {
    const endpoint = voteType === 'helpful' ? 'mark_helpful' : 'mark_not_helpful';
    const url = `${this.baseURL}/${reviewId}/${endpoint}/`;
    await this.makeRequest(url, {
      method: 'POST',
    });
  }

  // Buscar review do usuário para um jogo específico
  static async getUserReviewForGame(gameId: number, currentUserId?: string): Promise<Review | null> {
    try {
      const response = await this.getGameReviews(gameId);
      const token = localStorage.getItem('authToken');
      
      if (!token || !currentUserId) return null;

      // Filtrar pela review do usuário atual
      const userReview = response.results.find(review => 
        review.user_detail.id.toString() === currentUserId.toString()
      );
      
      return userReview || null;
    } catch (error) {
      console.error('Erro ao buscar review do usuário:', error);
      return null;
    }
  }
}
