/// <reference types="vite/client" />

// The stylesheet test reads the file as text. This project does not depend
// on @types/node; the signature below is the only call we make.
declare module "node:fs" {
  export function readFileSync(path: URL, encoding: "utf8"): string;
}
