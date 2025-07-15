"use client"

import type React from "react"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Progress } from "@/components/ui/progress"
import { Gamepad2, UserPlus, User, Mail, Lock, Eye, EyeOff, XCircle, CheckCircle, LogIn, Info } from "lucide-react"

interface FormData {
  username: string
  email: string
  password: string
  confirmPassword: string
  acceptTerms: boolean
}

interface FormErrors {
  [key: string]: string
}

interface PasswordStrength {
  score: number
  feedback: string[]
  color: string
}

export default function RegisterPage() {
  const [formData, setFormData] = useState<FormData>({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    acceptTerms: false,
  })

  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [errors, setErrors] = useState<FormErrors>({})
  const [passwordStrength, setPasswordStrength] = useState<PasswordStrength>({
    score: 0,
    feedback: [],
    color: "bg-red-500",
  })

  // Password strength calculation
  const calculatePasswordStrength = (password: string): PasswordStrength => {
    let score = 0
    const feedback: string[] = []

    if (password.length >= 8) {
      score += 25
    } else {
      feedback.push("Pelo menos 8 caracteres")
    }

    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) {
      score += 25
    } else {
      feedback.push("Letras maiúsculas e minúsculas")
    }

    if (/\d/.test(password)) {
      score += 25
    } else {
      feedback.push("Pelo menos um número")
    }

    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      score += 25
    } else {
      feedback.push("Pelo menos um caractere especial")
    }

    let color = "bg-red-500"
    if (score >= 75) color = "bg-green-500"
    else if (score >= 50) color = "bg-yellow-500"
    else if (score >= 25) color = "bg-orange-500"

    return { score, feedback, color }
  }

  useEffect(() => {
    if (formData.password) {
      setPasswordStrength(calculatePasswordStrength(formData.password))
    } else {
      setPasswordStrength({ score: 0, feedback: [], color: "bg-red-500" })
    }
  }, [formData.password])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }))
    }
  }

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {}

    // Username validation
    if (!formData.username.trim()) {
      newErrors.username = "Nome de usuário é obrigatório"
    } else if (formData.username.length < 3) {
      newErrors.username = "Nome de usuário deve ter pelo menos 3 caracteres"
    } else if (!/^[a-zA-Z0-9_]+$/.test(formData.username)) {
      newErrors.username = "Nome de usuário pode conter apenas letras, números e underscore"
    }

    // Email validation
    if (!formData.email.trim()) {
      newErrors.email = "Email é obrigatório"
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Email inválido"
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = "Senha é obrigatória"
    } else if (passwordStrength.score < 50) {
      newErrors.password = "Senha muito fraca"
    }

    // Confirm password validation
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = "Confirmação de senha é obrigatória"
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Senhas não coincidem"
    }

    // Terms validation
    if (!formData.acceptTerms) {
      newErrors.acceptTerms = "Você deve aceitar os termos de serviço"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()

  if (!validateForm()) return
  setIsLoading(true)

  try {
    const response = await fetch("http://localhost:8000/api/v1/users/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        password2: formData.confirmPassword,
        first_name: "", // se quiser permitir no formulário depois
        last_name: ""
      }),
    })

    if (!response.ok) {
      const data = await response.json()
      console.error("Erro na criação:", data)
      throw new Error("Erro ao criar conta.")
    }

    console.log("Usuário criado com sucesso:", await response.json())
    // Aqui você pode redirecionar para login, ou logar direto
  } catch (error) {
    console.error(error)
    setErrors({ general: "Erro ao criar conta. Tente novamente." })
  } finally {
    setIsLoading(false)
  }
}


  const getStrengthText = (score: number): string => {
    if (score >= 75) return "Forte"
    if (score >= 50) return "Média"
    if (score >= 25) return "Fraca"
    return "Muito fraca"
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-lg space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center space-x-2">
            <Gamepad2 className="h-12 w-12 text-blue-400" />
            <h1 className="text-4xl font-bold text-white">SteamRF</h1>
          </div>
          <p className="text-slate-400 text-lg">Crie sua conta para acessar o sistema de downgrade de jogos</p>
        </div>

        {/* Register Card */}
        <Card className="card-steam shadow-2xl">
          <CardHeader className="space-y-1 pb-6">
            <CardTitle className="text-2xl font-bold text-center text-white flex items-center justify-center space-x-2">
              <UserPlus className="h-6 w-6 text-blue-400" />
              <span>Criar Conta</span>
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

              {/* Email Field */}
              <div className="space-y-2">
                <Label htmlFor="email" className="text-slate-300 flex items-center space-x-1">
                  <Mail className="h-4 w-4" />
                  <span>Email</span>
                </Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className={`pl-10 input-steam ${errors.email ? "border-red-500 focus:border-red-500" : ""}`}
                    placeholder="Digite seu email"
                    disabled={isLoading}
                  />
                </div>
                {errors.email && (
                  <p className="text-red-400 text-sm flex items-center space-x-1">
                    <XCircle className="h-4 w-4" />
                    <span>{errors.email}</span>
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

                {/* Password Strength */}
                {formData.password && (
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-400">Força da senha:</span>
                      <span
                        className={`font-medium ${
                          passwordStrength.score >= 75
                            ? "text-green-400"
                            : passwordStrength.score >= 50
                              ? "text-yellow-400"
                              : passwordStrength.score >= 25
                                ? "text-orange-400"
                                : "text-red-400"
                        }`}
                      >
                        {getStrengthText(passwordStrength.score)}
                      </span>
                    </div>
                    <Progress value={passwordStrength.score} className="h-2" />
                  </div>
                )}

                {/* Password Requirements */}
                <div className="bg-slate-800/30 p-3 rounded-lg">
                  <p className="text-slate-300 text-sm flex items-center space-x-1 mb-2">
                    <Info className="h-4 w-4" />
                    <span>Sua senha deve ter:</span>
                  </p>
                  <ul className="text-sm space-y-1">
                    {passwordStrength.feedback.length > 0 ? (
                      passwordStrength.feedback.map((requirement, index) => (
                        <li key={index} className="text-slate-400 flex items-center space-x-2">
                          <XCircle className="h-3 w-3 text-red-400" />
                          <span>{requirement}</span>
                        </li>
                      ))
                    ) : (
                      <li className="text-green-400 flex items-center space-x-2">
                        <CheckCircle className="h-3 w-3" />
                        <span>Todos os requisitos atendidos</span>
                      </li>
                    )}
                  </ul>
                </div>

                {errors.password && (
                  <p className="text-red-400 text-sm flex items-center space-x-1">
                    <XCircle className="h-4 w-4" />
                    <span>{errors.password}</span>
                  </p>
                )}
              </div>

              {/* Confirm Password Field */}
              <div className="space-y-2">
                <Label htmlFor="confirmPassword" className="text-slate-300 flex items-center space-x-1">
                  <Lock className="h-4 w-4" />
                  <span>Confirmar senha</span>
                </Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
                  <Input
                    id="confirmPassword"
                    name="confirmPassword"
                    type={showConfirmPassword ? "text" : "password"}
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    className={`pl-10 pr-10 input-steam ${errors.confirmPassword ? "border-red-500 focus:border-red-500" : ""}`}
                    placeholder="Confirme sua senha"
                    disabled={isLoading}
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="absolute right-2 top-1/2 transform -translate-y-1/2 h-6 w-6 p-0 hover:bg-transparent"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  >
                    {showConfirmPassword ? (
                      <EyeOff className="h-4 w-4 text-slate-400" />
                    ) : (
                      <Eye className="h-4 w-4 text-slate-400" />
                    )}
                  </Button>
                </div>

                {/* Password Match Indicator */}
                {formData.confirmPassword && (
                  <div className="flex items-center space-x-2 text-sm">
                    {formData.password === formData.confirmPassword ? (
                      <>
                        <CheckCircle className="h-4 w-4 text-green-400" />
                        <span className="text-green-400">Senhas coincidem</span>
                      </>
                    ) : (
                      <>
                        <XCircle className="h-4 w-4 text-red-400" />
                        <span className="text-red-400">Senhas não coincidem</span>
                      </>
                    )}
                  </div>
                )}

                {errors.confirmPassword && (
                  <p className="text-red-400 text-sm flex items-center space-x-1">
                    <XCircle className="h-4 w-4" />
                    <span>{errors.confirmPassword}</span>
                  </p>
                )}
              </div>

              {/* Terms Checkbox */}
              <div className="space-y-2">
                <div className="flex items-start space-x-2">
                  <Checkbox
                    id="acceptTerms"
                    checked={formData.acceptTerms}
                    onCheckedChange={(checked) => {
                      setFormData((prev) => ({ ...prev, acceptTerms: checked as boolean }))
                      if (errors.acceptTerms) {
                        setErrors((prev) => ({ ...prev, acceptTerms: "" }))
                      }
                    }}
                    className={`border-slate-600 data-[state=checked]:bg-blue-600 mt-1 ${
                      errors.acceptTerms ? "border-red-500" : ""
                    }`}
                  />
                  <Label htmlFor="acceptTerms" className="text-slate-300 text-sm cursor-pointer leading-relaxed">
                    Concordo com os{" "}
                    <Link href="/terms" className="text-blue-400 hover:text-blue-300 underline">
                      Termos de Serviço
                    </Link>{" "}
                    e{" "}
                    <Link href="/privacy" className="text-blue-400 hover:text-blue-300 underline">
                      Política de Privacidade
                    </Link>
                  </Label>
                </div>
                {errors.acceptTerms && (
                  <p className="text-red-400 text-sm flex items-center space-x-1">
                    <XCircle className="h-4 w-4" />
                    <span>{errors.acceptTerms}</span>
                  </p>
                )}
              </div>

              {/* Submit Button */}
              <Button type="submit" className="w-full btn-steam text-lg py-6" disabled={isLoading}>
                {isLoading ? (
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Criando conta...</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-2">
                    <UserPlus className="h-5 w-5" />
                    <span>Criar Conta</span>
                  </div>
                )}
              </Button>
            </form>
          </CardContent>

          <CardFooter className="flex flex-col space-y-4 pt-6">
            <div className="text-center text-slate-400">
              Já tem uma conta?{" "}
              <Link
                href="/login"
                className="text-blue-400 hover:text-blue-300 font-semibold transition-colors inline-flex items-center space-x-1"
              >
                <LogIn className="h-4 w-4" />
                <span>Entrar</span>
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
