"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Slider } from "@/components/ui/slider"
import { Badge } from "@/components/ui/badge"
import { Filter, X } from "lucide-react"

interface Filters {
  genres: string[]
  developers: string[]
  maxPrice: number
  onSale: boolean
  search: string
}

interface FilterSidebarProps {
  filters: Filters
  onFilterChange: (key: keyof Filters, value: any) => void
  onClearFilters: () => void
}

const availableGenres = ["Ação", "Aventura", "RPG", "Estratégia", "Simulação", "Puzzle", "Esporte", "Cooperativo"]
const availableDevelopers = ["Valve", "CD Projekt Red", "Ubisoft", "Rockstar Games", "EA Sports"]

export function FilterSidebar({ filters, onFilterChange, onClearFilters }: FilterSidebarProps) {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(price)
  }

  const handleGenreChange = (genre: string, checked: boolean) => {
    const newGenres = checked ? [...filters.genres, genre] : filters.genres.filter((g) => g !== genre)
    onFilterChange("genres", newGenres)
  }

  const handleDeveloperChange = (developer: string, checked: boolean) => {
    const newDevelopers = checked
      ? [...filters.developers, developer]
      : filters.developers.filter((d) => d !== developer)
    onFilterChange("developers", newDevelopers)
  }

  const hasActiveFilters =
    filters.genres.length > 0 ||
    filters.developers.length > 0 ||
    filters.maxPrice < 400 ||
    filters.onSale ||
    filters.search

  return (
    <Card className="bg-slate-800/50 border-slate-700 sticky top-4">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-white flex items-center gap-2">
            <Filter className="h-5 w-5" />
            Filtros
          </CardTitle>
          {hasActiveFilters && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onClearFilters}
              className="text-slate-400 hover:text-white hover:bg-slate-700"
            >
              <X className="h-4 w-4 mr-1" />
              Limpar
            </Button>
          )}
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Active Filters */}
        {hasActiveFilters && (
          <div>
            <Label className="text-slate-300 text-sm font-medium">Filtros Ativos:</Label>
            <div className="flex flex-wrap gap-1 mt-2">
              {filters.genres.map((genre) => (
                <Badge key={genre} variant="secondary" className="bg-blue-600 text-white">
                  {genre}
                  <button
                    onClick={() => handleGenreChange(genre, false)}
                    className="ml-1 hover:bg-blue-700 rounded-full p-0.5"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              ))}
              {filters.developers.map((dev) => (
                <Badge key={dev} variant="secondary" className="bg-purple-600 text-white">
                  {dev}
                  <button
                    onClick={() => handleDeveloperChange(dev, false)}
                    className="ml-1 hover:bg-purple-700 rounded-full p-0.5"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              ))}
              {filters.onSale && (
                <Badge variant="secondary" className="bg-green-600 text-white">
                  Em Promoção
                  <button
                    onClick={() => onFilterChange("onSale", false)}
                    className="ml-1 hover:bg-green-700 rounded-full p-0.5"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              )}
            </div>
          </div>
        )}

        {/* Genres */}
        <div>
          <Label className="text-slate-300 text-sm font-medium mb-3 block">Gêneros</Label>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {availableGenres.map((genre) => (
              <div key={genre} className="flex items-center space-x-2">
                <Checkbox
                  id={`genre-${genre}`}
                  checked={filters.genres.includes(genre)}
                  onCheckedChange={(checked) => handleGenreChange(genre, checked as boolean)}
                  className="border-slate-600 data-[state=checked]:bg-blue-600"
                />
                <Label htmlFor={`genre-${genre}`} className="text-slate-300 text-sm cursor-pointer hover:text-white">
                  {genre}
                </Label>
              </div>
            ))}
          </div>
        </div>

        {/* Price Range */}
        <div>
          <Label className="text-slate-300 text-sm font-medium mb-3 block">
            Preço máximo: {formatPrice(filters.maxPrice)}
          </Label>
          <Slider
            value={[filters.maxPrice]}
            onValueChange={(value) => onFilterChange("maxPrice", value[0])}
            max={400}
            min={0}
            step={10}
            className="w-full"
          />
          <div className="flex justify-between text-xs text-slate-400 mt-1">
            <span>R$ 0</span>
            <span>R$ 400+</span>
          </div>
        </div>

        {/* On Sale */}
        <div>
          <div className="flex items-center space-x-2">
            <Checkbox
              id="on-sale"
              checked={filters.onSale}
              onCheckedChange={(checked) => onFilterChange("onSale", checked as boolean)}
              className="border-slate-600 data-[state=checked]:bg-green-600"
            />
            <Label htmlFor="on-sale" className="text-slate-300 text-sm cursor-pointer hover:text-white">
              Apenas jogos em promoção
            </Label>
          </div>
        </div>

        {/* Developers */}
        <div>
          <Label className="text-slate-300 text-sm font-medium mb-3 block">Desenvolvedores</Label>
          <div className="space-y-2 max-h-32 overflow-y-auto">
            {availableDevelopers.map((developer) => (
              <div key={developer} className="flex items-center space-x-2">
                <Checkbox
                  id={`dev-${developer}`}
                  checked={filters.developers.includes(developer)}
                  onCheckedChange={(checked) => handleDeveloperChange(developer, checked as boolean)}
                  className="border-slate-600 data-[state=checked]:bg-purple-600"
                />
                <Label htmlFor={`dev-${developer}`} className="text-slate-300 text-sm cursor-pointer hover:text-white">
                  {developer}
                </Label>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
