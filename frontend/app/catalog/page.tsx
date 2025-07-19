"use client"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { GameCard } from "@/components/game-card"
import { FilterSidebar } from "@/components/filter-sidebar"
import { Gamepad2, Filter, Search, Grid3X3, List, Loader2 } from "lucide-react"
import { CatalogProvider, useCatalog } from "@/lib/catalog-context"
import { Game, GameFilters } from "@/lib/catalog-service"

function CatalogPageContent() {
  const {
    games,
    isLoading,
    error,
    genres,
    developers,
    filters,
    totalItems,
    totalPages,
    currentPage,
    updateFilters,
    setPage,
    clearFilters
  } = useCatalog();

  const [viewMode, setViewMode] = useState<"grid" | "list">("grid")
  const [showFilters, setShowFilters] = useState(true)

  // Manipuladores de eventos
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    updateFilters({ search: e.target.value });
  };

  const handleSortChange = (value: string) => {
    updateFilters({ sortBy: value });
  };

  const handleItemsPerPageChange = (value: string) => {
    updateFilters({ pageSize: Number(value) });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-4">
            <Gamepad2 className="h-8 w-8 text-blue-400" />
            <h1 className="text-4xl font-bold text-white">Catálogo de Jogos</h1>
          </div>

          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbLink href="/" className="text-blue-300 hover:text-blue-100">
                  Início
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator className="text-slate-400" />
              <BreadcrumbItem>
                <BreadcrumbPage className="text-slate-300">Catálogo</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </div>

        {/* Search Bar */}
        <Card className="mb-6 bg-slate-800/50 border-slate-700">
          <CardContent className="p-4">
            <div className="flex gap-4 items-center">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
                <Input
                  placeholder="Buscar jogos..."
                  value={filters.search || ""}
                  onChange={handleSearchChange}
                  className="pl-10 bg-slate-700 border-slate-600 text-white placeholder:text-slate-400"
                />
              </div>
              <Button
                variant="outline"
                onClick={() => setShowFilters(!showFilters)}
                className="border-slate-600 text-slate-300 hover:bg-slate-700"
              >
                <Filter className="h-4 w-4 mr-2" />
                Filtros
              </Button>
            </div>
          </CardContent>
        </Card>

        <div className="flex gap-6">
          {/* Sidebar Filters */}
          {showFilters && (
            <div className="w-80 flex-shrink-0">
              <FilterSidebar 
                filters={{
                  genres: filters.genres || [],
                  developers: filters.developers || [],
                  minPrice: filters.minPrice || 0,
                  maxPrice: filters.maxPrice || 400,
                  onSale: filters.onSale || false,
                  search: filters.search || ""
                }} 
                availableGenres={genres}
                availableDevelopers={developers}
                onFilterChange={(key, value) => updateFilters({ [key]: value })} 
                onClearFilters={clearFilters} 
              />
            </div>
          )}

          {/* Main Content */}
          <div className="flex-1">
            {/* Controls */}
            <Card className="mb-6 bg-slate-800/50 border-slate-700">
              <CardContent className="p-4">
                <div className="flex justify-between items-center flex-wrap gap-4">
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                      <Label className="text-slate-300">Ordenar:</Label>
                      <Select value={filters.sortBy || "relevance"} onValueChange={handleSortChange}>
                        <SelectTrigger className="w-48 bg-slate-700 border-slate-600 text-white">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent className="bg-slate-800 border-slate-700">
                          <SelectItem value="relevance">Relevância</SelectItem>
                          <SelectItem value="price-low">Preço (menor)</SelectItem>
                          <SelectItem value="price-high">Preço (maior)</SelectItem>
                          <SelectItem value="name">Nome (A-Z)</SelectItem>
                          <SelectItem value="discount">Maior desconto</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="flex items-center gap-2">
                      <Label className="text-slate-300">Exibir:</Label>
                      <Select 
                        value={(filters.pageSize || 12).toString()} 
                        onValueChange={handleItemsPerPageChange}
                      >
                        <SelectTrigger className="w-20 bg-slate-700 border-slate-600 text-white">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent className="bg-slate-800 border-slate-700">
                          <SelectItem value="12">12</SelectItem>
                          <SelectItem value="24">24</SelectItem>
                          <SelectItem value="48">48</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <Button
                      variant={viewMode === "grid" ? "default" : "outline"}
                      size="sm"
                      onClick={() => setViewMode("grid")}
                      className="border-slate-600"
                    >
                      <Grid3X3 className="h-4 w-4" />
                    </Button>
                    <Button
                      variant={viewMode === "list" ? "default" : "outline"}
                      size="sm"
                      onClick={() => setViewMode("list")}
                      className="border-slate-600"
                    >
                      <List className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Loading State */}
            {isLoading && (
              <div className="flex justify-center items-center py-20">
                <Loader2 className="h-10 w-10 text-blue-400 animate-spin" />
                <span className="ml-3 text-slate-300">Carregando jogos...</span>
              </div>
            )}

            {/* Error State */}
            {error && !isLoading && (
              <Card className="bg-red-900/30 border-red-800 mb-6">
                <CardContent className="p-6 text-center">
                  <p className="text-red-300 mb-4">{error}</p>
                  <Button onClick={clearFilters} className="bg-blue-600 hover:bg-blue-700">
                    Tentar Novamente
                  </Button>
                </CardContent>
              </Card>
            )}

            {/* Results Info */}
            {!isLoading && !error && (
              <div className="mb-4 text-slate-300">
                Mostrando {games.length > 0 ? ((currentPage - 1) * (filters.pageSize || 12) + 1) : 0}-
                {Math.min(currentPage * (filters.pageSize || 12), totalItems)} de {totalItems} jogos
              </div>
            )}

            {/* Games Grid */}
            {!isLoading && !error && games.length > 0 ? (
              <div
                className={`grid gap-6 mb-8 ${
                  viewMode === "grid" ? "grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4" : "grid-cols-1"
                }`}
              >
                {games.map((game) => (
                  <GameCard key={game.id} game={game as unknown as Game} viewMode={viewMode} />
                ))}
              </div>
            ) : !isLoading && !error ? (
              <Card className="bg-slate-800/50 border-slate-700">
                <CardContent className="p-8 text-center">
                  <p className="text-slate-400 text-lg">Nenhum jogo encontrado com os filtros aplicados.</p>
                  <Button onClick={clearFilters} className="mt-4 bg-blue-600 hover:bg-blue-700">
                    Limpar Filtros
                  </Button>
                </CardContent>
              </Card>
            ) : null}

            {/* Pagination */}
            {!isLoading && !error && totalPages > 1 && (
              <div className="flex justify-center">
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    disabled={currentPage === 1}
                    onClick={() => setPage(currentPage - 1)}
                    className="border-slate-600 text-slate-300 hover:bg-slate-700"
                  >
                    Anterior
                  </Button>

                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    // Mostrar no máximo 5 páginas
                    let pageToShow;
                    if (totalPages <= 5) {
                      pageToShow = i + 1;
                    } else if (currentPage <= 3) {
                      pageToShow = i + 1;
                    } else if (currentPage >= totalPages - 2) {
                      pageToShow = totalPages - 4 + i;
                    } else {
                      pageToShow = currentPage - 2 + i;
                    }
                    
                    return (
                      <Button
                        key={pageToShow}
                        variant={currentPage === pageToShow ? "default" : "outline"}
                        onClick={() => setPage(pageToShow)}
                        className={`border-slate-600 ${
                          currentPage === pageToShow ? "bg-blue-600 hover:bg-blue-700" : "text-slate-300 hover:bg-slate-700"
                        }`}
                      >
                        {pageToShow}
                      </Button>
                    );
                  })}

                  <Button
                    variant="outline"
                    disabled={currentPage === totalPages}
                    onClick={() => setPage(currentPage + 1)}
                    className="border-slate-600 text-slate-300 hover:bg-slate-700"
                  >
                    Próximo
                  </Button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

// Componente principal que envolve o conteúdo com o provider
export default function CatalogPage() {
  return (
    <CatalogProvider>
      <CatalogPageContent />
    </CatalogProvider>
  );
}
