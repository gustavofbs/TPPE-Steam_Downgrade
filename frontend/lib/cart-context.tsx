"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { CartAPI, Cart, CartItem, Coupon } from './cart-api';
import { useAuth } from './auth-context';

type CartContextType = {
  cart: Cart | null;
  isLoading: boolean;
  appliedCoupon: Coupon | null;
  addToCart: (gameId: number, quantity?: number) => Promise<void>;
  removeFromCart: (gameId: number) => Promise<void>;
  updateQuantity: (gameId: number, quantity: number) => Promise<void>;
  clearCart: () => Promise<void>;
  applyCoupon: (code: string) => Promise<void>;
  removeCoupon: () => void;
  refreshCart: () => Promise<void>;
  getTotalItems: () => number;
  getSubtotal: () => number;
  getDiscountAmount: () => number;
  getFinalTotal: () => number;
};

const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: ReactNode }) {
  const [cart, setCart] = useState<Cart | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [appliedCoupon, setAppliedCoupon] = useState<Coupon | null>(null);
  const { isAuthenticated } = useAuth();

  // Carregar carrinho quando usuário estiver autenticado
  useEffect(() => {
    if (isAuthenticated) {
      refreshCart();
    } else {
      setCart(null);
      setAppliedCoupon(null);
    }
  }, [isAuthenticated]);

  const refreshCart = async () => {
    if (!isAuthenticated) return;
    
    setIsLoading(true);
    try {
      const cartData = await CartAPI.getCart();
      setCart(cartData);
    } catch (error) {
      console.error('Erro ao carregar carrinho:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const addToCart = async (gameId: number, quantity: number = 1) => {
    if (!isAuthenticated) {
      throw new Error('Usuário não autenticado');
    }

    setIsLoading(true);
    try {
      const updatedCart = await CartAPI.addItem(gameId, quantity);
      setCart(updatedCart);
    } catch (error) {
      console.error('Erro ao adicionar item ao carrinho:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const removeFromCart = async (gameId: number) => {
    if (!isAuthenticated) return;

    setIsLoading(true);
    try {
      const updatedCart = await CartAPI.removeItem(gameId);
      setCart(updatedCart);
    } catch (error) {
      console.error('Erro ao remover item do carrinho:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const updateQuantity = async (gameId: number, quantity: number) => {
    if (!isAuthenticated) return;
    
    if (quantity <= 0) {
      await removeFromCart(gameId);
      return;
    }

    setIsLoading(true);
    try {
      const updatedCart = await CartAPI.addItem(gameId, quantity);
      setCart(updatedCart);
    } catch (error) {
      console.error('Erro ao atualizar quantidade:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const clearCart = async () => {
    if (!isAuthenticated) return;

    setIsLoading(true);
    try {
      const updatedCart = await CartAPI.clearCart();
      setCart(updatedCart);
      setAppliedCoupon(null);
    } catch (error) {
      console.error('Erro ao limpar carrinho:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const applyCoupon = async (code: string) => {
    if (!code.trim()) return;

    try {
      const coupon = await CartAPI.validateCoupon(code);
      if (coupon.is_valid) {
        setAppliedCoupon(coupon);
      } else {
        throw new Error(coupon.message || 'Cupom inválido');
      }
    } catch (error) {
      console.error('Erro ao aplicar cupom:', error);
      throw error;
    }
  };

  const removeCoupon = () => {
    setAppliedCoupon(null);
  };

  // Funções de cálculo
  const getTotalItems = (): number => {
    return cart?.total_items || 0;
  };

  const getSubtotal = (): number => {
    if (!cart) return 0;
    return CartAPI.parsePrice(cart.total_price);
  };

  const getDiscountAmount = (): number => {
    if (!appliedCoupon || !cart) return 0;
    const subtotal = getSubtotal();
    return CartAPI.calculateCouponDiscount(subtotal, appliedCoupon.discount_percent);
  };

  const getFinalTotal = (): number => {
    const subtotal = getSubtotal();
    const discount = getDiscountAmount();
    return subtotal - discount;
  };

  const value: CartContextType = {
    cart,
    isLoading,
    appliedCoupon,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    applyCoupon,
    removeCoupon,
    refreshCart,
    getTotalItems,
    getSubtotal,
    getDiscountAmount,
    getFinalTotal,
  };

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
}
