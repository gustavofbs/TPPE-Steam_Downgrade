import Link from "next/link"
import { Gamepad2, ChevronRight, Facebook, Twitter, MessageCircle, Github } from "lucide-react"

export function Footer() {
  const quickLinks = [
    { href: "/about", label: "Sobre nós" },
    { href: "/terms", label: "Termos de uso" },
    { href: "/privacy", label: "Política de privacidade" },
    { href: "/contact", label: "Contato" },
  ]

  const socialLinks = [
    { href: "#", icon: Facebook, label: "Facebook" },
    { href: "#", icon: Twitter, label: "Twitter" },
    { href: "#", icon: MessageCircle, label: "Discord" },
    { href: "#", icon: Github, label: "GitHub" },
  ]

  return (
    <footer className="bg-slate-900/90 border-t border-slate-700 mt-auto">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand Section */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Gamepad2 className="h-8 w-8 text-blue-400" />
              <h3 className="text-xl font-bold text-white">SteamRF</h3>
            </div>
            <p className="text-slate-400 leading-relaxed">
              Plataforma de jogos digitais com foco em funcionalidades de downgrade de jogos.
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Links Rápidos</h3>
            <ul className="space-y-2">
              {quickLinks.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="flex items-center text-slate-400 hover:text-blue-300 transition-colors group"
                  >
                    <ChevronRight className="h-4 w-4 mr-2 group-hover:translate-x-1 transition-transform" />
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Social Links */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Conecte-se</h3>
            <div className="flex space-x-4">
              {socialLinks.map((social) => {
                const Icon = social.icon
                return (
                  <Link
                    key={social.label}
                    href={social.href}
                    className="p-3 bg-slate-800 hover:bg-slate-700 rounded-lg text-slate-400 hover:text-blue-300 transition-all duration-200 hover:scale-110"
                    aria-label={social.label}
                  >
                    <Icon className="h-5 w-5" />
                  </Link>
                )
              })}
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-slate-700 mt-8 pt-8">
          <div className="text-center text-slate-400">
            <p>&copy; 2025 SteamRF. Todos os direitos reservados.</p>
          </div>
        </div>
      </div>
    </footer>
  )
}
