"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { MessageCircle, UserPlus, Users, Clock, CheckCircle, X } from "lucide-react"
import { useFriends } from "@/lib/friends-context"
import { useAuth } from "@/lib/auth-context"
import { AddFriendModal } from "./add-friend-modal"

export function FriendsPanel() {
  const [activeTab, setActiveTab] = useState<'online' | 'all' | 'requests'>('online')
  const { user } = useAuth()
  const {
    friends,
    onlineFriends,
    pendingRequests,
    isLoadingFriends,
    error,
    acceptFriendRequest,
    rejectFriendRequest,
    refreshFriends
  } = useFriends()
  const [showAddFriendModal, setShowAddFriendModal] = useState(false)

  const getStatusColor = (isOnline: boolean) => {
    return isOnline ? 'bg-green-500' : 'bg-gray-500'
  }

  const handleAcceptRequest = async (requestId: string) => {
    try {
      await acceptFriendRequest(requestId)
    } catch (error) {
      console.error('Erro ao aceitar solicitação:', error)
    }
  }

  const handleRejectRequest = async (requestId: string) => {
    try {
      await rejectFriendRequest(requestId)
    } catch (error) {
      console.error('Erro ao rejeitar solicitação:', error)
    }
  }

  return (
    <Card className="card-steam">
      <CardHeader className="pb-3">
        <CardTitle className="text-white flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Users className="h-5 w-5 text-blue-400" />
            Amigos
          </div>
          <Badge variant="secondary" className="bg-slate-700 text-slate-300">
            {friends.length}
          </Badge>
        </CardTitle>
        
        <div className="flex space-x-1 mb-4">
          <Button
            variant={activeTab === 'online' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setActiveTab('online')}
            className="flex-1"
          >
            Online ({onlineFriends.length})
          </Button>
          <Button
            variant={activeTab === 'all' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setActiveTab('all')}
            className="flex-1"
          >
            Todos ({friends.length})
          </Button>
          <Button
            variant={activeTab === 'requests' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setActiveTab('requests')}
            className="flex-1 relative"
          >
            <UserPlus className="h-4 w-4" />
            {pendingRequests.length > 0 && (
              <Badge 
                variant="destructive" 
                className="absolute -top-2 -right-2 h-5 w-5 p-0 text-xs flex items-center justify-center"
              >
                {pendingRequests.length}
              </Badge>
            )}
          </Button>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-2">
        {isLoadingFriends ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-2"></div>
            <p className="text-sm text-slate-400">Carregando amigos...</p>
          </div>
        ) : error ? (
          <div className="text-center py-8">
            <p className="text-sm text-red-400 mb-2">{error}</p>
            <Button size="sm" onClick={refreshFriends} variant="outline">
              Tentar novamente
            </Button>
          </div>
        ) : (
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {activeTab === 'online' && onlineFriends.map((friend) => {
              const isOnline = onlineFriends.some(of => of.id === friend.id)
              return (
                <div key={friend.id} className="flex items-center space-x-3 p-2 rounded-lg hover:bg-slate-700/50 transition-colors">
                  <div className="relative">
                    <Avatar className="h-8 w-8">
                      <AvatarImage src={friend.avatar || undefined} alt={friend.username} />
                      <AvatarFallback>{friend.username.slice(0, 2).toUpperCase()}</AvatarFallback>
                    </Avatar>
                    <div className={`absolute -bottom-1 -right-1 h-3 w-3 rounded-full border-2 border-slate-800 ${getStatusColor(isOnline)}`} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-white truncate">{friend.username}</p>
                    <p className="text-xs text-slate-400 truncate">
                      {friend.bio || 'Navegando na loja'}
                    </p>
                  </div>
                  <Button size="sm" variant="ghost" className="h-8 w-8 p-0">
                    <MessageCircle className="h-4 w-4" />
                  </Button>
                </div>
              )
            })}

            {activeTab === 'all' && friends.map((friend) => {
              const isOnline = onlineFriends.some(of => of.id === friend.id)
              return (
                <div key={friend.id} className="flex items-center space-x-3 p-2 rounded-lg hover:bg-slate-700/50 transition-colors">
                  <div className="relative">
                    <Avatar className="h-8 w-8">
                      <AvatarImage src={friend.avatar || undefined} alt={friend.username} />
                      <AvatarFallback>{friend.username.slice(0, 2).toUpperCase()}</AvatarFallback>
                    </Avatar>
                    <div className={`absolute -bottom-1 -right-1 h-3 w-3 rounded-full border-2 border-slate-800 ${getStatusColor(isOnline)}`} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-white truncate">{friend.username}</p>
                    <p className="text-xs text-slate-400 truncate">
                      {isOnline 
                        ? (friend.bio || 'Online')
                        : `Visto ${friend.last_login ? new Date(friend.last_login).toLocaleDateString() : 'há muito tempo'}`
                      }
                    </p>
                  </div>
                  <Button size="sm" variant="ghost" className="h-8 w-8 p-0">
                    <MessageCircle className="h-4 w-4" />
                  </Button>
                </div>
              )
            })}

            {activeTab === 'requests' && pendingRequests.map((request) => {
              const sender = request.sender_detail
              return (
                <div key={request.id} className="flex items-center space-x-3 p-2 rounded-lg bg-slate-700/30">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={sender.avatar || undefined} alt={sender.username} />
                    <AvatarFallback>{sender.username.slice(0, 2).toUpperCase()}</AvatarFallback>
                  </Avatar>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-white truncate">{sender.username}</p>
                    <p className="text-xs text-slate-400">
                      {sender.first_name && sender.last_name ? `${sender.first_name} ${sender.last_name}` : 'Novo usuário'}
                    </p>
                  </div>
                  <div className="flex space-x-1">
                    <Button 
                      size="sm" 
                      variant="ghost" 
                      className="h-8 w-8 p-0 text-green-400 hover:text-green-300"
                      onClick={() => handleAcceptRequest(request.id)}
                      title="Aceitar solicitação"
                    >
                      <CheckCircle className="h-4 w-4" />
                    </Button>
                    <Button 
                      size="sm" 
                      variant="ghost" 
                      className="h-8 w-8 p-0 text-red-400 hover:text-red-300"
                      onClick={() => handleRejectRequest(request.id)}
                      title="Rejeitar solicitação"
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              )
            })}

            {((activeTab === 'online' && onlineFriends.length === 0) ||
              (activeTab === 'all' && friends.length === 0) ||
              (activeTab === 'requests' && pendingRequests.length === 0)) && (
              <div className="text-center py-8">
                <Clock className="h-8 w-8 text-slate-500 mx-auto mb-2" />
                <p className="text-sm text-slate-400">
                  {activeTab === 'online' && 'Nenhum amigo online'}
                  {activeTab === 'all' && 'Nenhum amigo adicionado'}
                  {activeTab === 'requests' && 'Nenhuma solicitação pendente'}
                </p>
                {activeTab === 'all' && (
                  <p className="text-xs text-slate-500 mt-1">
                    Use a busca para encontrar novos amigos!
                  </p>
                )}
              </div>
            )}
          </div>
        )}
        
        {/* Linha divisória sutil */}
        <div className="border-t border-slate-600/30 my-3"></div>
        
        <div className="flex items-center justify-between">
          <Button 
            size="sm" 
            variant="outline" 
            className="flex-1 mr-2"
            onClick={() => setShowAddFriendModal(true)}
          >
            <UserPlus className="h-4 w-4 mr-2" />
            Adicionar Amigo
          </Button>
          <Button size="sm" variant="outline" className="flex-1">
            <MessageCircle className="h-4 w-4 mr-2" />
            Chat
          </Button>
        </div>
        
        {/* Modal para adicionar amigo */}
        <AddFriendModal 
          open={showAddFriendModal} 
          onOpenChange={setShowAddFriendModal} 
        />
      </CardContent>
    </Card>
  )
}
