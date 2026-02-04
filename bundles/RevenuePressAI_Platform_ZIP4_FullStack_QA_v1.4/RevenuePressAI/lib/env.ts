export function mustEnv(name: string, fallback = ''): string {
  const v = process.env[name] || fallback;
  return v;
}
