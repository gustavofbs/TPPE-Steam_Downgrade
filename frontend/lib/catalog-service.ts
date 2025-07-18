// Serviço para gerenciar o catálogo de jogos
import { gamesAPI } from './api';

export interface Game {
  id: string;
  title: string;
  price: number;
  originalPrice: number | null;
  discount: number;
  image: string;
  genre: string[];
  developer: string;
  publisher?: string;
  releaseDate?: string;
  description?: string;
  onSale: boolean;
  rating?: number;
  versions?: GameVersion[];
}

export interface GameVersion {
  id: string;
  version: string;
  releaseDate: string;
  size: number; // em MB
  description?: string;
}

export interface GameFilters {
  genres?: string[];
  developers?: string[];
  maxPrice?: number;
  minPrice?: number;
  onSale?: boolean;
  search?: string;
  sortBy?: string;
  page?: number;
  pageSize?: number;
}

export interface CatalogResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Game[];
}

export class CatalogService {
  private static instance: CatalogService;

  private constructor() {}

  // Padrão Singleton
  public static getInstance(): CatalogService {
    if (!CatalogService.instance) {
      CatalogService.instance = new CatalogService();
    }
    return CatalogService.instance;
  }

  // Obter jogos com filtros
  async getGames(filters: GameFilters = {}): Promise<CatalogResponse> {
    try {
      const params: Record<string, string> = {};
      
      if (filters.search) params.search = filters.search;
      if (filters.genres?.length) params.genres = filters.genres.join(',');
      if (filters.developers?.length) params.developers = filters.developers.join(',');
      if (filters.maxPrice) params.max_price = filters.maxPrice.toString();
      if (filters.minPrice) params.min_price = filters.minPrice.toString();
      if (filters.onSale) params.on_sale = 'true';
      if (filters.sortBy) params.sort_by = filters.sortBy;
      if (filters.page) params.page = filters.page.toString();
      if (filters.pageSize) params.page_size = filters.pageSize.toString();
      
      const apiResponse = await gamesAPI.getGames(params);
      const mappedResults = apiResponse.results.map((g: any) => ({
        id: g.id,
        title: g.title,
        price: Number(g.discount_price ?? g.base_price),
        originalPrice: g.discount_percent > 0 ? Number(g.base_price) : null,
        discount: Number(g.discount_percent) || 0,
        image: g.cover_image,
        genre: Array.isArray(g.genres) ? g.genres : [],
        developer: g.developer_name || "",
        publisher: g.publisher_name || "",
        releaseDate: g.release_date,
        description: g.short_description,
        onSale: !!g.is_on_sale,
      }));
      return {
        ...apiResponse,
        results: mappedResults,
      };
    } catch (error) {
      console.error('Erro ao obter jogos:', error);
      throw error;
    }
  }

  // Obter detalhes de um jogo
  async getGameDetails(gameId: string): Promise<Game> {
    try {
      return await gamesAPI.getGame(gameId);
    } catch (error) {
      console.error(`Erro ao obter detalhes do jogo ${gameId}:`, error);
      throw error;
    }
  }

  // Obter versões de um jogo
  async getGameVersions(gameId: string): Promise<GameVersion[]> {
    try {
      return await gamesAPI.getGameVersions(gameId);
    } catch (error) {
      console.error(`Erro ao obter versões do jogo ${gameId}:`, error);
      throw error;
    }
  }

  // Obter gêneros disponíveis
  async getGenres(): Promise<{ id: number, name: string }[]> {
    try {
      const genresData = await gamesAPI.getGenres();
      return genresData.results ? genresData.results.map((genre: any) => ({ id: genre.id, name: genre.name })) : [];
    } catch (error) {
      console.error('Erro ao obter gêneros:', error);
      return [];
    }
  }

  async getDevelopers(): Promise<{ id: number, name: string }[]> {
    try {
      const developersData = await gamesAPI.getDevelopers();
      return developersData.results ? developersData.results.map((dev: any) => ({ id: dev.id, name: dev.name })) : [];
    } catch (error) {
      console.error('Erro ao obter desenvolvedores:', error);
      return [];
    }
  }

  // Adicionar jogo à lista de desejos
  async addToWishlist(gameId: string): Promise<void> {
    try {
      await gamesAPI.addToWishlist(gameId);
    } catch (error) {
      console.error(`Erro ao adicionar jogo ${gameId} à lista de desejos:`, error);
      throw error;
    }
  }

  // Comprar jogo (adicionar à biblioteca)
  async purchaseGame(gameId: string): Promise<void> {
    try {
      await gamesAPI.purchaseGame(gameId);
    } catch (error) {
      console.error(`Erro ao comprar jogo ${gameId}:`, error);
      throw error;
    }
  }
}
