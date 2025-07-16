// API base configuration
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Helper function for API requests
export async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const token = localStorage.getItem('authToken');

  const defaultHeaders: HeadersInit = {
    'Content-Type': 'application/json',
  };

  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`;
  }

  const finalHeaders = {
    ...defaultHeaders,
    ...options.headers,
  };

  console.log('[fetchAPI] Fazendo requisição para:', `${API_URL}${endpoint}`);
  console.log('[fetchAPI] Headers:', finalHeaders);
  console.log('[fetchAPI] Options:', options);

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: finalHeaders,
  });

  const data = await response.json();

  if (response.status === 401) {
    console.warn('[fetchAPI] 401 Unauthorized');
    localStorage.removeItem('authToken');
    if (typeof window !== 'undefined') {
      // window.location.href = '/login';
    }
  }

  if (!response.ok) {
    console.error('[fetchAPI] Erro:', data);
    throw new Error(data.detail || 'Erro ao processar solicitação');
  }

  return data;
}

// Authentication API
export const authAPI = {
  // Login user
  login: async (username: string, password: string) => {
    const response = await fetch(`${API_URL}/auth/token/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.detail || 'Credenciais inválidas');
    }
    
    // Store token in localStorage
    localStorage.setItem('authToken', data.access);
    
    return data;
  },
  
  // Register user
  register: async (userData: {
    username: string;
    email: string;
    password: string;
    password2: string;
    first_name?: string;
    last_name?: string;
  }) => {
    return fetchAPI('/users/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },
  
  // Get current user data
  getCurrentUser: async () => {
    return fetchAPI('/users/me/');
  },
  
  // Update user profile
  updateProfile: async (userId: string, profileData: any) => {
    return fetchAPI(`/users/${userId}/update_profile/`, {
      method: 'PUT',
      body: JSON.stringify(profileData),
    });
  },
  
  // Change password
  changePassword: async (userId: string, passwordData: {
    old_password: string;
    new_password: string;
    new_password2: string;
  }) => {
    return fetchAPI(`/users/${userId}/change_password/`, {
      method: 'POST',
      body: JSON.stringify(passwordData),
    });
  },
  
  // Logout user
  logout: () => {
    localStorage.removeItem('authToken');
  }
};

// Games API
export const gamesAPI = {
  // Get all games with optional filters
  getGames: async (params: Record<string, string> = {}) => {
    const queryParams = new URLSearchParams(params).toString();
    return fetchAPI(`/games/${queryParams ? `?${queryParams}` : ''}`);
  },
  
  // Get a single game by ID
  getGame: async (gameId: string) => {
    return fetchAPI(`/games/${gameId}/`);
  },
  
  // Get game versions (for downgrade functionality)
  getGameVersions: async (gameId: string) => {
    return fetchAPI(`/games/${gameId}/versions/`);
  }
};

// Library API
export const libraryAPI = {
  // Get user's library
  getLibrary: async () => {
    return fetchAPI('/purchases/library/my_library/');
  },
  
  // Get a specific library item
  getLibraryItem: async (itemId: string) => {
    return fetchAPI(`/library/${itemId}/`);
  },
  
  // Record playtime for a game
  recordPlaytime: async (itemId: string, minutes: number) => {
    return fetchAPI(`/library/${itemId}/record_playtime/`, {
      method: 'POST',
      body: JSON.stringify({ minutes }),
    });
  },
  
  // Toggle favorite status for a game
  toggleFavorite: async (itemId: string, isFavorite: boolean) => {
    return fetchAPI(`/library/${itemId}/`, {
      method: 'PATCH',
      body: JSON.stringify({ is_favorite: isFavorite }),
    });
  },
};

// Downloads API
export const downloadsAPI = {
  // Get download history
  getDownloadHistory: async (params: Record<string, string> = {}) => {
    const queryParams = new URLSearchParams(params).toString();
    return fetchAPI(`/downloads/${queryParams ? `?${queryParams}` : ''}`);
  },
  
  // Record a new download
  recordDownload: async (libraryItemId: string, gameVersionId: string) => {
    return fetchAPI('/downloads/', {
      method: 'POST',
      body: JSON.stringify({
        library_item: libraryItemId,
        game_version: gameVersionId,
      }),
    });
  },
};

// Wishlist API
export const wishlistAPI = {
  // Get user's wishlist
  getWishlist: async () => {
    return fetchAPI('/purchases/wishlist/my_wishlist/');
  },
  
  // Add game to wishlist
  addToWishlist: async (gameId: string, priority: number = 0) => {
    return fetchAPI('/purchases/wishlist/add_item/', {
      method: 'POST',
      body: JSON.stringify({
        game: gameId,
        priority,
      }),
    });
  },
  
  // Remove game from wishlist
  removeFromWishlist: async (gameId: string) => {
    return fetchAPI('/purchases/wishlist/remove_item/', {
      method: 'POST',
      body: JSON.stringify({
        game: gameId,
      }),
    });
  },
};

// User context and hooks will be implemented separately
