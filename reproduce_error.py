import math


def main_callback(r):
    def callback(x):
        if x > 50:
            return r + 20
        val = r * r - math.pow(x - 50, 2)
        print(f"DEBUG: r={r}, x={x}, x-50={x - 50}, val={val}")
        return math.sqrt(val) + 20

    return callback


z = 49.0
r = math.sqrt(50 * 50 - z * z)
x = 50 - r

print(f"z={z}, r={r}, x={x}")
try:
    res = main_callback(r)(x)
    print(f"Result: {res}")
except ValueError as e:
    print(f"Caught expected error: {e}")
