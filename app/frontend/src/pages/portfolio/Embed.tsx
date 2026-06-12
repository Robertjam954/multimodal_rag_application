/** Minimal mode used when the demo is embedded inside the Jekyll portfolio (iframe). */
import Chat from "../chat/Chat";

export default function Embed() {
    return (
        <div style={{ padding: 0 }}>
            <Chat />
        </div>
    );
}
