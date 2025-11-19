import Header from "@/components/Header";
import SearchSection from "@/components/SearchSection";
import PromoBanner from "@/components/PromoBanner";
import Categories from "@/components/Categories";
import PopularProducts from "@/components/PopularProducts";
import BottomNavigation from "@/components/BottomNavigation";

const Index = () => {
  return (
    <div className="click-obra-container">
      <Header />
      <main className="pb-24">
        <SearchSection />
        <PromoBanner />
        <Categories />
        <PopularProducts />
      </main>
      <BottomNavigation />
    </div>
  );
};

export default Index;