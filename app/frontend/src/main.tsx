import React, { useEffect } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { FluentProvider, webLightTheme, webDarkTheme, Theme } from "@fluentui/react-components";
import App from "./App";
import { useThemeStore } from "./theme";
import "./index.css";

const qc = new QueryClient();

// Rebrand Fluent's control colors to the green/navy palette used in index.css.
const brand = {
    colorBrandBackground: "#03ef62",
    colorBrandBackgroundHover: "#00d556",
    colorBrandBackgroundPressed: "#01a344",
    colorNeutralForegroundOnBrand: "#05192d",
    colorCompoundBrandBackground: "#03ef62",
    colorCompoundBrandBackgroundHover: "#00d556",
    colorCompoundBrandBackgroundPressed: "#01a344",
    colorCompoundBrandStroke: "#01a344",
    colorBrandStroke1: "#01a344",
    colorBrandForeground1: "#01a344",
    colorBrandForeground2: "#01a344",
};
const lightTheme: Theme = { ...webLightTheme, ...brand };
const darkTheme: Theme = { ...webDarkTheme, ...brand, colorBrandForeground1: "#03ef62", colorBrandForeground2: "#03ef62" };

function Root() {
    const dark = useThemeStore((s) => s.dark);
    useEffect(() => {
        document.documentElement.dataset.theme = dark ? "dark" : "light";
    }, [dark]);
    return (
        <FluentProvider theme={dark ? darkTheme : lightTheme} style={{ background: "transparent" }}>
            <QueryClientProvider client={qc}>
                <BrowserRouter>
                    <App />
                </BrowserRouter>
            </QueryClientProvider>
        </FluentProvider>
    );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <Root />
    </React.StrictMode>
);
