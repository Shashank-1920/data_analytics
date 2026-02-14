import http.server
import socketserver
import json
import os
import sys
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db_connector import connect_to_db, get_tables
from analytics import perform_analytics

PORT = 8000
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')

# Global variable to store the current connection
current_connection = None
current_schema = None


class DataAnalyticsHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        print(f"GET {self.path}")
        
        # API endpoints
        if path == '/api/tables':
            self.handle_get_tables()
            return
        
        # Strip query parameters
        path = path.split('?')[0]
        
        # Serve index.html for root
        if path in ('/', '', '/index.html'):
            self.serve_file('index.html')
            return
        
        # Remove leading slash and construct file path
        if path.startswith('/'):
            path = path[1:]
        
        file_path = os.path.join(FRONTEND_DIR, path)
        
        # Prevent directory traversal attacks
        try:
            file_path = os.path.realpath(file_path)
            frontend_dir = os.path.realpath(FRONTEND_DIR)
            if not file_path.startswith(frontend_dir):
                self.send_error_response(403, "Access denied")
                return
        except Exception:
            self.send_error_response(400, "Invalid path")
            return
        
        # Serve the file
        if os.path.isfile(file_path):
            self.serve_file_from_path(file_path)
        else:
            self.send_error_response(404, f"File not found: {path}")
    
    def serve_file(self, filename):
        """Serve a file from the frontend directory"""
        file_path = os.path.join(FRONTEND_DIR, filename)
        self.serve_file_from_path(file_path)
    
    def serve_file_from_path(self, file_path):
        """Serve a file from a full path"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Determine content type
            content_type = 'text/plain'
            if file_path.endswith('.html'):
                content_type = 'text/html'
            elif file_path.endswith('.css'):
                content_type = 'text/css'
            elif file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.json'):
                content_type = 'application/json'
            elif file_path.endswith('.png'):
                content_type = 'image/png'
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif file_path.endswith('.gif'):
                content_type = 'image/gif'
            elif file_path.endswith('.svg'):
                content_type = 'image/svg+xml'
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Content-Length', len(content))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error_response(404, "File not found")
        except Exception as e:
            self.send_error_response(500, f"Error serving file: {str(e)}")

    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        print(f"POST {self.path}")
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON")
            return

        if parsed_path.path == '/api/connect':
            self.handle_connect(data)
        elif parsed_path.path == '/api/analytics':
            self.handle_analytics(data)
        else:
            self.send_error_response(404, "Endpoint not found")

    def handle_connect(self, data):
        """Handle database connection"""
        global current_connection, current_schema
        
        try:
            host = data.get('host', '').strip()
            port = int(data.get('port', 3306))
            username = data.get('username', '').strip()
            password = data.get('password', '')
            schema = data.get('schema', '').strip()

            if not all([host, username, password, schema]):
                self.send_error_response(400, "Missing required fields: host, username, password, and schema are required")
                return

            print(f"\n--- Connection Attempt ---")
            print(f"Host: {host}")
            print(f"Port: {port}")
            print(f"Username: {username}")
            print(f"Schema: {schema}")

            connection = connect_to_db(host, port, username, password, schema)
            
            if connection:
                current_connection = connection
                current_schema = schema
                msg = f'Successfully connected to {schema} database at {host}:{port}'
                print(f"✓ {msg}\n")
                self.send_json_response({'status': 'success', 'message': msg})
            else:
                error_msg = "Failed to connect to the database. Check credentials and ensure MySQL is running."
                print(f"✗ {error_msg}\n")
                self.send_error_response(400, error_msg)
        except ValueError as e:
            self.send_error_response(400, f"Invalid port number: {str(e)}")
        except Exception as e:
            error_msg = f"Connection error: {str(e)}"
            print(f"✗ {error_msg}\n")
            self.send_error_response(500, error_msg)

    def handle_get_tables(self):
        """Handle table retrieval"""
        global current_connection
        
        if not current_connection:
            self.send_error_response(400, "Not connected to database")
            return

        try:
            tables = get_tables(current_connection)
            self.send_json_response({'status': 'success', 'tables': tables})
        except Exception as e:
            self.send_error_response(500, f"Error retrieving tables: {str(e)}")

    def handle_analytics(self, data):
        """Handle analytics request"""
        global current_connection
        
        if not current_connection:
            self.send_error_response(400, "Not connected to database")
            return

        try:
            table_name = data.get('table')
            if not table_name:
                self.send_error_response(400, "Table name required")
                return

            results = perform_analytics(current_connection, table_name)
            self.send_json_response({'status': 'success', 'data': results})
        except Exception as e:
            self.send_error_response(500, f"Analytics error: {str(e)}")

    def send_json_response(self, data, status_code=200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def send_error_response(self, status_code, message):
        """Send error response"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'error', 'message': message}).encode('utf-8'))

    def end_headers(self):
        """Override to add CORS headers - but call parent to actually send"""
        super().end_headers()

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


def run_server():
    """Start the HTTP server"""
    # allow rapid restarts during development
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), DataAnalyticsHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print(f"Serving frontend from: {FRONTEND_DIR}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            try:
                httpd.server_close()
            except Exception:
                pass


if __name__ == '__main__':
    run_server()
