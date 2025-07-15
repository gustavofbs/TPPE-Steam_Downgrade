"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Gamepad2, LogIn, User, Lock, Key, UserPlus, Eye, EyeOff, XCircle } from "lucide-react"
import { useAuth } from "@/lib/auth-context"

export default function LoginPage() {
  const { login, isLoading: authLoading } = useAuth()
  const router = useRouter()
  
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    rememberMe: false,
  })
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [errors, setErrors] = useState<{ [key: string]: string }>({})

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }))
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setErrors({})

    // Basic validation
    const newErrors: { [key: string]: string } = {}
    if (!formData.username.trim()) {
      newErrors.username = "Nome de usuário é obrigatório"
    }
    if (!formData.password) {
      newErrors.password = "Senha é obrigatória"
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      setIsLoading(false)
      return
    }

    // Call login from auth context
    try {
      await login(formData.username, formData.password)
      // Redirect to home page after successful login
      router.push('/')
    } catch (error: any) {
      setErrors({ 
        general: error.message || "Erro ao fazer login. Verifique suas credenciais e tente novamente." 
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center space-x-2">
            <Gamepad2 className="h-12 w-12 text-blue-400" />
            <h1 className="text-4xl font-bold text-white">SteamRF</h1>
          </div>
          <p className="text-slate-400 text-lg">Acesse sua conta para gerenciar seus jogos e versões</p>
        </div>

        {/* Login Card */}
        <Card className="card-steam shadow-2xl">
          <CardHeader className="space-y-1 pb-6">
            <CardTitle className="text-2xl font-bold text-center text-white flex items-center justify-center space-x-2">
              <LogIn className="h-6 w-6 text-blue-400" />
              <span>Entrar</span>
            </CardTitle>
          </CardHeader>

          <CardContent className="space-y-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* General Error */}
              {errors.general && (
                <div className="p-3 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm">
                  {errors.general}
                </div>
              )}

              {/* Username Field */}
              <div className="space-y-2">
                <Label htmlFor="username" className="text-slate-300 flex items-center space-x-1">
                  <User className="h-4 w-4" />
                  <span>Nome de usuário</span>
                </Label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
                  <Input
                    id="username"
                    name="username"
                    type="text"
                    value={formData.username}
                    onChange={handleInputChange}
                    className={`pl-10 input-steam ${errors.username ? "border-red-500 focus:border-red-500" : ""}`}
                    placeholder="Digite seu nome de usuário"
                    disabled={isLoading}
                  />
                </div>
                {errors.username && (
                  <p className="text-red-400 text-sm flex items-center space-x-1">
                    <XCircle className="h-4 w-4" />
                    <span>{errors.username}</span>
                  </p>
                )}
              </div>

              {/* Password Field */}
              <div className="space-y-2">
                <Label htmlFor="password" className="text-slate-300 flex items-center space-x-1">
                  <Lock className="h-4 w-4" />
                  <span>Senha</span>
                </Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
                  <Input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    value={formData.password}
                    onChange={handleInputChange}
                    className={`pl-10 pr-10 input-steam ${errors.password ? "border-red-500 focus:border-red-500" : ""}`}
                    placeholder="Digite sua senha"
                    disabled={isLoading}
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="absolute right-2 top-1/2 transform -translate-y-1/2 h-6 w-6 p-0 hover:bg-transparent"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4 text-slate-400" />
                    ) : (
                      <Eye className="h-4 w-4 text-slate-400" />
                    )}
                  </Button>
                </div>
                {errors.password && (
                  <p className="text-red-400 text-sm flex items-center space-x-1">
                    <XCircle className="h-4 w-4" />
                    <span>{errors.password}</span>
                  </p>
                )}
              </div>

              {/* Remember Me */}
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="rememberMe"
                  checked={formData.rememberMe}
                  onCheckedChange={(checked) => setFormData((prev) => ({ ...prev, rememberMe: checked as boolean }))}
                  className="border-slate-600 data-[state=checked]:bg-blue-600"
                />
                <Label htmlFor="rememberMe" className="text-slate-300 text-sm cursor-pointer">
                  Lembrar de mim
                </Label>
              </div>

              {/* Submit Button */}
              <Button type="submit" className="w-full btn-steam text-lg py-6" disabled={isLoading || authLoading}>
                {(isLoading || authLoading) ? (
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Entrando...</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-2">
                    <LogIn className="h-5 w-5" />
                    <span>Entrar</span>
                  </div>
                )}
              </Button>
            </form>
          </CardContent>

          <CardFooter className="flex flex-col space-y-4 pt-6">
            <div className="text-center">
              <Link
                href="/forgot-password"
                className="text-blue-400 hover:text-blue-300 transition-colors flex items-center justify-center space-x-1"
              >
                <Key className="h-4 w-4" />
                <span>Esqueceu sua senha?</span>
              </Link>
            </div>

            <div className="text-center text-slate-400">
              Não tem uma conta?{" "}
              <Link
                href="/register"
                className="text-blue-400 hover:text-blue-300 font-semibold transition-colors inline-flex items-center space-x-1"
              >
                <UserPlus className="h-4 w-4" />
                <span>Registrar-se</span>
              </Link>
            </div>
          </CardFooter>
        </Card>

        {/* Footer */}
        <div className="text-center">
          <p className="text-slate-500 text-sm">© 2025 SteamRF. Todos os direitos reservados.</p>
        </div>
      </div>
    </div>
  )
}
