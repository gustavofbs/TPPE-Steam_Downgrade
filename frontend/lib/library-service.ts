// Serviço para gerenciar a biblioteca de jogos do usuário
import { libraryAPI, downloadsAPI, wishlistAPI } from './api';

export interface Game {
  id: string;
  title: string;
  description: string;
  cover_image: string;
  release_date: string;
  developer: string;
  publisher: string;
  genres: string[];
  price: number;
  discount_percent: number;
  current_price: number;
  rating: number;
}

export interface GameVersion {
  id: string;
  version: string;
  release_date: string;
  description: string;
  download_url: string;
  size_mb: number;
}

export interface LibraryItem {
  id: string;
  game: string;
  game_detail: Game;
  acquired_at: string;
  playtime: number;
  formatted_playtime: string;
  last_played: string | null;
  is_favorite: boolean;
  downloads: DownloadHistory[];
}

export interface DownloadHistory {
  id: string;
  game_version: string;
  game_version_detail: {
    version: string;
    release_date: string;
    size_mb: number;
  };
  downloaded_at: string;
}

export interface Library {
  id: string;
  user: string;
  items: LibraryItem[];
  total_games: number;
  created_at: string;
}

export interface WishlistItem {
  id: string;
  game: string;
  game_detail: Game;
  added_at: string;
  priority: number;
}

export interface Wishlist {
  id: string;
  user: string;
  items: WishlistItem[];
  total_items: number;
  created_at: string;
}

export interface UserStats {
  totalGames: number;
  totalPlaytime: number;
  formattedPlaytime: string;
  recentlyPlayed: LibraryItem[];
  mostPlayed: LibraryItem[];
  totalAchievements: number;
  maxAchievements: number;
  achievementPercentage: number;
}

// Classe de serviço para biblioteca
export class LibraryService {
  private static instance: LibraryService;

  private constructor() {}

  // Padrão Singleton para garantir uma única instância
  public static getInstance(): LibraryService {
    if (!LibraryService.instance) {
      LibraryService.instance = new LibraryService();
    }
    return LibraryService.instance;
  }

  // Obter a biblioteca do usuário
  async getLibrary(): Promise<Library> {
    try {
      const response = await libraryAPI.getLibrary();
      return response;
    } catch (error) {
      console.error('Erro ao obter biblioteca:', error);
      throw error;
    }
  }

  // Obter detalhes de um item específico da biblioteca
  async getLibraryItem(itemId: string): Promise<LibraryItem> {
    try {
      const response = await libraryAPI.getLibraryItem(itemId);
      return response;
    } catch (error) {
      console.error(`Erro ao obter item da biblioteca ${itemId}:`, error);
      throw error;
    }
  }

  // Registrar tempo de jogo
  async recordPlaytime(itemId: string, minutes: number): Promise<LibraryItem> {
    try {
      const response = await libraryAPI.recordPlaytime(itemId, minutes);
      return response;
    } catch (error) {
      console.error('Erro ao registrar tempo de jogo:', error);
      throw error;
    }
  }

  // Marcar/desmarcar jogo como favorito
  async toggleFavorite(itemId: string, isFavorite: boolean): Promise<LibraryItem> {
    try {
      const response = await libraryAPI.toggleFavorite(itemId, isFavorite);
      return response;
    } catch (error) {
      console.error('Erro ao atualizar favorito:', error);
      throw error;
    }
  }

  // Obter histórico de downloads
  async getDownloadHistory(itemId?: string): Promise<DownloadHistory[]> {
    try {
      const params: Record<string, string> = {};
      if (itemId) {
        params['library_item'] = itemId;
      }
      
      const response = await downloadsAPI.getDownloadHistory(params);
      return response.results || response;
    } catch (error) {
      console.error('Erro ao obter histórico de downloads:', error);
      throw error;
    }
  }

  // Registrar um novo download
  async recordDownload(libraryItemId: string, gameVersionId: string): Promise<DownloadHistory> {
    try {
      const response = await downloadsAPI.recordDownload(libraryItemId, gameVersionId);
      return response;
    } catch (error) {
      console.error('Erro ao registrar download:', error);
      throw error;
    }
  }

  // Obter lista de desejos do usuário
  async getWishlist(): Promise<Wishlist> {
    try {
      const response = await wishlistAPI.getWishlist();
      return response;
    } catch (error) {
      console.error('Erro ao obter lista de desejos:', error);
      throw error;
    }
  }

  // Adicionar jogo à lista de desejos
  async addToWishlist(gameId: string, priority: number = 0): Promise<WishlistItem> {
    try {
      const response = await wishlistAPI.addToWishlist(gameId, priority);
      return response;
    } catch (error) {
      console.error('Erro ao adicionar à lista de desejos:', error);
      throw error;
    }
  }

  // Remover jogo da lista de desejos
  async removeFromWishlist(gameId: string): Promise<void> {
    try {
      await wishlistAPI.removeFromWishlist(gameId);
    } catch (error) {
      console.error('Erro ao remover da lista de desejos:', error);
      throw error;
    }
  }

  // Calcular estatísticas do usuário com base na biblioteca
  async getUserStats(): Promise<UserStats> {
    try {
      const library = await this.getLibrary();
      
      // Ordenar por tempo de jogo
      const sortedByPlaytime = [...library.items].sort((a, b) => b.playtime - a.playtime);
      
      // Ordenar por último jogado
      const recentlyPlayed = [...library.items]
        .filter(item => item.last_played)
        .sort((a, b) => {
          if (!a.last_played || !b.last_played) return 0;
          return new Date(b.last_played).getTime() - new Date(a.last_played).getTime();
        })
        .slice(0, 5);
      
      // Jogos mais jogados
      const mostPlayed = sortedByPlaytime.slice(0, 5);
      
      // Tempo total de jogo
      const totalPlaytime = library.items.reduce((sum, item) => sum + item.playtime, 0);
      
      // Formatar tempo de jogo
      const formattedPlaytime = this.formatPlaytime(totalPlaytime);
      
      // Simulação de conquistas (já que não temos essa informação no backend)
      // Em uma implementação real, isso viria de uma API específica
      const totalAchievements = Math.floor(Math.random() * 500);
      const maxAchievements = 1000;
      const achievementPercentage = (totalAchievements / maxAchievements) * 100;
      
      return {
        totalGames: library.total_games,
        totalPlaytime,
        formattedPlaytime,
        recentlyPlayed,
        mostPlayed,
        totalAchievements,
        maxAchievements,
        achievementPercentage
      };
    } catch (error) {
      console.error('Erro ao calcular estatísticas do usuário:', error);
      throw error;
    }
  }

  // Formatar tempo de jogo em minutos para um formato legível
  private formatPlaytime(minutes: number): string {
    if (minutes < 60) {
      return `${minutes} minutos`;
    }
    
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    
    if (hours < 24) {
      return `${hours} hora${hours !== 1 ? 's' : ''} ${remainingMinutes > 0 ? `e ${remainingMinutes} minuto${remainingMinutes !== 1 ? 's' : ''}` : ''}`;
    }
    
    const days = Math.floor(hours / 24);
    const remainingHours = hours % 24;
    
    return `${days} dia${days !== 1 ? 's' : ''} ${remainingHours > 0 ? `e ${remainingHours} hora${remainingHours !== 1 ? 's' : ''}` : ''}`;
  }
}
