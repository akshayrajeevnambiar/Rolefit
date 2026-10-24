import { placeholderMessage, placeholderMeta } from "./placeholder";

export function App() {
  return (
    <main>
      <p className="meta">{placeholderMeta()}</p>
      <h1>RoleFit</h1>
      <p>{placeholderMessage()}</p>
    </main>
  );
}
