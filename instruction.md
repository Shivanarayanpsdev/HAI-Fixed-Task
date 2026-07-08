There's a web server access log at /app/access.log (Apache/nginx "combined"-style format, one request per line). Parse it and write a small JSON summary report to /app/report.json.

The report must be a single JSON object with exactly these keys:

1. `total_requests` — an integer count of the non-empty lines in /app/access.log.
2. `unique_ips` — an integer count of distinct client IP addresses (the first whitespace-separated field on each line).
3. `top_path` — a string with the request path (e.g. `/index.html`) that appears most often across all requests, taken from the quoted request line (`"METHOD /path HTTP/1.1"`). If there's a tie, any one of the tied paths is acceptable.

Success criteria:

1. /app/report.json exists and contains a valid JSON object.
2. `total_requests` equals the number of non-empty lines in /app/access.log.
3. `unique_ips` equals the number of distinct client IP addresses in the log.
4. `top_path` equals the most frequently requested path in the log.
