"use client";
import { useState } from "react";
import { api } from "../../lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await api.post('/api/auth/login', { email, password });
      localStorage.setItem('access_token', res.data.access_token);
      window.location.href = '/dashboard';
    } catch (err) {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black text-white">
      <form onSubmit={handleLogin} className="bg-surface border border-white/10 p-8 rounded-xl w-96">
        <h1 className="text-2xl font-bold mb-6">Login to RecruitIQ</h1>
        <input className="w-full bg-black border p-2 mb-4 rounded" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
        <input className="w-full bg-black border p-2 mb-4 rounded" type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
        <button type="submit" className="w-full bg-accent py-2 rounded">Sign In</button>
      </form>
    </div>
  );
}