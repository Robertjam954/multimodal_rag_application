import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()],
    build: {
        outDir: "build",
        emptyOutDir: true,
        sourcemap: true,
    },
    server: {
        port: 5173,
        proxy: {
            "/chat": "http://localhost:50505",
            "/sql": "http://localhost:50505",
            "/papers": "http://localhost:50505",
            "/voice": "http://localhost:50505",
            "/config": "http://localhost:50505",
            "/auth_setup": "http://localhost:50505",
            "/chat_history": "http://localhost:50505",
            "/feedback": "http://localhost:50505",
            "/content": "http://localhost:50505",
        },
    },
});
