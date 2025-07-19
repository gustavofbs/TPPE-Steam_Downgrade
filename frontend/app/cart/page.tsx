"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { CartItem } from "@/components/cart-item"
import { ShoppingCart, Tag, Trash2, CreditCard } from "lucide-react"
import Link from "next/link"
import { useCart } from "@/lib/cart-context"
import { CartAPI } from "@/lib/cart-api"



export default function CartPage() {
  const {
    cart,
    isLoading,
    appliedCoupon,
    updateQuantity,
    removeFromCart,
    clearCart,
    applyCoupon,
    removeCoupon,
    getTotalItems,
    getSubtotal,
    getDiscountAmount,
    getFinalTotal,
  } = useCart()
  
  const [couponCode, setCouponCode] = useState("")
  const [isApplyingCoupon, setIsApplyingCoupon] = useState(false)
  const [isClearingCart, setIsClearingCart] = useState(false)

  // Dados calculados do contexto
  const totalItems = getTotalItems()
  const subtotal = getSubtotal()
  const discountAmount = getDiscountAmount()
  const finalTotal = getFinalTotal()

  const handleQuantityChange = async (gameId: number, newQuantity: number) => {
    try {
      await updateQuantity(gameId, newQuantity)
    } catch (error) {
      console.error("Erro ao atualizar quantidade:", error)
      alert("Erro ao atualizar quantidade. Tente novamente.")
    }
  }

  const handleRemoveItem = async (gameId: number) => {
    try {
      await removeFromCart(gameId)
    } catch (error) {
      console.error("Erro ao remover item:", error)
      alert("Erro ao remover item. Tente novamente.")
    }
  }

  const handleApplyCoupon = async () => {
    if (!couponCode.trim()) return

    setIsApplyingCoupon(true)
    try {
      await applyCoupon(couponCode)
      setCouponCode("")
    } catch (error) {
      console.error("Erro ao aplicar cupom:", error)
      alert(error instanceof Error ? error.message : "Cupom inválido!")
    } finally {
      setIsApplyingCoupon(false)
    }
  }

  const handleClearCart = async () => {
    setIsClearingCart(true)
    try {
      await clearCart()
    } catch (error) {
      console.error("Erro ao limpar carrinho:", error)
      alert("Erro ao limpar carrinho. Tente novamente.")
    } finally {
      setIsClearingCart(false)
    }
  }

  const handleRemoveCoupon = () => {
    removeCoupon()
  }

  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-center min-h-[400px]">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
          </div>
        </div>
      </div>
    )
  }

  if (!cart || cart.items.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-4">
              <ShoppingCart className="h-8 w-8 text-blue-400" />
              <h1 className="text-4xl font-bold text-white">Carrinho de Compras</h1>
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
                  <BreadcrumbPage className="text-slate-300">Carrinho</BreadcrumbPage>
                </BreadcrumbItem>
              </BreadcrumbList>
            </Breadcrumb>
          </div>

          {/* Empty Cart */}
          <Card className="card-steam">
            <CardContent className="p-12 text-center">
              <ShoppingCart className="h-24 w-24 text-slate-600 mx-auto mb-6" />
              <h2 className="text-2xl font-bold text-white mb-4">Seu carrinho está vazio</h2>
              <p className="text-slate-400 mb-8">Adicione alguns jogos incríveis ao seu carrinho para começar!</p>
              <Link href="/catalog">
                <Button className="btn-steam text-lg px-8 py-3">
                  <ShoppingCart className="mr-2 h-5 w-5" />
                  Explorar Jogos
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <ShoppingCart className="h-8 w-8 text-blue-400" />
              <h1 className="text-4xl font-bold text-white">Carrinho de Compras</h1>
            </div>
            <Button
              variant="outline"
              onClick={handleClearCart}
              disabled={isClearingCart}
              className="border-red-600 text-red-400 hover:bg-red-600 hover:text-white bg-transparent"
            >
              {isClearingCart ? (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current mr-2" />
              ) : (
                <Trash2 className="h-4 w-4 mr-2" />
              )}
              Limpar Carrinho
            </Button>
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
                <BreadcrumbPage className="text-slate-300">Carrinho</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2 space-y-4">
            <Card className="card-steam">
              <CardHeader>
                <CardTitle className="text-white">
                  Itens no Carrinho ({totalItems} {totalItems === 1 ? "item" : "itens"})
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {cart.items.map((item) => (
                  <CartItem
                    key={item.id}
                    item={item}
                    onQuantityChange={handleQuantityChange}
                    onRemove={handleRemoveItem}
                  />
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Order Summary */}
          <div className="space-y-6">
            {/* Coupon Section */}
            <Card className="card-steam">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Tag className="h-5 w-5 text-green-400" />
                  Cupom de Desconto
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {appliedCoupon ? (
                  <div className="p-3 bg-green-600/20 border border-green-600/50 rounded-lg">
                    <div className="flex items-center justify-between">
                      <div>
                        <Badge className="bg-green-600 hover:bg-green-600 mb-2">{appliedCoupon.code}</Badge>
                        <p className="text-sm text-green-400">
                          Desconto de {appliedCoupon.discount_percent}% aplicado!
                        </p>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={handleRemoveCoupon}
                        className="text-green-400 hover:text-green-300"
                      >
                        Remover
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="flex gap-2">
                    <Input
                      placeholder="Digite o código do cupom"
                      value={couponCode}
                      onChange={(e) => setCouponCode(e.target.value)}
                      className="input-steam"
                      onKeyPress={(e) => e.key === "Enter" && handleApplyCoupon()}
                    />
                    <Button
                      onClick={handleApplyCoupon}
                      disabled={isApplyingCoupon || !couponCode.trim()}
                      className="btn-steam"
                    >
                      {isApplyingCoupon ? (
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                      ) : (
                        "Aplicar"
                      )}
                    </Button>
                  </div>
                )}
                <div className="text-xs text-slate-400">Cupons disponíveis para teste: SAVE10, WELCOME20, STEAM50</div>
              </CardContent>
            </Card>

            {/* Order Summary */}
            <Card className="card-steam">
              <CardHeader>
                <CardTitle className="text-white">Resumo do Pedido</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex justify-between text-slate-300">
                    <span>Subtotal ({totalItems} itens):</span>
                    <span>{CartAPI.formatPrice(subtotal)}</span>
                  </div>

                  {appliedCoupon && (
                    <div className="flex justify-between text-green-400">
                      <span>Desconto ({appliedCoupon.code}):</span>
                      <span>-{CartAPI.formatPrice(discountAmount)}</span>
                    </div>
                  )}

                  <Separator className="bg-slate-700" />

                  <div className="flex justify-between text-xl font-bold text-white">
                    <span>Total:</span>
                    <span className="text-green-400">{CartAPI.formatPrice(finalTotal)}</span>
                  </div>
                </div>

                <Link href="/checkout">
                  <Button className="w-full btn-steam text-lg py-6">
                    <CreditCard className="mr-2 h-5 w-5" />
                    Prosseguir para Checkout
                  </Button>
                </Link>

                <div className="text-center">
                  <Link href="/catalog" className="text-blue-400 hover:text-blue-300 text-sm">
                    ← Continuar Comprando
                  </Link>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
