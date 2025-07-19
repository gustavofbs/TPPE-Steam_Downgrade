"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { CatalogService, Game, GameFilters, CatalogResponse, GameListItem } from './catalog-service';

interface CatalogContextType {
  games: GameListItem[];
  isLoading: boolean;
  error: string | null;
  genres: { id: number, name: string }[];
  developers: { id: number, name: string }[];
  filters: GameFilters;
  totalItems: number;
  totalPages: number;
  currentPage: number;
  updateFilters: (filters: Partial<GameFilters>) => void;
  setPage: (page: number) => void;
  clearFilters: () => void;
  addToWishlist: (gameId: string) => Promise<void>;
  purchaseGame: (gameId: string) => Promise<void>;
}

// Criar contexto
const CatalogContext = createContext<CatalogContextType | undefined>(undefined);

// Hook personalizado
export function useCatalog() {
  const context = useContext(CatalogContext);
  if (context === undefined) {
    throw new Error('useCatalog deve ser usado dentro de um CatalogProvider');
  }
  return context;
}

// Provider component
export function CatalogProvider({ children }: { children: ReactNode }) {
  const [games, setGames] = useState<GameListItem[]>([]);
  const [genres, setGenres] = useState<{ id: number, name: string }[]>([]);
  const [developers, setDevelopers] = useState<{ id: number, name: string }[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [totalItems, setTotalItems] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [filters, setFilters] = useState<GameFilters>({
    genres: [], // agora number[]
    developers: [], // agora number[]
    maxPrice: 400,
    minPrice: 0,
    onSale: false,
    search: "",
    sortBy: "relevance",
    page: 1,
    pageSize: 12
  });
  
  // Instância do serviço
  const catalogService = CatalogService.getInstance();

  // Carregar dados iniciais (gêneros e desenvolvedores)
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [genresData, developersData] = await Promise.all([
          catalogService.getGenres(),
          catalogService.getDevelopers()
        ]);
        
        setGenres(genresData);
        setDevelopers(developersData);
      } catch (err: any) {
        console.error('Erro ao carregar dados iniciais:', err);
        setError(err.message || 'Erro ao carregar dados iniciais');
      }
    };
    
    loadInitialData();
  }, []);

  // Carregar jogos quando os filtros mudam
  useEffect(() => {
    const loadGames = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        const response: CatalogResponse = await catalogService.getGames(filters);
        setGames(response.results);
        setTotalItems(response.count);
        setTotalPages(Math.ceil(response.count / (filters.pageSize || 12)));
      } catch (err: any) {
        console.error('Erro ao carregar jogos:', err);
        setError(err.message || 'Erro ao carregar jogos');
        setGames([]);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadGames();
  }, [filters]);

  // Atualizar filtros
  const updateFilters = (newFilters: Partial<GameFilters>) => {
    setFilters(prev => ({ ...prev, ...newFilters, page: 1 }));
  };

  // Mudar página
  const setPage = (page: number) => {
    setFilters(prev => ({ ...prev, page }));
  };

  // Limpar filtros
  const clearFilters = () => {
    setFilters({
      genres: [],
      developers: [],
      maxPrice: 400,
      minPrice: 0,
      onSale: false,
      search: "",
      sortBy: "relevance",
      page: 1,
      pageSize: 12
    });
  };

  // Adicionar à lista de desejos
  const addToWishlist = async (gameId: string) => {
    try {
      await catalogService.addToWishlist(gameId);
    } catch (err: any) {
      console.error('Erro ao adicionar à lista de desejos:', err);
      throw err;
    }
  };

  // Comprar jogo
  const purchaseGame = async (gameId: string) => {
    try {
      await catalogService.purchaseGame(gameId);
    } catch (err: any) {
      console.error('Erro ao comprar jogo:', err);
      throw err;
    }
  };

  // Valor do contexto
  const value = {
    games,
    isLoading,
    error,
    genres,
    developers,
    filters,
    totalItems,
    totalPages,
    currentPage: filters.page || 1,
    updateFilters,
    setPage,
    clearFilters,
    addToWishlist,
    purchaseGame
  };

  return (
    <CatalogContext.Provider value={value}>
      {children}
    </CatalogContext.Provider>
  );
}
