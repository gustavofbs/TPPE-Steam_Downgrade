"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { ProfileEditor } from "@/components/profile-editor"
import { UserProvider, useUser } from "@/lib/user-context"
import { User, Mail, Calendar, Edit3, Shield, Camera, Hash, Clock, Loader2, AlertCircle } from "lucide-react"

// Componente de carregamento
function LoadingState() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <Card className="card-steam mb-8">
        <CardContent className="p-8 text-center">
          <Loader2 className="h-12 w-12 animate-spin text-blue-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white">Carregando perfil...</h2>
          <p className="text-slate-400 mt-2">Por favor, aguarde enquanto buscamos suas informações.</p>
        </CardContent>
      </Card>
    </div>
  )
}

// Componente de erro
function ErrorState({ error, onRetry }: { error: string; onRetry: () => void }) {
  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <Card className="card-steam mb-8">
        <CardContent className="p-8 text-center">
          <AlertCircle className="h-12 w-12 text-red-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white">Erro ao carregar perfil</h2>
          <p className="text-slate-400 mt-2">{error}</p>
          <Button onClick={onRetry} className="mt-6 bg-blue-600 hover:bg-blue-700">
            Tentar Novamente
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}

// Componente principal do perfil
function ProfilePageContent() {
  const { user, isLoading, error, refreshUser, updateProfile, uploadAvatar } = useUser()
  const [isEditing, setIsEditing] = useState(false)
  const [isSaving, setIsSaving] = useState(false)

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("pt-BR", {
      year: "numeric",
      month: "long",
      day: "numeric",
    })
  }

  const calculateAge = (birthDate: string) => {
    const today = new Date()
    const birth = new Date(birthDate)
    let age = today.getFullYear() - birth.getFullYear()
    const monthDiff = today.getMonth() - birth.getMonth()
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--
    }
    return age
  }

  const handleSaveProfile = async (updatedData: any) => {
    setIsSaving(true)
    try {
      await updateProfile(updatedData)
      setIsEditing(false)
      console.log("Profile updated:", updatedData)
    } catch (error) {
      console.error("Error updating profile:", error)
      // Error is handled by the context
    } finally {
      setIsSaving(false)
    }
  }

  // Estados de carregamento e erro
  if (isLoading) return <LoadingState />
  if (error) return <ErrorState error={error} onRetry={refreshUser} />
  if (!user) return <ErrorState error="Usuário não encontrado" onRetry={refreshUser} />

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Profile Header */}
      <Card className="card-steam mb-8">
        <CardContent className="p-8">
          <div className="flex flex-col md:flex-row gap-6">
            {/* Avatar Section */}
            <div className="flex flex-col items-center space-y-4">
              <div className="relative group">
                <Avatar className="w-32 h-32 border-4 border-blue-400">
                  <AvatarImage src={user.profile.avatar || "/placeholder.svg"} alt={user.username} />
                  <AvatarFallback className="text-2xl bg-slate-700 text-white">
                    {user.first_name[0]}
                    {user.last_name[0]}
                  </AvatarFallback>
                </Avatar>
                <Button
                  size="sm"
                  className="absolute bottom-0 right-0 rounded-full w-8 h-8 p-0 bg-blue-600 hover:bg-blue-700"
                  onClick={() => setIsEditing(true)}
                >
                  <Camera className="h-4 w-4" />
                </Button>
              </div>
            </div>

            {/* Profile Info */}
            <div className="flex-1 space-y-4">
              <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                <div>
                  <h1 className="text-3xl font-bold text-white mb-2">
                    {user.first_name} {user.last_name}
                  </h1>
                  <div className="flex items-center gap-2 text-slate-400 mb-4">
                    <User className="h-4 w-4" />
                    <span>@{user.username}</span>
                  </div>

                  {/* Account Status */}
                  <div className="flex items-center gap-4 mb-4">
                    <Badge
                      className={user.is_active ? "bg-green-600 hover:bg-green-600" : "bg-red-600 hover:bg-red-600"}
                    >
                      <Shield className="h-3 w-3 mr-1" />
                      {user.is_active ? "Conta Ativa" : "Conta Inativa"}
                    </Badge>
                    <div className="flex items-center gap-1 text-sm text-slate-400">
                      <Calendar className="h-4 w-4" />
                      <span>Membro desde {formatDate(user.date_joined)}</span>
                    </div>
                  </div>
                </div>

                <Button onClick={() => setIsEditing(true)} className="btn-steam" disabled={isSaving}>
                  <Edit3 className="h-4 w-4 mr-2" />
                  Editar Perfil
                </Button>
              </div>

              {/* Bio */}
              <div className="bg-slate-800/30 p-4 rounded-lg">
                <h3 className="text-white font-medium mb-2">Biografia</h3>
                <p className="text-slate-300 leading-relaxed">
                  {user.profile.bio || "Este usuário ainda não adicionou uma biografia."}
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Detailed Information */}
      <Card className="card-steam">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <User className="h-5 w-5 text-blue-400" />
            Informações Detalhadas
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Personal Information */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-white mb-4">Dados Pessoais</h3>

              <div className="space-y-3">
                <div className="flex items-center gap-3 p-3 bg-slate-800/30 rounded-lg">
                  <Hash className="h-4 w-4 text-slate-400" />
                  <div>
                    <div className="text-sm text-slate-400">ID do Usuário</div>
                    <div className="text-white font-mono">#{user.id}</div>
                  </div>
                </div>

                <div className="flex items-center gap-3 p-3 bg-slate-800/30 rounded-lg">
                  <User className="h-4 w-4 text-slate-400" />
                  <div>
                    <div className="text-sm text-slate-400">Nome de Usuário</div>
                    <div className="text-white">@{user.username}</div>
                  </div>
                </div>

                <div className="flex items-center gap-3 p-3 bg-slate-800/30 rounded-lg">
                  <User className="h-4 w-4 text-slate-400" />
                  <div>
                    <div className="text-sm text-slate-400">Nome Completo</div>
                    <div className="text-white">
                      {user.first_name} {user.last_name}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 p-3 bg-slate-800/30 rounded-lg">
                  <Mail className="h-4 w-4 text-slate-400" />
                  <div>
                    <div className="text-sm text-slate-400">Email</div>
                    <div className="text-white">{user.email}</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Account Information */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-white mb-4">Informações da Conta</h3>

              <div className="space-y-3">
                <div className="flex items-center gap-3 p-3 bg-slate-800/30 rounded-lg">
                  <Calendar className="h-4 w-4 text-slate-400" />
                  <div>
                    <div className="text-sm text-slate-400">Data de Nascimento</div>
                    <div className="text-white">
                      {user.profile.birth_date
                        ? `${formatDate(user.profile.birth_date)} (${calculateAge(user.profile.birth_date)} anos)`
                        : "Não informado"}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 p-3 bg-slate-800/30 rounded-lg">
                  <Clock className="h-4 w-4 text-slate-400" />
                  <div>
                    <div className="text-sm text-slate-400">Data de Cadastro</div>
                    <div className="text-white">{formatDate(user.date_joined)}</div>
                  </div>
                </div>

                <div className="flex items-center gap-3 p-3 bg-slate-800/30 rounded-lg">
                  <Shield className="h-4 w-4 text-slate-400" />
                  <div>
                    <div className="text-sm text-slate-400">Status da Conta</div>
                    <Badge
                      className={user.is_active ? "bg-green-600 hover:bg-green-600" : "bg-red-600 hover:bg-red-600"}
                    >
                      {user.is_active ? "Ativa" : "Inativa"}
                    </Badge>
                  </div>
                </div>

                {/* Bio Section */}
                <div className="p-3 bg-slate-800/30 rounded-lg">
                  <div className="text-sm text-slate-400 mb-2">Biografia</div>
                  <div className="text-white leading-relaxed">
                    {user.profile.bio || (
                      <span className="text-slate-500 italic">Nenhuma biografia adicionada</span>
                    )}
                  </div>
                  {user.profile.bio && (
                    <div className="text-xs text-slate-500 mt-2">{user.profile.bio.length}/500 caracteres</div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Profile Editor Modal */}
      {isEditing && (
        <ProfileEditor
          user={user}
          onSave={handleSaveProfile}
          onCancel={() => setIsEditing(false)}
          isLoading={isSaving}
          uploadAvatar={uploadAvatar}
        />
      )}
    </div>
  )
}

// Wrapper com UserProvider
export default function ProfilePage() {
  return (
    <UserProvider>
      <ProfilePageContent />
    </UserProvider>
  )
}
