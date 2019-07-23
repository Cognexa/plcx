# ByMessage

Package for reading message in bytes or bits.

```yaml
receive:
  port: xxx
  messages:
    - name: message_1
      types: bits
      length: 64
      define: (0, 8, int, 1)  # start, end, type and expected value
      blocks:
        - (8, 24, '2letter', str)  # start, end, name and type
        - (24, 56, 'float', float)
        - (56, 57, 'bool1', bool)
        - (57, 58, 'bool2', bool)
send:
    port: xxx
    messages: []
```