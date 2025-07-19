"use client"

import { useState } from "react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { GameDetailProvider, useGameDetail } from "@/lib/game-detail-context"
import { GameReviews } from "@/components/game-reviews"
import {
  ShoppingCart,
  Heart,
  Star,
  Calendar,
  Globe,
  Download,
  Share2,
  ExternalLink,
  Tag,
  Building,
  Gamepad2,
  Loader2,
  AlertCircle
} from "lucide-react"

// Componentes de carregamento e erro
function LoadingState() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
      <div className="text-center">
        <Loader2 className="h-12 w-12 animate-spin text-blue-400 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-white">Carregando detalhes do jogo...</h2>
        <p className="text-slate-400 mt-2">Por favor, aguarde enquanto buscamos as informações.</p>
      </div>
    </div>
  )
}

function ErrorState({ error }: { error: string }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
      <div className="text-center max-w-md mx-auto">
        <AlertCircle className="h-12 w-12 text-red-400 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-white">Erro ao carregar o jogo</h2>
        <p className="text-slate-400 mt-2">{error}</p>
        <Button className="mt-6 bg-blue-600 hover:bg-blue-700" asChild>
          <Link href="/catalog">Voltar ao Catálogo</Link>
        </Button>
      </div>
    </div>
  )
}

// Componente principal da página de detalhes do jogo
function GameDetailContent() {
  const { game, versions, isLoading, error, selectedVersion, setSelectedVersion, addToWishlist, purchaseGame } = useGameDetail()
  const [isInWishlist, setIsInWishlist] = useState(false)
  const [isInCart, setIsInCart] = useState(false)

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(price)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("pt-BR", {
      year: "numeric",
      month: "long",
      day: "numeric",
    })
  }

  const handleAddToWishlist = async () => {
    if (!game) return
    try {
      await addToWishlist(game.id)
      setIsInWishlist(true)
    } catch (error) {
      console.error("Erro ao adicionar à lista de desejos:", error)
    }
  }

  const handlePurchase = async () => {
    if (!game || !selectedVersion) return
    try {
      await purchaseGame(game.id, selectedVersion.id)
      setIsInCart(true)
    } catch (error) {
      console.error("Erro ao comprar jogo:", error)
    }
  }

  if (isLoading) return <LoadingState />
  if (error) return <ErrorState error={error} />
  if (!game) return <ErrorState error="Jogo não encontrado" />

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Breadcrumb */}
        <Breadcrumb className="mb-6">
          <BreadcrumbList>
            <BreadcrumbItem>
              <BreadcrumbLink href="/" className="text-slate-400 hover:text-white">
                Início
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator className="text-slate-400" />
            <BreadcrumbItem>
              <BreadcrumbLink href="/catalog" className="text-slate-400 hover:text-white">
                Catálogo
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator className="text-slate-400" />
            <BreadcrumbItem>
              <BreadcrumbPage className="text-white">{game.title}</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>

        {/* Cabeçalho do jogo */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* Imagem de capa */}
          <div className="lg:col-span-1">
            <img
              src={game.cover_image}
              alt={game.title}
              className="w-full rounded-lg shadow-2xl"
            />
          </div>

          {/* Informações principais */}
          <div className="lg:col-span-2">
            <h1 className="text-4xl font-bold text-white mb-4">{game.title}</h1>
            
            <div className="flex flex-wrap gap-2 mb-4">
              {game.genre?.map((genre: any) => (
                <Badge key={genre.id} variant="secondary" className="bg-blue-600 text-white">
                  {genre.name}
                </Badge>
              ))}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div className="flex items-center gap-2 text-slate-300">
                <Building className="h-5 w-5" />
                <span>Desenvolvedor: {game.developer?.name}</span>
              </div>
              <div className="flex items-center gap-2 text-slate-300">
                <Building className="h-5 w-5" />
                <span>Publicador: {game.publisher?.name}</span>
              </div>
              <div className="flex items-center gap-2 text-slate-300">
                <Calendar className="h-5 w-5" />
                <span>Lançamento: {formatDate(game.release_date)}</span>
              </div>
              <div className="flex items-center gap-2 text-slate-300">
                <Gamepad2 className="h-5 w-5" />
                <span>Plataforma: PC</span>
              </div>
            </div>

            {/* Preços e botões */}
            <div className="bg-slate-800 rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  {game.discount_percent > 0 ? (
                    <div className="flex items-center gap-2">
                      <Badge className="bg-green-600 text-white">
                        -{game.discount_percent}%
                      </Badge>
                      <span className="text-slate-400 line-through">
                        {formatPrice(Number(game.base_price))}
                      </span>
                      <span className="text-2xl font-bold text-white">
                        {formatPrice(Number(game.discount_price))}
                      </span>
                    </div>
                  ) : (
                    <span className="text-2xl font-bold text-white">
                      {formatPrice(Number(game.base_price))}
                    </span>
                  )}
                </div>
              </div>

              <div className="flex gap-3">
                <Button
                  onClick={handlePurchase}
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white"
                  disabled={isInCart}
                >
                  <ShoppingCart className="h-4 w-4 mr-2" />
                  {isInCart ? "Adicionado ao carrinho" : "Comprar agora"}
                </Button>
                <Button
                  onClick={handleAddToWishlist}
                  variant="outline"
                  className="border-slate-600 text-slate-300 hover:bg-slate-700"
                  disabled={isInWishlist}
                >
                  <Heart className={`h-4 w-4 ${isInWishlist ? "fill-red-500 text-red-500" : ""}`} />
                </Button>
                <Button
                  variant="outline"
                  className="border-slate-600 text-slate-300 hover:bg-slate-700"
                >
                  <Share2 className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Conteúdo em abas */}
        <Tabs defaultValue="about" className="w-full">
          <TabsList className="grid w-full grid-cols-4 bg-slate-800">
            <TabsTrigger value="about" className="text-slate-300 data-[state=active]:text-white">
              Sobre
            </TabsTrigger>
            <TabsTrigger value="versions" className="text-slate-300 data-[state=active]:text-white">
              Versões
            </TabsTrigger>
            <TabsTrigger value="requirements" className="text-slate-300 data-[state=active]:text-white">
              Requisitos
            </TabsTrigger>
            <TabsTrigger value="reviews" className="text-slate-300 data-[state=active]:text-white">
              Avaliações
            </TabsTrigger>
          </TabsList>

          <TabsContent value="about" className="mt-6">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Sobre o jogo</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-slate-300 leading-relaxed">
                  {game.description}
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="versions" className="mt-6">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Versões disponíveis</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {versions.map((version: any) => (
                    <div
                      key={version.id}
                      className={`p-4 rounded-lg border cursor-pointer transition-colors ${
                        selectedVersion?.id === version.id
                          ? "border-blue-500 bg-blue-900/20"
                          : "border-slate-600 hover:border-slate-500"
                      }`}
                      onClick={() => setSelectedVersion(version)}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="text-white font-semibold">{version.version_number}</h3>
                          <p className="text-slate-400 text-sm">
                            Lançado em {formatDate(version.release_date)}
                          </p>
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge variant="outline" className="border-slate-600 text-slate-300">
                            {version.size_mb} MB
                          </Badge>
                          <Button size="sm" variant="outline" className="border-slate-600 text-slate-300">
                            <Download className="h-4 w-4 mr-1" />
                            Download
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="requirements" className="mt-6">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Requisitos do sistema</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-white font-semibold mb-3">Requisitos mínimos</h3>
                    <div className="space-y-2 text-slate-300">
                      <p><strong>SO:</strong> Windows 10 64-bit</p>
                      <p><strong>Processador:</strong> Intel Core i5-4590 / AMD FX 8350</p>
                      <p><strong>Memória:</strong> 8 GB RAM</p>
                      <p><strong>Placa de vídeo:</strong> NVIDIA GTX 1060 / AMD RX 580</p>
                      <p><strong>DirectX:</strong> Versão 11</p>
                      <p><strong>Armazenamento:</strong> 25 GB de espaço disponível</p>
                    </div>
                  </div>
                  <div>
                    <h3 className="text-white font-semibold mb-3">Requisitos recomendados</h3>
                    <div className="space-y-2 text-slate-300">
                      <p><strong>SO:</strong> Windows 11 64-bit</p>
                      <p><strong>Processador:</strong> Intel Core i7-9700K / AMD Ryzen 7 3700X</p>
                      <p><strong>Memória:</strong> 16 GB RAM</p>
                      <p><strong>Placa de vídeo:</strong> NVIDIA RTX 3070 / AMD RX 6700 XT</p>
                      <p><strong>DirectX:</strong> Versão 12</p>
                      <p><strong>Armazenamento:</strong> 50 GB de espaço disponível (SSD recomendado)</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="reviews" className="mt-6">
            <GameReviews gameId={Number(game.id)} gameName={game.title} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

// Componente wrapper com provider
export default function GameDetailPage({ params }: { params: { slug: string } }) {
  console.log('params:', params); // Veja o que aparece no console
  return (
    <GameDetailProvider slug={params.slug}>
      <GameDetailContent />
    </GameDetailProvider>
  )
}
