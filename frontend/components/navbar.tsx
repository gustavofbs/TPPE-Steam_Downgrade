"use client"

import type React from "react"

import { useState, useEffect, useRef } from "react"
import Link from "next/link"
import { useAuth } from "@/lib/auth-context"
import { GamesAPI, type Game } from "../lib/games-api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import {
  Gamepad2,
  Home,
  Store,
  Library,
  Heart,
  Search,
  User,
  ShoppingCart,
  Settings,
  LogOut,
  LogIn,
  UserPlus,
  Menu,
} from "lucide-react"

export function Navbar() {
  const { user, logout } = useAuth()
  const [searchQuery, setSearchQuery] = useState("")
  const [isOpen, setIsOpen] = useState(false)
  const [searchResults, setSearchResults] = useState<Game[]>([])
  const [showResults, setShowResults] = useState(false)
  const [isSearching, setIsSearching] = useState(false)
  const searchRef = useRef<HTMLDivElement>(null)

  // Debounce para busca
  useEffect(() => {
    const timeoutId = setTimeout(async () => {
      if (searchQuery.trim().length >= 2) {
        setIsSearching(true)
        try {
          const results = await GamesAPI.searchGames(searchQuery.trim(), 5)
          setSearchResults(results || [])
          setShowResults(true)
        } catch (error) {
          console.error('Erro na busca:', error)
          setSearchResults([])
        } finally {
          setIsSearching(false)
        }
      } else {
        setSearchResults([])
        setShowResults(false)
      }
    }, 300)

    return () => clearTimeout(timeoutId)
  }, [searchQuery])

  // Fechar resultados quando clicar fora
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setShowResults(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      // Redirecionar para página de busca com query
      window.location.href = `/catalog?search=${encodeURIComponent(searchQuery.trim())}`
    }
  }

  const handleGameSelect = (game: Game) => {
    setShowResults(false)
    setSearchQuery('')
    // Redirecionar para página do jogo
    window.location.href = `/games/${game.slug}`
  }

  const handleLogout = () => {
    logout()
    window.location.href = '/login'
  }

  const navItems = [
    { href: "/", label: "Início", icon: Home },
    { href: "/catalog", label: "Loja", icon: Store },
    { href: "/library", label: "Biblioteca", icon: Library },
    { href: "/wishlist", label: "Lista de Desejos", icon: Heart },
  ]

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-slate-700 bg-slate-900/95 backdrop-blur supports-[backdrop-filter]:bg-slate-900/60">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2 text-white hover:text-blue-300 transition-colors">
            <Gamepad2 className="h-8 w-8 text-blue-400" />
            <span className="text-xl font-bold">SteamRF</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className="flex items-center space-x-1 text-slate-300 hover:text-white transition-colors"
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </Link>
              )
            })}
          </div>

          {/* Search Bar with Autocomplete */}
          <div className="hidden md:flex items-center space-x-2" ref={searchRef}>
            <form onSubmit={handleSearch} className="relative">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4 z-10" />
                <Input
                  type="search"
                  placeholder="Buscar jogos..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onFocus={() => searchResults?.length > 0 && setShowResults(true)}
                  className="pl-10 w-64 input-steam"
                  autoComplete="off"
                />
                
                {/* Dropdown de resultados */}
                {showResults && (searchResults?.length > 0 || isSearching) && (
                  <div className="absolute top-full left-0 right-0 mt-1 bg-slate-800 border border-slate-700 rounded-lg shadow-lg z-50 max-h-80 overflow-y-auto">
                    {isSearching ? (
                      <div className="p-4 text-center text-slate-400">
                        <div className="animate-spin inline-block w-4 h-4 border-2 border-blue-400 border-t-transparent rounded-full mr-2"></div>
                        Buscando...
                      </div>
                    ) : (
                      <>
                        {searchResults?.map((game) => (
                          <button
                            key={game.id}
                            onClick={() => handleGameSelect(game)}
                            className="w-full p-3 text-left hover:bg-slate-700 transition-colors border-b border-slate-700 last:border-b-0 flex items-center space-x-3"
                          >
                            {game.cover_image && (
                              <img
                                src={game.cover_image}
                                alt={game.title}
                                className="w-10 h-10 object-cover rounded"
                              />
                            )}
                            <div className="flex-1 min-w-0">
                              <div className="text-white font-medium truncate">{game.title}</div>
                              <div className="text-slate-400 text-sm truncate">{game.developer_name}</div>
                              {game.is_on_sale ? (
                                <div className="flex items-center space-x-2 mt-1">
                                  <span className="text-slate-400 line-through text-xs">R$ {Number(game.base_price).toFixed(2)}</span>
                                  <span className="text-green-400 text-sm font-medium">R$ {Number(game.discount_price).toFixed(2)}</span>
                                </div>
                              ) : (
                                <div className="text-blue-400 text-sm mt-1">R$ {Number(game.base_price).toFixed(2)}</div>
                              )}
                            </div>
                          </button>
                        ))}
                        {searchResults?.length === 5 && (
                          <div className="p-3 text-center border-t border-slate-700">
                            <button
                              onClick={() => handleSearch({ preventDefault: () => {} } as React.FormEvent)}
                              className="text-blue-400 hover:text-blue-300 text-sm"
                            >
                              Ver todos os resultados
                            </button>
                          </div>
                        )}
                      </>
                    )}
                  </div>
                )}
              </div>
            </form>
            <Button onClick={() => handleSearch({ preventDefault: () => {} } as React.FormEvent)} className="btn-steam">
              <Search className="h-4 w-4" />
            </Button>
          </div>

          {/* User Menu */}
          <div className="hidden md:flex items-center space-x-4">
            {user ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="flex items-center space-x-2 text-slate-300 hover:text-white">
                    <User className="h-4 w-4" />
                    <span>{user.username || user.first_name || 'Usuário'}</span>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56 bg-slate-800 border-slate-700" align="end">
                  <DropdownMenuItem className="text-slate-300 hover:text-white hover:bg-slate-700" asChild>
                    <Link href="/profile">
                      <User className="mr-2 h-4 w-4" />
                      <span>Perfil</span>
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem className="text-slate-300 hover:text-white hover:bg-slate-700">
                    <ShoppingCart className="mr-2 h-4 w-4" />
                    <span>Compras</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem className="text-slate-300 hover:text-white hover:bg-slate-700">
                    <Settings className="mr-2 h-4 w-4" />
                    <span>Configurações</span>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator className="bg-slate-700" />
                  <DropdownMenuItem
                    onClick={handleLogout}
                    className="text-red-400 hover:text-red-300 hover:bg-slate-700"
                  >
                    <LogOut className="mr-2 h-4 w-4" />
                    <span>Sair</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : (
              <div className="flex items-center space-x-2">
                <Button asChild className="btn-steam">
                  <Link href="/login">
                    <LogIn className="mr-2 h-4 w-4" />
                    Entrar
                  </Link>
                </Button>
                <Button
                  variant="outline"
                  asChild
                  className="border-slate-600 text-slate-300 hover:bg-slate-700 bg-transparent"
                >
                  <Link href="/register">
                    <UserPlus className="mr-2 h-4 w-4" />
                    Registrar
                  </Link>
                </Button>
              </div>
            )}
          </div>

          {/* Mobile Menu */}
          <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild className="md:hidden">
              <Button variant="ghost" size="icon" className="text-slate-300">
                <Menu className="h-6 w-6" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-80 bg-slate-900 border-slate-700">
              <div className="flex flex-col space-y-4 mt-8">
                {/* Mobile Search */}
                <form onSubmit={handleSearch} className="flex space-x-2">
                  <Input
                    type="search"
                    placeholder="Buscar jogos..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="input-steam"
                  />
                  <Button type="submit" className="btn-steam">
                    <Search className="h-4 w-4" />
                  </Button>
                </form>

                {/* Mobile Navigation */}
                <div className="space-y-2">
                  {navItems.map((item) => {
                    const Icon = item.icon
                    return (
                      <Link
                        key={item.href}
                        href={item.href}
                        onClick={() => setIsOpen(false)}
                        className="flex items-center space-x-3 p-3 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition-colors"
                      >
                        <Icon className="h-5 w-5" />
                        <span>{item.label}</span>
                      </Link>
                    )
                  })}
                </div>

                {/* Mobile User Menu */}
                <div className="border-t border-slate-700 pt-4">
                  {user ? (
                    <div className="space-y-2">
                      <div className="flex items-center space-x-3 p-3 text-white">
                        <User className="h-5 w-5" />
                        <span>{user.username || user.first_name || 'Usuário'}</span>
                      </div>
                      <Link
                        href="/profile"
                        onClick={() => setIsOpen(false)}
                        className="flex items-center space-x-3 p-3 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition-colors"
                      >
                        <User className="h-5 w-5" />
                        <span>Perfil</span>
                      </Link>
                      <Link
                        href="/purchases"
                        onClick={() => setIsOpen(false)}
                        className="flex items-center space-x-3 p-3 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition-colors"
                      >
                        <ShoppingCart className="h-5 w-5" />
                        <span>Compras</span>
                      </Link>
                      <Link
                        href="/settings"
                        onClick={() => setIsOpen(false)}
                        className="flex items-center space-x-3 p-3 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition-colors"
                      >
                        <Settings className="h-5 w-5" />
                        <span>Configurações</span>
                      </Link>
                      <button
                        onClick={handleLogout}
                        className="flex items-center space-x-3 p-3 rounded-lg text-red-400 hover:text-red-300 hover:bg-slate-800 transition-colors w-full text-left"
                      >
                        <LogOut className="h-5 w-5" />
                        <span>Sair</span>
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <Button asChild className="w-full btn-steam">
                        <Link href="/login" onClick={() => setIsOpen(false)}>
                          <LogIn className="mr-2 h-4 w-4" />
                          Entrar
                        </Link>
                      </Button>
                      <Button
                        variant="outline"
                        asChild
                        className="w-full border-slate-600 text-slate-300 hover:bg-slate-700 bg-transparent"
                      >
                        <Link href="/register" onClick={() => setIsOpen(false)}>
                          <UserPlus className="mr-2 h-4 w-4" />
                          Registrar
                        </Link>
                      </Button>
                    </div>
                  )}
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </nav>
  )
}
