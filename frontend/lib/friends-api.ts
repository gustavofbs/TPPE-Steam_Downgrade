// API para gerenciamento de amizades e atividades sociais
import { fetchAPI } from './api';

export interface Friend {
  id: string;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  avatar?: string;
  bio?: string;
  last_login?: string;
  is_online?: boolean;
  profile?: {
    bio: string;
    avatar: string;
    is_online: boolean;
    last_seen: string;
    current_game?: {
      id: string;
      title: string;
    };
  };
}

export interface Friendship {
  id: string;
  sender: string;
  receiver: string;
  sender_detail: Friend;
  receiver_detail: Friend;
  status: 'pending' | 'accepted' | 'blocked';
  created_at: string;
  updated_at: string;
}

export interface FriendRequest {
  id: string;
  sender_detail: Friend;
  receiver_detail: Friend;
  status: string;
  created_at: string;
}

export interface UserActivity {
  id: string;
  user: string;
  user_detail: Friend;
  activity_type: 'game_purchase' | 'game_review' | 'achievement' | 'friendship';
  description: string;
  game?: {
    id: string;
    title: string;
    cover_image: string;
  };
  created_at: string;
  is_public: boolean;
}

export interface GameRecommendation {
  id: string;
  sender: string;
  receiver: string;
  sender_detail: Friend;
  receiver_detail: Friend;
  game: string;
  game_detail: {
    id: string;
    title: string;
    cover_image: string;
    price: number;
  };
  message: string;
  created_at: string;
  is_read: boolean;
}

export class FriendsAPI {
  private static baseURL = '/social/friendships';
  private static activitiesURL = '/social/activities';
  private static recommendationsURL = '/social/recommendations';

  // ===== GERENCIAMENTO DE AMIZADES =====

  /**
   * Buscar todas as amizades do usuário atual
   */
  static async getFriendships(): Promise<Friendship[]> {
    try {
      const response = await fetchAPI(this.baseURL + '/');
      return response.results || response;
    } catch (error) {
      console.error('Erro ao buscar amizades:', error);
      throw error;
    }
  }

  /**
   * Buscar apenas amigos aceitos
   */
  static async getFriends(): Promise<Friend[]> {
    try {
      const friendships = await this.getFriendships();
      const acceptedFriendships = friendships.filter(f => f.status === 'accepted');
      
      // Extrair os amigos (excluindo o usuário atual)
      const friends: Friend[] = [];
      acceptedFriendships.forEach(friendship => {
        // Adicionar tanto sender quanto receiver, o frontend filtrará o usuário atual
        friends.push(friendship.sender_detail);
        friends.push(friendship.receiver_detail);
      });
      
      return friends;
    } catch (error) {
      console.error('Erro ao buscar amigos:', error);
      throw error;
    }
  }

  /**
   * Buscar amigos online
   */
  static async getOnlineFriends(): Promise<Friend[]> {
    try {
      const friends = await this.getFriends();
      return friends.filter(friend => friend.is_online || friend.profile?.is_online);
    } catch (error) {
      console.error('Erro ao buscar amigos online:', error);
      throw error;
    }
  }

  /**
   * Buscar solicitações de amizade pendentes
   */
  static async getPendingRequests(): Promise<FriendRequest[]> {
    try {
      const response = await fetchAPI(this.baseURL + '/pending_requests/');
      return response.results || response;
    } catch (error) {
      console.error('Erro ao buscar solicitações pendentes:', error);
      throw error;
    }
  }

  /**
   * Aceitar solicitação de amizade
   */
  static async acceptFriendRequest(friendshipId: string): Promise<Friendship> {
    try {
      const response = await fetchAPI(`${this.baseURL}/${friendshipId}/accept/`, {
        method: 'POST'
      });
      return response;
    } catch (error) {
      console.error('Erro ao aceitar solicitação de amizade:', error);
      throw error;
    }
  }

  /**
   * Enviar solicitação de amizade
   */
  static async sendFriendRequest(receiverId: string): Promise<Friendship> {
    try {
      const response = await fetchAPI(this.baseURL + '/', {
        method: 'POST',
        body: JSON.stringify({
          receiver: receiverId
        })
      });
      return response;
    } catch (error) {
      console.error('Erro ao enviar solicitação de amizade:', error);
      throw error;
    }
  }

  /**
   * Rejeitar solicitação de amizade
   */
  static async rejectFriendRequest(friendshipId: string): Promise<void> {
    try {
      await fetchAPI(`${this.baseURL}/${friendshipId}/reject/`, {
        method: 'POST'
      });
    } catch (error) {
      console.error('Erro ao rejeitar solicitação de amizade:', error);
      throw error;
    }
  }

  /**
   * Bloquear usuário
   */
  static async blockUser(friendshipId: string): Promise<Friendship> {
    try {
      const response = await fetchAPI(`${this.baseURL}/${friendshipId}/block/`, {
        method: 'POST'
      });
      return response;
    } catch (error) {
      console.error('Erro ao bloquear usuário:', error);
      throw error;
    }
  }

  /**
   * Remover amizade
   */
  static async removeFriend(friendshipId: string): Promise<void> {
    try {
      await fetchAPI(`${this.baseURL}/${friendshipId}/`, {
        method: 'DELETE'
      });
    } catch (error) {
      console.error('Erro ao remover amizade:', error);
      throw error;
    }
  }

  // ===== ATIVIDADES SOCIAIS =====

  /**
   * Buscar atividades dos amigos
   */
  static async getFriendsActivities(): Promise<UserActivity[]> {
    try {
      const response = await fetchAPI(this.activitiesURL + '/friends_activities/');
      return response.results || response;
    } catch (error) {
      console.error('Erro ao buscar atividades dos amigos:', error);
      throw error;
    }
  }

  /**
   * Buscar atividades de um amigo específico
   */
  static async getFriendActivities(friendId: string): Promise<UserActivity[]> {
    try {
      const response = await fetchAPI(`${this.activitiesURL}/?user=${friendId}`);
      return response.results || response;
    } catch (error) {
      console.error('Erro ao buscar atividades do amigo:', error);
      throw error;
    }
  }

  // ===== RECOMENDAÇÕES =====

  /**
   * Buscar recomendações recebidas
   */
  static async getReceivedRecommendations(): Promise<GameRecommendation[]> {
    try {
      const response = await fetchAPI(this.recommendationsURL + '/received/');
      return response.results || response;
    } catch (error) {
      console.error('Erro ao buscar recomendações recebidas:', error);
      throw error;
    }
  }

  /**
   * Enviar recomendação de jogo
   */
  static async sendRecommendation(
    receiverId: string, 
    gameId: string, 
    message: string
  ): Promise<GameRecommendation> {
    try {
      const response = await fetchAPI(this.recommendationsURL + '/', {
        method: 'POST',
        body: JSON.stringify({
          receiver: receiverId,
          game: gameId,
          message: message
        })
      });
      return response;
    } catch (error) {
      console.error('Erro ao enviar recomendação:', error);
      throw error;
    }
  }

  /**
   * Marcar recomendação como lida
   */
  static async markRecommendationAsRead(recommendationId: string): Promise<GameRecommendation> {
    try {
      const response = await fetchAPI(`${this.recommendationsURL}/${recommendationId}/mark_read/`, {
        method: 'POST'
      });
      return response;
    } catch (error) {
      console.error('Erro ao marcar recomendação como lida:', error);
      throw error;
    }
  }

  // ===== BUSCA DE USUÁRIOS =====

  /**
   * Buscar usuários por nome de usuário
   */
  static async searchUsers(query: string): Promise<Friend[]> {
    try {
      const response = await fetchAPI(`/users/search/?q=${encodeURIComponent(query)}`);
      const users = response.results || response;
      
      // Mapear dados do UserSerializer para interface Friend
      return users.map((user: any) => ({
        id: user.id,
        username: user.username,
        email: user.email,
        first_name: user.first_name,
        last_name: user.last_name,
        avatar: user.profile?.avatar || null,
        bio: user.profile?.bio || null,
        last_login: user.last_login || null,
        is_online: false // Não temos essa informação na busca
      }));
    } catch (error) {
      console.error('Erro ao buscar usuários:', error);
      throw error;
    }
  }

  // ===== UTILITÁRIOS =====

  /**
   * Verificar se um usuário é amigo
   */
  static async isFriend(userId: string): Promise<boolean> {
    try {
      const friends = await this.getFriends();
      return friends.some(friend => friend.id === userId);
    } catch (error) {
      console.error('Erro ao verificar amizade:', error);
      return false;
    }
  }

  /**
   * Obter status da amizade com um usuário
   */
  static async getFriendshipStatus(userId: string): Promise<string | null> {
    try {
      const friendships = await this.getFriendships();
      const friendship = friendships.find(f => 
        f.sender_detail.id === userId || f.receiver_detail.id === userId
      );
      return friendship ? friendship.status : null;
    } catch (error) {
      console.error('Erro ao verificar status da amizade:', error);
      return null;
    }
  }
}

export default FriendsAPI;
