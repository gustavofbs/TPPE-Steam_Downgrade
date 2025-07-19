'use client'

import { useState } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Search, UserPlus, Loader2 } from 'lucide-react'
import { useFriends } from '@/lib/friends-context'
import { useAuth } from '@/lib/auth-context'
import { Friend } from '@/lib/friends-api'

interface AddFriendModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function AddFriendModal({ open, onOpenChange }: AddFriendModalProps) {
  const { user } = useAuth()
  const { searchUsers, sendFriendRequest, friends } = useFriends()
  
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<Friend[]>([])
  const [isSearching, setIsSearching] = useState(false)
  const [sendingTo, setSendingTo] = useState<string | null>(null)

  const handleSearch = async () => {
    if (!searchQuery.trim()) return

    setIsSearching(true)
    try {
      const results = await searchUsers(searchQuery)
      // Filtrar o usuário atual dos resultados
      const filteredResults = results.filter(u => u.id !== user?.id)
      setSearchResults(filteredResults)
    } catch (error) {
      console.error('Erro na busca:', error)
      setSearchResults([])
    } finally {
      setIsSearching(false)
    }
  }

  const handleSendRequest = async (receiverId: string) => {
    setSendingTo(receiverId)
    try {
      await sendFriendRequest(receiverId)
      // Remover usuário dos resultados após enviar solicitação
      setSearchResults(prev => prev.filter(u => u.id !== receiverId))
    } catch (error) {
      console.error('Erro ao enviar solicitação:', error)
    } finally {
      setSendingTo(null)
    }
  }

  const isAlreadyFriend = (userId: string) => {
    return friends.some(friend => friend.id === userId)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md bg-slate-800 border-slate-700">
        <DialogHeader>
          <DialogTitle className="text-white flex items-center gap-2">
            <UserPlus className="h-5 w-5" />
            Adicionar Amigo
          </DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4">
          {/* Campo de busca */}
          <div className="flex gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
              <Input
                placeholder="Buscar por nome de usuário..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                className="pl-10 bg-slate-700 border-slate-600 text-white placeholder:text-slate-400"
              />
            </div>
            <Button 
              onClick={handleSearch}
              disabled={isSearching || !searchQuery.trim()}
              className="bg-blue-600 hover:bg-blue-700"
            >
              {isSearching ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Search className="h-4 w-4" />
              )}
            </Button>
          </div>

          {/* Resultados da busca */}
          <div className="space-y-2 max-h-60 overflow-y-auto">
            {searchResults.length > 0 ? (
              searchResults.map((user) => (
                <div key={user.id} className="flex items-center space-x-3 p-3 rounded-lg bg-slate-700/50 border border-slate-600/50">
                  <Avatar className="h-10 w-10">
                    <AvatarImage src={user.avatar || undefined} alt={user.username} />
                    <AvatarFallback className="bg-slate-600 text-white">
                      {user.username.slice(0, 2).toUpperCase()}
                    </AvatarFallback>
                  </Avatar>
                  
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-white truncate">{user.username}</p>
                    {(user.first_name || user.last_name) && (
                      <p className="text-xs text-slate-400 truncate">
                        {user.first_name} {user.last_name}
                      </p>
                    )}
                  </div>
                  
                  <Button
                    size="sm"
                    onClick={() => handleSendRequest(user.id)}
                    disabled={sendingTo === user.id || isAlreadyFriend(user.id)}
                    className="bg-green-600 hover:bg-green-700 disabled:bg-slate-600"
                  >
                    {sendingTo === user.id ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : isAlreadyFriend(user.id) ? (
                      'Já é amigo'
                    ) : (
                      'Adicionar'
                    )}
                  </Button>
                </div>
              ))
            ) : searchQuery && !isSearching ? (
              <div className="text-center py-8">
                <Search className="h-8 w-8 text-slate-500 mx-auto mb-2" />
                <p className="text-sm text-slate-400">Nenhum usuário encontrado</p>
                <p className="text-xs text-slate-500 mt-1">
                  Tente buscar por outro nome de usuário
                </p>
              </div>
            ) : (
              <div className="text-center py-8">
                <UserPlus className="h-8 w-8 text-slate-500 mx-auto mb-2" />
                <p className="text-sm text-slate-400">Digite um nome de usuário para buscar</p>
                <p className="text-xs text-slate-500 mt-1">
                  Encontre novos amigos para adicionar!
                </p>
              </div>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
