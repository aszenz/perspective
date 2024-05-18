// this line/hack allows us to bypass the emscripten environment
// so we can run the same JS-file on both web and node.
globalThis.window = {};
