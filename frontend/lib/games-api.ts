// API service para jogos
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface Game {
  id: number;
  title: string;
  slug: string;
  short_description: string;
  release_date: string;
  base_price: string;
  discount_percent: number;
  discount_price: number;
  is_on_sale: boolean;
  cover_image: string | null;
  developer_name: string;
  publisher_name: string;
  genres: string[];
  is_featured: boolean;
  is_active: boolean;
  average_rating: number;
  review_count: number;
  recommendation_percentage: number;
}

export interface GameSearchResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Game[];
}

export class GamesAPI {
  private static baseURL = `${process.env.NEXT_PUBLIC_API_URL}/games/games`;

  private static getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('authToken');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  static async searchGames(query: string, limit: number = 5): Promise<Game[]> {
    try {
      const params = new URLSearchParams({
        search: query,
        limit: limit.toString(),
        ordering: 'title'
      });

      // Para operações de leitura, tentar sem autenticação primeiro
      let response = await fetch(`${this.baseURL}/?${params}`);
      
      // Se der 401, tentar com autenticação
      if (response.status === 401) {
        response = await fetch(`${this.baseURL}/?${params}`, {
          headers: this.getAuthHeaders()
        });
      }
      
      if (!response.ok) {
        throw new Error(`Erro na busca: ${response.status}`);
      }

      const data: GameSearchResponse = await response.json();
      return data.results;
    } catch (error) {
      console.error('Erro ao buscar jogos:', error);
      return [];
    }
  }

  static async getFeaturedGames(limit: number = 10): Promise<Game[]> {
    try {
      const params = new URLSearchParams({
        limit: limit.toString()
      });

      let response = await fetch(`${this.baseURL}/featured/?${params}`);
      
      if (response.status === 401) {
        response = await fetch(`${this.baseURL}/featured/?${params}`, {
          headers: this.getAuthHeaders()
        });
      }
      
      if (!response.ok) {
        throw new Error(`Erro ao buscar jogos em destaque: ${response.status}`);
      }

      const data: GameSearchResponse = await response.json();
      return data.results;
    } catch (error) {
      console.error('Erro ao buscar jogos em destaque:', error);
      return [];
    }
  }

  static async getGameBySlug(slug: string): Promise<Game | null> {
    try {
      let response = await fetch(`${this.baseURL}/${slug}/`);
      
      if (response.status === 401) {
        response = await fetch(`${this.baseURL}/${slug}/`, {
          headers: this.getAuthHeaders()
        });
      }
      
      if (!response.ok) {
        if (response.status === 404) {
          return null;
        }
        throw new Error(`Erro ao buscar jogo: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Erro ao buscar jogo:', error);
      return null;
    }
  }
}
