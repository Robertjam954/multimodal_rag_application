export function formatUSD(n: number | undefined): string {
    if (!n) return "$0.00";
    return n < 0.01 ? `$${(n * 100).toFixed(3)}¢` : `$${n.toFixed(4)}`;
}
