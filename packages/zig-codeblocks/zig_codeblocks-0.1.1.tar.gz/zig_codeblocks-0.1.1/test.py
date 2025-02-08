import zig_codeblocks as zc

src = """
```zig
/// The health status of a renderer. These must be shared across all
/// renderers even if some states aren't reachable so that our API users
/// can use the same enum for all renderers.
``````zig
pub const Health = enum(c_int) {
    healthy = 0,
    unhealthy = 1,
};
```
"""

print(list(zc.extract_codeblocks(src)))
