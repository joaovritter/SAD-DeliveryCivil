import { 
  Hammer, 
  Wrench, 
  Zap, 
  Paintbrush2, 
  TreePine, 
  Droplets,
  Shield,
  Building2 
} from "lucide-react";

const Categories = () => {
  const categories = [
    { id: 1, name: "Ferramentas", icon: Hammer, color: "text-orange-500" },
    { id: 2, name: "Hidráulica", icon: Droplets, color: "text-blue-500" },
    { id: 3, name: "Elétrica", icon: Zap, color: "text-yellow-500" },
    { id: 4, name: "Tintas", icon: Paintbrush2, color: "text-purple-500" },
    { id: 5, name: "Madeira", icon: TreePine, color: "text-green-500" },
    { id: 6, name: "Materiais", icon: Building2, color: "text-gray-600" },
    { id: 7, name: "Segurança", icon: Shield, color: "text-red-500" },
    { id: 8, name: "Acabamento", icon: Wrench, color: "text-indigo-500" }
  ];

  return (
    <section className="px-3 mb-6">
      <h2 className="text-lg font-bold mb-4 text-foreground">Categorias</h2>
      <div className="grid grid-cols-4 gap-2.5">
        {categories.map((category) => {
          const IconComponent = category.icon;
          return (
            <button
              key={category.id}
              className="category-card fade-in min-h-[80px]"
              style={{ animationDelay: `${category.id * 0.1}s` }}
            >
              <div className={`w-14 h-14 rounded-full bg-gray-100 flex items-center justify-center mb-2 ${category.color}`}>
                <IconComponent size={26} />
              </div>
              <span className="text-xs font-medium text-center text-foreground leading-tight">
                {category.name}
              </span>
            </button>
          );
        })}
      </div>
    </section>
  );
};

export default Categories;