import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Info, Heart, ShoppingCart } from "lucide-react"
import Image from "next/image"
import { Game } from "@/lib/catalog-service"
import { useCatalog } from "@/lib/catalog-context"
import { useState } from "react"
import Link from "next/link"

interface GameCardProps {
  game: Game
  viewMode: "grid" | "list"
}

export function GameCard({ game, viewMode }: GameCardProps) {
  const { addToWishlist, purchaseGame } = useCatalog();
  const [isAddingToWishlist, setIsAddingToWishlist] = useState(false);
  const [isPurchasing, setIsPurchasing] = useState(false);
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(price)
  }

  if (viewMode === "list") {
    return (
      <Card className="bg-slate-800/50 border-slate-700 hover:bg-slate-800/70 transition-all duration-300 group">
        <CardContent className="p-4">
          <div className="flex gap-4">
            <div className="relative w-32 h-20 flex-shrink-0">
              {game.discount > 0 && (
                <Badge className="absolute -top-2 -right-2 z-10 bg-green-600 hover:bg-green-600">
                  -{game.discount}%
                </Badge>
              )}
              <Image src={game.image || "/placeholder.svg"} alt={game.title} fill className="object-cover rounded" />
            </div>

            <div className="flex-1 flex justify-between items-center">
              <div>
                <h3 className="text-lg font-semibold text-white mb-1 group-hover:text-blue-300 transition-colors">
                  {game.title}
                </h3>
                <p className="text-sm text-slate-400 mb-2">{game.developer}</p>
                <div className="flex gap-1 flex-wrap">
                  {game.genre.map((g) => (
                    <Badge key={g} variant="secondary" className="text-xs bg-slate-700 text-slate-300">
                      {g}
                    </Badge>
                  ))}
                </div>
              </div>

              <div className="text-right">
                <div className="mb-2">
                  {game.originalPrice && (
                    <span className="text-sm text-slate-500 line-through block">{formatPrice(game.originalPrice)}</span>
                  )}
                  <span className={`text-lg font-bold ${game.onSale ? "text-green-400" : "text-white"}`}>
                    {formatPrice(game.price)}
                  </span>
                </div>

                <div className="flex gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    className="border-slate-600 text-slate-300 hover:bg-slate-700 bg-transparent"
                    onClick={async () => {
                      try {
                        setIsAddingToWishlist(true);
                        await addToWishlist(game.id);
                      } catch (error) {
                        console.error('Erro ao adicionar à lista de desejos:', error);
                      } finally {
                        setIsAddingToWishlist(false);
                      }
                    }}
                    disabled={isAddingToWishlist}
                  >
                    <Heart className="h-4 w-4" />
                  </Button>
                  <Link href={`/catalog/${game.id}`}>
                    <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                      <Info className="h-4 w-4 mr-1" />
                      Detalhes
                    </Button>
                  </Link>
                  <Button
                    size="sm"
                    className="bg-green-600 hover:bg-green-700"
                    onClick={async () => {
                      try {
                        setIsPurchasing(true);
                        await purchaseGame(game.id);
                      } catch (error) {
                        console.error('Erro ao comprar jogo:', error);
                      } finally {
                        setIsPurchasing(false);
                      }
                    }}
                    disabled={isPurchasing}
                  >
                    <ShoppingCart className="h-4 w-4 mr-1" />
                    Comprar
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="bg-slate-800/50 border-slate-700 hover:bg-slate-800/70 transition-all duration-300 hover:scale-105 group overflow-hidden">
      <div className="relative">
        {game.discount > 0 && (
          <Badge className="absolute top-2 right-2 z-10 bg-green-600 hover:bg-green-600">-{game.discount}%</Badge>
        )}
        <div className="relative h-48 w-full">
          <Image
            src={game.image || "/placeholder.svg"}
            alt={game.title}
            fill
            className="object-cover group-hover:scale-110 transition-transform duration-300"
          />
        </div>
      </div>

      <CardContent className="p-4">
        <h3 className="text-lg font-semibold text-white mb-2 truncate group-hover:text-blue-300 transition-colors">
          {game.title}
        </h3>
        <p className="text-sm text-slate-400 mb-2">{game.developer}</p>

        <div className="flex justify-between items-end">
          <div>
            {game.originalPrice && (
              <span className="text-sm text-slate-500 line-through block">{formatPrice(game.originalPrice)}</span>
            )}
            <span className={`text-lg font-bold ${game.onSale ? "text-green-400" : "text-white"}`}>
              {formatPrice(game.price)}
            </span>
          </div>

          <div className="flex gap-2">
            <Button
              size="sm"
              variant="outline"
              className="border-slate-600 text-slate-300 hover:bg-slate-700 bg-transparent"
              onClick={async () => {
                try {
                  setIsAddingToWishlist(true);
                  await addToWishlist(game.id);
                } catch (error) {
                  console.error('Erro ao adicionar à lista de desejos:', error);
                } finally {
                  setIsAddingToWishlist(false);
                }
              }}
              disabled={isAddingToWishlist}
            >
              <Heart className="h-4 w-4" />
            </Button>
            <Link href={`/catalog/${game.id}`}>
              <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                Detalhes
              </Button>
            </Link>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
