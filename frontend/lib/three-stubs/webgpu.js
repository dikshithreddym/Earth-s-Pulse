// Stub module for three/webgpu
// This is a workaround for globe.gl compatibility issues
// Export everything that might be imported
export default {};
export const WebGPURenderer = class {};
export const WebGPU = {};
// Minimal GPU-specific attributes/classes used by three-globe
export class StorageInstancedBufferAttribute {}

// Re-export three core symbols as a convenience
export * from 'three';
