import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { FluentProvider, webLightTheme, webDarkTheme } from "@fluentui/react-components";
import App from "./App";
import { useThemeStore } from "./theme";

const qc = new QueryClient();

function Root() {
    const dark = useThemeStore((s) => s.dark);
    return (
        <FluentProvider theme={dark ? webDarkTheme : webLightTheme}>
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
