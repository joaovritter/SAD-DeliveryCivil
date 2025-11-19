import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

// Importar Bootstrap CSS
import "bootstrap/dist/css/bootstrap.min.css";

createRoot(document.getElementById("root")!).render(<App />);
