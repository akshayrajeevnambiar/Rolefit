/// <reference types="vite/client" />

// Tests read files and resolve the Vite allow list. This project does not
// depend on @types/node. These are the only calls, with the types we use.
declare module "node:fs" {
  export function readFileSync(path: URL, encoding: "utf8"): string;
  export function realpathSync(path: string): string;
}

declare module "node:path" {
  export function resolve(...paths: string[]): string;
}

declare module "node:url" {
  export function fileURLToPath(url: URL): string;
}
