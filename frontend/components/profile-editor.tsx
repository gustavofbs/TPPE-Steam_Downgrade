"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { X, Upload, Save, User, XCircle } from "lucide-react"

interface ProfileEditorProps {
  user: any
  onSave: (data: any) => void
  onCancel: () => void
  isLoading: boolean
  uploadAvatar: (file: File) => Promise<any>
}

export function ProfileEditor({ user, onSave, onCancel, isLoading, uploadAvatar }: ProfileEditorProps) {
  const [formData, setFormData] = useState({
    first_name: user.first_name,
    last_name: user.last_name,
    email: user.email,
    profile: {
      bio: user.profile.bio || "",
      birth_date: user.profile.birth_date || "",
      avatar: user.profile.avatar,
    },
  })

  const [errors, setErrors] = useState<{ [key: string]: string }>({})

  const handleInputChange = (field: string, value: string) => {
    if (field.startsWith("profile.")) {
      const profileField = field.replace("profile.", "")
      setFormData((prev) => ({
        ...prev,
        profile: {
          ...prev.profile,
          [profileField]: value,
        },
      }))
    } else {
      setFormData((prev) => ({
        ...prev,
        [field]: value,
      }))
    }

    // Clear error when user starts typing
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: "" }))
    }
  }

  const validateForm = () => {
    const newErrors: { [key: string]: string } = {}

    if (!formData.first_name.trim()) {
      newErrors.first_name = "Nome é obrigatório"
    }

    if (!formData.last_name.trim()) {
      newErrors.last_name = "Sobrenome é obrigatório"
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email é obrigatório"
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Email inválido"
    }

    if (formData.profile.bio && formData.profile.bio.length > 500) {
      newErrors["profile.bio"] = "Biografia deve ter no máximo 500 caracteres"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (validateForm()) {
      onSave(formData)
    }
  }

  const handleAvatarUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      try {
        // Fazer upload do arquivo para o servidor
        await uploadAvatar(file)
        // O avatar será atualizado automaticamente no contexto do usuário
      } catch (error) {
        console.error('Erro ao fazer upload do avatar:', error)
        // Você pode adicionar uma notificação de erro aqui
      }
    }
  }

  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
      <Card className="card-steam w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-white flex items-center gap-2">
            <User className="h-5 w-5 text-blue-400" />
            Editar Perfil
          </CardTitle>
          <Button variant="ghost" size="sm" onClick={onCancel} className="text-slate-400 hover:text-white">
            <X className="h-4 w-4" />
          </Button>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Avatar Upload */}
            <div className="flex flex-col items-center space-y-4">
              <Avatar className="w-24 h-24 border-4 border-blue-400">
                <AvatarImage src={formData.profile.avatar || "/placeholder.svg"} alt="Avatar" />
                <AvatarFallback className="text-xl bg-slate-700 text-white">
                  {formData.first_name[0]}
                  {formData.last_name[0]}
                </AvatarFallback>
              </Avatar>

              <div>
                <input
                  type="file"
                  id="avatar-upload"
                  accept="image/*"
                  onChange={handleAvatarUpload}
                  className="hidden"
                />
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => document.getElementById("avatar-upload")?.click()}
                  className="border-slate-600 text-slate-300 hover:bg-slate-700 bg-transparent"
                >
                  <Upload className="h-4 w-4 mr-2" />
                  Alterar Avatar
                </Button>
              </div>
            </div>

            {/* Personal Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="first_name" className="text-slate-300">
                  Nome *
                </Label>
                <Input
                  id="first_name"
                  value={formData.first_name}
                  onChange={(e) => handleInputChange("first_name", e.target.value)}
                  className={`input-steam ${errors.first_name ? "border-red-500" : ""}`}
                  disabled={isLoading}
                />
                {errors.first_name && (
                  <p className="text-red-400 text-sm flex items-center gap-1">
                    <XCircle className="h-4 w-4" />
                    {errors.first_name}
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="last_name" className="text-slate-300">
                  Sobrenome *
                </Label>
                <Input
                  id="last_name"
                  value={formData.last_name}
                  onChange={(e) => handleInputChange("last_name", e.target.value)}
                  className={`input-steam ${errors.last_name ? "border-red-500" : ""}`}
                  disabled={isLoading}
                />
                {errors.last_name && (
                  <p className="text-red-400 text-sm flex items-center gap-1">
                    <XCircle className="h-4 w-4" />
                    {errors.last_name}
                  </p>
                )}
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="email" className="text-slate-300">
                Email *
              </Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange("email", e.target.value)}
                className={`input-steam ${errors.email ? "border-red-500" : ""}`}
                disabled={isLoading}
              />
              {errors.email && (
                <p className="text-red-400 text-sm flex items-center gap-1">
                  <XCircle className="h-4 w-4" />
                  {errors.email}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="birth_date" className="text-slate-300">
                Data de Nascimento
              </Label>
              <Input
                id="birth_date"
                type="date"
                value={formData.profile.birth_date || ""}
                onChange={(e) => handleInputChange("profile.birth_date", e.target.value)}
                className="input-steam"
                disabled={isLoading}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="bio" className="text-slate-300">
                Biografia
              </Label>
              <Textarea
                id="bio"
                value={formData.profile.bio || ""}
                onChange={(e) => handleInputChange("profile.bio", e.target.value)}
                placeholder="Conte um pouco sobre você..."
                className={`input-steam min-h-[100px] resize-none ${errors["profile.bio"] ? "border-red-500" : ""}`}
                maxLength={500}
                disabled={isLoading}
              />
              <div className="flex justify-between text-sm">
                {errors["profile.bio"] && (
                  <p className="text-red-400 flex items-center gap-1">
                    <XCircle className="h-4 w-4" />
                    {errors["profile.bio"]}
                  </p>
                )}
                <p className="text-slate-400 ml-auto">{formData.profile.bio?.length || 0}/500 caracteres</p>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4">
              <Button type="submit" disabled={isLoading} className="flex-1 btn-steam">
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Salvando...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4 mr-2" />
                    Salvar Alterações
                  </>
                )}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={onCancel}
                disabled={isLoading}
                className="border-slate-600 text-slate-300 hover:bg-slate-700 bg-transparent"
              >
                Cancelar
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
