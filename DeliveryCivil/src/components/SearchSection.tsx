import { Search } from "lucide-react";

const SearchSection = () => {
  return (
    <section className="p-3">
      <div className="relative">
        <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-muted-foreground pointer-events-none" />
        <input
          type="search"
          placeholder="Buscar materiais de construção..."
          className="search-input fade-in"
        />
      </div>
    </section>
  );
};

export default SearchSection;