import { create } from "zustand";

interface ThemeState {
    dark: boolean;
    toggle: () => void;
}

export const useThemeStore = create<ThemeState>((set) => ({
    dark: window.matchMedia("(prefers-color-scheme: dark)").matches,
    toggle: () => set((s) => ({ dark: !s.dark })),
}));
