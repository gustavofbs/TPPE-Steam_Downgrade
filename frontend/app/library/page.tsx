"use client"

import { useState, useMemo, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { GameLibraryCard } from "@/components/game-library-card"
import { LibraryStats } from "@/components/library-stats"
import { FriendsPanel } from "@/components/friends-panel"
import { Library as LibraryIcon, Search, Grid3X3, List, AlertCircle } from "lucide-react"
import { LibraryProvider, useLibrary } from "@/lib/library-context"
import { useAuth } from "@/lib/auth-context"
import { useRouter } from "next/navigation"

// Mock data for user's library
const mockLibraryGames = [
  {
    id: 1,
    title: "Half-Life 3",
    image: "/placeholder.svg?height=200&width=150",
    isInstalled: true,
    lastPlayed: "Ontem",
    totalPlaytime: "45 horas",
    achievements: { unlocked: 8, total: 15 },
    installSize: "25.4 GB",
    version: "1.2.3",
    status: "ready", // ready, installing, updating, downloading
  },
  {
    id: 2,
    title: "Portal 3",
    image: "/placeholder.svg?height=200&width=150",
    isInstalled: true,
    lastPlayed: "3 dias atrás",
    totalPlaytime: "12 horas",
    achievements: { unlocked: 5, total: 20 },
    installSize: "15.2 GB",
    version: "2.1.0",
    status: "ready",
  },
  {
    id: 3,
    title: "Left 4 Dead 3",
    image: "/placeholder.svg?height=200&width=150",
    isInstalled: false,
    lastPlayed: "Nunca",
    totalPlaytime: "0 horas",
    achievements: { unlocked: 0, total: 25 },
    installSize: "32.1 GB",
    version: "1.0.0",
    status: "not_installed",
  },
  {
    id: 4,
    title: "The Witcher 4",
    image: "/placeholder.svg?height=200&width=150",
    isInstalled: false,
    lastPlayed: "Nunca",
    totalPlaytime: "0 horas",
    achievements: { unlocked: 0, total: 30 },
    installSize: "55.8 GB",
    version: "1.0.0",
    status: "not_installed",
  },
  {
    id: 5,
    title: "Cyberpunk 2078",
    image: "/placeholder.svg?height=200&width=150",
    isInstalled: false,
    lastPlayed: "1 semana atrás",
    totalPlaytime: "8 horas",
    achievements: { unlocked: 3, total: 40 },
    installSize: "70.2 GB",
    version: "2.0.1",
    status: "downloading",
    downloadProgress: 35,
  },
  {
    id: 6,
    title: "GTA VI",
    image: "/placeholder.svg?height=200&width=150",
    isInstalled: true,
    lastPlayed: "2 horas atrás",
    totalPlaytime: "120 horas",
    achievements: { unlocked: 25, total: 50 },
    installSize: "95.5 GB",
    version: "1.5.2",
    status: "updating",
    downloadProgress: 67,
  },
]

// Wrapper component para prover o contexto da biblioteca
export default function LibraryPageWrapper() {
  return (
    <LibraryProvider>
      <LibraryPageContent />
    </LibraryProvider>
  )
}

// Componente principal da biblioteca que usa o contexto
function LibraryPageContent() {
  const router = useRouter();
  const { isAuthenticated, user } = useAuth();
  const { library, isLoading, error, userStats } = useLibrary();
  const [searchQuery, setSearchQuery] = useState("")
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid")
  const [sortOption, setSortOption] = useState("name_asc")
  const [filterInstalled, setFilterInstalled] = useState<boolean | null>(null)
  const [activeTab, setActiveTab] = useState("all")

  // Redirecionar para login se não estiver autenticado
  useEffect(() => {
    if (!isAuthenticated && !isLoading) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  // Converter itens da biblioteca para o formato esperado pelos componentes
  const convertLibraryItems = useMemo(() => {
    if (!library || !library.items) return [];

    return library.items.map(item => ({
      id: item.id,
      title: item.game_detail.title,
      image: item.game_detail.cover_image || "/placeholder.svg?height=200&width=150",
      isInstalled: item.downloads && item.downloads.length > 0,
      lastPlayed: item.last_played ? new Date(item.last_played).toLocaleDateString('pt-BR') : 'Nunca',
      totalPlaytime: item.formatted_playtime,
      achievements: { 
        unlocked: Math.floor(Math.random() * 20), // Simulação, já que não temos essa info no backend
        total: Math.floor(Math.random() * 30) + 20 
      },
      installSize: item.downloads && item.downloads.length > 0 
        ? `${item.downloads[0].game_version_detail.size_mb / 1000} GB` 
        : 'Não instalado',
      version: item.downloads && item.downloads.length > 0 
        ? item.downloads[0].game_version_detail.version 
        : '',
      status: item.downloads && item.downloads.length > 0 ? "ready" : "not_installed",
      isFavorite: item.is_favorite
    }));
  }, [library]);

  // Filter and sort games based on user selections
  const filteredGames = useMemo(() => {
    let result = [...(convertLibraryItems || [])]

    // Filter by search query
    if (searchQuery) {
      result = result.filter((game) =>
        game.title.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }

    // Filter by installation status
    if (filterInstalled !== null) {
      result = result.filter((game) => game.isInstalled === filterInstalled)
    }

    // Filter by tab
    if (activeTab === "installed") {
      result = result.filter((game) => game.isInstalled)
    } else if (activeTab === "not_installed") {
      result = result.filter((game) => !game.isInstalled)
    } else if (activeTab === "favorites") {
      result = result.filter((game) => game.isFavorite)
    }

    // Sort games
    switch (sortOption) {
      case "name_asc":
        result.sort((a, b) => a.title.localeCompare(b.title))
        break
      case "name_desc":
        result.sort((a, b) => b.title.localeCompare(a.title))
        break
      case "recent":
        // Ordenar por último jogado
        result.sort((a, b) => {
          if (a.lastPlayed === 'Nunca' && b.lastPlayed === 'Nunca') return 0;
          if (a.lastPlayed === 'Nunca') return 1;
          if (b.lastPlayed === 'Nunca') return -1;
          return new Date(b.lastPlayed).getTime() - new Date(a.lastPlayed).getTime();
        })
        break
      case "playtime":
        // Ordenar por tempo de jogo (usando id como fallback para estabilidade)
        result.sort((a, b) => {
          const aTime = parseInt(a.totalPlaytime) || 0;
          const bTime = parseInt(b.totalPlaytime) || 0;
          return bTime - aTime || a.id.localeCompare(b.id);
        })
        break
    }

    return result
  }, [searchQuery, sortOption, filterInstalled, activeTab, convertLibraryItems])

  // Se não estiver autenticado, não renderizar nada (será redirecionado)
  if (!isAuthenticated && !isLoading) {
    return null;
  }

  // Se estiver carregando, mostrar indicador
  if (isLoading) {
    return (
      <div className="container mx-auto py-6 flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-steam-blue mx-auto mb-4"></div>
          <p className="text-steam-text-secondary">Carregando sua biblioteca...</p>
        </div>
      </div>
    );
  }

  // Se houver erro, mostrar mensagem
  if (error) {
    return (
      <div className="container mx-auto py-6 flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-400 mb-4">{error}</p>
          <Button onClick={() => window.location.reload()}>Tentar novamente</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-6 space-y-8">
      <div className="flex flex-col md:flex-row gap-6">
        {/* Main content */}
        <Tabs defaultValue="all">
        <div className="flex-1 space-y-6">
          <div className="flex items-center justify-between">
            <h1 className="text-3xl font-bold flex items-center gap-2">
              <LibraryIcon className="h-8 w-8" /> Minha Biblioteca
            </h1>
            <div className="flex items-center gap-2">
              <Button
                variant={viewMode === "grid" ? "default" : "outline"}
                size="icon"
                onClick={() => setViewMode("grid")}
              >
                <Grid3X3 className="h-4 w-4" />
              </Button>
              <Button
                variant={viewMode === "list" ? "default" : "outline"}
                size="icon"
                onClick={() => setViewMode("list")}
              >
                <List className="h-4 w-4" />
              </Button>
            </div>
          </div>
          <div className="flex justify-between items-center mb-4">
            <TabsList>
              <TabsTrigger value="all">
                Todos <Badge variant="outline" className="ml-2">{convertLibraryItems.length}</Badge>
              </TabsTrigger>
              <TabsTrigger value="installed">
                Instalados{" "}
                <Badge variant="outline" className="ml-2">
                  {convertLibraryItems.filter((g) => g.isInstalled).length}
                </Badge>
              </TabsTrigger>
              <TabsTrigger value="not_installed">
                Não Instalados{" "}
                <Badge variant="outline" className="ml-2">
                  {convertLibraryItems.filter((g) => !g.isInstalled).length}
                </Badge>
              </TabsTrigger>
              <TabsTrigger value="favorites">
                Favoritos{" "}
                <Badge variant="outline" className="ml-2">
                  {convertLibraryItems.filter((g) => g.isFavorite).length}
                </Badge>
              </TabsTrigger>
            </TabsList>
            <div className="flex items-center gap-2">
              <Select value={sortOption} onValueChange={setSortOption}>
                <SelectTrigger className="w-48 bg-slate-700 border-slate-600 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-slate-800 border-slate-700">
                  <SelectItem value="name_asc">Nome (A-Z)</SelectItem>
                  <SelectItem value="name_desc">Nome (Z-A)</SelectItem>
                  <SelectItem value="recent">Jogados recentemente</SelectItem>
                  <SelectItem value="playtime">Tempo de jogo</SelectItem>
                </SelectContent>
              </Select>
              <Button
                variant={filterInstalled === null ? "default" : "outline"}
                size="icon"
                onClick={() => setFilterInstalled(null)}
              >
                <Grid3X3 className="h-4 w-4" />
              </Button>
              <Button
                variant={filterInstalled === true ? "default" : "outline"}
                size="icon"
                onClick={() => setFilterInstalled(true)}
              >
                <List className="h-4 w-4" />
              </Button>
              <Button
                variant={filterInstalled === false ? "default" : "outline"}
                size="icon"
                onClick={() => setFilterInstalled(false)}
              >
                <AlertCircle className="h-4 w-4" />
              </Button>
            </div>
          </div>
          <GameLibraryGrid games={filteredGames} viewMode={viewMode} />
        </div>
        </Tabs>

        {/* Sidebar */}
        <div className="w-full md:w-80 space-y-6">
          <LibraryStats />
          <FriendsPanel />
        </div>
      </div>
    </div>
  )
}

// Game Library Grid Component
function GameLibraryGrid({ games, viewMode }: { games: any[]; viewMode: "grid" | "list" }) {
  if (games.length === 0) {
    return (
      <div className="text-center py-12">
        <LibraryIcon className="h-12 w-12 mx-auto text-steam-text-secondary mb-4" />
        <h3 className="text-xl font-medium mb-2">Nenhum jogo encontrado</h3>
        <p className="text-steam-text-secondary">
          Tente ajustar seus filtros ou adicione jogos à sua biblioteca
        </p>
      </div>
    )
  }

  return (
    <div className={`grid gap-4 ${viewMode === "grid" ? "grid-cols-1 md:grid-cols-2" : "grid-cols-1"}`}>
      {games.map((game) => (
        <GameLibraryCard key={game.id} game={game} viewMode={viewMode} />
      ))}
    </div>
  )
}
