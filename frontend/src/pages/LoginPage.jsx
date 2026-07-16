/**
 * Login Page — premium glassmorphism design.
 */
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Button, Input } from "../components/common";
import { Sparkles } from "lucide-react";
import toast from "react-hot-toast";
import logoImg from "../assets/logo.jpg";

const galleryImages = [
  "https://images.unsplash.com/photo-1497375638960-ca368c7231e4?auto=format&fit=crop&q=80&w=1920", // Volunteers together
  "https://images.unsplash.com/photo-1469571486292-0ba58a3f068b?auto=format&fit=crop&q=80&w=1920", // Volunteering
  "https://images.unsplash.com/photo-1529390079861-591de354faf5?auto=format&fit=crop&q=80&w=1920", // Learning
  "https://images.unsplash.com/photo-1528605105345-5344ea20e269?auto=format&fit=crop&q=80&w=1920"  // Art & Community
];

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [bgIndex, setBgIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setBgIndex((prev) => (prev + 1) % galleryImages.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(email, password);
      toast.success("Welcome back!");
      navigate("/dashboard");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 relative overflow-hidden">
      {/* Background Slideshow */}
      {galleryImages.map((src, index) => (
        <div
          key={src}
          className={`absolute inset-0 bg-cover bg-center transition-opacity duration-1000 ${
            index === bgIndex ? "opacity-100" : "opacity-0"
          }`}
          style={{ backgroundImage: `url(${src})` }}
        />
      ))}
      {/* Dark overlay for contrast */}
      <div className="absolute inset-0 bg-black/50 backdrop-blur-[2px]" />

      <div className="w-full max-w-md animate-slide-up relative z-10">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="w-20 h-20 rounded-2xl overflow-hidden flex items-center justify-center shadow-2xl mx-auto mb-4 bg-white border border-white/20">
            <img src={logoImg} alt="Amaanitvam Logo" className="w-full h-full object-cover" />
          </div>
          <h1 className="text-3xl font-bold text-white drop-shadow-md">Welcome Back</h1>
          <p className="text-white/80 mt-1 drop-shadow">Sign in to your volunteer portal</p>
        </div>

        {/* Form */}
        <div className="bg-white/95 backdrop-blur-xl p-8 rounded-2xl shadow-2xl border border-white/20">
          <form onSubmit={handleSubmit} className="space-y-5">
            <Input
              id="email"
              label="Email Address"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="username"
              required
            />
            <Input
              id="password"
              label="Password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
            <Button type="submit" loading={loading} className="w-full">
              Sign In
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-surface-500">
              Don&apos;t have an account?{" "}
              <Link to="/register" className="text-primary-600 font-semibold hover:text-primary-700">
                Create one
              </Link>
            </p>
          </div>

          {/* Demo credentials */}
          <div className="mt-6 pt-6 border-t border-surface-100">
            <p className="text-xs text-surface-400 text-center mb-3">Demo Accounts</p>
            <div className="grid grid-cols-3 gap-2">
              {[
                { label: "Admin", email: "admin@amaanitvam.org", pass: "Admin@123" },
                { label: "Coord", email: "coordinator@amaanitvam.org", pass: "Coord@123" },
                { label: "Vol", email: "volunteer@amaanitvam.org", pass: "Vol@123" },
              ].map((demo) => (
                <button
                  key={demo.label}
                  type="button"
                  onClick={() => { setEmail(demo.email); setPassword(demo.pass); }}
                  className="px-3 py-2 text-xs font-medium bg-surface-50 hover:bg-surface-100 rounded-lg transition-colors text-surface-600"
                >
                  {demo.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
