// API service para carrinho de compras
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface CartItem {
  id: number;
  game_id: number;
  game: {
    id: number;
    slug: string;
    title: string;
    cover_image: string | null;
    base_price: string;
    current_price: string;
    discount_percent: number;
    developer_name: string;
    publisher_name: string;
  };
  quantity: number;
  unit_price: string;
  subtotal: string;
  added_at: string;
}

export interface Cart {
  id: number;
  user: number;
  items: CartItem[];
  total_items: number;
  total_price: string;
  created_at: string;
  updated_at: string;
}

export interface Coupon {
  code: string;
  discount_percent: number;
  is_valid: boolean;
  message: string;
}

export class CartAPI {
  private static baseURL = `${API_BASE_URL}/purchases/cart`;

  private static async makeRequest(url: string, options: RequestInit = {}) {
    const token = localStorage.getItem('authToken');
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    };

    console.log('[CartAPI] Fazendo requisição para:', url);
    console.log('[CartAPI] Headers:', headers);
    console.log('[CartAPI] Body:', options.body);
    
    const response = await fetch(url, { ...options, headers });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('[CartAPI] Erro na resposta:', response.status, errorData);
      throw new Error(errorData.detail || errorData.error || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Buscar carrinho do usuário
  static async getCart(): Promise<Cart> {
    const url = `${this.baseURL}/my_cart/`;
    return this.makeRequest(url);
  }

  // Adicionar item ao carrinho
  static async addItem(gameId: number, quantity: number = 1): Promise<Cart> {
    const url = `${this.baseURL}/add_item/`;
    return this.makeRequest(url, {
      method: 'POST',
      body: JSON.stringify({
        game: gameId,
        quantity: quantity,
      }),
    });
  }

  // Remover item do carrinho
  static async removeItem(gameId: number): Promise<Cart> {
    const url = `${this.baseURL}/remove_item/`;
    return this.makeRequest(url, {
      method: 'POST',
      body: JSON.stringify({
        game: gameId,
      }),
    });
  }

  // Limpar carrinho
  static async clearCart(): Promise<Cart> {
    const url = `${this.baseURL}/clear/`;
    return this.makeRequest(url, {
      method: 'POST',
    });
  }

  // Validar cupom
  static async validateCoupon(code: string): Promise<Coupon> {
    const url = `${API_BASE_URL}/purchases/coupons/validate/`;
    return this.makeRequest(url, {
      method: 'POST',
      body: JSON.stringify({ code }),
    });
  }

  // Calcular desconto do cupom
  static calculateCouponDiscount(subtotal: number, discountPercent: number): number {
    return (subtotal * discountPercent) / 100;
  }

  // Formatar preço
  static formatPrice(price: string | number): string {
    const numPrice = typeof price === 'string' ? parseFloat(price) : price;
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(numPrice);
  }

  // Converter preço string para number
  static parsePrice(price: string): number {
    return parseFloat(price);
  }
}
