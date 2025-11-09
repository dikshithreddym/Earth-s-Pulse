// Stub module for three/tsl
// This is a workaround for globe.gl compatibility issues
// Export everything that might be imported
export default {};
export const TSL = {};
// Provide minimal implementations for shader-like helpers expected by three-globe
export const If = (cond, a, b) => (cond ? a : b);
export const storage = {};
export const instanceIndex = 0;
export const sqrt = Math.sqrt;
export const cos = Math.cos;
export const exp = Math.exp;
export const uniform = (..._args) => null;
export class Loop {}
export const asin = Math.asin;
export const float = (v) => Number(v);
export const negate = (v) => -v;
export const sin = Math.sin;

// Re-export three core symbols as a convenience
export * from 'three';

