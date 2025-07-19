"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Filter, X } from "lucide-react"

interface Filters {
  genres: number[];
  developers: number[];
  maxPrice: number;
  minPrice: number;
  onSale: boolean;
  search: string;
}

interface GenreOrDev {
  id: number;
  name: string;
}

interface FilterSidebarProps {
  filters: Filters;
  availableGenres?: GenreOrDev[];
  availableDevelopers?: GenreOrDev[];
  onFilterChange: (key: keyof Filters, value: any) => void;
  onClearFilters: () => void;
}

// Gêneros e desenvolvedores agora são fornecidos como props

export function FilterSidebar({ 
  filters, 
  availableGenres = [], 
  availableDevelopers = [], 
  onFilterChange, 
  onClearFilters 
}: FilterSidebarProps) {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(price)
  }

  const handleGenreChange = (genreId: number, checked: boolean) => {
    const newGenres = checked
      ? [...filters.genres, genreId]
      : filters.genres.filter((g) => g !== genreId);
    onFilterChange("genres", newGenres);
  };

  const handleDeveloperChange = (devId: number, checked: boolean) => {
    const newDevelopers = checked
      ? [...filters.developers, devId]
      : filters.developers.filter((d) => d !== devId);
    onFilterChange("developers", newDevelopers);
  }

  const hasActiveFilters =
    filters.genres.length > 0 ||
    filters.developers.length > 0 ||
    filters.maxPrice < 400 ||
    filters.minPrice > 0 ||
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
              {filters.genres.map((genreId) => {
                const genreObj = availableGenres.find(g => g.id === genreId);
                return genreObj ? (
                  <Badge key={genreId} variant="secondary" className="bg-blue-600 text-white">
                    {genreObj.name}
                    <button
                      onClick={() => handleGenreChange(genreId, false)}
                      className="ml-1 hover:bg-blue-700 rounded-full p-0.5"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </Badge>
                ) : null;
              })} 
              {filters.developers.map((devId) => {
                const devObj = availableDevelopers.find(d => d.id === devId);
                return devObj ? (
                  <Badge key={devId} variant="secondary" className="bg-purple-600 text-white">
                    {devObj.name}
                    <button
                      onClick={() => handleDeveloperChange(devId, false)}
                      className="ml-1 hover:bg-purple-700 rounded-full p-0.5"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </Badge>
                ) : null;
              })} 
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
              <div key={genre.id} className="flex items-center space-x-2">
                <Checkbox
                  id={`genre-${genre.id}`}
                  checked={filters.genres.includes(genre.id)}
                  onCheckedChange={(checked) => handleGenreChange(genre.id, checked as boolean)}
                  className="border-slate-600 data-[state=checked]:bg-blue-600"
                />
                <Label htmlFor={`genre-${genre.id}`} className="text-slate-300 text-sm cursor-pointer hover:text-white">
                  {genre.name}
                </Label>
              </div>
            ))}
          </div>
        </div>

        {/* Price Range */}
        <div>
          <Label className="text-slate-300 text-sm font-medium mb-3 block">
            Faixa de Preço
          </Label>
          <div className="space-y-3">
            <div>
              <Label htmlFor="min-price" className="text-slate-400 text-xs mb-1 block">
                Preço Mínimo
              </Label>
              <Input
                id="min-price"
                type="number"
                placeholder="0"
                value={filters.minPrice}
                onChange={(e) => {
                  const value = e.target.value === "" ? 0 : Number(e.target.value);
                  onFilterChange("minPrice", value);
                }}
                className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-400"
                min="0"
                step="10"
              />
            </div>
            <div>
              <Label htmlFor="max-price" className="text-slate-400 text-xs mb-1 block">
                Preço Máximo
              </Label>
              <Input
                id="max-price"
                type="number"
                placeholder="400"
                value={filters.maxPrice === 400 ? "" : filters.maxPrice}
                onChange={(e) => onFilterChange("maxPrice", Number(e.target.value) || 400)}
                className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-400"
                min="0"
                step="10"
              />
            </div>
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
            {availableDevelopers.map((dev) => (
              <div key={dev.id} className="flex items-center space-x-2">
                <Checkbox
                  id={`dev-${dev.id}`}
                  checked={filters.developers.includes(dev.id)}
                  onCheckedChange={(checked) => handleDeveloperChange(dev.id, checked as boolean)}
                  className="border-slate-600 data-[state=checked]:bg-purple-600"
                />
                <Label htmlFor={`dev-${dev.id}`} className="text-slate-300 text-sm cursor-pointer hover:text-white">
                  {dev.name}
                </Label>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
