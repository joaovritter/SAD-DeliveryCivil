import { MapPin, Bell } from "lucide-react";

const Header = () => {
  return (
    <header className="p-3 border-b border-border sticky top-0 bg-card z-40">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 flex-1 min-w-0">
          <MapPin className="w-5 h-5 text-primary flex-shrink-0" />
          <div className="min-w-0">
            <p className="text-xs text-muted-foreground">Entregar em</p>
            <p className="font-semibold text-sm text-foreground truncate">Centro, São Paulo - SP</p>
          </div>
        </div>
        <button className="relative p-2 min-w-[44px] min-h-[44px] flex items-center justify-center">
          <Bell className="w-6 h-6 text-muted-foreground" />
          <div className="absolute top-1 right-1 w-2.5 h-2.5 bg-destructive rounded-full animate-pulse-primary"></div>
        </button>
      </div>
    </header>
  );
};

export default Header;