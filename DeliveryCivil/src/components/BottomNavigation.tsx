import { Home, Search, ShoppingCart, User, BarChart3 } from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";

const BottomNavigation = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { id: "home", icon: Home, label: "Início", path: "/" },
    { id: "search", icon: Search, label: "Buscar", path: "/" },
    { id: "cart", icon: ShoppingCart, label: "Carrinho", path: "/cart" },
    { id: "reports", icon: BarChart3, label: "Relatórios", path: "/reports" },
    { id: "profile", icon: User, label: "Conta", path: "/" }
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="bottom-nav">
      <ul className="flex justify-around">
        {navItems.map((item) => {
          const IconComponent = item.icon;
          return (
            <li key={item.id}>
              <button
                className={`nav-item ${isActive(item.path) ? 'active' : ''}`}
                onClick={() => navigate(item.path)}
              >
                <IconComponent size={20} />
                <span className="text-xs mt-1">{item.label}</span>
              </button>
            </li>
          );
        })}
      </ul>
    </nav>
  );
};

export default BottomNavigation;