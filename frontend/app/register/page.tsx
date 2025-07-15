"use client";

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { User, Lock, Mail, UserCheck, AlertCircle } from 'lucide-react';
import { useAuth } from '@/lib/auth-context';

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuth();
  
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
    first_name: '',
    last_name: '',
  });
  
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    
    // Validação básica
    if (!formData.username || !formData.email || !formData.password || !formData.password2) {
      setError('Por favor, preencha todos os campos obrigatórios.');
      setIsLoading(false);
      return;
    }
    
    if (formData.password !== formData.password2) {
      setError('As senhas não coincidem.');
      setIsLoading(false);
      return;
    }
    
    try {
      await register(formData);
      router.push('/catalog'); // Redireciona para o catálogo após registro bem-sucedido
    } catch (err: any) {
      console.error('Erro no registro:', err);
      setError(err.message || 'Ocorreu um erro durante o registro. Por favor, tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="flex items-center justify-center min-h-screen bg-steam-dark p-4">
      <Card className="w-full max-w-md bg-steam-card border-steam-border shadow-lg">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-steam-blue">Criar uma conta Steam</CardTitle>
          <CardDescription>
            Crie uma nova conta para acessar o Steam Downgrade
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="bg-red-900/30 border border-red-800 rounded-md p-3 mb-4 flex items-start gap-2">
              <AlertCircle className="h-5 w-5 text-red-500 mt-0.5" />
              <p className="text-sm text-red-400">{error}</p>
            </div>
          )}
          
          <form onSubmit={handleSubmit}>
            <div className="grid gap-4">
              <div className="grid gap-2">
                <Label htmlFor="username">Nome de usuário</Label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-4 w-4 text-steam-text-secondary" />
                  <Input
                    id="username"
                    name="username"
                    placeholder="Digite seu nome de usuário"
                    className="pl-10"
                    value={formData.username}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>
              
              <div className="grid gap-2">
                <Label htmlFor="email">Email</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-4 w-4 text-steam-text-secondary" />
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    placeholder="Digite seu email"
                    className="pl-10"
                    value={formData.email}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="first_name">Nome</Label>
                  <div className="relative">
                    <UserCheck className="absolute left-3 top-3 h-4 w-4 text-steam-text-secondary" />
                    <Input
                      id="first_name"
                      name="first_name"
                      placeholder="Nome"
                      className="pl-10"
                      value={formData.first_name}
                      onChange={handleChange}
                    />
                  </div>
                </div>
                
                <div className="grid gap-2">
                  <Label htmlFor="last_name">Sobrenome</Label>
                  <Input
                    id="last_name"
                    name="last_name"
                    placeholder="Sobrenome"
                    value={formData.last_name}
                    onChange={handleChange}
                  />
                </div>
              </div>
              
              <div className="grid gap-2">
                <Label htmlFor="password">Senha</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-steam-text-secondary" />
                  <Input
                    id="password"
                    name="password"
                    type="password"
                    placeholder="Digite sua senha"
                    className="pl-10"
                    value={formData.password}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>
              
              <div className="grid gap-2">
                <Label htmlFor="password2">Confirmar senha</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-steam-text-secondary" />
                  <Input
                    id="password2"
                    name="password2"
                    type="password"
                    placeholder="Confirme sua senha"
                    className="pl-10"
                    value={formData.password2}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>
              
              <Button 
                type="submit" 
                className="bg-steam-blue hover:bg-steam-blue-hover"
                disabled={isLoading}
              >
                {isLoading ? 'Registrando...' : 'Registrar'}
              </Button>
            </div>
          </form>
        </CardContent>
        <CardFooter className="flex flex-col space-y-2">
          <div className="text-sm text-steam-text-secondary text-center">
            Já tem uma conta?{' '}
            <Link href="/login" className="text-steam-blue hover:text-steam-blue-hover">
              Faça login
            </Link>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}
