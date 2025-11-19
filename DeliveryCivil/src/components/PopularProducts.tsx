import { ShoppingCart, Star } from "lucide-react";
import cimentoImage from "@/assets/cimento.jpg";
import furadeiraImage from "@/assets/furadeira.jpg";
import tintaImage from "@/assets/tinta.jpg";
import parafusadeiraImage from "@/assets/parafusadeira.jpg";
import tuboPvcImage from "@/assets/tubo-pvc.jpg";
import areiaImage from "@/assets/areia.jpg";

const PopularProducts = () => {
  const products = [
    {
      id: 1,
      name: "Cimento CP-II 50kg",
      price: "R$ 24,90",
      originalPrice: "R$ 32,90",
      rating: 4.8,
      image: cimentoImage,
      discount: "24% OFF"
    },
    {
      id: 2,
      name: "Furadeira Bosch 650W",
      price: "R$ 189,90",
      originalPrice: "R$ 249,90",
      rating: 4.9,
      image: furadeiraImage,
      discount: "24% OFF"
    },
    {
      id: 3,
      name: "Tinta Látex Branca 18L",
      price: "R$ 89,90",
      originalPrice: "R$ 119,90",
      rating: 4.7,
      image: tintaImage,
      discount: "25% OFF"
    },
    {
      id: 4,
      name: "Parafusadeira Makita",
      price: "R$ 299,90",
      originalPrice: "R$ 399,90",
      rating: 4.9,
      image: parafusadeiraImage,
      discount: "25% OFF"
    },
    {
      id: 5,
      name: "Tubo PVC 100mm",
      price: "R$ 19,90",
      originalPrice: "R$ 24,90",
      rating: 4.6,
      image: tuboPvcImage,
      discount: "20% OFF"
    },
    {
      id: 6,
      name: "Areia Lavada 20kg",
      price: "R$ 8,90",
      originalPrice: "R$ 12,90",
      rating: 4.5,
      image: areiaImage,
      discount: "31% OFF"
    }
  ];

  return (
    <section className="px-3 pb-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-foreground">Populares</h2>
        <button className="text-primary text-sm font-semibold min-h-[44px] px-3">Ver todos</button>
      </div>
      <div className="grid grid-cols-2 gap-2.5">
        {products.map((product) => (
          <div
            key={product.id}
            className="product-card bounce-in"
            style={{ animationDelay: `${product.id * 0.1}s` }}
          >
            <div className="relative">
              {product.discount && (
                <div className="absolute top-2 left-2 bg-destructive text-destructive-foreground text-xs font-bold px-2 py-1 rounded z-10">
                  {product.discount}
                </div>
              )}
              <div className="aspect-square bg-gray-100 rounded-t-xl overflow-hidden">
                <img 
                  src={product.image} 
                  alt={product.name}
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
            
            <div className="p-3">
              <h3 className="font-semibold text-sm text-card-foreground mb-1 line-clamp-2">
                {product.name}
              </h3>
              
              <div className="flex items-center gap-1 mb-2">
                <Star className="w-3 h-3 fill-warning text-warning" />
                <span className="text-xs text-muted-foreground">{product.rating}</span>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-bold text-foreground">{product.price}</div>
                  {product.originalPrice && (
                    <div className="text-xs text-muted-foreground line-through">
                      {product.originalPrice}
                    </div>
                  )}
                </div>
                
                <button className="w-10 h-10 bg-primary text-primary-foreground rounded-full flex items-center justify-center active:scale-95 transition-transform">
                  <ShoppingCart size={18} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default PopularProducts;