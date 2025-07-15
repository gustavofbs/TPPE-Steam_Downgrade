import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Gamepad2, Store, Library, Heart, TrendingUp } from "lucide-react"

export default function HomePage() {
  const features = [
    {
      icon: Store,
      title: "Loja Completa",
      description: "Milhares de jogos disponíveis com os melhores preços",
    },
    {
      icon: Library,
      title: "Biblioteca Pessoal",
      description: "Organize e gerencie todos os seus jogos em um só lugar",
    },
    {
      icon: Heart,
      title: "Lista de Desejos",
      description: "Salve seus jogos favoritos e receba notificações de promoções",
    },
    {
      icon: TrendingUp,
      title: "Downgrade de Versões",
      description: "Funcionalidade exclusiva para reverter versões de jogos",
    },
  ]

  return (
    <div className="container mx-auto px-4 py-12">
      {/* Hero Section */}
      <div className="text-center space-y-8 mb-16">
        <div className="space-y-4">
          <h1 className="text-5xl md:text-7xl font-bold text-white">
            Bem-vindo ao <span className="text-blue-400">SteamRF</span>
          </h1>
          <p className="text-xl text-slate-400 max-w-2xl mx-auto">
            A plataforma definitiva para jogos digitais com funcionalidades exclusivas de downgrade e gerenciamento
            avançado
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button asChild size="lg" className="btn-steam text-lg px-8 py-6">
            <Link href="/catalog">
              <Store className="mr-2 h-5 w-5" />
              Explorar Loja
            </Link>
          </Button>
          <Button
            asChild
            variant="outline"
            size="lg"
            className="border-slate-600 text-slate-300 hover:bg-slate-700 text-lg px-8 py-6 bg-transparent"
          >
            <Link href="/register">
              <Gamepad2 className="mr-2 h-5 w-5" />
              Criar Conta
            </Link>
          </Button>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {features.map((feature, index) => {
          const Icon = feature.icon
          return (
            <Card key={index} className="card-steam hover:bg-slate-800/70 transition-all duration-300 group">
              <CardContent className="p-6 text-center space-y-4">
                <div className="mx-auto w-16 h-16 bg-blue-600/20 rounded-full flex items-center justify-center group-hover:bg-blue-600/30 transition-colors">
                  <Icon className="h-8 w-8 text-blue-400" />
                </div>
                <h3 className="text-xl font-semibold text-white">{feature.title}</h3>
                <p className="text-slate-400">{feature.description}</p>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
