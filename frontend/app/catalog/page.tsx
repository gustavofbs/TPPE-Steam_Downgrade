"use client"

import { useState, useMemo } from "react"
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
import { Gamepad2, Filter, Search, Grid3X3, List } from "lucide-react"

// Mock data for games
const mockGames = [
  {
    id: 1,
    title: "Half-Life 3",
    price: 99.95,
    originalPrice: 199.9,
    discount: 50,
    image: "/placeholder.svg?height=200&width=300",
    genre: ["Ação", "Aventura"],
    developer: "Valve",
    onSale: true,
  },
  {
    id: 2,
    title: "Portal 3",
    price: 129.9,
    originalPrice: null,
    discount: 0,
    image: "/placeholder.svg?height=200&width=300",
    genre: ["Puzzle", "Aventura"],
    developer: "Valve",
    onSale: false,
  },
  {
    id: 3,
    title: "Left 4 Dead 3",
    price: 39.97,
    originalPrice: 159.9,
    discount: 75,
    image: "/placeholder.svg?height=200&width=300",
    genre: ["Ação", "Cooperativo"],
    developer: "Valve",
    onSale: true,
  },
  {
    id: 4,
    title: "The Witcher 4",
    price: 249.9,
    originalPrice: null,
    discount: 0,
    image: "/placeholder.svg?height=200&width=300",
    genre: ["RPG", "Aventura"],
    developer: "CD Projekt Red",
    onSale: false,
  },
  {
    id: 5,
    title: "Cyberpunk 2078",
    price: 209.93,
    originalPrice: 299.9,
    discount: 30,
    image: "/placeholder.svg?height=200&width=300",
    genre: ["RPG", "Ação"],
    developer: "CD Projekt Red",
    onSale: true,
  },
  {
    id: 6,
    title: "GTA VI",
    price: 349.9,
    originalPrice: null,
    discount: 0,
    image: "/placeholder.svg?height=200&width=300",
    genre: ["Ação", "Aventura"],
    developer: "Rockstar Games",
    onSale: false,
  },
  {
    id: 7,
    title: "Assassin's Creed: Future",
    price: 179.9,
    originalPrice: null,
    discount: 0,
    image: "/placeholder.svg?height=200&width=300",
    genre: ["Ação", "Aventura"],
    developer: "Ubisoft",
    onSale: false,
  },
  {
    id: 8,
    title: "FIFA 2025",
    price: 89.95,
    originalPrice: 179.9,
    discount: 50,
    image: "/placeholder.svg?height=200&width=300",
    genre: ["Esporte", "Simulação"],
    developer: "EA Sports",
    onSale: true,
  },
]

interface Filters {
  genres: string[]
  developers: string[]
  maxPrice: number
  onSale: boolean
  search: string
}

export default function CatalogPage() {
  const [filters, setFilters] = useState<Filters>({
    genres: [],
    developers: [],
    maxPrice: 400,
    onSale: false,
    search: "",
  })

  const [sortBy, setSortBy] = useState("relevance")
  const [itemsPerPage, setItemsPerPage] = useState(12)
  const [currentPage, setCurrentPage] = useState(1)
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid")
  const [showFilters, setShowFilters] = useState(true)

  // Filter and sort games
  const filteredGames = useMemo(() => {
    const filtered = mockGames.filter((game) => {
      // Search filter
      if (filters.search && !game.title.toLowerCase().includes(filters.search.toLowerCase())) {
        return false
      }

      // Genre filter
      if (filters.genres.length > 0 && !filters.genres.some((genre) => game.genre.includes(genre))) {
        return false
      }

      // Developer filter
      if (filters.developers.length > 0 && !filters.developers.includes(game.developer)) {
        return false
      }

      // Price filter
      if (game.price > filters.maxPrice) {
        return false
      }

      // On sale filter
      if (filters.onSale && !game.onSale) {
        return false
      }

      return true
    })

    // Sort games
    switch (sortBy) {
      case "price-low":
        filtered.sort((a, b) => a.price - b.price)
        break
      case "price-high":
        filtered.sort((a, b) => b.price - a.price)
        break
      case "name":
        filtered.sort((a, b) => a.title.localeCompare(b.title))
        break
      case "discount":
        filtered.sort((a, b) => b.discount - a.discount)
        break
      default:
        // Keep original order for relevance
        break
    }

    return filtered
  }, [filters, sortBy])

  // Pagination
  const totalPages = Math.ceil(filteredGames.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const paginatedGames = filteredGames.slice(startIndex, startIndex + itemsPerPage)

  const updateFilter = (key: keyof Filters, value: any) => {
    setFilters((prev) => ({ ...prev, [key]: value }))
    setCurrentPage(1) // Reset to first page when filtering
  }

  const clearFilters = () => {
    setFilters({
      genres: [],
      developers: [],
      maxPrice: 400,
      onSale: false,
      search: "",
    })
    setCurrentPage(1)
  }

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
                  value={filters.search}
                  onChange={(e) => updateFilter("search", e.target.value)}
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
              <FilterSidebar filters={filters} onFilterChange={updateFilter} onClearFilters={clearFilters} />
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
                      <Select value={sortBy} onValueChange={setSortBy}>
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
                      <Select value={itemsPerPage.toString()} onValueChange={(value) => setItemsPerPage(Number(value))}>
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

            {/* Results Info */}
            <div className="mb-4 text-slate-300">
              Mostrando {startIndex + 1}-{Math.min(startIndex + itemsPerPage, filteredGames.length)} de{" "}
              {filteredGames.length} jogos
            </div>

            {/* Games Grid */}
            {paginatedGames.length > 0 ? (
              <div
                className={`grid gap-6 mb-8 ${
                  viewMode === "grid" ? "grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4" : "grid-cols-1"
                }`}
              >
                {paginatedGames.map((game) => (
                  <GameCard key={game.id} game={game} viewMode={viewMode} />
                ))}
              </div>
            ) : (
              <Card className="bg-slate-800/50 border-slate-700">
                <CardContent className="p-8 text-center">
                  <p className="text-slate-400 text-lg">Nenhum jogo encontrado com os filtros aplicados.</p>
                  <Button onClick={clearFilters} className="mt-4 bg-blue-600 hover:bg-blue-700">
                    Limpar Filtros
                  </Button>
                </CardContent>
              </Card>
            )}

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center">
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    disabled={currentPage === 1}
                    onClick={() => setCurrentPage(currentPage - 1)}
                    className="border-slate-600 text-slate-300 hover:bg-slate-700"
                  >
                    Anterior
                  </Button>

                  {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                    <Button
                      key={page}
                      variant={currentPage === page ? "default" : "outline"}
                      onClick={() => setCurrentPage(page)}
                      className={`border-slate-600 ${
                        currentPage === page ? "bg-blue-600 hover:bg-blue-700" : "text-slate-300 hover:bg-slate-700"
                      }`}
                    >
                      {page}
                    </Button>
                  ))}

                  <Button
                    variant="outline"
                    disabled={currentPage === totalPages}
                    onClick={() => setCurrentPage(currentPage + 1)}
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
