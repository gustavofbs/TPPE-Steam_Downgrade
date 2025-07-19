"use client"

import { useState } from "react"
import Link from "next/link"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Minus, Plus, Trash2, ExternalLink } from "lucide-react"
import Image from "next/image"
import { CartItem as CartItemType } from "@/lib/cart-api"
import { CartAPI } from "@/lib/cart-api"

interface CartItemProps {
  item: CartItemType
  onQuantityChange: (gameId: number, newQuantity: number) => Promise<void>
  onRemove: (gameId: number) => Promise<void>
}

export function CartItem({ item, onQuantityChange, onRemove }: CartItemProps) {
  const [isUpdating, setIsUpdating] = useState(false)
  const [isRemoving, setIsRemoving] = useState(false)

  const handleQuantityChange = async (newQuantity: number) => {
    if (newQuantity < 1) return
    setIsUpdating(true)
    try {
      await onQuantityChange(item.game_id, newQuantity)
    } catch (error) {
      console.error('Erro ao atualizar quantidade:', error)
    } finally {
      setIsUpdating(false)
    }
  }

  const handleRemove = async () => {
    setIsRemoving(true)
    try {
      await onRemove(item.game_id)
    } catch (error) {
      console.error('Erro ao remover item:', error)
    } finally {
      setIsRemoving(false)
    }
  }

  // Parse preços do backend (strings) para números
  const basePrice = parseFloat(item.game.base_price)
  const currentPrice = parseFloat(item.game.current_price || item.game.base_price)
  const unitPrice = parseFloat(item.unit_price)
  const subtotal = parseFloat(item.subtotal)

  return (
    <Card className="card-steam hover:bg-slate-800/70 transition-all duration-300">
      <CardContent className="p-4">
        <div className="flex gap-4">
          {/* Game Image */}
          <div className="relative w-24 h-32 flex-shrink-0">
            {item.game.discount_percent > 0 && (
              <Badge className="absolute -top-2 -right-2 z-10 bg-green-600 hover:bg-green-600 text-xs">
                -{item.game.discount_percent}%
              </Badge>
            )}
            <Link href={`/games/${item.game.slug}`}>
              <Image
                src={item.game.cover_image || "/placeholder.svg"}
                alt={item.game.title}
                fill
                className="object-cover rounded cursor-pointer hover:scale-105 transition-transform"
              />
            </Link>
          </div>

          {/* Game Info */}
          <div className="flex-1 space-y-2">
            <div className="flex items-start justify-between">
              <div>
                <Link href={`/games/${item.game.slug}`}>
                  <h3 className="text-lg font-semibold text-white hover:text-blue-300 transition-colors cursor-pointer flex items-center gap-2">
                    {item.game.title}
                    <ExternalLink className="h-4 w-4" />
                  </h3>
                </Link>
                <p className="text-sm text-slate-400">{item.game.developer_name}</p>
              </div>

              <Button
                variant="ghost"
                size="sm"
                onClick={handleRemove}
                disabled={isRemoving}
                className="text-red-400 hover:text-red-300 hover:bg-red-600/20"
              >
                {isRemoving ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current" />
                ) : (
                  <Trash2 className="h-4 w-4" />
                )}
              </Button>
            </div>

            {/* Price Info */}
            <div className="space-y-1">
              {basePrice > currentPrice && (
                <div className="flex items-center gap-2">
                  <span className="text-sm text-slate-500 line-through">{CartAPI.formatPrice(basePrice)}</span>
                  <Badge className="bg-green-600 hover:bg-green-600 text-xs">-{item.game.discount_percent}% OFF</Badge>
                </div>
              )}
              <div className="text-lg font-bold text-green-400">{CartAPI.formatPrice(unitPrice)}</div>
            </div>

            {/* Quantity Controls */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-sm text-slate-300">Quantidade:</span>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleQuantityChange(item.quantity - 1)}
                    disabled={isUpdating || item.quantity <= 1}
                    className="h-8 w-8 p-0 border-slate-600 bg-transparent"
                  >
                    <Minus className="h-4 w-4" />
                  </Button>

                  <Input
                    type="number"
                    min="1"
                    max="10"
                    value={item.quantity}
                    onChange={(e) => handleQuantityChange(Number(e.target.value))}
                    className="w-16 h-8 text-center input-steam"
                    disabled={isUpdating}
                  />

                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleQuantityChange(item.quantity + 1)}
                    disabled={isUpdating || item.quantity >= 10}
                    className="h-8 w-8 p-0 border-slate-600 bg-transparent"
                  >
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              {/* Subtotal */}
              <div className="text-right">
                <div className="text-sm text-slate-400">Subtotal:</div>
                <div className="text-xl font-bold text-white">{CartAPI.formatPrice(subtotal)}</div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
