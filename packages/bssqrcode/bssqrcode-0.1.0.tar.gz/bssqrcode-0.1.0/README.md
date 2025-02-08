# bssqrcode

`bssqrcode` is a QR code generation library designed for **personal use** with **enhanced data security**.

## Features

- **Secure QR code generation**
- **Supports dynamic content encoding**
- **Optimized scanning technology**

## Installation

```bash
pip install bssqrcode
```

USAGE:
from bssqrcode import bssqrcode

key = bssqrcode.generate_key()
data = "Sample Text"

bssqrcode.create_qr(data, key, "test_qr.png")
decoded = bssqrcode.scan_qr("test_qr.png", key)
print("Decoded Data:", decoded)
