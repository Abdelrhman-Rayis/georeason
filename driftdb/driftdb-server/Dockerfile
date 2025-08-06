# Builder stage
# docker build -f driftdb-server/Dockerfile .
FROM rust:1.72-slim as builder

WORKDIR /usr/src/driftdb

# Copy the entire project to build the server
COPY . .

# Build the server with release profile
WORKDIR /usr/src/driftdb/driftdb-server
RUN cargo build --release

# Runtime stage
FROM debian:bookworm-slim

# Install necessary runtime dependencies
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy the built binary from the builder stage
COPY --from=builder /usr/src/driftdb/target/release/driftdb-server /usr/local/bin/driftdb-server

# Expose the port the server runs on
EXPOSE 8080

# Run the server
CMD ["driftdb-server", "--host", "0.0.0.0"]