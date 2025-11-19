import { Minus, Plus, Trash2, ArrowLeft } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import BottomNavigation from "@/components/BottomNavigation";

const Cart = () => {
  const navigate = useNavigate();

  const cartItems = [
    {
      id: 1,
      name: "Cimento 50kg",
      price: 32.90,
      quantity: 2,
      image: "/src/assets/cimento.jpg"
    },
    {
      id: 2,
      name: "Tinta Acrílica 18L",
      price: 159.90,
      quantity: 1,
      image: "/src/assets/tinta.jpg"
    }
  ];

  const subtotal = cartItems.reduce((acc, item) => acc + (item.price * item.quantity), 0);
  const delivery = 15.00;
  const total = subtotal + delivery;

  return (
    <div className="click-obra-container">
      <header className="sticky top-0 z-50 bg-background border-b">
        <div className="flex items-center gap-4 p-4">
          <button onClick={() => navigate("/")} className="p-2 -ml-2">
            <ArrowLeft size={24} />
          </button>
          <h1 className="text-xl font-bold">Carrinho</h1>
        </div>
      </header>

      <main className="pb-32 p-4">
        <div className="space-y-4">
          {cartItems.map((item) => (
            <div key={item.id} className="product-card p-4">
              <div className="flex gap-4">
                <img 
                  src={item.image} 
                  alt={item.name}
                  className="w-20 h-20 object-cover rounded-lg"
                />
                <div className="flex-1">
                  <h3 className="font-semibold">{item.name}</h3>
                  <p className="text-primary font-bold mt-1">
                    R$ {item.price.toFixed(2)}
                  </p>
                  <div className="flex items-center gap-3 mt-2">
                    <button className="w-8 h-8 flex items-center justify-center rounded-full border-2 border-primary text-primary">
                      <Minus size={16} />
                    </button>
                    <span className="font-semibold">{item.quantity}</span>
                    <button className="w-8 h-8 flex items-center justify-center rounded-full bg-primary text-white">
                      <Plus size={16} />
                    </button>
                  </div>
                </div>
                <button className="text-destructive p-2">
                  <Trash2 size={20} />
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 p-4 bg-card rounded-lg border">
          <h2 className="font-bold mb-4">Resumo do pedido</h2>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Subtotal</span>
              <span>R$ {subtotal.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Taxa de entrega</span>
              <span>R$ {delivery.toFixed(2)}</span>
            </div>
            <div className="h-px bg-border my-3" />
            <div className="flex justify-between font-bold text-lg">
              <span>Total</span>
              <span className="text-primary">R$ {total.toFixed(2)}</span>
            </div>
          </div>
        </div>
      </main>

      <div className="fixed bottom-16 left-0 right-0 p-4 bg-background border-t">
        <Button className="w-full h-14 text-lg">
          Finalizar pedido
        </Button>
      </div>

      <BottomNavigation />
    </div>
  );
};

export default Cart;
