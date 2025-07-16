"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { CatalogService, Game, GameFilters, CatalogResponse } from './catalog-service';

interface CatalogContextType {
  games: Game[];
  isLoading: boolean;
  error: string | null;
  genres: string[];
  developers: string[];
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
  const [games, setGames] = useState<Game[]>([]);
  const [genres, setGenres] = useState<string[]>([]);
  const [developers, setDevelopers] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [totalItems, setTotalItems] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [filters, setFilters] = useState<GameFilters>({
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
        
        // Garante que sejam arrays
        setGenres(Array.isArray(genresData) ? genresData : []);
        setDevelopers(Array.isArray(developersData) ? developersData : []);
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
        console.log("CATALOG RESPONSE:", response);
        setGames(Array.isArray(response.results) ? response.results : []);
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
    currentPage: Number(filters.page) || 1,
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
