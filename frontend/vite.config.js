import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    // Inside Docker the API is reachable by its service name.
    proxy: { "/api": process.env.VITE_API_TARGET || "http://api:8000" },
  },
});