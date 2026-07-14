import { NavLink, Route, Routes } from "react-router-dom";
import { useThemeStore } from "./theme";
import Chat from "./pages/chat/Chat";
import Papers from "./pages/papers/Papers";
import Voice from "./pages/voice/Voice";
import Sql from "./pages/sql/Sql";
import Embed from "./pages/portfolio/Embed";

export default function App() {
    const dark = useThemeStore((s) => s.dark);
    const toggle = useThemeStore((s) => s.toggle);
    return (
        <div style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
            <header className="topnav">
                <NavLink to="/" className="brand">
                    <span className="brand-dot" />
                    RAG Tutor
                </NavLink>
                <nav className="nav-links">
                    <NavLink to="/" end className={({ isActive }) => `nav-pill${isActive ? " active" : ""}`}>
                        Chat
                    </NavLink>
                    <NavLink to="/papers" className={({ isActive }) => `nav-pill${isActive ? " active" : ""}`}>
                        Papers
                    </NavLink>
                    <NavLink to="/voice" className={({ isActive }) => `nav-pill${isActive ? " active" : ""}`}>
                        Voice
                    </NavLink>
                    <NavLink to="/sql" className={({ isActive }) => `nav-pill${isActive ? " active" : ""}`}>
                        SQL
                    </NavLink>
                </nav>
                <button className="icon-btn" onClick={toggle} title="Toggle theme" aria-label="Toggle theme">
                    {dark ? "☀" : "☾"}
                </button>
            </header>
            <main style={{ flex: 1, display: "flex", flexDirection: "column" }}>
                <Routes>
                    <Route path="/" element={<Chat />} />
                    <Route path="/papers" element={<Papers />} />
                    <Route path="/voice" element={<Voice />} />
                    <Route path="/sql" element={<Sql />} />
                    <Route path="/embed" element={<Embed />} />
                </Routes>
            </main>
            <footer className="footer">
                Multimodal RAG Tutor · grounded answers with citations ·{" "}
                <a href="https://github.com/Robertjam954/multimodal_rag_application">source on GitHub</a>
            </footer>
        </div>
    );
}
