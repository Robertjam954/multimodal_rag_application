import { NavLink, Route, Routes } from "react-router-dom";
import { Button } from "@fluentui/react-components";
import { useThemeStore } from "./theme";
import Chat from "./pages/chat/Chat";
import Papers from "./pages/papers/Papers";
import Voice from "./pages/voice/Voice";
import Sql from "./pages/sql/Sql";
import Embed from "./pages/portfolio/Embed";

const navLinkStyle: React.CSSProperties = {
    padding: "8px 14px",
    textDecoration: "none",
    color: "inherit",
    borderRadius: 6,
};

export default function App() {
    const toggle = useThemeStore((s) => s.toggle);
    return (
        <div style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
            <header
                style={{
                    display: "flex",
                    gap: 12,
                    padding: "10px 20px",
                    borderBottom: "1px solid var(--colorNeutralStroke2)",
                    alignItems: "center",
                }}
            >
                <strong>mmRAG</strong>
                <nav style={{ display: "flex", gap: 4, flex: 1 }}>
                    <NavLink to="/" style={navLinkStyle}>
                        Chat
                    </NavLink>
                    <NavLink to="/papers" style={navLinkStyle}>
                        Papers
                    </NavLink>
                    <NavLink to="/voice" style={navLinkStyle}>
                        Voice
                    </NavLink>
                    <NavLink to="/sql" style={navLinkStyle}>
                        SQL
                    </NavLink>
                </nav>
                <Button appearance="subtle" onClick={toggle}>
                    Theme
                </Button>
            </header>
            <main style={{ flex: 1, padding: 20 }}>
                <Routes>
                    <Route path="/" element={<Chat />} />
                    <Route path="/papers" element={<Papers />} />
                    <Route path="/voice" element={<Voice />} />
                    <Route path="/sql" element={<Sql />} />
                    <Route path="/embed" element={<Embed />} />
                </Routes>
            </main>
            <footer style={{ padding: 16, fontSize: 12, opacity: 0.7, textAlign: "center" }}>
                multimodal RAG demo - <a href="https://github.com/Robertjam954/multimodal_rag_application">source</a>
            </footer>
        </div>
    );
}
