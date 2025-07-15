// API base configuration
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Helper function for API requests
export async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const token = localStorage.getItem('authToken');
  
  const defaultHeaders: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  if (token) {
    defaultHeaders['Authorization'] = `Token ${token}`;
  }
  
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  });

  // Handle unauthorized responses
  if (response.status === 401) {
    localStorage.removeItem('authToken');
    // Redirect to login if needed
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  }

  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.detail || 'Ocorreu um erro ao processar sua solicitação');
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
    localStorage.setItem('authToken', data.token);
    
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
    return fetchAPI(`/games/?${queryParams}`);
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

// User context and hooks will be implemented separately
