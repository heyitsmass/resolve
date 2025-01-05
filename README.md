# Domain Resolver

A multi-threaded tool for efficiently validating and resolving domain names and subdomains. This tool helps security researchers and penetration testers quickly identify resolvable domains from a list of potential subdomains, saving time by filtering out invalid endpoints before further testing.

## Features

- Multi-threaded domain resolution
- Multiple hostname format checking (www, http://, https://)
- Bulk processing from input files
- Custom thread count configuration
- Flexible input handling (single domain or file input)
- Results saved to configurable output file

## Installation

```bash
git clone https://github.com/heyitsmass/resolve
cd domain-resolver
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Check a single domain
python resolver.py -s example.com

# Process domains from a file
python resolver.py -f domains.txt

# Specify thread count and output file
python resolver.py -f domains.txt -t 20 -o results.txt
```

### Command Line Arguments

- `-s` : Single site to check (domain or IP address)
- `-f` : Input file containing list of domains to check
- `-t` : Number of threads to use (default: 10)
- `-o` : Output file name (default: resolve.out)

### Example Input File Format

```text
example.com
subdomain.example.com
test.example.com
www.example.com
https://secure.example.com
```

### Example Output

```text
example.com
www.example.com
https://example.com
http://example.com
secure.example.com
https://secure.example.com
```

## How It Works

1. **Input Processing**: The tool accepts either a single domain via `-s` or a file of domains via `-f`.

2. **Format Checking**: For each domain, it checks multiple formats:

   - Base domain (example.com)
   - WWW prefix (www.example.com)
   - HTTP prefix (http://example.com)
   - HTTPS prefix (https://example.com)

3. **Resolution**: Each format is checked for DNS resolution using `socket.gethostbyname()`.

4. **Result Storage**: Successfully resolved domains are saved to the output file.

## Code Example

Here's how to use the tool programmatically:

```python
from resolver import HostForms

# Create instance
host_forms = HostForms()

# Check single domain
results = host_forms.get_valid_hosts("example.com")
if results:
    print("Resolved domains:", results)

# Process multiple domains concurrently
hosts = ["example.com", "test.example.com"]
with ThreadPoolExecutor(max_workers=10) as executor:
    for host in hosts:
        executor.submit(check_host, host)
```

## Error Handling

- Invalid URLs in the input file are skipped with a "Skipped:" message
- DNS resolution failures are silently ignored
- Invalid command-line arguments trigger usage help

## Performance Tips

1. Adjust thread count (`-t`) based on your system capabilities
2. For large domain lists, consider batch processing
3. DNS resolution timeout is system-dependent

## Security Considerations

- Tool performs basic DNS lookups only
- No active scanning or probing of services
- Respects DNS rate limits of target infrastructure
- Designed for authorized security testing only

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License, Copyright (c) 2025 Brandon C.
