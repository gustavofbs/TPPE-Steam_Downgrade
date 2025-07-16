import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Users, UserPlus, MessageCircle, Gamepad2 } from "lucide-react"

// Mock friends data
const mockFriends = [
  {
    id: 1,
    username: "GamerFriend1",
    status: "online",
    currentGame: "Half-Life 3",
    avatar: "/placeholder.svg?height=32&width=32",
  },
  {
    id: 2,
    username: "ProPlayer99",
    status: "in-game",
    currentGame: "Portal 3",
    avatar: "/placeholder.svg?height=32&width=32",
  },
  {
    id: 3,
    username: "CasualGamer",
    status: "away",
    currentGame: null,
    avatar: "/placeholder.svg?height=32&width=32",
  },
]

export function FriendsPanel() {
  const onlineFriends = mockFriends.filter((friend) => friend.status === "online" || friend.status === "in-game")

  return (
    <Card className="card-steam">
      <CardHeader className="pb-3">
        <CardTitle className="text-white flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Users className="h-5 w-5 text-blue-400" />
            Amigos Online
          </div>
          <Badge variant="secondary" className="bg-slate-700 text-slate-300">
            {onlineFriends.length}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {onlineFriends.length > 0 ? (
          <>
            {onlineFriends.map((friend) => (
              <div
                key={friend.id}
                className="flex items-center gap-3 p-2 rounded-lg hover:bg-slate-800/50 transition-colors"
              >
                <div className="relative">
                  <div className="w-8 h-8 bg-slate-600 rounded-full flex items-center justify-center">
                    <Users className="h-4 w-4 text-slate-300" />
                  </div>
                  <div
                    className={`absolute -bottom-1 -right-1 w-3 h-3 rounded-full border-2 border-slate-800 ${
                      friend.status === "online"
                        ? "bg-green-500"
                        : friend.status === "in-game"
                          ? "bg-blue-500"
                          : "bg-yellow-500"
                    }`}
                  />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-white truncate">{friend.username}</div>
                  {friend.currentGame ? (
                    <div className="text-xs text-slate-400 flex items-center gap-1">
                      <Gamepad2 className="h-3 w-3" />
                      <span className="truncate">{friend.currentGame}</span>
                    </div>
                  ) : (
                    <div className="text-xs text-slate-500">Online</div>
                  )}
                </div>
                <Button variant="ghost" size="sm" className="h-6 w-6 p-0 hover:bg-slate-700">
                  <MessageCircle className="h-3 w-3" />
                </Button>
              </div>
            ))}
            <Button
              variant="outline"
              className="w-full border-slate-600 text-slate-300 hover:bg-slate-700 bg-transparent"
            >
              <UserPlus className="h-4 w-4 mr-2" />
              Adicionar Amigo
            </Button>
          </>
        ) : (
          <div className="text-center py-6">
            <Users className="h-12 w-12 text-slate-600 mx-auto mb-3" />
            <p className="text-slate-400 text-sm mb-3">Nenhum amigo online</p>
            <Button variant="outline" className="border-slate-600 text-slate-300 hover:bg-slate-700 bg-transparent">
              <UserPlus className="h-4 w-4 mr-2" />
              Encontrar Amigos
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
