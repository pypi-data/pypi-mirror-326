"""Mock Hapax server for testing the RAG pipeline."""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import openai
from prometheus_client import start_http_server, Counter, Histogram
import time
import socket

# Initialize metrics
REQUESTS = Counter('hapax_http_requests_total', 'Total requests', ['endpoint', 'status'])
LATENCY = Histogram('hapax_http_request_duration_seconds', 'Request duration')

class MockHapaxHandler(BaseHTTPRequestHandler):
    """Handler for mock Hapax server."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/health':
            REQUESTS.labels(endpoint='/health', status='200').inc()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
        else:
            REQUESTS.labels(endpoint=self.path, status='404').inc()
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/v1/completions':
            # Read request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            # Start timing
            start = time.time()
            
            try:
                # Forward to OpenAI
                client = openai.OpenAI()
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": data['input']}],
                    temperature=0
                )
                content = response.choices[0].message.content
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'content': content
                }).encode())
                
                # Record metrics
                REQUESTS.labels(endpoint='/v1/completions', status='200').inc()
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': str(e)
                }).encode())
                REQUESTS.labels(endpoint='/v1/completions', status='500').inc()
            
            # Record latency
            LATENCY.observe(time.time() - start)
        else:
            REQUESTS.labels(endpoint=self.path, status='404').inc()
            self.send_response(404)
            self.end_headers()

def is_port_in_use(port: int) -> bool:
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except OSError:
            return True

def find_available_port(start_port: int, max_attempts: int = 100) -> int:
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        if not is_port_in_use(port):
            return port
    raise RuntimeError(f"No available ports found between {start_port} and {start_port + max_attempts - 1}")

def run_server(port=None, metrics_port=None):
    """Run the mock Hapax server."""
    # Get ports from environment or use higher default ports
    server_port = port or int(os.getenv('HAPAX_MOCK_PORT', '9090'))
    metrics_port = metrics_port or int(os.getenv('HAPAX_MOCK_METRICS_PORT', '9091'))
    
    # If ports are in use, find available ones
    if is_port_in_use(server_port):
        print(f"Port {server_port} is in use, finding another port...")
        try:
            server_port = find_available_port(9090)
        except RuntimeError as e:
            print(f"Error: {e}")
            print("Please specify a different port using HAPAX_MOCK_PORT")
            exit(1)
    
    if is_port_in_use(metrics_port):
        print(f"Port {metrics_port} is in use, finding another port...")
        try:
            metrics_port = find_available_port(9091)
        except RuntimeError as e:
            print(f"Error: {e}")
            print("Please specify a different port using HAPAX_MOCK_METRICS_PORT")
            exit(1)
    
    try:
        # Start Prometheus metrics server
        start_http_server(metrics_port)
        print(f'Metrics server running on port {metrics_port}')
        
        # Start HTTP server
        server = HTTPServer(('localhost', server_port), MockHapaxHandler)
        print(f'Mock Hapax server running on port {server_port}')
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        server.server_close()
    except Exception as e:
        print(f"Error starting servers: {e}")
        raise

if __name__ == '__main__':
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("""
Error: OpenAI API key not found!

Please set your OpenAI API key using one of these methods:

1. Export as environment variable:
   export OPENAI_API_KEY=your-api-key-here

2. Create a .env file in the project root:
   OPENAI_API_KEY=your-api-key-here

You can get an API key from: https://platform.openai.com/api-keys
""")
        exit(1)
    run_server()
