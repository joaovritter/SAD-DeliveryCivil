import { useState, useEffect } from "react";

const PromoBanner = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  
  const banners = [
    {
      id: 1,
      title: "Cimento em Promoção",
      subtitle: "Até 30% OFF",
      description: "Válido até 30/09",
      gradient: "bg-gradient-to-r from-orange-500 to-red-500"
    },
    {
      id: 2,
      title: "Ferramentas Premium",
      subtitle: "Frete Grátis",
      description: "Para toda São Paulo",
      gradient: "bg-gradient-to-r from-blue-500 to-purple-500"
    },
    {
      id: 3,
      title: "Kit Construção",
      subtitle: "50% OFF",
      description: "Primeira compra",
      gradient: "bg-gradient-to-r from-green-500 to-teal-500"
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % banners.length);
    }, 5000);

    return () => clearInterval(timer);
  }, [banners.length]);

  return (
    <section className="px-3 mb-6">
      <div className="promo-banner h-36 p-4 flex items-center justify-between text-white slide-in">
        <div className="flex-1 pr-2">
          <h2 className="text-lg font-bold mb-1">{banners[currentSlide].title}</h2>
          <p className="text-xl font-bold">{banners[currentSlide].subtitle}</p>
          <p className="text-sm opacity-90 mt-1">{banners[currentSlide].description}</p>
        </div>
        <div className="flex space-x-2">
          {banners.map((_, index) => (
            <div
              key={index}
              className={`w-2 h-2 rounded-full transition-all duration-300 ${
                index === currentSlide ? 'bg-white' : 'bg-white/50'
              }`}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default PromoBanner;